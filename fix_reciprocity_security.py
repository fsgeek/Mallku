#!/usr/bin/env python3
"""
Demonstrate proper security-aware reciprocity tracking implementation.

This shows how the ReciprocityTracker should integrate with the UUID mapping
layer and field-level security model.
"""

import asyncio
import sys
from pathlib import Path
from uuid import uuid4

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# ruff: noqa: E402
from mallku.core.security.registry import SecurityRegistry
from mallku.streams.reciprocity.secured_reciprocity_models import ReciprocityActivityData


class SecureReciprocityTracker:
    """
    Reciprocity tracker that properly integrates with the security model.

    This demonstrates how database operations should go through the
    UUID mapping layer and field obfuscation.
    """

    def __init__(self):
        """Initialize with security registry."""
        self.security_registry = SecurityRegistry()
        # Create new registry for reciprocity tracking
        # In production, this would load from persistent storage

    async def record_interaction_securely(self, interaction_data: dict) -> str:
        """
        Record interaction using proper security model.

        Returns the obfuscated interaction ID for reference.
        """

        # Create secured model instance
        secured_interaction = ReciprocityActivityData(
            memory_anchor_uuid=uuid4(),  # Would come from Memory Anchor Service
            interaction_id=uuid4(),
            participant_type="human_ai_interaction",
            contribution_type="knowledge_exchange",
            **interaction_data
        )

        # Get obfuscated version for storage
        obfuscated_data = secured_interaction.to_storage_dict(self.security_registry)

        print("🔒 Original vs Obfuscated Data:")
        print(f"   Original interaction_id: {secured_interaction.interaction_id}")
        print(f"   Obfuscated interaction_id: {obfuscated_data.get('interaction_id', 'N/A')}")

        if 'timestamp' in obfuscated_data:
            print(f"   Original timestamp: {secured_interaction.timestamp}")
            print(f"   Obfuscated timestamp: {obfuscated_data['timestamp']}")

        # In a real implementation, this would go to ArangoDB
        # with proper schema validation
        print("   ✅ Would store obfuscated data in database")

        # Save registry changes
        self.security_registry.save_to_file("reciprocity_security_registry.json")

        return str(secured_interaction.interaction_id)

    async def retrieve_interaction_securely(self, obfuscated_id: str):
        """
        Retrieve and deobfuscate interaction data.
        """

        # In real implementation, query ArangoDB using obfuscated ID
        mock_stored_data = {
            "interaction_id": obfuscated_id,
            "timestamp": "2025-06-01T03:30:00+00:00",  # Would be offset
            "participant_type": "human_ai_interaction",
            "contribution_type": "knowledge_exchange"
        }

        # Deobfuscate using registry
        try:
            deobfuscated = ReciprocityActivityData.from_storage_dict(
                mock_stored_data,
                self.security_registry
            )

            print("🔓 Deobfuscated Data Retrieved:")
            print(f"   Interaction ID: {deobfuscated.interaction_id}")
            print(f"   Timestamp: {deobfuscated.timestamp}")
            print(f"   Type: {deobfuscated.participant_type}")

            return deobfuscated

        except Exception as e:
            print(f"❌ Deobfuscation failed: {e}")
            return None


async def demonstrate_security_integration():
    """Show how reciprocity tracking should integrate with security."""

    print("🔐 Demonstrating Secure Reciprocity Tracking")
    print("=" * 50)

    tracker = SecureReciprocityTracker()

    # Record interaction with security
    interaction_data = {
        "participant_type": "human_ai_interaction",
        "contribution_type": "knowledge_exchange"
    }

    print("\n1. Recording Interaction Securely:")
    obfuscated_id = await tracker.record_interaction_securely(interaction_data)

    print("\n2. Retrieving Interaction by Obfuscated ID:")
    await tracker.retrieve_interaction_securely(obfuscated_id)

    print("\n3. Security Registry Status:")
    print(f"   UUID mappings: {len(tracker.security_registry.uuid_mappings)}")
    print(f"   Field configs: {len(tracker.security_registry.field_configs)}")

    # Show what the current implementation is missing
    print("\n❌ Current Reciprocity Service Issues:")
    print("   - Bypasses UUID mapping layer entirely")
    print("   - Stores sensitive data in clear text")
    print("   - No schema validation at database level")
    print("   - Direct AQL queries without field mapping")

    print("\n✅ What Should Be Fixed:")
    print("   - All database operations through security registry")
    print("   - Use SecuredModel for all reciprocity data")
    print("   - Add ArangoDB collection validation rules")
    print("   - Migrate existing data through security transformation")


if __name__ == "__main__":
    asyncio.run(demonstrate_security_integration())
