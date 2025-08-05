#!/usr/bin/env python3
"""
JAEGIS Critical System Identification Tool
Identifies files that cannot be moved without breaking functionality
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, List, Set

class CriticalSystemIdentifier:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.critical_systems = {}
        self.immovable_files = set()
        self.high_risk_files = set()
        
    def identify_critical_systems(self):
        """Identify all critical systems and their dependencies"""
        print("🔍 Identifying critical systems...")
        
        # Define critical system categories
        critical_categories = {
            "security": self._identify_security_critical(),
            "github_integration": self._identify_github_critical(),
            "core_orchestration": self._identify_orchestration_critical(),
            "configuration": self._identify_config_critical(),
            "deployment": self._identify_deployment_critical(),
            "cli_systems": self._identify_cli_critical()
        }
        
        for category, files in critical_categories.items():
            self.critical_systems[category] = files
            print(f"  📋 {category}: {len(files)} critical files")
        
        # Identify immovable files
        self._identify_immovable_files()
        
        print(f"✅ Identified {sum(len(files) for files in self.critical_systems.values())} critical files")
        print(f"🚫 Found {len(self.immovable_files)} immovable files")
        
    def _identify_security_critical(self) -> List[Dict]:
        """Identify security-critical files"""
        security_files = []
        
        # Primary security scanner
        security_scanner = self.repo_path / "security_scanner.py"
        if security_scanner.exists():
            security_files.append({
                "file": "security_scanner.py",
                "reason": "Core security scanning functionality",
                "dependencies": self._get_file_imports(security_scanner),
                "imported_by": self._find_files_importing("security_scanner"),
                "risk_level": "critical",
                "can_move": True,
                "move_requirements": ["Update all import statements", "Update configuration paths"]
            })
        
        # Security configuration
        security_config = self.repo_path / "security_config.json"
        if security_config.exists():
            security_files.append({
                "file": "security_config.json",
                "reason": "Security scanner configuration",
                "referenced_by": self._find_files_referencing("security_config.json"),
                "risk_level": "high",
                "can_move": True,
                "move_requirements": ["Update path references in security_scanner.py"]
            })
        
        return security_files
    
    def _identify_github_critical(self) -> List[Dict]:
        """Identify GitHub integration critical files"""
        github_files = []
        
        # Multi-account uploader
        uploader = self.repo_path / "multi_account_github_uploader.py"
        if uploader.exists():
            github_files.append({
                "file": "multi_account_github_uploader.py",
                "reason": "Multi-account GitHub upload functionality",
                "dependencies": self._get_file_imports(uploader),
                "risk_level": "critical",
                "can_move": True,
                "move_requirements": ["Update security_scanner import", "Update config paths"]
            })
        
        # Auto-sync script
        auto_sync = self.repo_path / "JAEGIS" / "JAEGIS-METHOD" / "jaegis-auto-sync.py"
        if auto_sync.exists():
            github_files.append({
                "file": "JAEGIS/JAEGIS-METHOD/jaegis-auto-sync.py",
                "reason": "Automated GitHub synchronization",
                "dependencies": self._get_file_imports(auto_sync),
                "risk_level": "critical",
                "can_move": True,
                "move_requirements": ["Update security_scanner import", "Update file paths"]
            })
        
        return github_files
    
    def _identify_orchestration_critical(self) -> List[Dict]:
        """Identify core orchestration critical files"""
        orchestration_files = []
        
        # Enhanced orchestrator
        orchestrator_files = [
            "jaegis_enhanced_orchestrator.py",
            "jaegis_v2_enhanced_orchestrator.py",
            "JAEGIS_Enhanced_System/jaegis_enhanced_orchestrator.py"
        ]
        
        for orch_file in orchestrator_files:
            file_path = self.repo_path / orch_file
            if file_path.exists():
                orchestration_files.append({
                    "file": orch_file,
                    "reason": "Core JAEGIS orchestration",
                    "dependencies": self._get_file_imports(file_path),
                    "risk_level": "critical",
                    "can_move": True,
                    "move_requirements": ["Update all module imports", "Update config paths"]
                })
        
        return orchestration_files
    
    def _identify_config_critical(self) -> List[Dict]:
        """Identify configuration critical files"""
        config_files = []
        
        critical_configs = [
            "agent-config.txt",
            "enhanced-agent-config.txt",
            "iuas-agent-config.txt",
            "garas-agent-config.txt",
            "openrouter-config.json",
            "jaegis_config.json",
            "sync-config.json"
        ]
        
        for config_file in critical_configs:
            file_path = self.repo_path / config_file
            if file_path.exists():
                config_files.append({
                    "file": config_file,
                    "reason": "Critical system configuration",
                    "referenced_by": self._find_files_referencing(config_file),
                    "risk_level": "high",
                    "can_move": True,
                    "move_requirements": ["Update all path references"]
                })
        
        return config_files
    
    def _identify_deployment_critical(self) -> List[Dict]:
        """Identify deployment critical files"""
        deployment_files = []
        
        # Docker files
        docker_files = ["Dockerfile", "docker-compose.yml"]
        for docker_file in docker_files:
            file_path = self.repo_path / docker_file
            if file_path.exists():
                deployment_files.append({
                    "file": docker_file,
                    "reason": "Container deployment configuration",
                    "risk_level": "high",
                    "can_move": False,  # Docker files should stay at root
                    "move_requirements": ["Update COPY paths", "Update volume mounts"]
                })
        
        return deployment_files
    
    def _identify_cli_critical(self) -> List[Dict]:
        """Identify CLI critical files"""
        cli_files = []
        
        # CLI scripts
        cli_scripts = [
            "jaegis-cli.py",
            "jaegis-failsafe-cli.py",
            "eJAEGIS/cli/main.py"
        ]
        
        for cli_script in cli_scripts:
            file_path = self.repo_path / cli_script
            if file_path.exists():
                cli_files.append({
                    "file": cli_script,
                    "reason": "Command-line interface",
                    "dependencies": self._get_file_imports(file_path),
                    "risk_level": "medium",
                    "can_move": True,
                    "move_requirements": ["Update import paths", "Update config references"]
                })
        
        return cli_files
    
    def _identify_immovable_files(self):
        """Identify files that cannot be moved"""
        # Files that must stay at repository root
        root_files = {
            "README.md",
            "LICENSE",
            "CHANGELOG.md",
            "CONTRIBUTING.md",
            "requirements.txt",
            "Dockerfile",
            "docker-compose.yml",
            ".gitignore",
            ".github/workflows/*.yml"
        }
        
        for file_pattern in root_files:
            if '*' in file_pattern:
                # Handle wildcard patterns
                parent = self.repo_path / file_pattern.split('*')[0]
                if parent.exists():
                    for file_path in parent.glob('*' + file_pattern.split('*')[1]):
                        self.immovable_files.add(str(file_path.relative_to(self.repo_path)))
            else:
                file_path = self.repo_path / file_pattern
                if file_path.exists():
                    self.immovable_files.add(file_pattern)
    
    def _get_file_imports(self, file_path: Path) -> List[str]:
        """Get import statements from Python file"""
        imports = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            import re
            # Find import statements
            import_patterns = [
                r'^import\s+([^\s#]+)',
                r'^from\s+([^\s#]+)\s+import'
            ]
            
            for pattern in import_patterns:
                matches = re.findall(pattern, content, re.MULTILINE)
                imports.extend(matches)
                
        except Exception as e:
            imports.append(f"Error reading file: {e}")
        
        return list(set(imports))
    
    def _find_files_importing(self, module_name: str) -> List[str]:
        """Find files that import a specific module"""
        importing_files = []
        
        for py_file in self.repo_path.rglob("*.py"):
            if '.git' in str(py_file):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if f"import {module_name}" in content or f"from {module_name}" in content:
                    importing_files.append(str(py_file.relative_to(self.repo_path)))
                    
            except Exception:
                continue
        
        return importing_files
    
    def _find_files_referencing(self, file_name: str) -> List[str]:
        """Find files that reference a specific file"""
        referencing_files = []
        
        # Search in all text files
        for file_path in self.repo_path.rglob("*"):
            if file_path.is_file() and '.git' not in str(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if file_name in content:
                        referencing_files.append(str(file_path.relative_to(self.repo_path)))
                        
                except Exception:
                    continue
        
        return referencing_files
    
    def generate_migration_constraints(self) -> Dict:
        """Generate migration constraints based on critical system analysis"""
        constraints = {
            "immovable_files": list(self.immovable_files),
            "migration_order": self._determine_migration_order(),
            "validation_requirements": self._generate_validation_requirements(),
            "rollback_checkpoints": self._define_rollback_checkpoints()
        }
        
        return constraints
    
    def _determine_migration_order(self) -> List[Dict]:
        """Determine optimal migration order"""
        # Migration phases based on dependency analysis
        migration_phases = [
            {
                "phase": 1,
                "name": "Security Systems",
                "files": [f["file"] for f in self.critical_systems.get("security", [])],
                "reason": "Security must be validated first"
            },
            {
                "phase": 2,
                "name": "Configuration Files",
                "files": [f["file"] for f in self.critical_systems.get("configuration", [])],
                "reason": "Configs needed before dependent systems"
            },
            {
                "phase": 3,
                "name": "GitHub Integration",
                "files": [f["file"] for f in self.critical_systems.get("github_integration", [])],
                "reason": "Core upload functionality"
            },
            {
                "phase": 4,
                "name": "Core Orchestration",
                "files": [f["file"] for f in self.critical_systems.get("core_orchestration", [])],
                "reason": "Main system orchestrators"
            },
            {
                "phase": 5,
                "name": "CLI Systems",
                "files": [f["file"] for f in self.critical_systems.get("cli_systems", [])],
                "reason": "User interfaces"
            }
        ]
        
        return migration_phases
    
    def _generate_validation_requirements(self) -> Dict:
        """Generate validation requirements for each critical system"""
        validation_reqs = {}
        
        for category, files in self.critical_systems.items():
            validation_reqs[category] = []
            
            for file_info in files:
                validation_reqs[category].append({
                    "file": file_info["file"],
                    "validation_command": self._get_validation_command(file_info),
                    "success_criteria": self._get_success_criteria(file_info),
                    "timeout_seconds": 30
                })
        
        return validation_reqs
    
    def _get_validation_command(self, file_info: Dict) -> str:
        """Get validation command for file"""
        file_name = file_info["file"]
        
        if file_name.endswith(".py"):
            module_name = Path(file_name).stem
            return f"python -c 'import {module_name}; print(\"Import successful\")'"
        elif file_name.endswith(".json"):
            return f"python -c 'import json; json.load(open(\"{file_name}\"))'"
        elif "docker" in file_name.lower():
            return "docker-compose config"
        else:
            return f"test -f {file_name}"
    
    def _get_success_criteria(self, file_info: Dict) -> str:
        """Get success criteria for validation"""
        if file_info["file"].endswith(".py"):
            return "No import errors, 'Import successful' printed"
        elif file_info["file"].endswith(".json"):
            return "Valid JSON, no parsing errors"
        elif "docker" in file_info["file"].lower():
            return "Valid Docker configuration"
        else:
            return "File exists and is readable"
    
    def _define_rollback_checkpoints(self) -> List[Dict]:
        """Define rollback checkpoints"""
        checkpoints = [
            {
                "checkpoint": "pre_migration",
                "description": "Before any changes",
                "validation": "All systems operational",
                "rollback_command": "git reset --hard HEAD"
            },
            {
                "checkpoint": "security_migrated",
                "description": "After security system migration",
                "validation": "Security scanner functional",
                "rollback_command": "git reset --hard pre_migration"
            },
            {
                "checkpoint": "config_migrated",
                "description": "After configuration migration",
                "validation": "All configs loadable",
                "rollback_command": "git reset --hard security_migrated"
            },
            {
                "checkpoint": "github_migrated",
                "description": "After GitHub integration migration",
                "validation": "Upload/sync functional",
                "rollback_command": "git reset --hard config_migrated"
            },
            {
                "checkpoint": "core_migrated",
                "description": "After core system migration",
                "validation": "Orchestration functional",
                "rollback_command": "git reset --hard github_migrated"
            }
        ]
        
        return checkpoints
    
    def save_critical_analysis(self, output_path: str = "critical_systems_analysis.json"):
        """Save critical systems analysis"""
        analysis_data = {
            "critical_systems": self.critical_systems,
            "immovable_files": list(self.immovable_files),
            "migration_constraints": self.generate_migration_constraints(),
            "summary": {
                "total_critical_files": sum(len(files) for files in self.critical_systems.values()),
                "immovable_files_count": len(self.immovable_files),
                "high_risk_count": len([f for files in self.critical_systems.values() for f in files if f.get("risk_level") == "critical"])
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(analysis_data, f, indent=2)
        
        print(f"💾 Critical systems analysis saved to {output_path}")

def main():
    """Main execution"""
    identifier = CriticalSystemIdentifier(".")
    
    # Identify critical systems
    identifier.identify_critical_systems()
    
    # Save analysis
    identifier.save_critical_analysis()
    
    print("🎉 Critical systems identification complete!")

if __name__ == "__main__":
    main()
