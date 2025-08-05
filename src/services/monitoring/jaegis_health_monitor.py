#!/usr/bin/env python3

"""
eJAEGIS Health Monitoring System

Comprehensive health monitoring and verification system for eJAEGIS installations.
Provides real-time status monitoring, automated troubleshooting, and system validation.
"""

import sys
import os
import json
import time
import psutil
import requests
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple

class eJAEGISHealthCheck:
    """Individual health check implementation"""
    
    def __init__(self, name: str, description: str, critical: bool = False):
        self.name = name
        self.description = description
        self.critical = critical
        self.last_result = None
        self.last_run = None
    
    def run(self) -> Tuple[bool, str, Dict[str, Any]]:
        """Run the health check. Returns (success, message, details)"""
        raise NotImplementedError
    
    def get_resolution_steps(self) -> List[str]:
        """Get resolution steps for when this check fails"""
        return ["Check the eJAEGIS documentation for troubleshooting steps"]

class PythonEnvironmentCheck(eJAEGISHealthCheck):
    """Check Python environment and dependencies"""
    
    def __init__(self):
        super().__init__(
            "Python Environment",
            "Verify Python version and required dependencies",
            critical=True
        )
    
    def run(self) -> Tuple[bool, str, Dict[str, Any]]:
        details = {}
        
        try:
            # Check Python version
            python_version = sys.version_info
            details["python_version"] = f"{python_version.major}.{python_version.minor}.{python_version.micro}"
            
            if python_version < (3, 8):
                return False, f"Python version {details['python_version']} is too old (requires 3.8+)", details
            
            # Check required modules
            required_modules = ["requests", "psutil", "pathlib", "json", "datetime"]
            missing_modules = []
            
            for module in required_modules:
                try:
                    __import__(module)
                    details[f"module_{module}"] = "available"
                except ImportError:
                    missing_modules.append(module)
                    details[f"module_{module}"] = "missing"
            
            if missing_modules:
                return False, f"Missing required modules: {', '.join(missing_modules)}", details
            
            # Check pip availability
            try:
                import pip
                details["pip_available"] = True
            except ImportError:
                details["pip_available"] = False
                return False, "pip is not available", details
            
            return True, f"Python environment OK (version {details['python_version']})", details
            
        except Exception as e:
            return False, f"Error checking Python environment: {e}", details
    
    def get_resolution_steps(self) -> List[str]:
        return [
            "Ensure Python 3.8+ is installed",
            "Install missing modules with: pip install <module_name>",
            "Verify pip is installed and working",
            "Check Python PATH configuration"
        ]

class FileSystemCheck(eJAEGISHealthCheck):
    """Check file system permissions and directory structure"""
    
    def __init__(self, eJAEGIS_dir: Path):
        super().__init__(
            "File System",
            "Verify directory structure and permissions",
            critical=True
        )
        self.eJAEGIS_dir = eJAEGIS_dir
    
    def run(self) -> Tuple[bool, str, Dict[str, Any]]:
        details = {}
        
        try:
            # Check if eJAEGIS directory exists
            if not self.eJAEGIS_dir.exists():
                return False, f"eJAEGIS directory does not exist: {self.eJAEGIS_dir}", details
            
            details["eJAEGIS_dir"] = str(self.eJAEGIS_dir)
            details["eJAEGIS_dir_exists"] = True
            
            # Check required subdirectories
            required_dirs = ["config", "logs", "data", "temp"]
            missing_dirs = []
            
            for dir_name in required_dirs:
                dir_path = self.eJAEGIS_dir / dir_name
                if dir_path.exists():
                    details[f"dir_{dir_name}"] = "exists"
                    # Check write permissions
                    if os.access(dir_path, os.W_OK):
                        details[f"dir_{dir_name}_writable"] = True
                    else:
                        details[f"dir_{dir_name}_writable"] = False
                        return False, f"No write permission for {dir_path}", details
                else:
                    missing_dirs.append(dir_name)
                    details[f"dir_{dir_name}"] = "missing"
            
            if missing_dirs:
                return False, f"Missing required directories: {', '.join(missing_dirs)}", details
            
            # Check disk space
            try:
                disk_usage = psutil.disk_usage(str(self.eJAEGIS_dir))
                free_gb = disk_usage.free / (1024**3)
                details["free_space_gb"] = round(free_gb, 2)
                
                if free_gb < 1.0:  # Less than 1GB free
                    return False, f"Low disk space: {free_gb:.2f}GB free", details
                
            except Exception as e:
                details["disk_check_error"] = str(e)
            
            return True, "File system structure OK", details
            
        except Exception as e:
            return False, f"Error checking file system: {e}", details
    
    def get_resolution_steps(self) -> List[str]:
        return [
            "Create missing directories manually",
            "Check and fix directory permissions",
            "Free up disk space if needed",
            "Verify eJAEGIS installation path"
        ]

