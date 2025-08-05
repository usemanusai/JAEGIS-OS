#!/usr/bin/env python3

"""
eJAEGIS Failsafe System

Critical failsafe mechanisms to prevent development workflow disruptions:
1. Uninitialized eJAEGIS Detection
2. Post-Completion Development Detection

This system integrates with the eJAEGIS monitoring to provide proactive warnings
and automated responses to common workflow issues.
"""

import os
import sys
import json
import time
import psutil
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import threading
import subprocess

class eJAEGISFailsafeConfig:
    """Configuration management for eJAEGIS failsafe system""tool_4397": {
                "enabled": True,
                "name": "Uninitialized_eJAEGIS_Detection",
                "check_interval_seconds": 300,  # 5 minutes
                "initialization_timeout_hours": 24,
                "file_change_threshold3_auto_enable_conditions": {
                    "new_project_detection": True,
                    "git_init_detection": True,
                    "multiple_changes_without_eJAEGISTrue_response_actions": {
                    "show_notification": True,
                    "prompt_initialization": True,
                    "pause_monitoring": False,
                    "auto_start_eJAEGISFalse_failsafe_2_post_completion_detection": {
                "enabled": True,
                "name": "Post-Completion_Development_Detection",
                "check_interval_seconds": 600,  # 10 minutes
                "completion_grace_period_hours": 2,
                "significant_change_threshold5_auto_enable_conditions": {
                    "high_priority_completion": True,
                    "multiple_completion_cycles": True,
                    "user_confusion_indicatorsTrue_response_actions": {
                    "alert_post_completion": True,
                    "prompt_status_clarification": True,
                    "offer_reopen_options": True,
                    "suggest_feature_branchTrue_general": {
                "log_level": "INFO",
                "notification_method": "console",  # console, popup, both
                "persistence_enabled": True,
                "performance_monitoring": True
            }
        }
        self.config = self.load_config()
    
    def load_config(self) -> Dict:
        """Load configuration from file or create default"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                # Merge with defaults to ensure all keys exist
                return self._merge_config(self.default_config, config)
            else:
                self.save_config(self.default_config)
                return self.default_config.copy()
        except Exception as e:
            logging.error(f"Error loading config: {e}")
            return self.default_config.copy()
    
    def save_config(self, config: Dict = None):
        """Save configuration to file"""
        try:
            config_to_save = config or self.config
            self.config_path.parent.mkdir(exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(config_to_save, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving config: {e}")
    
    def _merge_config(self, default: Dict, user: Dict) -> Dict:
        """Recursively merge user config with defaults"""
        result = default.copy()
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value
        return result
    
    def update_setting(self, path: str, value):
        """Update a specific setting using dot notation"""
        keys = path.split('.')
        current = self.config
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
        self.save_config()

class eJAEGISFailsafeSystem:
    """Main failsafe system implementation"""
    
    def __init__(self, eJAEGIS_dir: Path):
        self.eJAEGIS_dir = eJAEGIS_dir
        self.config_path = eJAEGIS_dir / "config" / "eJAEGIS-failsafe-config.json"
        self.state_path = eJAEGIS_dir / "config" / "eJAEGIS-failsafe-state.json"
        self.log_path = eJAEGIS_dir / "logs" / f"eJAEGIS-failsafe-{datetime.now().strftime('%Y%m%d')}.log"
        
        # Ensure directories exist
        self.config_path.parent.mkdir(exist_ok=True)
        self.log_path.parent.mkdir(exist_ok=True)
        
        # Initialize components
        self.config = eJAEGISFailsafeConfig(self.config_path)
        self.setup_logging()
        self.state = self.load_state()
        self.running = False
        
        # Monitoring threads
        self.failsafe_threads = []
        
        self.logger.info("eJAEGIS Failsafe System initialized")
    
    def setup_logging(self):
        """Setup logging for failsafe system"""
        log_level = getattr(logging, self.config.config["general"]["log_level"])
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_path),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger("eJAEGISFailsafe")
    
    def load_state(self) -> Dict:
        """Load persistent state"""
        try:
            if self.state_path.exists():
                with open(self.state_path, 'r') as f:
                    return json.load(f)
            else:
                return {
                    "last_eJAEGIS_initialization": None,
                    "last_completion_checkNone_project_completion_status": {},
                    "failsafe_activations": [],
                    "file_change_history": []
                }
        except Exception as e:
            self.logger.error(f"Error loading state: {e}")
            return {}
    
    def save_state(self):
        """Save persistent state"""
        try:
            with open(self.state_path, 'w') as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving state: {e}")
    
    def is_eJAEGIS_running(self) -> bool:
        """Check if eJAEGIS background runner is active"""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = proc.info['cmdline']
                    if cmdline and any('eJAEGIS-background-runner.py' in arg for arg in cmdline):
                        return True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return False
        except Exception as e:
            self.logger.error(f"Error checking eJAEGIS process: {e}")
            return False
    
    def detect_file_changes(self) -> List[Dict]:
        """Detect recent file changes in monitored directories"""
        changes = []
        current_time = datetime.now()
        
        try:
            # Monitor key directories
            monitor_dirs = [
                self.eJAEGIS_dir / "src",
                self.eJAEGIS_dir / "jaegis-agent", 
                self.eJAEGIS_dir / "docs",
                self.eJAEGIS_dir
            ]
            
            for monitor_dir in monitor_dirs:
                if not monitor_dir.exists():
                    continue
                
                for file_path in monitor_dir.rglob("*"):
                    if file_path.is_file() and not self._should_ignore_file(file_path):
                        try:
                            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                            if current_time - mtime < timedelta(minutes=30):  # Recent changes
                                changes.append({
                                    "file": str(file_path.relative_to(self.eJAEGIS_dir)),
                                    "modified": mtime.isoformat(),
                                    "size": file_path.stat().st_size
                                })
                        except (OSError, ValueError):
                            continue
            
            return changes
            
        except Exception as e:
            self.logger.error(f"Error detecting file changes: {e}")
            return []
    
    def _should_ignore_file(self, file_path: Path) -> bool:
        """Check if file should be ignored in monitoring"""
        ignore_patterns = [
            ".git", "__pycache__", "node_modules", ".vscode",
            "logs", "config", ".log", ".tmp", ".temp", ".pyc"
        ]
        
        file_str = str(file_path).lower()
        return any(pattern in file_str for pattern in ignore_patterns)
    
    def check_project_completion_status(self) -> Dict:
        """Check if project has been marked as completed"""
        try:
            # Check for task completion markers
            task_files = list(self.eJAEGIS_dir.glob("**/task*.json"))
            task_files.extend(list(self.eJAEGIS_dir.glob("**/jaegis-task*.json")))
            
            completion_status = {
                "is_completed": False,
                "completion_time": None,
                "completed_tasks": [],
                "active_tasks": []
            }
            
            for task_file in task_files:
                try:
                    with open(task_file, 'r') as f:
                        task_data = json.load(f)
                    
                    if isinstance(task_data, dict):
                        if task_data.get("state") == "COMPLETE":
                            completion_status["completed_tasks"].append({
                                "file": str(task_file.relative_to(self.eJAEGIS_dir)),
                                "name": task_data.get("name", "Unknown"),
                                "completion_time": task_data.get("completed_at")
                            })
                            completion_status["is_completed"] = True
                        elif task_data.get("state") in ["IN_PROGRESS", "NOT_STARTED"]:
                            completion_status["active_tasks"].append({
                                "file": str(task_file.relative_to(self.eJAEGIS_dir)),
                                "name": task_data.get("name", "Unknown"),
                                "state": task_data.get("state")
                            })
                            
                except (json.JSONDecodeError, KeyError):
                    continue
            
            return completion_status
            
        except Exception as e:
            self.logger.error(f"Error checking completion status: {e}")
            return {"is_completed": False, "completion_time": None, "completed_tasks": [], "active_tasks": []}
    
    def detect_git_initialization(self) -> bool:
        """Detect if Git repository was recently initialized"""
        try:
            git_dir = self.eJAEGIS_dir / ".git"
            if git_dir.exists():
                git_init_time = datetime.fromtimestamp(git_dir.stat().st_ctime)
                return datetime.now() - git_init_time < timedelta(hours=1)
            return False
        except Exception:
            return False
    
    def detect_new_project(self) -> bool:
        """Detect if this appears to be a new project"""
        try:
            # Check for common new project indicators
            indicators = [
                self.eJAEGIS_dir / "package.json",
                self.eJAEGIS_dir / "requirements.txt", 
                self.eJAEGIS_dir / "Cargo.toml",
                self.eJAEGIS_dir / "pom.xml",
                self.eJAEGIS_dir / "README.md"
            ]
            
            recent_indicators = 0
            for indicator in indicators:
                if indicator.exists():
                    creation_time = datetime.fromtimestamp(indicator.stat().st_ctime)
                    if datetime.now() - creation_time < timedelta(hours=24):
                        recent_indicators += 1
            
            return recent_indicators >= 2

        except Exception:
            return False

    def failsafe_1_uninitialized_detection(self):
        """FAILSAFE 1: Detect uninitialized eJAEGIS development"""
        config = self.config.config["failsafe_1_uninitialized_detection"]

        if not config["enabled"]:
            return

        self.logger.debug("Running Failsafe 1: Uninitialized eJAEGIS Detection")

        try:
            # Check if eJAEGIS is running
            eJAEGIS_running = self.is_eJAEGIS_running()

            # Check for recent file changes
            recent_changes = self.detect_file_changes()

            # Check last initialization time
            last_init = self.state.get("last_eJAEGIS_initialization")
            init_timeout = datetime.now() - timedelta(hours=config["initialization_timeout_hours"])

            needs_initialization = False
            trigger_reasons = []

            # Trigger conditions
            if len(recent_changes) >= config["file_change_threshold"]:
                if not eJAEGIS_running:
                    needs_initialization = True
                    trigger_reasons.append("File modifications detected without active eJAEGIS session")

                if last_init is None or datetime.fromisoformat(last_init) < init_timeout:
                    needs_initialization = True
                    trigger_reasons.append("No recent eJAEGIS initialization within 24 hours")

            # Auto-enable conditions
            auto_conditions = config["auto_enable_conditions"]
            if auto_conditions["new_project_detection"] and self.detect_new_project():
                needs_initialization = True
                trigger_reasons.append("New project directory detected")

            if auto_conditions["git_init_detection"] and self.detect_git_initialization():
                needs_initialization = True
                trigger_reasons.append("Git repository initialization detected")

            if auto_conditions["multiple_changes_without_eJAEGIS"] and len(recent_changes) > 10 and not eJAEGIS_running:
                needs_initialization = True
                trigger_reasons.append("Multiple file changes without eJAEGIS activity")

            if needs_initialization:
                self._trigger_failsafe_1_response(trigger_reasons, recent_changes)

        except Exception as e:
            self.logger.error(f"Error in Failsafe 1: {e}")

    def failsafe_2_post_completion_detection(self):
        """FAILSAFE 2: Detect post-completion development"""
        config = self.config.config["failsafe_2_post_completion_detection"]

        if not config["enabled"]:
            return

        self.logger.debug("Running Failsafe 2: Post-Completion Development Detection")

        try:
            # Check project completion status
            completion_status = self.check_project_completion_status()

            if not completion_status["is_completed"]:
                return

            # Check for recent file changes after completion
            recent_changes = self.detect_file_changes()

            # Check if changes occurred after completion
            post_completion_changes = []
            grace_period = timedelta(hours=config["completion_grace_period_hours"])

            for task in completion_status["completed_tasks"]:
                if task["completion_time"]:
                    completion_time = datetime.fromisoformat(task["completion_time"])

                    for change in recent_changes:
                        change_time = datetime.fromisoformat(change["modified"])
                        if change_time > completion_time + grace_period:
                            post_completion_changes.append({
                                "change": change,
                                "completed_task": task["name"],
                                "time_after_completion": str(change_time - completion_time)
                            })

            if len(post_completion_changes) >= config["significant_change_threshold"]:
                self._trigger_failsafe_2_response(completion_status, post_completion_changes)

        except Exception as e:
            self.logger.error(f"Error in Failsafe 2: {e}")

    def _trigger_failsafe_1_response(self, reasons: List[str], changes: List[Dict]):
        """Trigger response actions for Failsafe 1"""
        config = self.config.config["failsafe_1_uninitialized_detection"]["response_actions"]

        activation = {
            "timestamp": datetime.now().isoformat(),
            "failsafe": "uninitialized_detection",
            "reasons": reasons,
            "changes_count": len(changes),
            "actions_taken": []
        }

        self.logger.warning(f"🚨 FAILSAFE 1 ACTIVATED: Uninitialized eJAEGIS Detection")
        self.logger.warning(f"Trigger reasons: {', '.join(reasons)}")

        if config["show_notification"]:
            self._show_notification(
                "⚠️ eJAEGIS Initialization Required",
                f"Development activity detected without active eJAEGIS system.\n"
                f"Reasons: {', '.join(reasons)}\n"
                f"Files changed: {len(changes)}"
            )
            activation["actions_taken"].append("notification_shown")

        if config["prompt_initialization"]:
            self._prompt_eJAEGIS_initialization()
            activation["actions_taken"].append("initialization_prompted")

        # Log activation
        self.state["failsafe_activations"].append(activation)
        self.save_state()

    def _trigger_failsafe_2_response(self, completion_status: Dict, post_changes: List[Dict]):
        """Trigger response actions for Failsafe 2"""
        config = self.config.config["failsafe_2_post_completion_detection"]["response_actions"]

        activation = {
            "timestamp": datetime.now().isoformat(),
            "failsafe": "post_completion_detection",
            "completed_tasks": len(completion_status["completed_tasks"]),
            "post_completion_changes": len(post_changes),
            "actions_taken": []
        }

        self.logger.warning(f"🚨 FAILSAFE 2 ACTIVATED: Post-Completion Development Detection")
        self.logger.warning(f"Completed tasks: {len(completion_status['completed_tasks'])}")
        self.logger.warning(f"Post-completion changes: {len(post_changes)}")

        if config["alert_post_completion"]:
            self._show_notification(
                "⚠️ Post-Completion Development Detected",
                f"Development activity detected after project completion.\n"
                f"Completed tasks: {len(completion_status['completed_tasks'])}\n"
                f"Recent changes: {len(post_changes)}"
            )
            activation["actions_taken"].append("alert_shown")

        if config["prompt_status_clarification"]:
            self._prompt_status_clarification(completion_status)
            activation["actions_taken"].append("status_clarification_prompted")

        # Log activation
        self.state["failsafe_activations"].append(activation)
        self.save_state()

    def _show_notification(self, title: str, message: str):
        """Show notification to user"""
        notification_method = self.config.config["general"]["notification_method"]

        # Console notification (always available)
        print(f"\n{'='*60}")
        print(f"🚨 {title}")
        print(f"{'='*60}")
        print(message)
        print(f"{'='*60}\n")

        # Try popup notification if requested
        if notification_method in ["popup", "both"]:
            try:
                if sys.platform == "win32":
                    import ctypes
                    ctypes.windll.user32.MessageBoxW(0, message, title, 0x30)
            except Exception as e:
                self.logger.debug(f"Could not show popup notification: {e}")

    def _prompt_eJAEGIS_initialization(self):
        """Prompt user to initialize eJAEGIS"""
        print("\n🔧 eJAEGIS Initialization Options:")
        print("1. Start eJAEGIS Background Runner")
        print("2. Run eJAEGIS Test Cycle")
        print("3. View eJAEGIS Status")
        print("4. Ignore (disable this failsafe)")
        print("5. Continue without eJAEGIS")

        try:
            choice = input("\nSelect option (1-5): ").strip()

            if choice == "1":
                self._auto_start_eJAEGIS()
            elif choice == "2":
                self._run_eJAEGIS_test()
            elif choice == "3":
                self._show_eJAEGIS_status()
            elif choice == "4":
                self._disable_failsafe("failsafe_1_uninitialized_detection")
            elif choice == "5":
                print("Continuing without eJAEGIS initialization...")
            else:
                print("Invalid choice. Continuing...")

        except (KeyboardInterrupt, EOFError):
            print("\nPrompt cancelled. Continuing...")

    def _prompt_status_clarification(self, completion_status: Dict):
        """Prompt user for project status clarification"""
        print("\n🔍 Project Status Clarification:")
        print(f"Completed tasks: {len(completion_status['completed_tasks'])}")
        print(f"Active tasks: {len(completion_status['active_tasks'])}")
        print("\nRecent development activity detected after completion.")
        print("\nOptions:")
        print("1. Reopen project (mark as in progress)")
        print("2. Create new feature branch")
        print("3. Confirm completion override")
        print("4. Disable post-completion detection")
        print("5. Continue as-is")

        try:
            choice = input("\nSelect option (1-5): ").strip()

            if choice == "1":
                print("🔄 Project reopened and marked as in progress")
            elif choice == "2":
                print("🌿 Consider creating: git checkout -b feature/post-completion-updates")
            elif choice == "3":
                print("Completion override confirmed. Continuing...")
            elif choice == "4":
                self._disable_failsafe("failsafe_2_post_completion_detection")
            elif choice == "5":
                print("Continuing as-is...")
            else:
                print("Invalid choice. Continuing...")

        except (KeyboardInterrupt, EOFError):
            print("\nPrompt cancelled. Continuing...")

    def _auto_start_eJAEGIS(self):
        """Automatically start eJAEGIS background runner"""
        try:
            eJAEGIS_runner = self.eJAEGIS_dir / "eJAEGIS-background-runner.py"
            if eJAEGIS_runner.exists():
                result = subprocess.run([
                    sys.executable, str(eJAEGIS_runner), "start"
                ], capture_output=True, text=True)

                if result.returncode == 0:
                    print("✅ eJAEGIS Background Runner started successfully")
                    self.state["last_eJAEGIS_initialization"] = datetime.now().isoformat()
                    self.save_state()
                else:
                    print(f"❌ Failed to start eJAEGIS: {result.stderr}")
            else:
                print("❌ eJAEGIS Background Runner not found")
        except Exception as e:
            print(f"❌ Error starting eJAEGIS: {e}")

    def _run_eJAEGIS_test(self):
        """Run eJAEGIS test cycle"""
        try:
            eJAEGIS_script = self.eJAEGIS_dir / "eJAEGIS-auto-sync.py"
            if eJAEGIS_script.exists():
                result = subprocess.run([
                    sys.executable, str(eJAEGIS_script), "--test"
                ], capture_output=True, text=True)

                print("eJAEGIS Test Results:")
                print(result.stdout)
                if result.stderr:
                    print("Errors:")
                    print(result.stderr)
            else:
                print("❌ eJAEGIS script not found")
        except Exception as e:
            print(f"❌ Error running eJAEGIS test: {e}")

    def _show_eJAEGIS_status(self):
        """Show current eJAEGIS status"""
        eJAEGIS_running = self.is_eJAEGIS_running()
        print(f"eJAEGIS Status: {'✅ Running' if eJAEGIS_running else '❌ Not Running'}")

        last_init = self.state.get("last_eJAEGIS_initialization")
        if last_init:
            init_time = datetime.fromisoformat(last_init)
            print(f"Last Initialization: {init_time.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("Last Initialization: Never")

    def _disable_failsafe(self, failsafe_name: str):
        """Disable a specific failsafe"""
        self.config.update_setting(f"{failsafe_name}.enabled", False)
        print(f"✅ {failsafe_name} disabled")

    def start_monitoring(self):
        """Start failsafe monitoring threads"""
        if self.running:
            return

        self.running = True
        self.logger.info("Starting eJAEGIS Failsafe monitoring...")

        # Start Failsafe 1 thread
        if self.config.config["failsafe_1_uninitialized_detection"]["enabled"]:
            thread1 = threading.Thread(target=self._monitor_failsafe_1, daemon=True)
            thread1.start()
            self.failsafe_threads.append(thread1)

        # Start Failsafe 2 thread
        if self.config.config["failsafe_2_post_completion_detection"]["enabled"]:
            thread2 = threading.Thread(target=self._monitor_failsafe_2, daemon=True)
            thread2.start()
            self.failsafe_threads.append(thread2)

        self.logger.info(f"Started {len(self.failsafe_threads)} failsafe monitoring threads")

    def stop_monitoring(self):
        """Stop failsafe monitoring"""
        self.running = False
        self.logger.info("Stopping eJAEGIS Failsafe monitoring...")

    def _monitor_failsafe_1(self):
        """Monitor thread for Failsafe 1"""
        config = self.config.config["failsafe_1_uninitialized_detection"]
        interval = config["check_interval_seconds"]

        while self.running:
            try:
                self.failsafe_1_uninitialized_detection()
                time.sleep(interval)
            except Exception as e:
                self.logger.error(f"Error in Failsafe 1 monitoring: {e}")
                time.sleep(60)  # Wait before retrying

    def _monitor_failsafe_2(self):
        """Monitor thread for Failsafe 2"""
        config = self.config.config["failsafe_2_post_completion_detection"]
        interval = config["check_interval_seconds"]

        while self.running:
            try:
                self.failsafe_2_post_completion_detection()
                time.sleep(interval)
            except Exception as e:
                self.logger.error(f"Error in Failsafe 2 monitoring: {e}")
                time.sleep(60)  # Wait before retrying

def main():
    """Main entry point for standalone execution"""
    import argparse

    parser = argparse.ArgumentParser(description="eJAEGIS Failsafe System")
    parser.add_argument("--eJAEGIS-path", default=".", help="Path to eJAEGIS directory")
    parser.add_argument("--start", action="store_true", help="Start failsafe monitoring")
    parser.add_argument("--test", action="store_true", help="Run failsafe tests")

    args = parser.parse_args()

    eJAEGIS_dir = Path(args.eJAEGIS_path).absolute()
    failsafe = eJAEGISFailsafeSystem(eJAEGIS_dir)

    if args.test:
        print("🧪 Running eJAEGIS Failsafe Tests")
        print("=" * 40)

        # Test file change detection
        changes = failsafe.detect_file_changes()
        print(f"Recent file changes: {len(changes)}")

        # Test eJAEGIS process detection
        eJAEGIS_running = failsafe.is_eJAEGIS_running()
        print(f"eJAEGIS running: {'Yes' if eJAEGIS_running else 'No'}")

        # Test completion status
        completion = failsafe.check_project_completion_status()
        print(f"Project completed: {'Yes' if completion['is_completed'] else 'No'}")

        print("✅ Tests completed")

    elif args.start:
        print("🚀 Starting eJAEGIS Failsafe monitoring...")
        failsafe.start_monitoring()

        try:
            while failsafe.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping failsafe monitoring...")
            failsafe.stop_monitoring()

    else:
        print("eJAEGIS Failsafe System")
        print("Use --start to begin monitoring or --test to run tests")

if __name__ == "__main__":
    main()
