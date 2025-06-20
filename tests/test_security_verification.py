#!/usr/bin/env python3
"""
Verification tests for security implementation.

These tests verify that our security architecture actually works as designed.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from datetime import UTC, datetime, timedelta

from mallku.core.security import (
    FieldIndexStrategy,
    FieldSecurityConfig,
    SearchCapability,
    SecurityRegistry,
    TemporalEncoder,
    TransformerRegistry,
)


def test_temporal_offset_preserves_relationships():
    """Verify temporal offset maintains time relationships."""
    print("Testing temporal offset...")

    # Create encoder
    encoder = TemporalEncoder(offset_seconds=86400 * 365)  # 1 year offset

    # Test times
    now = datetime.now(UTC)
    hour_ago = now - timedelta(hours=1)
    day_ago = now - timedelta(days=1)

    # Encode
    enc_now = encoder.encode(now)
    enc_hour = encoder.encode(hour_ago)
    enc_day = encoder.encode(day_ago)

    # Verify relationships preserved
    assert enc_now > enc_hour > enc_day, "Temporal ordering not preserved"
    assert abs((enc_now - enc_hour) - 3600) < 1, "Hour difference not preserved"
    assert abs((enc_now - enc_day) - 86400) < 1, "Day difference not preserved"

    # Verify decode works
    decoded = encoder.decode(enc_now)
    assert abs((decoded - now).total_seconds()) < 1, "Decode not accurate"

    print("✓ Temporal offset correctly preserves relationships")


def test_bucket_transformation():
    """Verify bucketing works correctly."""
    print("\nTesting bucket transformation...")

    config = FieldSecurityConfig(
        index_strategy=FieldIndexStrategy.BUCKETED, bucket_boundaries=[-1.0, -0.5, 0.0, 0.5, 1.0]
    )

    registry = TransformerRegistry(b"test_key", TemporalEncoder())

    # Test values and expected buckets
    test_cases = [
        (-0.8, (-1.0, -0.5)),
        (-0.3, (-0.5, 0.0)),
        (0.0, (-0.5, 0.0)),  # Edge case
        (0.3, (0.0, 0.5)),
        (0.8, (0.5, 1.0)),
        (1.5, (1.0, float("inf"))),  # Above range
        (-1.5, (float("-inf"), -1.0)),  # Below range
    ]

    for value, expected_bucket in test_cases:
        result = registry.transform_value(value, config)
        actual_bucket = (result["bucket_min"], result["bucket_max"])
        assert actual_bucket == expected_bucket, (
            f"Value {value} gave {actual_bucket}, expected {expected_bucket}"
        )

    print("✓ Bucketing correctly assigns values to ranges")


def test_registry_uuid_generation():
    """Verify registry creates consistent UUIDs."""
    print("\nTesting registry UUID generation...")

    registry1 = SecurityRegistry()
    registry2 = SecurityRegistry()

    # Same field should get same UUID across instances
    uuid1 = registry1.get_or_create_mapping("user_email")
    uuid2 = registry2.get_or_create_mapping("user_email")

    assert uuid1 == uuid2, "UUIDs not deterministic"
    assert len(uuid1) == 36, "UUID wrong format"
    assert uuid1 != "user_email", "UUID not obfuscated"

    # Different fields get different UUIDs
    uuid3 = registry1.get_or_create_mapping("user_id")
    assert uuid3 != uuid1, "Different fields got same UUID"

    # Reverse lookup works
    assert registry1.get_semantic_name(uuid1) == "user_email"

    print("✓ Registry generates consistent, deterministic UUIDs")


def test_blind_indexing():
    """Verify blind indexing provides consistent hashes."""
    print("\nTesting blind indexing...")

    config = FieldSecurityConfig(index_strategy=FieldIndexStrategy.BLIND)

    key = b"consistent_test_key"
    registry1 = TransformerRegistry(key, TemporalEncoder())
    registry2 = TransformerRegistry(key, TemporalEncoder())

    # Same value should get same blind index
    value = "user@example.com"
    result1 = registry1.transform_value(value, config)
    result2 = registry2.transform_value(value, config)

    assert result1["blind_index"] == result2["blind_index"], "Blind index not consistent"
    assert len(result1["blind_index"]) == 16, "Blind index wrong length"
    assert result1["blind_index"] != value, "Value not obfuscated"

    # Different values get different indexes
    result3 = registry1.transform_value("other@example.com", config)
    assert result3["blind_index"] != result1["blind_index"], "Different values same index"

    print("✓ Blind indexing creates consistent, unique indexes")


def test_security_validation():
    """Verify security config validation works."""
    print("\nTesting security validation...")

    # Invalid config - RANGE query with BLIND index
    config = FieldSecurityConfig(
        index_strategy=FieldIndexStrategy.BLIND, search_capabilities=[SearchCapability.RANGE]
    )

    warnings = config.validate_configuration()
    assert len(warnings) > 0, "Should warn about BLIND not supporting RANGE"
    assert "RANGE" in warnings[0], "Warning should mention RANGE"

    # Valid config - RANGE with BUCKETED
    config2 = FieldSecurityConfig(
        index_strategy=FieldIndexStrategy.BUCKETED,
        search_capabilities=[SearchCapability.RANGE],
        bucket_boundaries=[0, 1, 2],
    )

    warnings2 = config2.validate_configuration()
    assert len(warnings2) == 0, "Valid config should have no warnings"

    print("✓ Security validation catches configuration issues")


if __name__ == "__main__":
    print("=== Security Implementation Verification ===\n")

    try:
        test_temporal_offset_preserves_relationships()
        test_bucket_transformation()
        test_registry_uuid_generation()
        test_blind_indexing()
        test_security_validation()

        print("\n=== All Tests Passed ===")
        print("The security implementation works as designed.")

    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
