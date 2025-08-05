#!/usr/bin/env python3

"""
eJAEGIS Failsafe Command Line Interface

Provides command-line control for eJAEGIS failsafe mechanisms with support
for manual enable/disable commands and status reporting.
"""

import sys
import argparse
from pathlib import Path
from eJAEGIS_failsafe_system import eJAEGISFailsafeSystem

def handle_command(args):
    """Handle failsafe commands"""
    eJAEGIS_dir = Path(args.eJAEGIS_path).absolute()
    failsafe = eJAEGISFailsafeSystem(eJAEGIS_dir)
    
    command = args.command.lower().replace('-', '_').replace('/', '')
    
    # Command mappings
    command_map = {
        # Failsafe 1 commands
        'disable_eJAEGIS_init_check': ('failsafe_1_uninitialized_detection.enabled', False),
        'turn_off_eJAEGIS_init_failsafe': ('failsafe_1_uninitialized_detection.enabled', False),
        'enable_eJAEGIS_init_check': ('failsafe_1_uninitialized_detection.enabled', True),
        'turn_on_eJAEGIS_init_failsafe': ('failsafe_1_uninitialized_detection.enabled', True),
        
        # Failsafe 2 commands
        'disable_completion_check': ('failsafe_2_post_completion_detection.enabled', False),
        'turn_off_completion_failsafe': ('failsafe_2_post_completion_detection.enabled', False),
        'enable_completion_check': ('failsafe_2_post_completion_detection.enabled', True),
        'turn_on_completion_failsafe': ('failsafe_2_post_completion_detection.enabled', True),
    }
    
    if command in command_map:
        setting_path, value = command_map[command]
        failsafe.config.update_setting(setting_path, value)
        
        failsafe_name = "Uninitialized eJAEGIS Detection" if "init" in command else "Post-Completion Development Detection"
        status = "enabled" if value else "disabled"
        print(f"✅ {failsafe_name} {status}")
        
    elif command == 'status':
        show_status(failsafe)
    elif command == 'test':
        run_test(failsafe)
    elif command == 'start':
        start_monitoring(failsafe)
    elif command == 'stop':
        stop_monitoring(failsafe)
    elif command == 'config':
        show_config(failsafe)
    elif command == 'reset':
        reset_config(failsafe)
    else:
        print(f"❌ Unknown command: {args.command}")
        show_help()

def show_status(failsafe):
    """Show current failsafe status"""
    print("🔧 eJAEGIS Failsafe System Status")
    print("=" * 40)
    
    config = failsafe.config.config
    
    # Failsafe 1 status
    fs1_enabled = config["failsafe_1_uninitialized_detection"]["enabled"]
    print(f"Failsafe 1 (Uninitialized Detection): {'✅ Enabled' if fs1_enabled else '❌ Disabled'}")
    
    # Failsafe 2 status
    fs2_enabled = config["failsafe_2_post_completion_detection"]["enabled"]
    print(f"Failsafe 2 (Post-Completion Detection): {'✅ Enabled' if fs2_enabled else '❌ Disabled'}")
    
    # eJAEGIS runner status
    eJAEGIS_running = failsafe.is_eJAEGIS_running()
    print(f"eJAEGIS Background Runner: {'✅ Running' if eJAEGIS_running else '❌ Not Running'}")
    
    # Recent activations
    activations = failsafe.state.get("failsafe_activations", [])
    recent_activations = [a for a in activations if a["timestamp"] > "2024-01-01"]  # Recent activations
    print(f"Recent Activations: {len(recent_activations)}")
    
    if recent_activations:
        print("\nRecent Failsafe Activations:")
        for activation in recent_activations[-3:]:  # Show last 3
            timestamp = activation["timestamp"][:19].replace('T', ' ')
            failsafe_name = activation["failsafe"].replace('_', ' ').title()
            print(f"  • {timestamp}: {failsafe_name}")

def run_test(failsafe):
    """Run failsafe tests"""
    print("🧪 Running eJAEGIS Failsafe Tests")
    print("=" * 40)
    
    # Test 1: Check file change detection
    print("Test 1: File Change Detection")
    changes = failsafe.detect_file_changes()
    print(f"  Recent changes detected: {len(changes)}")
    
    # Test 2: Check eJAEGIS process detection
    print("Test 2: eJAEGIS Process Detection")
    eJAEGIS_running = failsafe.is_eJAEGIS_running()
    print(f"  eJAEGIS running: {'Yes' if eJAEGIS_running else 'No'}")
    
    # Test 3: Check project completion status
    print("Test 3: Project Completion Status")
    completion = failsafe.check_project_completion_status()
    print(f"  Project completed: {'Yes' if completion['is_completed'] else 'No'}")
    print(f"  Completed tasks: {len(completion['completed_tasks'])}")
    print(f"  Active tasks: {len(completion['active_tasks'])}")
    
    # Test 4: Check new project detection
    print("Test 4: New Project Detection")
    new_project = failsafe.detect_new_project()
    print(f"  New project detected: {'Yes' if new_project else 'No'}")
    
    # Test 5: Check Git initialization
    print("Test 5: Git Initialization Detection")
    git_init = failsafe.detect_git_initialization()
    print(f"  Recent Git init: {'Yes' if git_init else 'No'}")
    
    print("\n✅ Failsafe tests completed")

