"""Check how mallku is installed."""

import sys
from pathlib import Path


def test_check_mallku_installation():
    """Check if mallku is properly installed."""
    print("\n=== Checking mallku installation ===")
    
    # Check site-packages
    for path in sys.path:
        if 'site-packages' in str(path):
            site_packages = Path(path)
            print(f"\nChecking site-packages: {site_packages}")
            
            # Look for mallku
            mallku_paths = list(site_packages.glob("mallku*"))
            if mallku_paths:
                print("Found mallku-related files:")
                for p in mallku_paths:
                    print(f"  - {p.name}")
                    if p.name.endswith('.pth'):
                        # Read .pth file
                        try:
                            content = p.read_text().strip()
                            print(f"    Content: {content}")
                        except Exception as e:
                            print(f"    Error reading: {e}")
            else:
                print("  No mallku files found")
    
    # Check if there's a .pth file
    print("\n=== Checking for .pth files ===")
    pth_files = []
    for path in sys.path:
        if Path(path).exists():
            pth_files.extend(Path(path).glob("*.pth"))
    
    if pth_files:
        print("Found .pth files:")
        for pth in pth_files:
            print(f"  - {pth}")
            try:
                content = pth.read_text().strip()
                print(f"    Content: {content}")
            except Exception:
                pass
    else:
        print("No .pth files found")
    
    assert True  # Always pass to see output