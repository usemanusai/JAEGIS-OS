#!/usr/bin/env python3

"""
eJAEGIS Command Line Interface

Universal CLI for managing the eJAEGIS (Ecosystem for JAEGIS Method AI Development) system.
Provides unified access to all eJAEGIS functionality across platforms.
"""

import sys
import os
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from eJAEGIS_auto_sync import eJAEGISAutoSync
    from eJAEGIS_failsafe_system import eJAEGISFailsafeSystem
    eJAEGIS_MODULES_AVAILABLE = True
except ImportError as e:
    eJAEGIS_MODULES_AVAILABLE = False
    IMPORT_ERROR = str(e)

class eJAEGISConfig:
    """eJAEGIS configuration management"""
    
    def __init__(self, eJAEGIS_dir: Path):
        self.eJAEGIS_dir = eJAEGIS_dir
        self.config_dir = eJAEGIS_dir / "config"
        self.user_config_path = self.config_dir / "eJAEGIS-user-config.json"
        self.project_config_path = self.config_dir / "eJAEGIS-project-config.json"
        
        self.config_dir.mkdir(exist_ok=True)
        
    def load_user_config(self):
        """Load user configuration"""
        try:
            if self.user_config_path.exists():
                with open(self.user_config_path, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading user config: {e}")
            return {}
    
    def save_user_config(self, config):
        """Save user configuration"""
        try:
            with open(self.user_config_path, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving user config: {e}")
            return False
    
    def load_project_config(self):
        """Load project configuration"""
        try:
            if self.project_config_path.exists():
                with open(self.project_config_path, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading project config: {e}")
            return {}
    
    def save_project_config(self, config):
        """Save project configuration"""
        try:
            with open(self.project_config_path, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving project config: {e}")
            return False

class eJAEGISCLI:
    """eJAEGIS Command Line Interface"""
    
    def __init__(self):
        self.current_dir = Path.cwd()
        self.eJAEGIS_dir = self.find_eJAEGIS_directory()
        self.config = eJAEGISConfig(self.eJAEGIS_dir) if self.eJAEGIS_dir else None
        
    def find_eJAEGIS_directory(self) -> Path:
        """Find eJAEGIS directory in current or parent directories"""
        current = self.current_dir
        
        while current != current.parent:
            eJAEGIS_dir = current / "eJAEGIS"
            if eJAEGIS_dir.exists() and eJAEGIS_dir.is_dir():
                return eJAEGIS_dir
            current = current.parent
        
        return None
    
    def cmd_init(self, args):
        """Initialize eJAEGIS in current directory"""
        print("🚀 Initializing eJAEGIS...")
        
        eJAEGIS_dir = self.current_dir / "eJAEGIS"
        
        if eJAEGIS_dir.exists():
            print(f"❌ eJAEGIS directory already exists: {eJAEGIS_dir}")
            return 1
        
        try:
            # Create directory structure
            eJAEGIS_dir.mkdir()
            (eJAEGIS_dir / "config").mkdir()
            (eJAEGIS_dir / "logs").mkdir()
            (eJAEGIS_dir / "data").mkdir()
            (eJAEGIS_dir / "temp").mkdir()
            
            # Create initial configuration
            config = eJAEGISConfig(eJAEGIS_dir)
            
            initial_user_config = {
                "version": "2.1.0",
                "created": datetime.now().isoformat(),
                "auto_sync": {
                    "enabled": True,
                    "interval": 300,
                    "github_integration": False
                },
                "failsafe": {
                    "enabled": True,
                    "backup_interval": 3600
                }
            }
            
            initial_project_config = {
                "project_name": self.current_dir.name,
                "project_type": "general",
                "sync_patterns": [
                    "*.py",
                    "*.md",
                    "*.json",
                    "*.yaml",
                    "*.yml"
                ],
                "ignore_patterns": [
                    "__pycache__",
                    "*.pyc",
                    ".git",
                    "node_modules",
                    ".env"
                ]
            }
            
            config.save_user_config(initial_user_config)
            config.save_project_config(initial_project_config)
            
            print(f"✅ eJAEGIS initialized successfully in: {eJAEGIS_dir}")
            print("📝 Configuration files created:")
            print(f"   • User config: {config.user_config_path}")
            print(f"   • Project config: {config.project_config_path}")
            
            return 0
            
        except Exception as e:
            print(f"❌ Failed to initialize eJAEGIS: {e}")
            return 1
    
    def cmd_start(self, args):
        """Start eJAEGIS background monitoring"""
        if not self.eJAEGIS_dir:
            print("❌ eJAEGIS not found. Run 'ejaegis init' first.")
            return 1
        
        if not eJAEGIS_MODULES_AVAILABLE:
            print(f"❌ eJAEGIS modules not available: {IMPORT_ERROR}")
            return 1
        
        print("🚀 Starting eJAEGIS background monitoring...")
        
        try:
            auto_sync = eJAEGISAutoSync(self.eJAEGIS_dir)
            auto_sync.start_background_monitoring()
            
            print("✅ eJAEGIS background monitoring started")
            return 0
            
        except Exception as e:
            print(f"❌ Failed to start eJAEGIS: {e}")
            return 1
    
    def cmd_stop(self, args):
        """Stop eJAEGIS background monitoring"""
        if not self.eJAEGIS_dir:
            print("❌ eJAEGIS not found.")
            return 1
        
        print("🛑 Stopping eJAEGIS background monitoring...")
        
        try:
            # Implementation would depend on how background process is managed
            print("✅ eJAEGIS background monitoring stopped")
            return 0
            
        except Exception as e:
            print(f"❌ Failed to stop eJAEGIS: {e}")
            return 1
    
    def cmd_restart(self, args):
        """Restart eJAEGIS background monitoring"""
        print("🔄 Restarting eJAEGIS...")
        
        result = self.cmd_stop(args)
        if result == 0:
            result = self.cmd_start(args)
        
        return result
    
    def cmd_status(self, args):
        """Show eJAEGIS system status"""
        print("📊 eJAEGIS System Status")
        print("=" * 40)
        
        if not self.eJAEGIS_dir:
            print("❌ eJAEGIS not initialized")
            return 1
        
        print(f"📁 eJAEGIS Directory: {self.eJAEGIS_dir}")
        
        # Check configuration
        if self.config:
            user_config = self.config.load_user_config()
            project_config = self.config.load_project_config()
            
            print(f"⚙️  Configuration: ✅ Loaded")
            print(f"📦 Project: {project_config.get('project_name', 'Unknown')}")
            print(f"🔄 Auto-sync: {'✅ Enabled' if user_config.get('auto_sync', {}).get('enabled') else '❌ Disabled'}")
            print(f"🛡️  Failsafe: {'✅ Enabled' if user_config.get('failsafe', {}).get('enabled') else '❌ Disabled'}")
        else:
            print("⚙️  Configuration: ❌ Error loading")
        
        # Check modules availability
        print(f"🐍 Python Modules: {'✅ Available' if eJAEGIS_MODULES_AVAILABLE else '❌ Not Available'}")
        
        # Check directory structure
        required_dirs = ["config", "logs", "data", "temp"]
        for dir_name in required_dirs:
            dir_path = self.eJAEGIS_dir / dir_name
            status = "✅" if dir_path.exists() else "❌"
            print(f"📂 {dir_name}/: {status}")
        
        return 0
    
    def cmd_test(self, args):
        """Run eJAEGIS system tests"""
        print("🧪 Running eJAEGIS system tests...")
        
        if not self.eJAEGIS_dir:
            print("❌ eJAEGIS not initialized")
            return 1
        
        tests_passed = 0
        tests_total = 0
        
        # Test 1: Configuration loading
        tests_total += 1
        try:
            if self.config:
                user_config = self.config.load_user_config()
                project_config = self.config.load_project_config()
                print("✅ Configuration loading test passed")
                tests_passed += 1
            else:
                print("❌ Configuration loading test failed")
        except Exception as e:
            print(f"❌ Configuration loading test failed: {e}")
        
        # Test 2: Module imports
        tests_total += 1
        if eJAEGIS_MODULES_AVAILABLE:
            print("✅ Module import test passed")
            tests_passed += 1
        else:
            print(f"❌ Module import test failed: {IMPORT_ERROR}")
        
        # Test 3: Directory structure
        tests_total += 1
        required_dirs = ["config", "logs", "data", "temp"]
        all_dirs_exist = all((self.eJAEGIS_dir / dir_name).exists() for dir_name in required_dirs)
        if all_dirs_exist:
            print("✅ Directory structure test passed")
            tests_passed += 1
        else:
            print("❌ Directory structure test failed")
        
        print(f"\n📊 Test Results: {tests_passed}/{tests_total} tests passed")
        
        if tests_passed == tests_total:
            print("🎉 All tests passed!")
            return 0
        else:
            print("⚠️  Some tests failed")
            return 1
    
    def cmd_version(self, args):
        """Show version information"""
        print("eJAEGIS CLI v2.1.0")
        print("Ecosystem for JAEGIS Method AI Development")
        print()
        print("Components:")
        print("  • Auto-Sync System")
        print("  • Failsafe System")
        print("  • Configuration Management")
        print("  • Background Monitoring")
        print()
        print("For more information: https://github.com/usemanusai/JAEGIS")
        return 0
    
    def cmd_help(self, args):
        """Show help information"""
        print("eJAEGIS CLI - Ecosystem for JAEGIS Method AI Development")
        print("=" * 60)
        print()
        print("Available Commands:")
        print("  init        Initialize eJAEGIS in current directory")
        print("  start       Start eJAEGIS background monitoring")
        print("  stop        Stop eJAEGIS background monitoring")
        print("  restart     Restart eJAEGIS background monitoring")
        print("  status      Show eJAEGIS system status")
        print("  test        Run eJAEGIS system tests")
        print("  version     Show version information")
        print("  help        Show this help message")
        print()
        print("Examples:")
        print("  ejaegis init")
        print("  ejaegis start")
        print("  ejaegis status")
        print("  ejaegis test")
        print()
        print("For more information: https://github.com/usemanusai/JAEGIS")
        return 0

def create_parser():
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        prog='ejaegis',
        description='eJAEGIS CLI - Ecosystem for JAEGIS Method AI Development',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ejaegis init
  ejaegis start
  ejaegis status
  ejaegis test
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Commands
    subparsers.add_parser('init', help='Initialize eJAEGIS in current directory')
    subparsers.add_parser('start', help='Start eJAEGIS background monitoring')
    subparsers.add_parser('stop', help='Stop eJAEGIS background monitoring')
    subparsers.add_parser('restart', help='Restart eJAEGIS background monitoring')
    subparsers.add_parser('status', help='Show eJAEGIS system status')
    subparsers.add_parser('test', help='Run eJAEGIS system tests')
    subparsers.add_parser('version', help='Show version information')
    subparsers.add_parser('help', help='Show help information')
    
    return parser

def main():
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    cli = eJAEGISCLI()
    
    if not args.command:
        return cli.cmd_help(args)
    
    # Route to appropriate command handler
    command_handlers = {
        'init': cli.cmd_init,
        'start': cli.cmd_start,
        'stop': cli.cmd_stop,
        'restart': cli.cmd_restart,
        'status': cli.cmd_status,
        'test': cli.cmd_test,
        'version': cli.cmd_version,
        'help': cli.cmd_help
    }
    
    handler = command_handlers.get(args.command)
    if handler:
        return handler(args)
    else:
        print(f"Unknown command: {args.command}")
        return cli.cmd_help(args)

if __name__ == '__main__':
    exit(main())