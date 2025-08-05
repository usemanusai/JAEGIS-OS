#!/usr/bin/env python3
"""
JAEGIS Method Status Display System Demo
Demonstrates the complete status system functionality

Shows status display, command processing, and integration
with the existing JAEGIS architecture.
"""

import os
import sys
import time
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def demo_status_system():
    """Demonstrate the JAEGIS Method Status Display System"""
    
    print("🚀 JAEGIS Method Status Display System Demo")
    print("=" * 60)
    print()
    
    try:
        # Import status system components
        from core.status import (
            get_status_manager, 
            get_status_display, 
            is_status_enabled,
            handle_status_command,
            JAEGISState
        )
        from core.status.response_wrapper import get_response_wrapper, wrap_ai_response
        
        print("✅ Status system imported successfully")
        print()
        
        # Get status manager and wrapper
        status_manager = get_status_manager()
        response_wrapper = get_response_wrapper()
        
        # Demo 1: Initial Status Display
        print("📊 Demo 1: Initial Status Display")
        print("-" * 40)
        
        status_box = get_status_display()
        if status_box:
            print(status_box)
        else:
            print("Status display is disabled or unavailable")
        print()
        
        # Demo 2: System Initialization
        print("🔧 Demo 2: System Initialization")
        print("-" * 40)
        
        init_result = handle_status_command('init')
        print(f"Initialization result: {init_result.get('success', False)}")
        print(f"Message: {init_result.get('message', 'No message')}")
        print()
        
        # Show status after initialization
        print("Status after initialization:")
        status_box = get_status_display()
        if status_box:
            print(status_box)
        print()
        
        # Demo 3: Command Processing
        print("⚙️ Demo 3: Command Processing")
        print("-" * 40)
        
        test_commands = ['status', 'sync', 'status-off', 'status-on']
        
        for cmd in test_commands:
            print(f"Processing command: '{cmd}'")
            result = handle_status_command(cmd)
            print(f"  Success: {result.get('success', False)}")
            print(f"  Message: {result.get('message', result.get('error', 'No message'))}")
            print()
            
            # Show status display state after status-off/status-on
            if cmd in ['status-off', 'status-on']:
                print(f"  Status display enabled: {is_status_enabled()}")
                print()
        
        # Demo 4: Response Wrapping
        print("🔄 Demo 4: Response Wrapping")
        print("-" * 40)
        
        # Ensure status is enabled for demo
        handle_status_command('status-on')
        
        sample_response = """I have successfully analyzed your request and implemented the required functionality. 

The JAEGIS Method Status Display System is now fully operational with the following features:
- Real-time system state tracking
- Persistent user preferences
- Integration with S.C.R.I.P.T. and A.T.L.A.S. frameworks
- Natural language command processing

All components are working correctly and ready for production use."""
        
        wrapped_response = wrap_ai_response(sample_response)
        print("Wrapped AI Response:")
        print(wrapped_response)
        print()
        
        # Demo 5: Status States
        print("🔄 Demo 5: Status State Changes")
        print("-" * 40)
        
        states_to_demo = [
            (JAEGISState.ACTIVE, None),
            (JAEGISState.ERROR, "Demo error condition"),
            (JAEGISState.INITIALIZING, None),
            (JAEGISState.ACTIVE, None)
        ]
        
        for state, error_details in states_to_demo:
            print(f"Setting state to: {state.value}")
            status_manager.set_state(state, error_details)
            
            # Small delay to show uptime changes
            time.sleep(1)
            
            status_box = get_status_display()
            if status_box:
                print(status_box)
            print()
        
        # Demo 6: System Health Check
        print("🏥 Demo 6: System Health Check")
        print("-" * 40)
        
        health_result = handle_status_command('status')
        if health_result.get('success', False):
            health_info = health_result.get('status', {})
            print(f"System State: {health_info.get('state', 'Unknown')}")
            print(f"Uptime: {health_info.get('uptime', 'N/A')}")
            print(f"Activation Time: {health_info.get('activation_time', 'Never')}")
            print(f"S.C.R.I.P.T. Available: {health_info.get('script_available', False)}")
            
            services = health_info.get('services', {})
            if services:
                print("\nService Health:")
                for service, status in services.items():
                    if isinstance(status, dict):
                        print(f"  {service}: {status.get('status', 'unknown')}")
        else:
            print(f"Health check failed: {health_result.get('error', 'Unknown error')}")
        print()
        
        # Demo 7: Command Integration with Adjudicator
        print("🧠 Demo 7: Command Adjudicator Integration")
        print("-" * 40)
        
        try:
            from core.intelligence.command_adjudicator import CommandAdjudicator
            
            adjudicator = CommandAdjudicator()
            
            test_natural_commands = [
                "initialize the system",
                "sync the repositories", 
                "turn off status display",
                "show system status"
            ]
            
            for cmd in test_natural_commands:
                print(f"Natural language command: '{cmd}'")
                result = adjudicator.adjudicate(cmd)
                print(f"  Intent: {result.get('intent', 'unknown')}")
                print(f"  Success: {result.get('success', False)}")
                if 'message' in result:
                    print(f"  Message: {result['message']}")
                if 'error' in result:
                    print(f"  Error: {result['error']}")
                print()
                
        except ImportError:
            print("Command Adjudicator not available for integration demo")
            print()
        
        # Demo 8: Graceful Shutdown
        print("🔴 Demo 8: Graceful Shutdown")
        print("-" * 40)
        
        shutdown_result = handle_status_command('exit')
        print(f"Shutdown result: {shutdown_result.get('success', False)}")
        print(f"Message: {shutdown_result.get('message', 'No message')}")
        
        # Final status display
        print("\nFinal status:")
        status_box = get_status_display()
        if status_box:
            print(status_box)
        
        print("\n🎉 JAEGIS Method Status Display System Demo Complete!")
        print("=" * 60)
        
        return True
        
    except ImportError as e:
        print(f"❌ Status system not available: {e}")
        print("\nTo use the status system, ensure all components are properly installed:")
        print("1. S.C.R.I.P.T. framework for persistence")
        print("2. Status system modules in core/status/")
        print("3. Command Adjudicator integration")
        return False
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def demo_response_integration():
    """Demonstrate response integration"""
    
    print("\n🔄 Response Integration Demo")
    print("=" * 40)
    
    try:
        from core.status.response_wrapper import process_user_command, wrap_ai_response
        
        # Simulate user commands
        user_inputs = [
            "init",
            "Hello, how are you?",
            "status-off", 
            "What's the weather like?",
            "status-on",
            "sync"
        ]
        
        for user_input in user_inputs:
            print(f"\nUser: {user_input}")
            
            # Check if it's a status command
            command_response = process_user_command(user_input)
            
            if command_response:
                # It was a status command
                wrapped_response = wrap_ai_response(command_response, show_start=False)
                print(f"Assistant: {wrapped_response}")
            else:
                # Regular AI response
                ai_response = f"I understand you said '{user_input}'. This is a simulated AI response."
                wrapped_response = wrap_ai_response(ai_response)
                print(f"Assistant: {wrapped_response}")
        
        return True
        
    except Exception as e:
        print(f"❌ Response integration demo failed: {e}")
        return False

if __name__ == "__main__":
    # Run the complete demo
    success = demo_status_system()
    
    if success:
        demo_response_integration()
    
    print(f"\nDemo completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
