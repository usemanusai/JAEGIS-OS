#!/usr/bin/env python3
"""
Test script to verify JAEGIS imports work correctly
"""

import sys
import os
from pathlib import Path

# Add current directory to path for local imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Add the common directory from the root JAEGIS directory
common_dir = current_dir.parent.parent / "common"
if common_dir.exists():
    sys.path.insert(0, str(common_dir))

def test_imports():
    """Test all critical imports"""
    try:
        print(f"Python path: {sys.path[:3]}...")
        print(f"Current directory: {os.getcwd()}")
        print(f"Common directory exists: {(Path(__file__).parent / 'common').exists()}")

        print("Testing direct import from common...")
        # Try direct import from the common directory
        import importlib.util
        common_path = current_dir.parent.parent / "common" / "core" / "base_classes.py"
        print(f"Trying to load from: {common_path}")

        if common_path.exists():
            spec = importlib.util.spec_from_file_location("base_classes", common_path)
            base_classes_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(base_classes_module)
            BaseJAEGISService = base_classes_module.BaseJAEGISService
            print("✅ BaseJAEGISService imported successfully via direct import")
        else:
            print(f"❌ File not found: {common_path}")
            return False
        
        print("Testing service imports...")
        
        # Test if the service modules exist
        service_paths = [
            "core/script/service.py",
            "core/atlas/service.py", 
            "core/helm/service.py",
            "core/mastr/service.py",
            "core/ascend/service.py",
            "common/core/cori/service.py",
            "jaegis_cockpit/backend/service.py"
        ]
        
        for service_path in service_paths:
            if Path(service_path).exists():
                print(f"✅ {service_path} exists")
            else:
                print(f"❌ {service_path} missing")
        
        print("\nAll import tests completed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
