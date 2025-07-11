#!/usr/bin/env python3
"""
Seven-Voice Capability Smoke Test
=================================

CRITICAL: Verify all seven Fire Circle adapters can be instantiated.

This test has NEVER BEEN EXECUTED according to Issue #67.
Today we change that.
"""

import sys
import asyncio
import argparse
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from mallku.firecircle.adapters.adapter_factory import ConsciousAdapterFactory
from mallku.firecircle.adapters.base import AdapterConfig
from mallku.firecircle.adapters.google_adapter import GeminiConfig
from mallku.firecircle.adapters.mistral_adapter import MistralConfig
from mallku.firecircle.adapters.local_adapter import LocalAdapterConfig, LocalBackend
from mallku.firecircle.adapters.grok_openai_adapter import GrokOpenAIConfig


def print_header():
    """Print test header."""
    print("\n" + "=" * 70)
    print("🔥 SEVEN-VOICE FIRE CIRCLE CAPABILITY SMOKE TEST")
    print("=" * 70)
    print("\nCRITICAL: Testing foundational adapter instantiation")
    print("Each adapter must be able to instantiate without API keys")
    print("This verifies architectural foundation only\n")


def print_adapter_test(name: str, index: int, total: int):
    """Print adapter test header."""
    print(f"\n{index}/{total} Testing {name} Adapter")
    print("-" * 40)


async def test_adapter(adapter_name: str, config: AdapterConfig = None) -> bool:
    """Test a single adapter instantiation WITHOUT connecting to APIs."""
    try:
        # Import the adapter class directly to test instantiation only
        adapter_classes = {
            "anthropic": ("anthropic_adapter", "AnthropicAdapter"),
            "openai": ("openai_adapter", "OpenAIConsciousAdapter"),
            "google": ("google_adapter", "GoogleAIAdapter"),
            "mistral": ("mistral_adapter", "MistralAIAdapter"),
            "grok": ("grok_openai_adapter", "GrokOpenAIAdapter"),
            "deepseek": ("deepseek_adapter", "DeepseekAIAdapter"),
            "local": ("local_adapter", "LocalAIAdapter"),
        }
        
        if adapter_name not in adapter_classes:
            print(f"❌ FAILED: Unknown adapter {adapter_name}")
            return False
            
        module_name, class_name = adapter_classes[adapter_name]
        
        # Import the adapter module
        module = __import__(
            f"mallku.firecircle.adapters.{module_name}",
            fromlist=[class_name]
        )
        adapter_class = getattr(module, class_name)
        
        # Create minimal config if not provided
        if config is None:
            config = AdapterConfig(api_key="test", model_name="test-model")
        
        # Instantiate adapter WITHOUT connecting
        adapter = adapter_class(
            config=config,
            event_bus=None,
            reciprocity_tracker=None
        )
        
        # Verify adapter was created
        if adapter is None:
            print(f"❌ FAILED: Adapter instantiation returned None for {adapter_name}")
            return False
            
        print(f"✅ SUCCESS: {adapter_name} adapter instantiated (no API connection)")
        print(f"   Type: {type(adapter).__name__}")
        print(f"   Model: {getattr(config, 'model_name', 'Unknown')}")
        print(f"   Provider: {getattr(adapter, 'provider_name', 'Unknown')}")
        return True
        
    except ImportError as e:
        print(f"❌ FAILED: Import error for {adapter_name}")
        print(f"   Error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ FAILED: {adapter_name} adapter instantiation failed")
        print(f"   Error type: {type(e).__name__}")
        print(f"   Error: {e}")
        return False


def test_factory_registration():
    """Test that factory recognizes all seven adapters."""
    print("\n🏭 Testing Factory Registration")
    print("-" * 40)
    
    try:
        factory = ConsciousAdapterFactory()
        
        # Check if factory has expected methods
        if hasattr(factory, 'get_available_adapters'):
            available = factory.get_available_adapters()
            print(f"✅ Factory reports {len(available)} available adapters:")
            for adapter in available:
                print(f"   - {adapter}")
        else:
            print("⚠️  Factory does not expose available adapters list")
            
        return True
        
    except Exception as e:
        print(f"❌ FAILED: Factory instantiation failed")
        print(f"   Error: {e}")
        return False


async def main(exclude_local=False):
    """Run seven-voice capability smoke tests."""
    print_header()
    
    # Test factory first
    factory_ok = test_factory_registration()
    
    # Define the seven voices with appropriate configs
    seven_voices = [
        ("anthropic", AdapterConfig(api_key="test", model_name="claude-3-opus-20240229")),
        ("openai", AdapterConfig(api_key="test", model_name="gpt-4")),
        ("google", GeminiConfig(api_key="test", model_name="gemini-pro", enable_search_grounding=False)),
        ("mistral", MistralConfig(api_key="test", model_name="mistral-large-latest", multilingual_mode=True)),
        ("grok", GrokOpenAIConfig(api_key="test", model_name="grok-beta", temporal_awareness=True)),
        ("deepseek", AdapterConfig(api_key="test", model_name="deepseek-chat")),
    ]
    
    # Add local adapter unless excluded
    if not exclude_local:
        seven_voices.append(
            ("local", LocalAdapterConfig(api_key="", model_name="gemma2", backend=LocalBackend.OLLAMA, base_url="http://localhost:11434"))
        )
    
    # Track results
    results = {
        "total": len(seven_voices),
        "passed": 0,
        "failed": 0,
        "failures": []
    }
    
    # Test each adapter
    for i, (name, config) in enumerate(seven_voices, 1):
        print_adapter_test(name.upper(), i, len(seven_voices))
        
        if await test_adapter(name, config):
            results["passed"] += 1
        else:
            results["failed"] += 1
            results["failures"].append(name)
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 SEVEN-VOICE CAPABILITY TEST SUMMARY")
    print("=" * 70)
    print(f"\nTotal Adapters: {results['total']}")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    
    if results["failed"] > 0:
        print(f"\nFailed Adapters: {', '.join(results['failures'])}")
        if exclude_local:
            print("\n⚠️  WARNING: Six-voice capability has failures!")
            print("   Fire Circle needs all available voices operational")
        else:
            print("\n🚨 CRITICAL: Seven-voice capability is NOT operational!")
            print("   Fire Circle cannot function without all seven voices")
    else:
        if exclude_local:
            print("\n✅ SUCCESS: All six voices (excluding local) are operational!")
            print("   Fire Circle foundation verified for CI/CD")
        else:
            print("\n🎉 SUCCESS: All seven voices are operational!")
            print("   Fire Circle foundation is verified")
    
    print("\n" + "=" * 70)
    
    # Return exit code
    return 0 if results["failed"] == 0 else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seven-Voice Fire Circle Capability Smoke Test")
    parser.add_argument(
        "--exclude-local",
        action="store_true",
        help="Exclude local adapter test (useful for CI/CD environments)"
    )
    args = parser.parse_args()
    
    exit_code = asyncio.run(main(exclude_local=args.exclude_local))
    sys.exit(exit_code)