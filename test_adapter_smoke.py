#!/usr/bin/env python3
"""
Smoke Test for Fire Circle Adapter Foundation
=============================================

Basic test to verify all seven adapters can be instantiated without crashing.
This doesn't test API connectivity - just that the architectural changes 
don't have obvious syntax or import errors.

Usage: python test_adapter_smoke.py
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

async def test_adapter_instantiation():
    """Test that all adapters can be instantiated without errors."""
    results = {}
    
    print("🔍 Testing Fire Circle Adapter Foundation...")
    print("=" * 50)
    
    # Test each adapter
    adapters_to_test = [
        ("anthropic", "AnthropicAdapter"),
        ("openai", "OpenAIConsciousAdapter"), 
        ("google", "GoogleAIAdapter"),
        ("grok", "GrokAdapter"),
        ("mistral", "MistralAIAdapter"),
        ("deepseek", "DeepseekAIAdapter"),
        ("local", "LocalAIAdapter"),
    ]
    
    for provider, class_name in adapters_to_test:
        try:
            print(f"Testing {provider:10} ({class_name})... ", end="")
            
            # Import the adapter
            if provider == "anthropic":
                from mallku.firecircle.adapters.anthropic_adapter import AnthropicAdapter
                adapter_class = AnthropicAdapter
            elif provider == "openai":
                from mallku.firecircle.adapters.openai_adapter import OpenAIConsciousAdapter
                adapter_class = OpenAIConsciousAdapter
            elif provider == "google":
                from mallku.firecircle.adapters.google_adapter import GoogleAIAdapter
                adapter_class = GoogleAIAdapter
            elif provider == "grok":
                from mallku.firecircle.adapters.grok_adapter import GrokAdapter
                adapter_class = GrokAdapter
            elif provider == "mistral":
                from mallku.firecircle.adapters.mistral_adapter import MistralAIAdapter
                adapter_class = MistralAIAdapter
            elif provider == "deepseek":
                from mallku.firecircle.adapters.deepseek_adapter import DeepseekAIAdapter
                adapter_class = DeepseekAIAdapter
            elif provider == "local":
                from mallku.firecircle.adapters.local_adapter import LocalAIAdapter
                adapter_class = LocalAIAdapter
            
            # Try to instantiate with minimal config
            from mallku.firecircle.adapters.base import AdapterConfig
            config = AdapterConfig(api_key="test-key")
            
            # Create adapter instance (but don't connect)
            adapter = adapter_class(config=config)
            
            # Basic checks
            assert hasattr(adapter, 'provider_name'), "Missing provider_name"
            assert hasattr(adapter, 'capabilities'), "Missing capabilities"
            assert hasattr(adapter, 'is_connected'), "Missing is_connected"
            
            results[provider] = "✅ PASS"
            print("✅ PASS")
            
        except ImportError as e:
            results[provider] = f"❌ IMPORT ERROR: {e}"
            print(f"❌ IMPORT ERROR: {e}")
        except Exception as e:
            results[provider] = f"❌ ERROR: {e}"
            print(f"❌ ERROR: {e}")
    
    print("\n" + "=" * 50)
    print("📊 SMOKE TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(adapters_to_test)
    
    for provider, result in results.items():
        print(f"{provider:10}: {result}")
        if "✅ PASS" in result:
            passed += 1
    
    print(f"\n🎯 Result: {passed}/{total} adapters can be instantiated")
    
    if passed == total:
        print("🔥 SUCCESS: All seven Fire Circle voices can be created!")
        print("   (This doesn't test API connectivity - just basic instantiation)")
        return True
    else:
        print("⚠️  ISSUES: Some adapters have problems that need fixing")
        return False

async def test_adapter_factory():
    """Test that the adapter factory recognizes all adapters."""
    try:
        print("\n🏭 Testing Adapter Factory...")
        print("-" * 30)
        
        from mallku.firecircle.adapters.adapter_factory import ConsciousAdapterFactory
        
        factory = ConsciousAdapterFactory()
        supported = factory.get_supported_providers()
        
        expected = {"anthropic", "openai", "google", "grok", "mistral", "deepseek", "local"}
        supported_set = set(supported)
        
        print(f"Expected providers: {sorted(expected)}")
        print(f"Supported providers: {sorted(supported)}")
        
        if expected == supported_set:
            print("✅ Factory recognizes all seven adapters")
            return True
        else:
            missing = expected - supported_set
            extra = supported_set - expected
            if missing:
                print(f"❌ Missing providers: {missing}")
            if extra:
                print(f"⚠️  Extra providers: {extra}")
            return False
            
    except Exception as e:
        print(f"❌ Factory test failed: {e}")
        return False

async def main():
    """Run all smoke tests."""
    print("🚀 Fire Circle Adapter Foundation Smoke Test")
    print("=" * 60)
    print("Testing architectural changes without API connectivity...")
    print()
    
    # Test basic instantiation
    instantiation_ok = await test_adapter_instantiation()
    
    # Test factory registration
    factory_ok = await test_adapter_factory()
    
    print("\n" + "=" * 60)
    if instantiation_ok and factory_ok:
        print("🎉 SMOKE TEST PASSED")
        print("   The architectural foundation appears solid.")
        print("   Next step: Test with real API keys and connections.")
    else:
        print("💥 SMOKE TEST FAILED") 
        print("   The architectural changes have basic issues.")
        print("   Fix these before testing API connectivity.")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