class ConfigurationCheck(eJAEGISHealthCheck):
    """Check configuration files and settings"""
    
    def __init__(self, eJAEGIS_dir: Path):
        super().__init__(
            "Configuration",
            "Verify configuration files and settings",
            critical=False
        )
        self.eJAEGIS_dir = eJAEGIS_dir
    
    def run(self) -> Tuple[bool, str, Dict[str, Any]]:
        details = {}
        
        try:
            config_dir = self.eJAEGIS_dir / "config"
            
            # Check user config
            user_config_path = config_dir / "eJAEGIS-user-config.json"
            if user_config_path.exists():
                try:
                    with open(user_config_path, 'r') as f:
                        user_config = json.load(f)
                    details["user_config"] = "valid"
                    details["user_config_version"] = user_config.get("version", "unknown")
                except json.JSONDecodeError:
                    details["user_config"] = "invalid_json"
                    return False, "User config file contains invalid JSON", details
            else:
                details["user_config"] = "missing"
                return False, "User config file is missing", details
            
            # Check project config
            project_config_path = config_dir / "eJAEGIS-project-config.json"
            if project_config_path.exists():
                try:
                    with open(project_config_path, 'r') as f:
                        project_config = json.load(f)
                    details["project_config"] = "valid"
                    details["project_name"] = project_config.get("project_name", "unknown")
                except json.JSONDecodeError:
                    details["project_config"] = "invalid_json"
                    return False, "Project config file contains invalid JSON", details
            else:
                details["project_config"] = "missing"
                # Project config is optional, so this is just a warning
                details["project_config_warning"] = "Project config file is missing (optional)"
            
            return True, "Configuration files OK", details
            
        except Exception as e:
            return False, f"Error checking configuration: {e}", details
    
    def get_resolution_steps(self) -> List[str]:
        return [
            "Run 'ejaegis init' to create missing config files",
            "Check config file syntax with a JSON validator",
            "Restore config files from backup if available",
            "Reset configuration to defaults"
        ]

