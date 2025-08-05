#!/usr/bin/env python3

"""
eJAEGIS Background Runner

A simpler alternative to Windows service that runs eJAEGIS Auto-Sync in the background.
This approach is more reliable and easier to manage than Windows services.
"""

import sys
import os
import time
import signal
import subprocess
import threading
from pathlib import Path
from datetime import datetime

# Import failsafe system
try:
    from eJAEGIS_failsafe_system import eJAEGISFailsafeSystem
    FAILSAFE_AVAILABLE = True
except ImportError:
    FAILSAFE_AVAILABLE = False

class eJAEGISBackgroundRunner:
    def __init__(self):
        self.running = False
        self.process = None
        self.script_dir = Path(__file__).parent.absolute()
        self.pid_file = self.script_dir / "eJAEGIS-runner.pid"
        self.log_file = self.script_dir / "logs" / f"eJAEGIS-background-{datetime.now().strftime('%Y%m%d')}.log"

        # Ensure logs directory exists
        self.log_file.parent.mkdir(exist_ok=True)

        # Initialize failsafe system
        self.failsafe = None
        if FAILSAFE_AVAILABLE:
            try:
                self.failsafe = eJAEGISFailsafeSystem(self.script_dir)
                self.log("Failsafe system initialized")
            except Exception as e:
                self.log(f"Warning: Could not initialize failsafe system: {e}")

        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.log(f"Received signal {signum}, shutting down...")
        self.stop()
        sys.exit(0)

    def log(self, message):
        """Log a message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        
        print(log_message)
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_message + "\n")
        except Exception as e:
            print(f"Failed to write to log file: {e}")

    def write_pid(self):
        """Write current process PID to file"""
        try:
            with open(self.pid_file, 'w') as f:
                f.write(str(os.getpid()))
            self.log(f"PID file written: {self.pid_file}")
        except Exception as e:
            self.log(f"Failed to write PID file: {e}")

    def remove_pid(self):
        """Remove PID file"""
        try:
            if self.pid_file.exists():
                self.pid_file.unlink()
                self.log("PID file removed")
        except Exception as e:
            self.log(f"Failed to remove PID file: {e}")

    def is_running(self):
        """Check if background runner is already running"""
        if not self.pid_file.exists():
            return False
        
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            # Check if process with this PID exists
            try:
                os.kill(pid, 0)  # Signal 0 just checks if process exists
                return True
            except OSError:
                # Process doesn't exist, remove stale PID file
                self.remove_pid()
                return False
                
        except (ValueError, FileNotFoundError):
            return False

    def start(self):
        """Start the background runner"""
        if self.is_running():
            print("❌ eJAEGIS Background Runner is already running")
            return False
        
        print("🚀 Starting eJAEGIS Background Runner...")
        self.log("eJAEGIS Background Runner starting...")
        
        # Write PID file
        self.write_pid()
        
        # Import and create auto-sync instance
        try:
            sys.path.insert(0, str(self.script_dir))
            from eJAEGIS_auto_sync import eJAEGISAutoSync
            
            auto_sync = eJAEGISAutoSync(self.script_dir)
            self.log(f"Created auto-sync instance for: {self.script_dir}")
            
        except Exception as e:
            self.log(f"Failed to create auto-sync instance: {e}")
            self.remove_pid()
            return False
        
        self.running = True
        
        # Start monitoring loop
        try:
            self.log("Starting monitoring loop...")
            
            while self.running:
                try:
                    # Run auto-sync cycle
                    self.log("Running auto-sync cycle...")
                    auto_sync.run_sync_cycle()
                    
                    # Run failsafe checks if available
                    if self.failsafe:
                        try:
                            self.failsafe.run_health_checks()
                        except Exception as e:
                            self.log(f"Failsafe check error: {e}")
                    
                    # Wait before next cycle
                    self.log("Cycle complete, waiting for next cycle...")
                    time.sleep(300)  # 5 minutes
                    
                except KeyboardInterrupt:
                    self.log("Received keyboard interrupt")
                    break
                except Exception as e:
                    self.log(f"Error in monitoring loop: {e}")
                    time.sleep(60)  # Wait 1 minute before retrying
                    
        except Exception as e:
            self.log(f"Fatal error in background runner: {e}")
            return False
        finally:
            self.running = False
            self.remove_pid()
            self.log("eJAEGIS Background Runner stopped")
        
        return True

    def stop(self):
        """Stop the background runner"""
        if not self.is_running():
            print("❌ eJAEGIS Background Runner is not running")
            return False
        
        print("🛑 Stopping eJAEGIS Background Runner...")
        
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            # Send termination signal
            os.kill(pid, signal.SIGTERM)
            
            # Wait for process to stop
            for _ in range(10):  # Wait up to 10 seconds
                try:
                    os.kill(pid, 0)
                    time.sleep(1)
                except OSError:
                    break
            else:
                # Force kill if still running
                try:
                    os.kill(pid, signal.SIGKILL)
                    print("⚠️  Forced termination of background runner")
                except OSError:
                    pass
            
            self.remove_pid()
            print("✅ eJAEGIS Background Runner stopped")
            return True
            
        except Exception as e:
            print(f"❌ Error stopping background runner: {e}")
            return False

    def status(self):
        """Show status of background runner"""
        if self.is_running():
            try:
                with open(self.pid_file, 'r') as f:
                    pid = int(f.read().strip())
                print(f"✅ eJAEGIS Background Runner is running (PID: {pid})")
                
                # Show recent log entries
                if self.log_file.exists():
                    print("\nRecent log entries:")
                    try:
                        with open(self.log_file, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                            for line in lines[-5:]:  # Show last 5 lines
                                print(f"  {line.strip()}")
                    except Exception as e:
                        print(f"  Error reading log file: {e}")
                
            except Exception as e:
                print(f"❌ Error checking status: {e}")
        else:
            print("❌ eJAEGIS Background Runner is not running")

    def restart(self):
        """Restart the background runner"""
        print("🔄 Restarting eJAEGIS Background Runner...")
        
        if self.is_running():
            self.stop()
            time.sleep(2)  # Wait a moment
        
        return self.start()

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="eJAEGIS Background Runner")
    parser.add_argument('action', choices=['start', 'stop', 'restart', 'status'], 
                       help='Action to perform')
    
    args = parser.parse_args()
    
    runner = eJAEGISBackgroundRunner()
    
    if args.action == 'start':
        if runner.start():
            return 0
        else:
            return 1
    elif args.action == 'stop':
        if runner.stop():
            return 0
        else:
            return 1
    elif args.action == 'restart':
        if runner.restart():
            return 0
        else:
            return 1
    elif args.action == 'status':
        runner.status()
        return 0

if __name__ == "__main__":
    exit(main())