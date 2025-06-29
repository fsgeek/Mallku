#!/usr/bin/env python3
"""
Migrate Fire Circle Memories to Database
========================================

Thirty-Ninth Artisan - Database Weaver
Migration tool from JSON file storage to ArangoDB

This script helps transition existing Fire Circle memories from
file-based storage to database persistence, preserving all
consciousness metadata and relationships.
"""

import json
import logging
from pathlib import Path
from typing import Any

from .database_store import DatabaseMemoryStore
from .memory_store import MemoryStore
from .models import EpisodicMemory, MemoryCluster, WisdomConsolidation

logger = logging.getLogger(__name__)


class MemoryMigrator:
    """Migrate memories from file storage to database."""

    def __init__(
        self,
        source_path: Path | None = None,
        collection_prefix: str = "fc_",
        dry_run: bool = False,
    ):
        """Initialize migrator.

        Args:
            source_path: Path to existing file-based storage
            collection_prefix: Prefix for database collections
            dry_run: If True, only report what would be migrated
        """
        self.source_path = source_path or Path("data/fire_circle_memory")
        self.dry_run = dry_run

        # Initialize stores
        self.file_store = MemoryStore(storage_path=self.source_path)
        if not dry_run:
            self.db_store = DatabaseMemoryStore(collection_prefix=collection_prefix)

        # Migration stats
        self.stats = {
            "episodes_migrated": 0,
            "clusters_migrated": 0,
            "wisdom_migrated": 0,
            "errors": 0,
        }

    def migrate_all(self) -> dict[str, Any]:
        """Migrate all memories to database.

        Returns:
            Migration statistics
        """
        logger.info(f"Starting migration from {self.source_path}")

        # Migrate episodic memories
        self._migrate_episodes()

        # Migrate memory clusters
        self._migrate_clusters()

        # Migrate wisdom consolidations
        self._migrate_wisdom()

        logger.info(
            f"Migration {'simulation' if self.dry_run else 'complete'}: "
            f"{self.stats['episodes_migrated']} episodes, "
            f"{self.stats['clusters_migrated']} clusters, "
            f"{self.stats['wisdom_migrated']} wisdom consolidations"
        )

        if self.stats["errors"] > 0:
            logger.warning(f"Encountered {self.stats['errors']} errors during migration")

        return self.stats

    def _migrate_episodes(self) -> None:
        """Migrate episodic memories."""
        episodes_dir = self.source_path / "episodes"
        if not episodes_dir.exists():
            logger.info("No episodes directory found")
            return

        for memory_file in episodes_dir.glob("*.json"):
            try:
                with open(memory_file) as f:
                    data = json.load(f)

                memory = EpisodicMemory(**data)

                if self.dry_run:
                    logger.info(f"Would migrate episode: {memory.episode_id}")
                else:
                    self.db_store.store_episode(memory)
                    logger.debug(f"Migrated episode: {memory.episode_id}")

                self.stats["episodes_migrated"] += 1

            except Exception as e:
                logger.error(f"Failed to migrate {memory_file}: {e}")
                self.stats["errors"] += 1

    def _migrate_clusters(self) -> None:
        """Migrate memory clusters."""
        clusters_dir = self.source_path / "clusters"
        if not clusters_dir.exists():
            logger.info("No clusters directory found")
            return

        for cluster_file in clusters_dir.glob("*.json"):
            try:
                with open(cluster_file) as f:
                    data = json.load(f)

                cluster = MemoryCluster(**data)

                if self.dry_run:
                    logger.info(f"Would migrate cluster: {cluster.cluster_id}")
                else:
                    # Store cluster directly in database
                    cluster_doc = {
                        "_key": str(cluster.cluster_id),
                        "cluster_id": str(cluster.cluster_id),
                        "theme": cluster.theme,
                        "memory_ids": [str(mid) for mid in cluster.memory_ids],
                        "consolidated_insights": cluster.consolidated_insights,
                        "evolution_pattern": cluster.evolution_pattern,
                        "earliest_memory": cluster.earliest_memory.isoformat(),
                        "latest_memory": cluster.latest_memory.isoformat(),
                        "sacred_moment_count": cluster.sacred_moment_count,
                        "transformation_potential": cluster.transformation_potential,
                    }
                    self.db_store.db.collection(self.db_store.clusters_collection).insert(
                        cluster_doc
                    )
                    logger.debug(f"Migrated cluster: {cluster.cluster_id}")

                self.stats["clusters_migrated"] += 1

            except Exception as e:
                logger.error(f"Failed to migrate {cluster_file}: {e}")
                self.stats["errors"] += 1

    def _migrate_wisdom(self) -> None:
        """Migrate wisdom consolidations."""
        wisdom_dir = self.source_path / "wisdom"
        if not wisdom_dir.exists():
            logger.info("No wisdom directory found")
            return

        for wisdom_file in wisdom_dir.glob("*.json"):
            try:
                with open(wisdom_file) as f:
                    data = json.load(f)

                consolidation = WisdomConsolidation(**data)

                if self.dry_run:
                    logger.info(f"Would migrate wisdom: {consolidation.consolidation_id}")
                else:
                    # Store consolidation directly in database
                    wisdom_doc = {
                        "_key": str(consolidation.consolidation_id),
                        "consolidation_id": str(consolidation.consolidation_id),
                        "created_at": consolidation.created_at.isoformat(),
                        "source_episodes": [str(eid) for eid in consolidation.source_episodes],
                        "source_clusters": [str(cid) for cid in consolidation.source_clusters],
                        "core_insight": consolidation.core_insight,
                        "elaboration": consolidation.elaboration,
                        "practical_applications": consolidation.practical_applications,
                        "applicable_domains": consolidation.applicable_domains,
                        "voice_alignments": consolidation.voice_alignments,
                        "civilizational_relevance": consolidation.civilizational_relevance,
                        "ayni_demonstration": consolidation.ayni_demonstration,
                        "times_referenced": consolidation.times_referenced,
                        "episodes_influenced": [
                            str(eid) for eid in consolidation.episodes_influenced
                        ],
                    }
                    self.db_store.db.collection(self.db_store.wisdom_collection).insert(wisdom_doc)
                    logger.debug(f"Migrated wisdom: {consolidation.consolidation_id}")

                self.stats["wisdom_migrated"] += 1

            except Exception as e:
                logger.error(f"Failed to migrate {wisdom_file}: {e}")
                self.stats["errors"] += 1


def main():
    """Run migration from command line."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Migrate Fire Circle memories from files to database"
    )
    parser.add_argument(
        "--source",
        type=Path,
        help="Source directory for file-based memories",
        default=Path("data/fire_circle_memory"),
    )
    parser.add_argument(
        "--prefix",
        help="Collection prefix for database",
        default="fc_",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate migration without writing to database",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Run migration
    migrator = MemoryMigrator(
        source_path=args.source,
        collection_prefix=args.prefix,
        dry_run=args.dry_run,
    )

    stats = migrator.migrate_all()

    # Print summary
    print("\nMigration Summary:")
    print(f"  Episodes migrated: {stats['episodes_migrated']}")
    print(f"  Clusters migrated: {stats['clusters_migrated']}")
    print(f"  Wisdom migrated: {stats['wisdom_migrated']}")
    if stats["errors"] > 0:
        print(f"  Errors encountered: {stats['errors']}")

    if args.dry_run:
        print("\nThis was a dry run. No data was written to the database.")
        print("Remove --dry-run to perform actual migration.")


if __name__ == "__main__":
    main()
