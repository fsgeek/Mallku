"""Enhanced debug test to understand import issues in CI."""

import sys
import os
import subprocess
import importlib.util
import pkg_resources
from pathlib import Path


def test_comprehensive_import_debug():
    """Comprehensive test to debug why imports fail in CI."""
    print("\n=== ENVIRONMENT INFORMATION ===")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"HOME: {os.environ.get('HOME', 'NOT SET')}")
    print(f"PYTHONPATH: {os.environ.get('PYTHONPATH', 'NOT SET')}")
    
    print("\n=== SYS.PATH CONTENTS ===")
    for i, path in enumerate(sys.path):
        print(f"  [{i}] {path}")
    
    # Check directory structure
    print("\n=== DIRECTORY STRUCTURE ===")
    cwd = Path.cwd()
    print(f"Project root: {cwd}")
    
    src_path = cwd / "src"
    if src_path.exists():
        print(f"✓ src/ exists at {src_path}")
        mallku_path = src_path / "mallku"
        if mallku_path.exists():
            print(f"✓ src/mallku/ exists")
            init_file = mallku_path / "__init__.py"
            print(f"  __init__.py exists: {init_file.exists()}")
            if init_file.exists():
                print(f"  __init__.py size: {init_file.stat().st_size} bytes")
        else:
            print("✗ src/mallku/ does NOT exist")
    else:
        print("✗ src/ does NOT exist")
    
    # Check installed packages
    print("\n=== INSTALLED PACKAGE CHECK ===")
    try:
        dist = pkg_resources.get_distribution('mallku')
        print(f"✓ mallku is installed via pkg_resources")
        print(f"  Version: {dist.version}")
        print(f"  Location: {dist.location}")
    except pkg_resources.DistributionNotFound:
        print("✗ mallku NOT found via pkg_resources")
    
    # Check with pip
    print("\n=== PIP SHOW MALLKU ===")
    result = subprocess.run(['pip', 'show', 'mallku'], capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout)
    else:
        print("✗ pip show mallku failed")
        print(f"stderr: {result.stderr}")
    
    # Check editable installs
    print("\n=== EDITABLE INSTALLS ===")
    result = subprocess.run(['pip', 'list', '--editable'], capture_output=True, text=True)
    print(result.stdout)
    
    # Check .pth files
    print("\n=== CHECKING .PTH FILES ===")
    site_packages = [p for p in sys.path if 'site-packages' in p]
    for sp in site_packages:
        sp_path = Path(sp)
        if sp_path.exists():
            pth_files = list(sp_path.glob('*.pth'))
            if pth_files:
                print(f"Found .pth files in {sp}:")
                for pth in pth_files:
                    print(f"  {pth.name}: {pth.read_text().strip()}")
    
    # Try to find mallku module spec
    print("\n=== MODULE SPEC SEARCH ===")
    spec = importlib.util.find_spec('mallku')
    if spec:
        print(f"✓ Module spec found!")
        print(f"  Name: {spec.name}")
        print(f"  Origin: {spec.origin}")
        print(f"  Submodule locations: {spec.submodule_search_locations}")
    else:
        print("✗ Module spec NOT found")
    
    # Import attempts
    print("\n=== IMPORT ATTEMPTS ===")
    
    # Attempt 1: Direct import
    print("\n1. Direct import attempt:")
    try:
        import mallku
        print(f"  ✓ Success! mallku.__file__ = {mallku.__file__}")
        print(f"  mallku.__path__ = {getattr(mallku, '__path__', 'No __path__')}")
    except ImportError as e:
        print(f"  ✗ Failed: {e}")
    
    # Attempt 2: Add src to path
    print("\n2. After adding src to sys.path:")
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
        print(f"  Added {src_path} to sys.path[0]")
    
    try:
        import mallku
        print(f"  ✓ Success! mallku.__file__ = {mallku.__file__}")
    except ImportError as e:
        print(f"  ✗ Failed: {e}")
        
        # Check if it's a deeper issue
        print("\n  Checking for import errors in mallku/__init__.py:")
        init_path = src_path / "mallku" / "__init__.py"
        if init_path.exists():
            # Try to exec the file to see what breaks
            try:
                exec(compile(init_path.read_text(), str(init_path), 'exec'))
                print("    ✓ __init__.py executes without errors")
            except Exception as exec_err:
                print(f"    ✗ Error executing __init__.py: {exec_err}")
    
    # Attempt 3: Import submodules
    print("\n3. Submodule import attempts:")
    submodules = ['core', 'core.database', 'firecircle', 'services']
    for submod in submodules:
        try:
            mod = __import__(f'mallku.{submod}', fromlist=[''])
            print(f"  ✓ mallku.{submod} imported successfully")
        except ImportError as e:
            print(f"  ✗ mallku.{submod} failed: {e}")
    
    # Check pytest behavior
    print("\n=== PYTEST SPECIFIC CHECKS ===")
    print(f"__file__ of this test: {__file__}")
    print(f"pytest imported: {'pytest' in sys.modules}")
    if 'pytest' in sys.modules:
        import pytest
        print(f"pytest version: {pytest.__version__}")
    
    # Always pass so we see output
    assert True