class eJAEGISProcessCheck(eJAEGISHealthCheck):
    """Check for running eJAEGIS processes"""
    
    def __init__(self):
        super().__init__(
            "Process Status",
            "Check for running eJAEGIS processes",
            critical=False
        )
    
    def run(self) -> Tuple[bool, str, Dict[str, Any]]:
        details = {}
        
        try:
            # Look for eJAEGIS-related processes
            eJAEGIS_processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = ' '.join(proc.info['cmdline'] or [])
                    if 'eJAEGIS' in cmdline or 'jaegis' in cmdline.lower():
                        eJAEGIS_processes.append({
                            'pid': proc.info['pid'],
                            'name': proc.info['name'],
                            'cmdline': cmdline
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            details["eJAEGIS_processes"] = eJAEGIS_processes
            details["process_count"] = len(eJAEGIS_processes)
            
            if eJAEGIS_processes:
                return True, f"Found {len(eJAEGIS_processes)} eJAEGIS process(es)", details
            else:
                return True, "No eJAEGIS processes currently running", details
            
        except Exception as e:
            return False, f"Error checking processes: {e}", details
    
    def get_resolution_steps(self) -> List[str]:
        return [
            "Start eJAEGIS services with 'ejaegis start'",
            "Check for process conflicts or errors",
            "Verify system resources are available",
            "Review process logs for issues"
        ]

class GitHubConnectivityCheck(eJAEGISHealthCheck):
    """Check GitHub API connectivity"""
    
    def __init__(self, github_token: str):
        super().__init__(
            "GitHub Connectivity",
            "Test GitHub API connectivity and authentication",
            critical=False
        )
        self.github_token = github_token
    
    def run(self) -> Tuple[bool, str, Dict[str, Any]]:
        details = {}
        
        try:
            # Test GitHub API connectivity
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            response = requests.get('https://api.github.com/user', headers=headers, timeout=10)
            details["status_code"] = response.status_code
            
            if response.status_code == 200:
                user_data = response.json()
                details["github_user"] = user_data.get("login", "unknown")
                details["rate_limit_remaining"] = response.headers.get("X-RateLimit-Remaining", "unknown")
                return True, f"GitHub API OK (user: {details['github_user']})", details
            elif response.status_code == 401:
                return False, "GitHub authentication failed (invalid token)", details
            else:
                return False, f"GitHub API error: {response.status_code}", details
            
        except requests.RequestException as e:
            details["connection_error"] = str(e)
            return False, f"GitHub connectivity error: {e}", details
        except Exception as e:
            return False, f"Error checking GitHub connectivity: {e}", details
    
    def get_resolution_steps(self) -> List[str]:
        return [
            "Verify GitHub token is valid and has required permissions",
            "Check internet connectivity",
            "Verify GitHub API is accessible (not blocked by firewall)",
            "Update GitHub token in configuration"
        ]

class eJAEGISHealthMonitor:
    """Main health monitoring system"""
    
    def __init__(self, eJAEGIS_dir: Path):
        self.eJAEGIS_dir = eJAEGIS_dir
        self.checks = []
        self.last_run = None
        self.setup_checks()
    
    def setup_checks(self):
        """Initialize all health checks"""
        self.checks = [
            PythonEnvironmentCheck(),
            FileSystemCheck(self.eJAEGIS_dir),
            ConfigurationCheck(self.eJAEGIS_dir),
            eJAEGISProcessCheck()
        ]
        
        # Add GitHub check if token is available
        try:
            config_path = self.eJAEGIS_dir / "config" / "eJAEGIS-user-config.json"
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    github_token = config.get("github", {}).get("token")
                    if github_token:
                        self.checks.append(GitHubConnectivityCheck(github_token))
        except Exception:
            pass
    
    def run_all_checks(self) -> Dict[str, Any]:
        """Run all health checks and return results"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "healthy",
            "checks": {},
            "summary": {
                "total": len(self.checks),
                "passed": 0,
                "failed": 0,
                "critical_failed": 0
            }
        }
        
        for check in self.checks:
            try:
                success, message, details = check.run()
                check.last_result = (success, message, details)
                check.last_run = datetime.now()
                
                results["checks"][check.name] = {
                    "success": success,
                    "message": message,
                    "details": details,
                    "critical": check.critical,
                    "resolution_steps": check.get_resolution_steps() if not success else []
                }
                
                if success:
                    results["summary"]["passed"] += 1
                else:
                    results["summary"]["failed"] += 1
                    if check.critical:
                        results["summary"]["critical_failed"] += 1
                        results["overall_status"] = "critical"
                    elif results["overall_status"] == "healthy":
                        results["overall_status"] = "warning"
                        
            except Exception as e:
                results["checks"][check.name] = {
                    "success": False,
                    "message": f"Check failed with exception: {e}",
                    "details": {"exception": str(e)},
                    "critical": check.critical,
                    "resolution_steps": ["Contact support with error details"]
                }
                results["summary"]["failed"] += 1
                if check.critical:
                    results["summary"]["critical_failed"] += 1
                    results["overall_status"] = "critical"
        
        self.last_run = datetime.now()
        return results
    
    def get_status_summary(self) -> str:
        """Get a brief status summary"""
        if not self.last_run:
            return "Health checks have not been run yet"
        
        results = self.run_all_checks()
        status = results["overall_status"]
        summary = results["summary"]
        
        if status == "healthy":
            return f"✅ System healthy ({summary['passed']}/{summary['total']} checks passed)"
        elif status == "warning":
            return f"⚠️  System has warnings ({summary['failed']} non-critical issues)"
        else:
            return f"❌ System critical ({summary['critical_failed']} critical issues)"
    
    def print_detailed_report(self):
        """Print a detailed health report"""
        results = self.run_all_checks()
        
        print("=" * 60)
        print("eJAEGIS Health Monitor Report")
        print("=" * 60)
        print(f"Timestamp: {results['timestamp']}")
        print(f"Overall Status: {results['overall_status'].upper()}")
        print(f"eJAEGIS Directory: {self.eJAEGIS_dir}")
        print()
        
        # Summary
        summary = results["summary"]
        print("Summary:")
        print(f"  Total Checks: {summary['total']}")
        print(f"  Passed: {summary['passed']}")
        print(f"  Failed: {summary['failed']}")
        print(f"  Critical Failed: {summary['critical_failed']}")
        print()
        
        # Individual check results
        for check_name, check_result in results["checks"].items():
            status_icon = "✅" if check_result["success"] else "❌"
            critical_marker = " [CRITICAL]" if check_result["critical"] else ""
            
            print(f"{status_icon} {check_name}{critical_marker}")
            print(f"   {check_result['message']}")
            
            if not check_result["success"] and check_result["resolution_steps"]:
                print("   Resolution steps:")
                for step in check_result["resolution_steps"]:
                    print(f"     • {step}")
            print()

def main():
    """Main entry point for health monitor"""
    import argparse
    
    parser = argparse.ArgumentParser(description="eJAEGIS Health Monitor")
    parser.add_argument("--eJAEGIS-dir", type=Path, help="eJAEGIS directory path")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--summary", action="store_true", help="Show only summary")
    
    args = parser.parse_args()
    
    # Find eJAEGIS directory
    if args.eJAEGIS_dir:
        eJAEGIS_dir = args.eJAEGIS_dir
    else:
        # Look for eJAEGIS directory in current or parent directories
        current = Path.cwd()
        eJAEGIS_dir = None
        
        while current != current.parent:
            potential_dir = current / "eJAEGIS"
            if potential_dir.exists() and potential_dir.is_dir():
                eJAEGIS_dir = potential_dir
                break
            current = current.parent
        
        if not eJAEGIS_dir:
            print("❌ eJAEGIS directory not found. Use --eJAEGIS-dir to specify path.")
            return 1
    
    # Create and run health monitor
    monitor = eJAEGISHealthMonitor(eJAEGIS_dir)
    
    if args.summary:
        print(monitor.get_status_summary())
    elif args.json:
        results = monitor.run_all_checks()
        print(json.dumps(results, indent=2))
    else:
        monitor.print_detailed_report()
    
    return 0

if __name__ == "__main__":
    exit(main())