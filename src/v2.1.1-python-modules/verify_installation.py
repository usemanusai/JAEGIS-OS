#!/usr/bin/env python3
"""
JAEGIS Installation Verification
================================

This script verifies that your JAEGIS installation is complete and ready to run.
"""

import sys
import os
from pathlib import Path

def print_header():
    """Print verification header"""
    print("="*80)
    print("🔍 JAEGIS INSTALLATION VERIFICATION")
    print("="*80)

def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} (Good)")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (Need 3.8+)")
        return False

def check_required_modules():
    """Check required Python modules"""
    print("📦 Checking required modules...")
    
    required_modules = [
        'asyncio',
        'logging',
        'pathlib',
        'sqlite3',
        'json',
        'typing'
    ]
    
    all_good = True
    for module in required_modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError:
            print(f"   ❌ {module} (missing)")
            all_good = False
    
    return all_good

def check_file_structure():
    """Check JAEGIS file structure"""
    print("📁 Checking JAEGIS file structure...")
    
    current_dir = Path(__file__).parent
    
    required_files = [
        'jaegis_simple.py',
        'QUICK_START.md',
        'run_genesis_test.bat'
    ]
    
    required_dirs = [
        'core',
        'jaegis_cockpit',
        'jaegis_cockpit/frontend',
        'jaegis_cockpit/backend'
    ]
    
    all_good = True
    
    # Check files
    for file_path in required_files:
        full_path = current_dir / file_path
        if full_path.exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} (missing)")
            all_good = False
    
    # Check directories
    for dir_path in required_dirs:
        full_path = current_dir / dir_path
        if full_path.exists() and full_path.is_dir():
            print(f"   ✅ {dir_path}/")
        else:
            print(f"   ❌ {dir_path}/ (missing)")
            all_good = False
    
    return all_good

def check_common_library():
    """Check common library structure"""
    print("🔧 Checking common library...")
    
    current_dir = Path(__file__).parent
    common_dir = current_dir.parent.parent / "common"
    
    if not common_dir.exists():
        print("   ❌ Common library not found")
        return False
    
    required_common_files = [
        'core/base_classes.py',
        'core/__init__.py',
        'core/database.py',
        'core/config_management.py'
    ]
    
    all_good = True
    for file_path in required_common_files:
        full_path = common_dir / file_path
        if full_path.exists():
            print(f"   ✅ common/{file_path}")
        else:
            print(f"   ❌ common/{file_path} (missing)")
            all_good = False
    
    return all_good

def check_core_frameworks():
    """Check core JAEGIS frameworks"""
    print("🏗️ Checking core frameworks...")
    
    current_dir = Path(__file__).parent
    
    frameworks = [
        'core/script',
        'core/atlas', 
        'core/helm',
        'core/mastr',
        'core/ascend'
    ]
    
    all_good = True
    for framework in frameworks:
        framework_dir = current_dir / framework
        if framework_dir.exists() and framework_dir.is_dir():
            # Check for key files
            key_files = list(framework_dir.glob('*.py'))
            if key_files:
                print(f"   ✅ {framework}/ ({len(key_files)} Python files)")
            else:
                print(f"   ⚠️ {framework}/ (no Python files)")
                all_good = False
        else:
            print(f"   ❌ {framework}/ (missing)")
            all_good = False
    
    return all_good

def check_cockpit_interface():
    """Check JAEGIS Cockpit interface"""
    print("🎛️ Checking JAEGIS Cockpit...")
    
    current_dir = Path(__file__).parent
    
    # Check backend
    backend_dir = current_dir / 'jaegis_cockpit' / 'backend'
    if backend_dir.exists():
        backend_files = list(backend_dir.glob('*.py'))
        print(f"   ✅ Backend ({len(backend_files)} Python files)")
    else:
        print("   ❌ Backend (missing)")
        return False
    
    # Check frontend
    frontend_dir = current_dir / 'jaegis_cockpit' / 'frontend'
    if frontend_dir.exists():
        # Check for key frontend files
        package_json = frontend_dir / 'package.json'
        src_dir = frontend_dir / 'src'
        
        if package_json.exists() and src_dir.exists():
            print("   ✅ Frontend (SvelteKit structure)")
        else:
            print("   ⚠️ Frontend (incomplete structure)")
    else:
        print("   ❌ Frontend (missing)")
        return False
    
    return True

def run_basic_test():
    """Run a basic functionality test"""
    print("🧪 Running basic functionality test...")
    
    try:
        # Test basic Python functionality
        import asyncio
        import logging
        
        async def test_async():
            await asyncio.sleep(0.01)
            return True
        
        result = asyncio.run(test_async())
        if result:
            print("   ✅ Async/await functionality")
        else:
            print("   ❌ Async/await functionality")
            return False
        
        # Test logging
        logger = logging.getLogger('test')
        logger.info("Test message")
        print("   ✅ Logging functionality")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Basic test failed: {e}")
        return False

def print_summary(results):
    """Print verification summary"""
    print("\n" + "="*80)
    print("📋 VERIFICATION SUMMARY")
    print("="*80)
    
    total_checks = len(results)
    passed_checks = sum(results.values())
    
    for check_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {check_name}")
    
    print(f"\nOverall: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks == total_checks:
        print("\n🎉 JAEGIS INSTALLATION VERIFIED!")
        print("✅ Your JAEGIS ecosystem is ready to run!")
        print("\n🚀 Next steps:")
        print("   1. Run: python jaegis_simple.py --genesis-test")
        print("   2. Or double-click: run_genesis_test.bat")
        print("   3. See QUICK_START.md for detailed instructions")
    else:
        print("\n⚠️ INSTALLATION INCOMPLETE")
        print("❌ Some components are missing or incomplete")
        print("📖 Please check the failed items above")

def main():
    """Main verification function"""
    print_header()
    
    results = {}
    
    # Run all checks
    results["Python Version"] = check_python_version()
    results["Required Modules"] = check_required_modules()
    results["File Structure"] = check_file_structure()
    results["Common Library"] = check_common_library()
    results["Core Frameworks"] = check_core_frameworks()
    results["Cockpit Interface"] = check_cockpit_interface()
    results["Basic Functionality"] = run_basic_test()
    
    # Print summary
    print_summary(results)
    
    return all(results.values())

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
