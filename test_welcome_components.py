#!/usr/bin/env python3
"""
Test Welcome Components
=======================

46th Artisan - Verify the unified welcome works without interaction

This script tests the core components of welcome_to_mallku.py
without requiring user input, ensuring all functions work correctly.
"""

import sys
from pathlib import Path

# Import the welcome experience
from welcome_to_mallku import WelcomeExperience


def test_welcome_components():
    """Test individual components of the welcome experience."""
    
    print("Testing Welcome to Mallku Components")
    print("=" * 40)
    
    welcome = WelcomeExperience()
    
    # Test setup checking
    print("\n1. Testing setup checks...")
    try:
        welcome.check_python_version()
        print("   ✓ Python version check works")
    except Exception as e:
        print(f"   ✗ Python version check failed: {e}")
    
    try:
        welcome.check_project_structure()
        print("   ✓ Project structure check works")
    except Exception as e:
        print(f"   ✗ Project structure check failed: {e}")
    
    try:
        welcome.check_api_keys()
        print("   ✓ API keys check works")
    except Exception as e:
        print(f"   ✗ API keys check failed: {e}")
    
    try:
        welcome.check_dependencies()
        print("   ✓ Dependencies check works")
    except Exception as e:
        print(f"   ✗ Dependencies check failed: {e}")
    
    # Test data gathering
    print(f"\n2. Setup analysis results:")
    print(f"   - Python version: {welcome.context['python_version'].major}.{welcome.context['python_version'].minor}")
    print(f"   - Has API keys: {welcome.context['has_api_keys']}")
    print(f"   - Voice count: {welcome.context['voice_count']}")
    print(f"   - Available voices: {', '.join(welcome.voices_available) if welcome.voices_available else 'None'}")
    print(f"   - Issues found: {len(welcome.setup_issues)}")
    
    if welcome.setup_issues:
        print("\n3. Setup issues detected:")
        for issue in welcome.setup_issues:
            print(f"   - {issue}")
    else:
        print("\n3. No setup issues detected!")
    
    # Test text printing
    print("\n4. Testing text display...")
    try:
        welcome.print_slowly("Test text", delay=0.001)  # Fast for testing
        print("   ✓ Slow printing works")
    except Exception as e:
        print(f"   ✗ Slow printing failed: {e}")
    
    print("\n✅ Component testing complete!")
    
    # Return whether setup is ready
    return len(welcome.setup_issues) == 0


if __name__ == "__main__":
    is_ready = test_welcome_components()
    sys.exit(0 if is_ready else 1)