#!/usr/bin/env python3
"""
Quick demo of improved JAEGIS Method Status Display formatting
Shows the enhanced visual output compared to the original format
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def show_improved_formatting():
    """Show the improved status display formatting"""
    
    print("🎨 JAEGIS Method Status Display - Improved Formatting")
    print("=" * 60)
    print()
    
    # Show what the old format looked like
    print("📋 BEFORE - Original Format:")
    print("-" * 35)
    old_format = """┌─ JAEGIS Method Status ───────────────┐
│ State: 🟢 Active                     │
│ Uptime: 02:15:30                     │
│ Activated: 2024-01-15 14:30:00       │
│ Commands: init | sync | exit | status-off │
└──────────────────────────────────────┘"""
    print(old_format)
    
    print("\n\n✨ AFTER - Improved Format:")
    print("-" * 35)
    
    try:
        # Try to import and use the actual status system
        from core.status import get_status_manager, JAEGISState
        from core.status.status_display import StatusDisplay
        
        # Create status manager and set active state
        manager = get_status_manager()
        manager.set_state(JAEGISState.ACTIVE)
        
        # Create display and show premium format
        display = StatusDisplay(manager)
        premium_box = display.get_premium_status_box()
        
        if premium_box:
            print(premium_box)
        else:
            # Fallback to showing the expected format
            show_expected_format()
            
    except ImportError:
        print("Status system not available - showing expected format:")
        show_expected_format()
    except Exception as e:
        print(f"Error generating status: {e}")
        show_expected_format()
    
    print("\n\n🚀 Enhanced Startup Banner:")
    print("-" * 35)
    
    try:
        display = StatusDisplay(manager)
        banner = display.get_startup_banner()
        print(banner)
    except:
        show_expected_banner()
    
    print("\n\n📈 Key Improvements:")
    print("-" * 35)
    improvements = [
        "✅ Double-line borders (╔═══╗) for professional appearance",
        "✅ Enhanced Unicode characters and emojis",
        "✅ Better alignment with separator columns (│)",
        "✅ Cleaner command display with bullet points (•)",
        "✅ More descriptive labels (System, Runtime, Started)",
        "✅ Compact date/time format for readability",
        "✅ State-based styling and visual indicators",
        "✅ Improved spacing and padding",
        "✅ Enhanced error state handling",
        "✅ Better color coding support"
    ]
    
    for improvement in improvements:
        print(f"  {improvement}")
    
    print(f"\n🎯 The new format is more visually appealing, easier to read,")
    print(f"   and provides better information density while maintaining")
    print(f"   professional appearance suitable for enterprise use.")

def show_expected_format():
    """Show the expected improved format when status system isn't available"""
    expected_format = """╔═ ⚡ JAEGIS Method Status ═══════════════════════════╗
║ System    │ 🟢 Active                                ║
║ Runtime   │ ⏱️  02:15:30                             ║
║ Started   │ 🚀 01/15 14:30                           ║
╟──────────────────────────────────────────────────────╢
║ Available │ 🔧 init • 🔄 sync • 🛑 exit • 👁️ status-off ║
╚══════════════════════════════════════════════════════╝"""
    print(expected_format)

def show_expected_banner():
    """Show the expected improved banner"""
    expected_banner = """╔══════════════════════════════════════════════════╗
║                 ⚡ JAEGIS Method v2.2             ║
║           Advanced AI Agent Orchestration         ║
║                                                   ║
║  🤖 128 Agents    │  🔐 S.C.R.I.P.T. Framework   ║
║  🌐 A.T.L.A.S.    │  🧠 Command Adjudicator      ║
║  📊 Status System │  🔄 Real-time Monitoring     ║
╚══════════════════════════════════════════════════╝"""
    print(expected_banner)

def show_different_states():
    """Show how different states look with improved formatting"""
    
    print("\n\n🔄 Different System States:")
    print("-" * 35)
    
    states = [
        ("🟢 Active", "System fully operational"),
        ("🟡 Initializing", "System starting up"),
        ("🔴 Inactive", "System offline"),
        ("❌ Error", "System error state")
    ]
    
    for state_icon, description in states:
        print(f"\n{state_icon} State - {description}:")
        
        # Show a sample of how each state would look
        if "Active" in description:
            sample = """╔═ ⚡ JAEGIS Method Status ═══════════════════════════╗
║ System    │ 🟢 Active                                ║
║ Runtime   │ ⏱️  02:15:30                             ║
║ Started   │ 🚀 01/15 14:30                           ║
╟──────────────────────────────────────────────────────╢
║ Available │ 🔧 init • 🔄 sync • 🛑 exit • 👁️ status-off ║
╚══════════════════════════════════════════════════════╝"""
        elif "Initializing" in description:
            sample = """╔═ ⚡ JAEGIS Method Status ═══════════════════════════╗
║ System    │ 🟡 Initializing                         ║
║ Runtime   │ ⏱️  00:00:15                             ║
║ Started   │ 🚀 01/15 14:30                           ║
╟──────────────────────────────────────────────────────╢
║ Available │ 🔧 init • 🔄 sync • 🛑 exit • 👁️ status-off ║
╚══════════════════════════════════════════════════════╝"""
        elif "Inactive" in description:
            sample = """┌─ ⚡ JAEGIS Method Status ─────────────────────────────┐
│ System    │ 🔴 Inactive                              │
│ Runtime   │ ⏸️  Not Running                          │
│ Started   │ 🚫 Never Initialized                     │
├──────────────────────────────────────────────────────┤
│ Available │ 🔧 init • 🔄 sync • 🛑 exit • 👁️ status-off │
└──────────────────────────────────────────────────────┘"""
        else:  # Error state
            sample = """╔═ ⚡ JAEGIS Method Status ═══════════════════════════╗
║ System    │ ❌ Error                                 ║
║ Runtime   │ ⏱️  01:45:22                             ║
║ Started   │ 🚀 01/15 14:30                           ║
╟──────────────────────────────────────────────────────╢
║ Available │ 🔧 init • 🔄 sync • 🛑 exit • 👁️ status-off ║
╚══════════════════════════════════════════════════════╝"""
        
        print(sample)

if __name__ == "__main__":
    show_improved_formatting()
    show_different_states()
    
    print(f"\n\n🎉 Improved formatting demonstration complete!")
    print(f"The JAEGIS Method Status Display now provides a much more")
    print(f"professional and visually appealing experience! ✨")
