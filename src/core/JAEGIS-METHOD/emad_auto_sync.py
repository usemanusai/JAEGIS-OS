#!/usr/bin/env python3

"""
eJAEGIS Auto-Sync Module (Python-compatible filename)

This is a Python-compatible filename version of eJAEGIS-auto-sync.py
that can be imported properly by the Windows service wrapper.

This file imports and re-exports everything from the main eJAEGIS-auto-sync.py file.
"""

import sys
import importlib.util
from pathlib import Path

# Import from the main hyphenated filename
main_script_path = Path(__file__).parent / "eJAEGIS-auto-sync.py"

if main_script_path.exists():
    spec = importlib.util.spec_from_file_location("eJAEGIS_auto_sync_main", main_script_path)
    eJAEGIS_auto_sync_main = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(eJAEGIS_auto_sync_main)
    
    # Re-export all the important classes and constants
    eJAEGISAutoSync = eJAEGIS_auto_sync_main.eJAEGISAutoSync
    DEFAULT_JAEGIS_PATH = eJAEGIS_auto_sync_main.DEFAULT_JAEGIS_PATH
    DEFAULT_MONITOR_INTERVAL = eJAEGIS_auto_sync_main.DEFAULT_MONITOR_INTERVAL
    
    # Re-export the main function if needed
    if hasattr(eJAEGIS_auto_sync_main, 'main'):
        main = eJAEGIS_auto_sync_main.main
    
    # Make this module act as a proxy to the main module
    __all__ = ['eJAEGISAutoSync', 'DEFAULT_JAEGIS_PATH', 'DEFAULT_MONITOR_INTERVAL', 'main']
    
else:
    raise ImportError(f"Main script not found: {main_script_path}")

# If this file is run directly, execute the main function
if __name__ == '__main__':
    if 'main' in globals():
        sys.exit(main())
    else:
        print("Error: main function not available")
        sys.exit(1)
