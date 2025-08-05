#!/usr/bin/env python3
"""
Test script for improved JAEGIS Method Status Display formatting
Shows the enhanced visual output with better styling and formatting
"""

import sys
import os
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_improved_display():
    """Test the improved status display formatting"""
    
    print("🎨 JAEGIS Method Status Display - Improved Formatting Test")
    print("=" * 65)
    print()
    
    try:
        # Import status system components
        from core.status import get_status_manager, JAEGISState
        from core.status.status_display import StatusDisplay
        
        print("✅ Status system imported successfully")
        print()
        
        # Create status manager and display
        manager = get_status_manager()
        display = StatusDisplay(manager)
        
        # Test different states with improved formatting
        test_states = [
            (JAEGISState.ACTIVE, None, "Active System"),
            (JAEGISState.INITIALIZING, None, "System Starting Up"),
            (JAEGISState.INACTIVE, None, "System Offline"),
            (JAEGISState.ERROR, "Connection timeout to S.C.R.I.P.T. API", "Error State")
        ]
        
        for state, error_details, description in test_states:
            print(f"📊 {description}")
            print("-" * 40)
            
            # Set the state
            manager.set_state(state, error_details)
            
            # Show premium status box
            print("Premium Status Box:")
            premium_box = display.get_premium_status_box()
            if premium_box:
                print(premium_box)
            else:
                print("Status display disabled")
            
            print()
            
            # Show enhanced status line
            print("Status Line:")
            status_line = display.get_status_line()
            if status_line:
                print(status_line)
            else:
                print("Status line disabled")
            
            print("\n" + "=" * 65 + "\n")
        
        # Test startup banner
        print("🚀 Enhanced Startup Banner")
        print("-" * 40)
        banner = display.get_startup_banner()
        print(banner)
        print()
        
        # Test command help
        print("📖 Command Help Display")
        print("-" * 40)
        help_display = display.get_command_help()
        print(help_display)
        print()
        
        # Test different display modes
        print("🔄 Display Mode Comparison")
        print("-" * 40)
        
        # Set to active state for comparison
        manager.set_state(JAEGISState.ACTIVE)
        
        print("1. Premium Status Box (Default):")
        premium = display.get_premium_status_box()
        if premium:
            print(premium)
        print()
        
        print("2. Compact Status Box (Legacy):")
        compact = display._get_compact_status_box()
        if compact:
            print(compact)
        print()
        
        print("3. Detailed Status Box:")
        detailed = display._get_detailed_status_box()
        if detailed:
            print(detailed)
        print()
        
        # Test fallback display
        print("🛡️ Fallback Display Test")
        print("-" * 40)
        fallback = display._get_fallback_status()
        print(f"Fallback: {fallback}")
        print()
        
        print("🎉 Improved formatting test completed successfully!")
        print("=" * 65)
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\nMake sure the status system is properly installed.")
        return False
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_response_integration():
    """Test the improved formatting in response integration"""
    
    print("\n🔄 Response Integration Test with Improved Formatting")
    print("=" * 65)
    print()
    
    try:
        from core.status.response_wrapper import wrap_ai_response
        
        # Test response wrapping with improved formatting
        sample_responses = [
            "Hello! I'm ready to help you with JAEGIS Method operations.",
            "I've successfully initialized the JAEGIS Method system. All 128 agents are now active and ready for deployment.",
            "The synchronization process has completed successfully. All repositories are now up to date.",
            "System status check completed. All services are running optimally."
        ]
        
        for i, response in enumerate(sample_responses, 1):
            print(f"📝 Sample Response {i}:")
            print("-" * 40)
            
            wrapped = wrap_ai_response(response)
            print(wrapped)
            
            print("\n" + "=" * 65 + "\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Response integration test failed: {e}")
        return False

def show_formatting_comparison():
    """Show before/after comparison of formatting"""
    
    print("📊 Formatting Comparison: Before vs After")
    print("=" * 65)
    print()
    
    print("BEFORE (Original Format):")
    print("-" * 30)
    old_format = """┌─ JAEGIS Method Status ───────────────┐
│ State: 🟢 Active                     │
│ Uptime: 02:15:30                     │
│ Activated: 2024-01-15 14:30:00       │
│ Commands: init | sync | exit | status-off │
└──────────────────────────────────────┘"""
    print(old_format)
    
    print("\n\nAFTER (Improved Format):")
    print("-" * 30)
    new_format = """╔═ ⚡ JAEGIS Method Status ═══════════════════════════╗
║ System    │ 🟢 Active                                ║
║ Runtime   │ ⏱️  02:15:30                             ║
║ Started   │ 🚀 01/15 14:30                           ║
╟──────────────────────────────────────────────────────╢
║ Available │ 🔧 init • 🔄 sync • 🛑 exit • 👁️ status-off ║
╚══════════════════════════════════════════════════════╝"""
    print(new_format)
    
    print("\n\n✨ Key Improvements:")
    print("• Double-line borders for more professional appearance")
    print("• Enhanced Unicode characters and emojis")
    print("• Better alignment with separator columns (│)")
    print("• Cleaner command display with bullet points (•)")
    print("• More descriptive labels (System, Runtime, Started)")
    print("• Compact date/time format for better readability")
    print("• State-based styling and visual indicators")

if __name__ == "__main__":
    print(f"🕒 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Show formatting comparison first
    show_formatting_comparison()
    print("\n" + "=" * 65 + "\n")
    
    # Run the improved display test
    success = test_improved_display()
    
    if success:
        # Test response integration
        test_response_integration()
        print("✅ All tests completed successfully!")
    else:
        print("❌ Tests failed!")
    
    print(f"\n🕒 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
