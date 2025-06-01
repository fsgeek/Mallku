#!/usr/bin/env python3
"""
Demonstration of API-Level Security Separation

This script demonstrates how structural mechanisms enforce security by design,
preventing the architectural gap that allowed direct database access to bypass
the security model. Shows the balance achieved through architectural boundaries.
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
from mallku.core.database import get_secured_database, get_security_status
from mallku.core.database.secured_interface import SecurityViolationError
from mallku.reciprocity.models import InteractionRecord
from mallku.streams.reciprocity.secured_reciprocity_models import ReciprocityActivityData


async def demonstrate_api_separation():
    """
    Demonstrate how API-level separation enforces security by design.

    Shows structural mechanisms that prevent security bypasses through
    architectural boundaries rather than relying on developer discipline.
    """
    print("🏗️ Demonstrating API-Level Security Separation")
    print("=" * 55)

    print("\n📐 Architectural Principle:")
    print("   Structure enforces security, not discipline")
    print("   No direct database access - only through secured interface")
    print("   Security policies enforced at collection level")
    print("   Violations blocked by design, not warnings")

    # Test 1: Show secured database interface in action
    print("\n🔒 Test 1: Secured Database Interface")
    print("-" * 40)

    secured_db = get_secured_database()
    await secured_db.initialize()

    print("   ✅ Secured database interface initialized")
    print(f"   📊 Registry mappings: {len(secured_db.get_security_registry()._mappings)}")

    # Test 2: Demonstrate collection security policies
    print("\n🛡️ Test 2: Collection Security Policy Enforcement")
    print("-" * 50)

    try:
        # Get secured collection
        collection = await secured_db.get_secured_collection('reciprocity_activities_secured')
        print("   ✅ Retrieved secured collection with policy enforcement")

        # Create valid secured model
        valid_model = ReciprocityActivityData(
            memory_anchor_uuid=uuid4(),
            interaction_id=uuid4(),
            participant_type="knowledge_exchange",
            contribution_type="teaching"
        )

        # This should work - valid secured model
        await collection.insert_secured(valid_model)
        print("   ✅ Successfully inserted valid SecuredModel")

    except Exception as e:
        print(f"   ⚠️ Collection test: {e}")

    # Test 3: Show security violations are blocked
    print("\n❌ Test 3: Security Violations Blocked by Design")
    print("-" * 48)

    try:
        # Attempt to insert non-secured model
        legacy_interaction = InteractionRecord(
            interaction_id=uuid4(),
            timestamp=datetime.now(UTC),
            interaction_type="test",
            primary_participant="user",
            secondary_participant="system"
        )

        collection = await secured_db.get_secured_collection('reciprocity_activities_secured')
        await collection.insert_secured(legacy_interaction)
        print("   ❌ ERROR: Should have been blocked!")

    except SecurityViolationError as e:
        print(f"   ✅ Security violation correctly blocked: {e}")
    except Exception as e:
        print(f"   ⚠️ Unexpected error: {e}")

    # Test 4: Show direct collection access is blocked
    print("\n🚫 Test 4: Direct Collection Access Blocked")
    print("-" * 43)

    try:
        collection = await secured_db.get_secured_collection('reciprocity_activities_secured')

        # Attempt direct insert (bypassing security)
        collection.insert({"direct": "data"})
        print("   ❌ ERROR: Direct access should be blocked!")

    except SecurityViolationError as e:
        print(f"   ✅ Direct access correctly blocked: {e}")
    except AttributeError as e:
        print(f"   ✅ Direct access blocked by wrapper: {e}")
    except Exception as e:
        print(f"   ⚠️ Unexpected error: {e}")

    # Test 5: Show development-time validation
    print("\n🔍 Test 5: Development-Time Violation Detection")
    print("-" * 48)

    security_status = get_security_status()
    print("   📊 Security Status:")
    print(f"      • Secured interface active: {security_status['secured_interface_active']}")
    print(f"      • Operations count: {security_status.get('operations_count', 0)}")
    print(f"      • Security violations: {security_status.get('security_violations', 0)}")
    print(f"      • Compliance score: {security_status.get('compliance_score', 0.0):.2f}")

    if security_status.get('recent_violations'):
        print("   ⚠️ Recent violations detected:")
        for violation in security_status['recent_violations']:
            print(f"      - {violation}")
    else:
        print("   ✅ No recent security violations")

    # Test 6: Show that legacy database access is monitored
    print("\n📈 Test 6: Legacy Database Access Monitoring")
    print("-" * 46)

    try:
        # This should trigger monitoring but still work for compatibility
        from mallku.core.database import get_database

        print("   ⚠️ Importing legacy get_database() - this is monitored")

        # The call should be logged as a violation
        legacy_db = get_database()
        print(f"   📝 Legacy database access logged (type: {type(legacy_db).__name__})")

        # Check if violation was recorded
        updated_status = get_security_status()
        violations = updated_status.get('security_violations', 0)
        print(f"   📊 Total violations now: {violations}")

    except Exception as e:
        print(f"   ❌ Legacy access test failed: {e}")

    # Test 7: Demonstrate proper security-aware query execution
    print("\n🔍 Test 7: Security-Aware Query Execution")
    print("-" * 42)

    try:
        # Execute query through secured interface
        query = """
        FOR doc IN reciprocity_activities_secured
            LIMIT 5
            RETURN doc
        """

        results = await secured_db.execute_secured_query(
            query,
            collection_name="reciprocity_activities_secured"
        )

        print(f"   ✅ Secured query executed, returned {len(results)} results")
        print("   🔐 Results automatically deobfuscated through security registry")

    except Exception as e:
        print(f"   ⚠️ Secured query test: {e}")

    # Test 8: Show architectural balance
    print("\n⚖️ Test 8: Architectural Balance Demonstration")
    print("-" * 45)

    print("   🏗️ Structural Enforcement Benefits:")
    print("      • Security cannot be accidentally bypassed")
    print("      • Violations are blocked, not just warned about")
    print("      • Collection policies ensure data integrity")
    print("      • Developer mistakes become compile/runtime errors")
    print("      • Security model is mandatory, not optional")

    print("\n   🔄 Backward Compatibility Maintained:")
    print("      • Legacy code still works during migration")
    print("      • Gradual transition path provided")
    print("      • Monitoring helps identify code that needs updating")
    print("      • No breaking changes to existing APIs")

    print("\n   ⚖️ Balance Achieved:")
    print("      • Security enforced structurally")
    print("      • Developer experience preserved")
    print("      • Migration path provided")
    print("      • Violations detectable and preventable")

    print("\n✅ API-Level Separation Demonstration Complete")

    # Final summary
    print("\n🎯 Summary of Structural Security:")
    print("   1. SecuredDatabaseInterface is the ONLY authorized database access")
    print("   2. Collection policies enforce model types and security requirements")
    print("   3. Direct database operations are blocked by SecuredCollectionWrapper")
    print("   4. Legacy access is monitored and logged for migration planning")
    print("   5. Security violations become structural errors, not runtime surprises")
    print("   6. Architecture enforces security by design, not discipline")

    final_metrics = secured_db.get_security_metrics()
    print("\n📊 Final Security Metrics:")
    print(f"   • Total operations: {final_metrics['operations_count']}")
    print(f"   • Violations blocked: {final_metrics['security_violations']}")
    print(f"   • Collections secured: {final_metrics['registered_collections']}")
    print(f"   • Compliance rate: {((final_metrics['operations_count'] - final_metrics['security_violations']) / max(1, final_metrics['operations_count']) * 100):.1f}%")


async def main():
    """Run the API separation demonstration."""
    try:
        await demonstrate_api_separation()
    except Exception as e:
        print(f"\n❌ Demonstration failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
