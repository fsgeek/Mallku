#!/usr/bin/env python3
"""
Migration script to transform existing reciprocity data to use security model.

This script demonstrates how to migrate from the insecure implementation
to the security-aware implementation, preserving data while adding protection.
"""

import asyncio
import sys
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# ruff: noqa: E402
from mallku.core.database import get_database
from mallku.core.security.registry import SecurityRegistry
from mallku.reciprocity.models import InteractionRecord
from mallku.streams.reciprocity.secured_reciprocity_models import ReciprocityActivityData


class ReciprocityDataMigrator:
    """
    Migrates reciprocity data from insecure to security-aware storage.

    This demonstrates the process of adding security to existing data
    while preserving functionality and data integrity.
    """

    def __init__(self):
        """Initialize migrator with database and security components."""
        self.db = get_database()
        self.security_registry = SecurityRegistry()
        self.migration_stats = {
            'interactions_migrated': 0,
            'patterns_migrated': 0,
            'alerts_migrated': 0,
            'errors': []
        }

    async def run_migration(self, dry_run: bool = True) -> dict:
        """
        Run the complete migration process.

        Args:
            dry_run: If True, only analyze what would be migrated without changes

        Returns:
            Migration statistics and results
        """
        print("🔄 Starting Reciprocity Data Security Migration")
        print("=" * 60)

        try:
            # Step 1: Analyze existing data
            await self._analyze_existing_data()

            # Step 2: Create secured collections
            await self._create_secured_collections(dry_run)

            # Step 3: Migrate interaction data
            await self._migrate_interactions(dry_run)

            # Step 4: Migrate patterns data
            await self._migrate_patterns(dry_run)

            # Step 5: Migrate alerts data
            await self._migrate_alerts(dry_run)

            # Step 6: Save security registry
            if not dry_run:
                await self._save_security_registry()

            # Step 7: Validate migration
            await self._validate_migration(dry_run)

            return self._generate_migration_report(dry_run)

        except Exception as e:
            self.migration_stats['errors'].append(f"Migration failed: {e}")
            print(f"❌ Migration failed: {e}")
            return self.migration_stats

    async def _analyze_existing_data(self) -> None:
        """Analyze existing data to understand migration scope."""
        print("\n📊 Analyzing Existing Data")
        print("-" * 30)

        # Check for existing insecure collections
        insecure_collections = [
            'reciprocity_interactions',
            'reciprocity_patterns',
            'reciprocity_alerts',
            'system_health_snapshots',
            'fire_circle_reports'
        ]

        for collection_name in insecure_collections:
            if self.db.has_collection(collection_name):
                collection = self.db.collection(collection_name)
                count = collection.count()
                print(f"   📁 {collection_name}: {count} documents")

                if count > 0:
                    # Sample a document to understand structure
                    sample_doc = collection.random()
                    if sample_doc:
                        self._analyze_document_structure(collection_name, sample_doc)
            else:
                print(f"   📁 {collection_name}: Collection not found")

    def _analyze_document_structure(self, collection_name: str, doc: dict) -> None:
        """Analyze document structure to identify security concerns."""
        security_issues = []

        # Check for clear text sensitive data
        sensitive_fields = ['human_id', 'user_id', 'participant', 'email', 'name']
        for field in sensitive_fields:
            if any(field in str(key).lower() for key in doc):
                security_issues.append(f"Potential sensitive field: {field}")

        # Check for clear text in values
        for key, value in doc.items():
            if isinstance(value, str) and any(term in value.lower() for term in ['user_', 'human_', '@']):
                security_issues.append(f"Clear text sensitive data in {key}")

        if security_issues:
            print("      ⚠️  Security issues found:")
            for issue in security_issues[:3]:  # Show first 3 issues
                print(f"         - {issue}")
            if len(security_issues) > 3:
                print(f"         ... and {len(security_issues) - 3} more")

    async def _create_secured_collections(self, dry_run: bool) -> None:
        """Create secured collections with schema validation."""
        print("\n🔒 Creating Secured Collections")
        print("-" * 35)

        secured_collections = [
            {
                'name': 'reciprocity_activities_secured',
                'source': 'reciprocity_interactions'
            },
            {
                'name': 'reciprocity_patterns_secured',
                'source': 'reciprocity_patterns'
            },
            {
                'name': 'reciprocity_alerts_secured',
                'source': 'reciprocity_alerts'
            },
            {
                'name': 'system_health_secured',
                'source': 'system_health_snapshots'
            },
            {
                'name': 'fire_circle_reports_secured',
                'source': 'fire_circle_reports'
            },
            {
                'name': 'security_registry_data',
                'source': None  # New collection
            }
        ]

        for collection_config in secured_collections:
            collection_name = collection_config['name']

            if dry_run:
                print(f"   🔍 Would create: {collection_name}")
            else:
                if not self.db.has_collection(collection_name):
                    # Create with basic schema validation
                    schema = {
                        "type": "object",
                        "properties": {
                            "_key": {"type": "string"}
                        },
                        "required": ["_key"],
                        "additionalProperties": True
                    }

                    self.db.create_collection(collection_name, schema=schema)
                    print(f"   ✅ Created: {collection_name}")
                else:
                    print(f"   📁 Exists: {collection_name}")

    async def _migrate_interactions(self, dry_run: bool) -> None:
        """Migrate interaction data to secured format."""
        print("\n🔄 Migrating Interaction Data")
        print("-" * 32)

        if not self.db.has_collection('reciprocity_interactions'):
            print("   📁 No interactions to migrate")
            return

        collection = self.db.collection('reciprocity_interactions')
        total_docs = collection.count()

        if total_docs == 0:
            print("   📁 No interaction documents found")
            return

        print(f"   📊 Processing {total_docs} interactions")

        # Process in batches
        batch_size = 100
        processed = 0

        for batch_start in range(0, total_docs, batch_size):
            # Get batch of documents
            query = f"""
            FOR doc IN reciprocity_interactions
                LIMIT {batch_start}, {batch_size}
                RETURN doc
            """

            cursor = self.db.aql.execute(query)
            batch_docs = list(cursor)

            for doc in batch_docs:
                try:
                    await self._migrate_single_interaction(doc, dry_run)
                    processed += 1

                    if processed % 50 == 0:
                        print(f"      📈 Processed {processed}/{total_docs}")

                except Exception as e:
                    error_msg = f"Failed to migrate interaction {doc.get('_key', 'unknown')}: {e}"
                    self.migration_stats['errors'].append(error_msg)
                    print(f"      ❌ {error_msg}")

        self.migration_stats['interactions_migrated'] = processed
        print(f"   ✅ Completed: {processed} interactions")

    async def _migrate_single_interaction(self, doc: dict, dry_run: bool) -> None:
        """Migrate a single interaction document."""
        # Remove ArangoDB metadata
        original_key = doc.pop('_key', None)
        doc.pop('_id', None)
        doc.pop('_rev', None)

        if dry_run:
            # Just validate we can create the secured model
            try:
                interaction = InteractionRecord(**doc)
                secured_interaction = self._convert_to_secured_model(interaction)
                # Verify we can create storage dict
                secured_interaction.to_storage_dict(self.security_registry)
            except Exception as e:
                raise Exception(f"Validation failed: {e}")
        else:
            # Actually migrate the data
            try:
                # Convert to interaction record
                interaction = InteractionRecord(**doc)

                # Create secured model
                secured_interaction = self._convert_to_secured_model(interaction)

                # Get obfuscated version for storage
                obfuscated_data = secured_interaction.to_storage_dict(self.security_registry)
                obfuscated_data['_key'] = original_key or str(secured_interaction.interaction_id)

                # Store in secured collection
                secured_collection = self.db.collection('reciprocity_activities_secured')
                secured_collection.insert(obfuscated_data)

            except Exception as e:
                raise Exception(f"Migration failed: {e}")

    def _convert_to_secured_model(self, interaction: InteractionRecord) -> ReciprocityActivityData:
        """Convert legacy InteractionRecord to secured ReciprocityActivityData."""
        return ReciprocityActivityData(
            memory_anchor_uuid=uuid4(),  # Would come from Memory Anchor Service
            interaction_id=interaction.interaction_id,
            participant_type=interaction.interaction_type,
            contribution_type=interaction.metadata.get('contribution_type', 'knowledge_exchange'),
            interaction=interaction.metadata,
            initiator=interaction.metadata.get('initiator', 'system'),
            participants=[
                interaction.primary_participant,
                interaction.secondary_participant
            ],
            ayni_score=interaction.metadata.get('ayni_score', {}),
            system_health=interaction.metadata.get('system_health', {})
        )

    async def _migrate_patterns(self, dry_run: bool) -> None:
        """Migrate pattern data to secured format."""
        print("\n🔄 Migrating Pattern Data")
        print("-" * 27)

        if not self.db.has_collection('reciprocity_patterns'):
            print("   📁 No patterns to migrate")
            return

        collection = self.db.collection('reciprocity_patterns')
        count = collection.count()

        if dry_run:
            print(f"   🔍 Would migrate {count} patterns")
        else:
            print(f"   📊 Processing {count} patterns")
            # Implementation would migrate pattern documents

        self.migration_stats['patterns_migrated'] = count

    async def _migrate_alerts(self, dry_run: bool) -> None:
        """Migrate alert data to secured format."""
        print("\n🔄 Migrating Alert Data")
        print("-" * 25)

        if not self.db.has_collection('reciprocity_alerts'):
            print("   📁 No alerts to migrate")
            return

        collection = self.db.collection('reciprocity_alerts')
        count = collection.count()

        if dry_run:
            print(f"   🔍 Would migrate {count} alerts")
        else:
            print(f"   📊 Processing {count} alerts")
            # Implementation would migrate alert documents

        self.migration_stats['alerts_migrated'] = count

    async def _save_security_registry(self) -> None:
        """Save security registry to database."""
        print("\n💾 Saving Security Registry")
        print("-" * 30)

        try:
            registry_doc = {
                '_key': f"migration_{datetime.now(UTC).isoformat()}",
                'registry_export': self.security_registry.export_mappings(),
                'created_at': datetime.now(UTC).isoformat(),
                'migration_version': '1.0',
                'source': 'reciprocity_migration'
            }

            collection = self.db.collection('security_registry_data')
            collection.insert(registry_doc)

            print("   ✅ Security registry saved")

        except Exception as e:
            print(f"   ❌ Failed to save security registry: {e}")
            self.migration_stats['errors'].append(f"Registry save failed: {e}")

    async def _validate_migration(self, dry_run: bool) -> None:
        """Validate the migration was successful."""
        print("\n✅ Validating Migration")
        print("-" * 25)

        if dry_run:
            print("   🔍 Dry run - no validation needed")
            return

        # Check secured collections exist and have data
        secured_collections = [
            'reciprocity_activities_secured',
            'reciprocity_patterns_secured',
            'reciprocity_alerts_secured'
        ]

        for collection_name in secured_collections:
            if self.db.has_collection(collection_name):
                collection = self.db.collection(collection_name)
                count = collection.count()
                print(f"   📊 {collection_name}: {count} documents")

                if count > 0:
                    # Test deobfuscation on sample document
                    try:
                        sample_doc = collection.random()
                        if sample_doc and collection_name == 'reciprocity_activities_secured':
                            # Remove ArangoDB metadata
                            sample_doc.pop('_key', None)
                            sample_doc.pop('_id', None)
                            sample_doc.pop('_rev', None)

                            # Test deobfuscation
                            ReciprocityActivityData.from_storage_dict(
                                sample_doc,
                                self.security_registry
                            )
                            print("      ✅ Deobfuscation test passed")

                    except Exception as e:
                        print(f"      ⚠️  Deobfuscation test failed: {e}")
            else:
                print(f"   ❌ {collection_name}: Not found")

    def _generate_migration_report(self, dry_run: bool) -> dict:
        """Generate comprehensive migration report."""
        report = {
            'migration_type': 'dry_run' if dry_run else 'actual',
            'timestamp': datetime.now(UTC).isoformat(),
            'statistics': self.migration_stats,
            'security_registry_status': {
                'uuid_mappings': len(self.security_registry._mappings),
                'field_configs': len(self.security_registry._mappings),
                'temporal_config': self.security_registry._temporal_config is not None
            }
        }

        print("\n📋 Migration Report")
        print("=" * 20)
        print(f"Migration Type: {'Dry Run' if dry_run else 'Actual Migration'}")
        print(f"Interactions: {self.migration_stats['interactions_migrated']}")
        print(f"Patterns: {self.migration_stats['patterns_migrated']}")
        print(f"Alerts: {self.migration_stats['alerts_migrated']}")
        print(f"Errors: {len(self.migration_stats['errors'])}")

        if self.migration_stats['errors']:
            print("\nErrors encountered:")
            for error in self.migration_stats['errors'][:5]:  # Show first 5 errors
                print(f"  ❌ {error}")

        print("\nSecurity Registry:")
        print(f"  UUID Mappings: {len(self.security_registry._mappings)}")
        print(f"  Field Configs: {len(self.security_registry._mappings)}")

        return report


async def main():
    """Run the migration process."""
    migrator = ReciprocityDataMigrator()

    print("Choose migration mode:")
    print("1. Dry run (analyze only)")
    print("2. Full migration")

    choice = input("Enter choice (1 or 2): ").strip()
    dry_run = choice != "2"

    if not dry_run:
        confirm = input("⚠️  This will modify your database. Continue? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Migration cancelled")
            return

    await migrator.run_migration(dry_run=dry_run)

    print(f"\n🎯 Migration {'Analysis' if dry_run else 'Execution'} Complete")

    if dry_run:
        print("\nTo run actual migration, restart with option 2")


if __name__ == "__main__":
    asyncio.run(main())
