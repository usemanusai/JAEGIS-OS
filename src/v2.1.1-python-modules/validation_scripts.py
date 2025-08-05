#!/usr/bin/env python3
"""
JAEGIS Migration Validation Scripts
Automated validation for each system component during migration
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class MigrationValidator:
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.validation_results = {}
        self.checkpoints = {}
        
    def create_checkpoint(self, checkpoint_name: str) -> bool:
        """Create a Git checkpoint for rollback"""
        try:
            # Create a tag for the checkpoint
            result = subprocess.run([
                'git', 'tag', '-a', checkpoint_name, '-m', f'Migration checkpoint: {checkpoint_name}'
            ], capture_output=True, text=True, cwd=self.repo_path)
            
            if result.returncode == 0:
                self.checkpoints[checkpoint_name] = {
                    "timestamp": time.time(),
                    "commit_hash": self._get_current_commit_hash(),
                    "status": "created"
                }
                print(f"✅ Checkpoint '{checkpoint_name}' created successfully")
                return True
            else:
                print(f"❌ Failed to create checkpoint '{checkpoint_name}': {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error creating checkpoint '{checkpoint_name}': {e}")
            return False
    
    def rollback_to_checkpoint(self, checkpoint_name: str) -> bool:
        """Rollback to a specific checkpoint"""
        try:
            if checkpoint_name not in self.checkpoints:
                print(f"❌ Checkpoint '{checkpoint_name}' not found")
                return False
            
            # Reset to checkpoint
            result = subprocess.run([
                'git', 'reset', '--hard', checkpoint_name
            ], capture_output=True, text=True, cwd=self.repo_path)
            
            if result.returncode == 0:
                print(f"✅ Successfully rolled back to checkpoint '{checkpoint_name}'")
                return True
            else:
                print(f"❌ Failed to rollback to checkpoint '{checkpoint_name}': {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error rolling back to checkpoint '{checkpoint_name}': {e}")
            return False
    
    def validate_security_system(self) -> bool:
        """Validate security scanner functionality"""
        print("🔒 Validating security system...")
        
        validation_tests = [
            {
                "name": "Security Scanner Import",
                "command": "python -c 'from security_scanner import SecurityScanner; print(\"Import successful\")'",
                "expected_output": "Import successful",
                "timeout": 10
            },
            {
                "name": "Security Config Loading",
                "command": "python -c 'import json; json.load(open(\"security_config.json\")); print(\"Config valid\")'",
                "expected_output": "Config valid",
                "timeout": 5
            },
            {
                "name": "Security Scanner Functionality",
                "command": "python -c 'from security_scanner import SecurityScanner; s=SecurityScanner(); print(\"Scanner functional\")'",
                "expected_output": "Scanner functional",
                "timeout": 15
            }
        ]
        
        return self._run_validation_tests("security_system", validation_tests)
    
    def validate_github_integration(self) -> bool:
        """Validate GitHub integration functionality"""
        print("🐙 Validating GitHub integration...")
        
        validation_tests = [
            {
                "name": "Multi-Account Uploader Import",
                "command": "python -c 'from multi_account_github_uploader import MultiAccountGitHubUploader; print(\"Import successful\")'",
                "expected_output": "Import successful",
                "timeout": 10
            },
            {
                "name": "Auto-Sync Import",
                "command": "python -c 'import sys; sys.path.append(\"JAEGIS/JAEGIS-METHOD\"); from emad_auto_sync import eJAEGISAutoSync; print(\"Import successful\")'",
                "expected_output": "Import successful",
                "timeout": 10
            },
            {
                "name": "GitHub Fetcher Import",
                "command": "python -c 'from github_integration.github_fetcher import GitHubFetcher; print(\"Import successful\")'",
                "expected_output": "Import successful",
                "timeout": 10
            }
        ]
        
        return self._run_validation_tests("github_integration", validation_tests)
    
    def validate_core_orchestration(self) -> bool:
        """Validate core orchestration functionality"""
        print("🎼 Validating core orchestration...")
        
        validation_tests = [
            {
                "name": "Enhanced Orchestrator Import",
                "command": "python -c 'from jaegis_enhanced_orchestrator import JAEGISEnhancedOrchestrator; print(\"Import successful\")'",
                "expected_output": "Import successful",
                "timeout": 15
            },
            {
                "name": "V2 Orchestrator Import",
                "command": "python -c 'from jaegis_v2_enhanced_orchestrator import JAEGISV2EnhancedOrchestrator; print(\"Import successful\")'",
                "expected_output": "Import successful",
                "timeout": 15
            }
        ]
        
        return self._run_validation_tests("core_orchestration", validation_tests)
    
    def validate_nlds_system(self) -> bool:
        """Validate N.L.D.S. system functionality"""
        print("🧠 Validating N.L.D.S. system...")
        
        validation_tests = [
            {
                "name": "N.L.D.S. Core Import",
                "command": "python -c 'from nlds.processing import LogicalAnalysisEngine; print(\"Import successful\")'",
                "expected_output": "Import successful",
                "timeout": 10
            },
            {
                "name": "N.L.D.S. Implementation Import",
                "command": "python -c 'from core.nlds.implementation_project import NLDSImplementationProject; print(\"Import successful\")'",
                "expected_output": "Import successful",
                "timeout": 10
            }
        ]
        
        return self._run_validation_tests("nlds_system", validation_tests)
    
    def validate_pitces_framework(self) -> bool:
        """Validate P.I.T.C.E.S. framework functionality"""
        print("⚙️ Validating P.I.T.C.E.S. framework...")
        
        validation_tests = [
            {
                "name": "P.I.T.C.E.S. Controller Import",
                "command": "python -c 'from pitces.core.controller import PITCESController; print(\"Import successful\")'",
                "expected_output": "Import successful",
                "timeout": 10
            },
            {
                "name": "P.I.T.C.E.S. Framework Import",
                "command": "python -c 'from pitces.core.framework import PITCESFramework; print(\"Import successful\")'",
                "expected_output": "Import successful",
                "timeout": 10
            }
        ]
        
        return self._run_validation_tests("pitces_framework", validation_tests)
    
    def validate_project_chimera(self) -> bool:
        """Validate Project Chimera functionality"""
        print("🔬 Validating Project Chimera...")
        
        validation_tests = [
            {
                "name": "Chimera Orchestrator Import",
                "command": "python -c 'from JAEGIS_Enhanced_System.project_chimera.chimera_orchestrator import ChimeraOrchestrator; print(\"Import successful\")'",
                "expected_output": "Import successful",
                "timeout": 10
            },
            {
                "name": "Security Architecture Import",
                "command": "python -c 'from JAEGIS_Enhanced_System.project_chimera.security_architecture import VariableDepthSafetyAugmentation; print(\"Import successful\")'",
                "expected_output": "Import successful",
                "timeout": 10
            }
        ]
        
        return self._run_validation_tests("project_chimera", validation_tests)
    
    def validate_configuration_files(self) -> bool:
        """Validate configuration files"""
        print("⚙️ Validating configuration files...")
        
        config_files = [
            "agent-config.txt",
            "enhanced-agent-config.txt",
            "security_config.json",
            "openrouter-config.json",
            "jaegis_config.json"
        ]
        
        validation_tests = []
        for config_file in config_files:
            if (self.repo_path / config_file).exists():
                if config_file.endswith('.json'):
                    validation_tests.append({
                        "name": f"{config_file} Validation",
                        "command": f"python -c 'import json; json.load(open(\"{config_file}\")); print(\"Valid JSON\")'",
                        "expected_output": "Valid JSON",
                        "timeout": 5
                    })
                else:
                    validation_tests.append({
                        "name": f"{config_file} Existence",
                        "command": f"test -f {config_file} && echo 'File exists'",
                        "expected_output": "File exists",
                        "timeout": 5
                    })
        
        return self._run_validation_tests("configuration_files", validation_tests)
    
    def validate_docker_configuration(self) -> bool:
        """Validate Docker configuration"""
        print("🐳 Validating Docker configuration...")
        
        validation_tests = [
            {
                "name": "Docker Compose Validation",
                "command": "docker-compose config",
                "expected_output": None,  # Just check return code
                "timeout": 30
            },
            {
                "name": "Dockerfile Syntax",
                "command": "docker build --dry-run -f Dockerfile .",
                "expected_output": None,  # Just check return code
                "timeout": 60
            }
        ]
        
        return self._run_validation_tests("docker_configuration", validation_tests)
    
    def validate_cli_systems(self) -> bool:
        """Validate CLI systems"""
        print("💻 Validating CLI systems...")
        
        validation_tests = [
            {
                "name": "JAEGIS CLI Import",
                "command": "python -c 'import emad_cli; print(\"Import successful\")'",
                "expected_output": "Import successful",
                "timeout": 10
            },
            {
                "name": "eJAEGIS CLI Check",
                "command": "test -d eJAEGIS/cli && echo 'CLI directory exists'",
                "expected_output": "CLI directory exists",
                "timeout": 5
            }
        ]
        
        return self._run_validation_tests("cli_systems", validation_tests)
    
    def _run_validation_tests(self, system_name: str, tests: List[Dict]) -> bool:
        """Run a set of validation tests"""
        system_results = {
            "total_tests": len(tests),
            "passed_tests": 0,
            "failed_tests": 0,
            "test_results": []
        }
        
        for test in tests:
            result = self._run_single_test(test)
            system_results["test_results"].append(result)
            
            if result["passed"]:
                system_results["passed_tests"] += 1
                print(f"  ✅ {test['name']}")
            else:
                system_results["failed_tests"] += 1
                print(f"  ❌ {test['name']}: {result['error']}")
        
        self.validation_results[system_name] = system_results
        
        success_rate = system_results["passed_tests"] / system_results["total_tests"]
        print(f"  📊 {system_name}: {system_results['passed_tests']}/{system_results['total_tests']} tests passed ({success_rate:.1%})")
        
        return success_rate >= 0.8  # 80% success rate required
    
    def _run_single_test(self, test: Dict) -> Dict:
        """Run a single validation test"""
        try:
            result = subprocess.run(
                test["command"],
                shell=True,
                capture_output=True,
                text=True,
                timeout=test.get("timeout", 30),
                cwd=self.repo_path
            )
            
            # Check if test passed
            passed = result.returncode == 0
            
            # If expected output is specified, check it
            if passed and test.get("expected_output"):
                passed = test["expected_output"] in result.stdout
            
            return {
                "test_name": test["name"],
                "command": test["command"],
                "passed": passed,
                "return_code": result.returncode,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "error": result.stderr.strip() if not passed else None
            }
            
        except subprocess.TimeoutExpired:
            return {
                "test_name": test["name"],
                "command": test["command"],
                "passed": False,
                "error": f"Test timed out after {test.get('timeout', 30)} seconds"
            }
        except Exception as e:
            return {
                "test_name": test["name"],
                "command": test["command"],
                "passed": False,
                "error": str(e)
            }
    
    def _get_current_commit_hash(self) -> str:
        """Get current Git commit hash"""
        try:
            result = subprocess.run([
                'git', 'rev-parse', 'HEAD'
            ], capture_output=True, text=True, cwd=self.repo_path)
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return "unknown"
        except Exception:
            return "unknown"
    
    def run_full_validation(self) -> bool:
        """Run complete system validation"""
        print("🔍 Running full system validation...")
        
        validation_functions = [
            ("Security System", self.validate_security_system),
            ("GitHub Integration", self.validate_github_integration),
            ("Core Orchestration", self.validate_core_orchestration),
            ("N.L.D.S. System", self.validate_nlds_system),
            ("P.I.T.C.E.S. Framework", self.validate_pitces_framework),
            ("Project Chimera", self.validate_project_chimera),
            ("Configuration Files", self.validate_configuration_files),
            ("Docker Configuration", self.validate_docker_configuration),
            ("CLI Systems", self.validate_cli_systems)
        ]
        
        overall_success = True
        
        for system_name, validation_func in validation_functions:
            try:
                success = validation_func()
                if not success:
                    overall_success = False
                    print(f"❌ {system_name} validation failed")
                else:
                    print(f"✅ {system_name} validation passed")
            except Exception as e:
                overall_success = False
                print(f"❌ {system_name} validation error: {e}")
        
        return overall_success
    
    def generate_validation_report(self, output_path: str = "validation_report.json"):
        """Generate validation report"""
        report = {
            "timestamp": time.time(),
            "overall_success": all(
                result["passed_tests"] / result["total_tests"] >= 0.8
                for result in self.validation_results.values()
            ),
            "validation_results": self.validation_results,
            "checkpoints": self.checkpoints,
            "summary": {
                "total_systems": len(self.validation_results),
                "passed_systems": len([
                    r for r in self.validation_results.values()
                    if r["passed_tests"] / r["total_tests"] >= 0.8
                ]),
                "total_tests": sum(r["total_tests"] for r in self.validation_results.values()),
                "passed_tests": sum(r["passed_tests"] for r in self.validation_results.values())
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📊 Validation report saved to {output_path}")
        return report

def main():
    """Main execution for validation"""
    validator = MigrationValidator()
    
    # Create initial checkpoint
    validator.create_checkpoint("pre_validation")
    
    # Run full validation
    success = validator.run_full_validation()
    
    # Generate report
    report = validator.generate_validation_report()
    
    if success:
        print("🎉 All systems validation passed!")
    else:
        print("⚠️ Some systems failed validation. Check the report for details.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
