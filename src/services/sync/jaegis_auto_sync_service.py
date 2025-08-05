#!/usr/bin/env python3

"""
eJAEGIS Auto-Sync Windows Service Wrapper

This script provides Windows service functionality for the eJAEGIS Auto-Sync monitoring system.
It can be installed as a Windows service using the pywin32 package.

Installation:
1. Install pywin32: pip install pywin32
2. Install service: python eJAEGIS-auto-sync-service.py install
3. Start service: python eJAEGIS-auto-sync-service.py start

Usage:
python eJAEGIS-auto-sync-service.py [install|remove|start|stop|restart|debug]
"""

import sys
import os
import time
import logging
from pathlib import Path

try:
    import win32serviceutil
    import win32service
    import win32event
    import servicemanager
    WINDOWS_SERVICE_AVAILABLE = True
except ImportError:
    WINDOWS_SERVICE_AVAILABLE = False
    print("Warning: pywin32 not available. Windows service functionality disabled.")

# Import the main auto-sync class
sys.path.insert(0, str(Path(__file__).parent))
from eJAEGIS_auto_sync import eJAEGISAutoSync, DEFAULT_JAEGIS_PATH, DEFAULT_MONITOR_INTERVAL

class eJAEGISAutoSyncService(win32serviceutil.ServiceFramework):
    """Windows service wrapper for eJAEGIS Auto-Sync"""
    
    _svc_name_ = "eJAEGISAutoSync"
    _svc_display_name_ = "eJAEGIS Auto-Sync Monitoring Service"
    _svc_description_ = "Monitors JAEGIS-METHOD directory and automatically syncs changes to eJAEGIS GitHub repository"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_running = True

        # Configuration - use the directory where the service script is located
        self.script_dir = Path(__file__).parent.absolute()
        self.jaegis_path = Path(os.environ.get('eJAEGIS_JAEGIS_PATH', DEFAULT_JAEGIS_PATH))
        self.monitor_interval = int(os.environ.get('eJAEGIS_MONITOR_INTERVAL', DEFAULT_MONITOR_INTERVAL))

        # Setup logging
        log_dir = self.script_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / f"eJAEGIS-service-{time.strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def SvcStop(self):
        """Stop the service"""
        self.logger.info('eJAEGIS Auto-Sync service stop requested')
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.is_running = False
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        """Main service execution"""
        try:
            # Report that we're starting
            self.ReportServiceStatus(win32service.SERVICE_START_PENDING)

            self.logger.info('eJAEGIS Auto-Sync service starting...')
            servicemanager.LogMsg(
                servicemanager.EVENTLOG_INFORMATION_TYPE,
                servicemanager.PYS_SERVICE_STARTED,
                (self._svc_name_, '')
            )

            # Report that we're running
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)

            # Create and run auto-sync instance
            try:
                auto_sync = eJAEGISAutoSync(self.jaegis_path, self.monitor_interval)
                self.logger.info(f'Created auto-sync instance for path: {self.jaegis_path}')
            except Exception as e:
                self.logger.error(f'Failed to create auto-sync instance: {e}')
                return

            # Main service loop
            while self.is_running:
                try:
                    # Check if we should stop
                    if win32event.WaitForSingleObject(self.hWaitStop, 0) == win32event.WAIT_OBJECT_0:
                        self.logger.info('Service stop event received')
                        break

                    # Run auto-sync cycle
                    self.logger.debug('Running auto-sync cycle...')
                    auto_sync.run_sync_cycle()

                    # Wait for next cycle or stop event
                    wait_time = self.monitor_interval * 1000  # Convert to milliseconds
                    if win32event.WaitForSingleObject(self.hWaitStop, wait_time) == win32event.WAIT_OBJECT_0:
                        self.logger.info('Service stop event received during wait')
                        break

                except Exception as e:
                    self.logger.error(f'Error in service loop: {e}')
                    # Wait a bit before retrying
                    if win32event.WaitForSingleObject(self.hWaitStop, 60000) == win32event.WAIT_OBJECT_0:
                        break

        except Exception as e:
            self.logger.error(f'Service error: {e}')
            servicemanager.LogErrorMsg(f'eJAEGIS Auto-Sync service error: {e}')
        finally:
            self.logger.info('eJAEGIS Auto-Sync service stopped')
            servicemanager.LogMsg(
                servicemanager.EVENTLOG_INFORMATION_TYPE,
                servicemanager.PYS_SERVICE_STOPPED,
                (self._svc_name_, '')
            )

def run_debug():
    """Run in debug mode (foreground)"""
    print("Running eJAEGIS Auto-Sync in debug mode...")
    
    jaegis_path = Path(os.environ.get('eJAEGIS_JAEGIS_PATH', DEFAULT_JAEGIS_PATH))
    monitor_interval = int(os.environ.get('eJAEGIS_MONITOR_INTERVAL', DEFAULT_MONITOR_INTERVAL))
    
    auto_sync = eJAEGISAutoSync(jaegis_path, monitor_interval)
    
    try:
        auto_sync.run()
    except KeyboardInterrupt:
        print("Debug mode interrupted by user")

def main():
    """Main entry point"""
    if not WINDOWS_SERVICE_AVAILABLE:
        print("Error: pywin32 is required for Windows service functionality")
        print("Install with: pip install pywin32")
        return 1

    if len(sys.argv) == 1:
        # No arguments - show usage
        print("Usage:")
        print("  python eJAEGIS-auto-sync-service.py install    - Install the service")
        print("  python eJAEGIS-auto-sync-service.py remove     - Remove the service")
        print("  python eJAEGIS-auto-sync-service.py start      - Start the service")
        print("  python eJAEGIS-auto-sync-service.py stop       - Stop the service")
        print("  python eJAEGIS-auto-sync-service.py restart    - Restart the service")
        print("  python eJAEGIS-auto-sync-service.py debug      - Run in debug mode")
        print()
        print("Environment Variables:")
        print(f"  eJAEGIS_JAEGIS_PATH      - Path to JAEGIS directory (default: {DEFAULT_JAEGIS_PATH})")
        print(f"  eJAEGIS_MONITOR_INTERVAL - Monitor interval in seconds (default: {DEFAULT_MONITOR_INTERVAL})")
        return 1

    if 'debug' in sys.argv:
        run_debug()
        return 0

    # Handle service commands
    try:
        win32serviceutil.HandleCommandLine(eJAEGISAutoSyncService)
    except Exception as e:
        print(f"Service command failed: {e}")
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())