def start_monitoring(failsafe):
    """Start failsafe monitoring"""
    print("🚀 Starting eJAEGIS Failsafe monitoring...")
    failsafe.start_monitoring()
    print("✅ Failsafe monitoring started")
    print("Press Ctrl+C to stop monitoring")
    
    try:
        while failsafe.running:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping failsafe monitoring...")
        failsafe.stop_monitoring()
        print("✅ Failsafe monitoring stopped")

def stop_monitoring(failsafe):
    """Stop failsafe monitoring"""
    print("🛑 Stopping eJAEGIS Failsafe monitoring...")
    failsafe.stop_monitoring()
    print("✅ Failsafe monitoring stopped")

def show_config(failsafe):
    """Show current configuration"""
    print("⚙️ eJAEGIS Failsafe Configuration")
    print("=" * 40)
    
    config = failsafe.config.config
    
    print("Failsafe 1 - Uninitialized eJAEGIS Detection:")
    fs1 = config["failsafe_1_uninitialized_detection"]
    print(f"  Enabled: {fs1['enabled']}")
    print(f"  Check Interval: {fs1['check_interval_seconds']} seconds")
    print(f"  File Change Threshold: {fs1['file_change_threshold']}")
    print(f"  Initialization Timeout: {fs1['initialization_timeout_hours']} hours")
    
    print("\nFailsafe 2 - Post-Completion Development Detection:")
    fs2 = config["failsafe_2_post_completion_detection"]
    print(f"  Enabled: {fs2['enabled']}")
    print(f"  Check Interval: {fs2['check_interval_seconds']} seconds")
    print(f"  Grace Period: {fs2['completion_grace_period_hours']} hours")
    print(f"  Change Threshold: {fs2['significant_change_threshold']}")
    
    print("\nGeneral Settings:")
    general = config["general"]
    print(f"  Log Level: {general['log_level']}")
    print(f"  Notification Method: {general['notification_method']}")
    print(f"  Persistence Enabled: {general['persistence_enabled']}")

def reset_config(failsafe):
    """Reset configuration to defaults"""
    print("🔄 Resetting eJAEGIS Failsafe configuration to defaults...")
    
    # Confirm reset
    try:
        confirm = input("Are you sure you want to reset all settings? (y/N): ").lower().strip()
        if confirm != 'y':
            print("Reset cancelled")
            return
    except (KeyboardInterrupt, EOFError):
        print("\nReset cancelled")
        return
    
    # Reset to defaults
    failsafe.config.config = failsafe.config.default_config.copy()
    failsafe.config.save_config()
    
    print("✅ Configuration reset to defaults")

def show_help():
    """Show help information"""
    print("🔧 eJAEGIS Failsafe System Commands")
    print("=" * 40)
    print()
    print("Failsafe 1 (Uninitialized eJAEGIS Detection):")
    print("  /disable-eJAEGIS-init-check        - Disable initialization checking")
    print("  /turn-off-eJAEGIS-init-failsafe    - Turn off initialization failsafe")
    print("  /enable-eJAEGIS-init-check         - Enable initialization checking")
    print("  /turn-on-eJAEGIS-init-failsafe     - Turn on initialization failsafe")
    print()
    print("Failsafe 2 (Post-Completion Development Detection):")
    print("  /disable-completion-check       - Disable completion checking")
    print("  /turn-off-completion-failsafe   - Turn off completion failsafe")
    print("  /enable-completion-check        - Enable completion checking")
    print("  /turn-on-completion-failsafe    - Turn on completion failsafe")
    print()
    print("General Commands:")
    print("  status                          - Show current status")
    print("  test                            - Run failsafe tests")
    print("  start                           - Start monitoring")
    print("  stop                            - Stop monitoring")
    print("  config                          - Show configuration")
    print("  reset                           - Reset to defaults")
    print("  help                            - Show this help")
    print()
    print("Usage Examples:")
    print("  python eJAEGIS-failsafe-cli.py /disable-eJAEGIS-init-check")
    print("  python eJAEGIS-failsafe-cli.py status")
    print("  python eJAEGIS-failsafe-cli.py start")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="eJAEGIS Failsafe System Command Line Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "command",
        help="Failsafe command to execute"
    )
    
    parser.add_argument(
        "--eJAEGIS-path",
        default=".",
        help="Path to eJAEGIS directory (default: current directory)"
    )
    
    if len(sys.argv) == 1:
        show_help()
        return 0
    
    args = parser.parse_args()
    
    try:
        handle_command(args)
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
