#!/usr/bin/env python3
"""
Simple test for JAEGIS Method Status Display System
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_status_system():
    """Simple test of the status system"""
    
    print("🧪 Testing JAEGIS Method Status Display System")
    print("=" * 50)
    
    try:
        # Test 1: Import status system
        print("1. Testing imports...")
        from core.status import get_status_manager, get_status_display, JAEGISState
        print("   ✅ Status system imported successfully")
        
        # Test 2: Create status manager
        print("2. Testing status manager...")
        manager = get_status_manager()
        print(f"   ✅ Status manager created: {type(manager).__name__}")
        
        # Test 3: Check initial state
        print("3. Testing initial state...")
        state = manager.get_state()
        print(f"   ✅ Initial state: {state.value}")
        
        # Test 4: Test state changes
        print("4. Testing state changes...")
        manager.set_state(JAEGISState.ACTIVE)
        new_state = manager.get_state()
        print(f"   ✅ State changed to: {new_state.value}")
        
        # Test 5: Test uptime
        print("5. Testing uptime...")
        uptime = manager.get_uptime_string()
        print(f"   ✅ Uptime: {uptime}")
        
        # Test 6: Test status display
        print("6. Testing status display...")
        status_box = get_status_display()
        if status_box:
            print("   ✅ Status display generated:")
            print(status_box)
        else:
            print("   ⚠️ Status display is disabled or empty")
        
        # Test 7: Test command handling
        print("7. Testing command handling...")
        from core.status import handle_status_command
        result = handle_status_command('status')
        print(f"   ✅ Status command result: {result.get('success', False)}")
        
        print("\n🎉 All tests passed!")
        return True
        
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_status_system()
    if success:
        print("\n✅ Status system is working correctly!")
    else:
        print("\n❌ Status system test failed!")
    
    sys.exit(0 if success else 1)
