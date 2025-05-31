"""
Demonstration of Mallku's security architecture.

Shows how field-level security strategies balance protection with utility.
"""

import os
from datetime import UTC, datetime, timedelta

from mallku.core.security import (
    FieldIndexStrategy,
    FieldSecurityConfig,
    SearchCapability,
    TemporalEncoder,
    TransformerRegistry,
)


def demo_temporal_offset():
    """Demonstrate temporal offset encoding."""
    print("=== Temporal Offset Demo ===")

    # Create encoder with random offset
    encoder = TemporalEncoder()
    offset_days = encoder.offset_seconds / 86400

    # Original timestamps
    now = datetime.now(UTC)
    yesterday = now - timedelta(days=1)
    last_week = now - timedelta(days=7)

    # Encode timestamps
    encoded_now = encoder.encode(now)
    encoded_yesterday = encoder.encode(yesterday)
    encoded_last_week = encoder.encode(last_week)

    print(f"Temporal offset: {offset_days:.1f} days")
    print("\nOriginal timestamps:")
    print(f"  Now:        {now}")
    print(f"  Yesterday:  {yesterday}")
    print(f"  Last week:  {last_week}")

    print("\nEncoded timestamps (offset applied):")
    print(f"  Now:        {encoded_now}")
    print(f"  Yesterday:  {encoded_yesterday}")
    print(f"  Last week:  {encoded_last_week}")

    print("\nRelative differences preserved:")
    print(f"  Now - Yesterday:  {(encoded_now - encoded_yesterday) / 86400:.1f} days")
    print(f"  Now - Last week:  {(encoded_now - encoded_last_week) / 86400:.1f} days")

    # Show that queries still work
    print("\nRange query example:")
    print("  Find all records between yesterday and now")
    print(f"  Query: timestamp >= {encoded_yesterday} AND timestamp <= {encoded_now}")


def demo_bucketing():
    """Demonstrate bucketed transformation for reciprocity scores."""
    print("\n\n=== Bucketing Demo ===")

    # Configure bucketing for reciprocity scores
    config = FieldSecurityConfig(
        index_strategy=FieldIndexStrategy.BUCKETED,
        bucket_boundaries=[-1.0, -0.5, -0.1, 0.0, 0.1, 0.5, 1.0],
        search_capabilities=[SearchCapability.RANGE]
    )

    # Create transformer
    secret_key = os.urandom(32)
    registry = TransformerRegistry(secret_key, TemporalEncoder())

    # Test values representing different reciprocity states
    test_scores = [
        ("Severely imbalanced (human owes)", -0.85),
        ("Moderately imbalanced", -0.3),
        ("Nearly balanced", -0.05),
        ("Perfect balance", 0.0),
        ("AI gave slightly more", 0.15),
        ("AI gave much more", 0.7),
    ]

    print("Reciprocity score bucketing:")
    for label, score in test_scores:
        bucketed = registry.transform_value(score, config)
        print(f"  {label}: {score:>5.2f} → {bucketed['bucket_label']}")

    print("\nPrivacy benefit: Exact scores are hidden, but we can still:")
    print("  - Find severely imbalanced relationships")
    print("  - Track general reciprocity trends")
    print("  - Suggest rebalancing when needed")


def demo_blind_indexing():
    """Demonstrate blind indexing for user IDs."""
    print("\n\n=== Blind Indexing Demo ===")

    # Configure blind indexing
    config = FieldSecurityConfig(
        index_strategy=FieldIndexStrategy.BLIND,
        search_capabilities=[SearchCapability.EQUALITY]
    )

    # Create transformer
    secret_key = os.urandom(32)
    registry = TransformerRegistry(secret_key, TemporalEncoder())

    # User IDs to protect
    user_ids = [
        "user@example.com",
        "alice@mallku.ai",
        "bob@reciprocity.org"
    ]

    print("Blind indexing for user IDs:")
    blind_indexes = {}
    for user_id in user_ids:
        result = registry.transform_value(user_id, config)
        blind_index = result['blind_index']
        blind_indexes[user_id] = blind_index
        print(f"  {user_id} → {blind_index}")

    print("\nQuery demonstration:")
    search_for = "alice@mallku.ai"
    query_index = registry.transform_value(search_for, config, for_query=True)
    print(f"  Searching for: {search_for}")
    print(f"  Query index: {query_index}")
    print(f"  Match found: {query_index == blind_indexes[search_for]}")


def demo_security_trade_offs():
    """Demonstrate the security/utility trade-offs."""
    print("\n\n=== Security/Utility Trade-offs ===")

    print("Field Configuration Examples:")

    examples = [
        ("timestamp", "UUID_ONLY", "TEMPORAL_OFFSET",
         "Hides absolute time but preserves all temporal queries"),

        ("ayni_score", "ENCRYPTED", "BUCKETED",
         "Protects exact scores but enables range queries for balance monitoring"),

        ("user_id", "UUID_ONLY", "BLIND",
         "Enables user lookup without exposing identities"),

        ("interaction_details", "ENCRYPTED", "NONE",
         "Maximum security for sensitive content, no indexing"),

        ("system_metrics", "UUID_ONLY", "IDENTITY",
         "Less sensitive data with full query capability"),
    ]

    for field, obfuscation, index_strategy, reasoning in examples:
        print(f"\n  {field}:")
        print(f"    Obfuscation: {obfuscation}")
        print(f"    Index: {index_strategy}")
        print(f"    Reasoning: {reasoning}")


if __name__ == "__main__":
    demo_temporal_offset()
    demo_bucketing()
    demo_blind_indexing()
    demo_security_trade_offs()

    print("\n\n=== Summary ===")
    print("Mallku's security architecture demonstrates that we can:")
    print("  1. Protect sensitive data from database compromise")
    print("  2. Maintain essential query capabilities")
    print("  3. Make conscious, documented trade-offs")
    print("  4. Support both free-tier and self-hosted deployments")
    print("\nThis is engineering the balance between perfect and good.")
    print("Building cathedrals that serve their purpose.")
    print("Implementing Ayni in our treatment of user data.")
    print("\n✨ 🏔️ ✨")
