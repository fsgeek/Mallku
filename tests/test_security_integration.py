"""
Test the security integration with reciprocity models.

This demonstrates how the security framework balances protection with utility.
"""

import json
from datetime import UTC, datetime
from uuid import uuid4

from mallku.core.security import (
    SecurityRegistry,
    TemporalEncoder,
)
from mallku.streams.reciprocity.secured_reciprocity_models import (
    ReciprocityActivityData,
    ReciprocityBalance,
)


def test_security_integration():
    """Test the complete security integration."""

    # Create and configure registry
    registry = SecurityRegistry()

    # Configure models to use this registry
    ReciprocityActivityData.set_registry(registry)
    ReciprocityBalance.set_registry(registry)

    # Create sample reciprocity data
    activity = ReciprocityActivityData(
        memory_anchor_uuid=uuid4(),
        timestamp=datetime.now(UTC),
        interaction_id=uuid4(),
        interaction={
            "type": "query",
            "content_hash": "sha256:abcd1234",
            "complexity": 0.7
        },
        initiator="human",
        participants=["human", "claude"],
        ayni_score={
            "value_given": 0.3,
            "value_received": 0.8,
            "value_delta": -0.5,
            "balance_direction": "ai_gave_more"
        },
        system_health={
            "is_system_failure": False,
            "response_coherence": 0.98
        }
    )

    # Test production mode (default)
    print("=== Production Mode ===")
    prod_dict = activity.dict()
    print(json.dumps(prod_dict, indent=2, default=str))

    # Test development mode
    print("\n=== Development Mode ===")
    ReciprocityActivityData.set_development_mode(True)
    dev_dict = activity.dict()
    print(json.dumps(dev_dict, indent=2, default=str))

    # Test temporal encoding
    print("\n=== Temporal Encoding ===")
    temporal_config = registry.get_temporal_config()
    encoder = TemporalEncoder(temporal_config.offset_seconds)

    original_time = activity.timestamp
    encoded_time = encoder.encode(original_time)
    decoded_time = encoder.decode(encoded_time)

    print(f"Original: {original_time}")
    print(f"Encoded: {encoded_time}")
    print(f"Decoded: {decoded_time}")
    print(f"Offset days: {temporal_config.offset_days:.1f}")

    # Test security validation
    print("\n=== Security Validation ===")
    warnings = activity.validate_security_configuration()
    if warnings:
        print("Warnings found:")
        for field, field_warnings in warnings.items():
            print(f"  {field}: {field_warnings}")
    else:
        print("No security configuration warnings")

    # Test registry export/import
    print("\n=== Registry Persistence ===")
    export_data = registry.export_mappings()
    print(f"Exported {len(export_data['mappings'])} field mappings")

    # Create new registry from export
    new_registry = SecurityRegistry.from_export(export_data)
    print(f"Imported {len(new_registry._mappings)} field mappings")

    # Test balance tracking with bucketed fields
    print("\n=== Balance Tracking ===")
    balance = ReciprocityBalance(
        participant_a_id="user_123_obfuscated",
        participant_b_id="claude_456_obfuscated",
        current_balance=-0.6,  # Will be bucketed
        total_interactions=42,
        relationship_health=0.7  # Will be bucketed
    )

    balance_dict = balance.dict()
    print(f"Balance fields: {list(balance_dict.keys())}")

    # Show how bucketing works
    print("\n=== Bucketing Example ===")
    # The actual implementation would apply bucketing during storage
    balance_config = registry.get_security_config("current_balance")
    if balance_config and balance_config.bucket_boundaries:
        print(f"Balance buckets: {balance_config.bucket_boundaries}")
        print("Value -0.6 would be stored in bucket: [-0.8, -0.5)")


if __name__ == "__main__":
    test_security_integration()
