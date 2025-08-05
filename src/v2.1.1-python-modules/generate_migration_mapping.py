#!/usr/bin/env python3
"""
JAEGIS Migration Mapping Generator
Creates detailed migration mapping document in JSON format
"""

import json
from pathlib import Path
from typing import Dict, List

class MigrationMappingGenerator:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.migration_mapping = {}
        
        # Define ideal structure mapping
        self.ideal_structure = {
            # Security files
            "security_scanner.py": "security/security_scanner.py",
            "security_config.json": "config/system/security_config.json",
            
            # GitHub integration
            "multi_account_github_uploader.py": "integrations/github/multi_account_github_uploader.py",
            "JAEGIS/JAEGIS-METHOD/jaegis-auto-sync.py": "integrations/github/jaegis-auto-sync.py",
            "github_integration/github_fetcher.py": "integrations/github/github_fetcher.py",
            "github_integration/amasiap_protocol.py": "integrations/github/amasiap_protocol.py",
            "github_integration/squad_coordinator.py": "integrations/github/squad_coordinator.py",
            
            # Core agents
            "agent-config.txt": "core/agents/agent-config.txt",
            "enhanced-agent-config.txt": "core/agents/enhanced-agent-config.txt",
            "iuas-agent-config.txt": "core/agents/iuas-agent-config.txt",
            "garas-agent-config.txt": "core/agents/garas-agent-config.txt",
            
            # Core orchestration
            "jaegis_enhanced_orchestrator.py": "core/orchestration/jaegis_enhanced_orchestrator.py",
            "jaegis_v2_enhanced_orchestrator.py": "core/orchestration/jaegis_v2_enhanced_orchestrator.py",
            "JAEGIS_Enhanced_System/main.py": "core/orchestration/main.py",
            
            # N.L.D.S. system
            "nlds/": "core/nlds/",
            "core/nlds/": "core/nlds/",
            
            # P.I.T.C.E.S. framework
            "pitces/": "frameworks/pitces/",
            
            # Project Chimera
            "JAEGIS_Enhanced_System/project_chimera/": "frameworks/project_chimera/",
            
            # Cognitive pipeline
            "cognitive_pipeline/": "frameworks/cognitive_pipeline/",
            
            # Configuration files
            "openrouter-config.json": "integrations/openrouter/openrouter-config.json",
            "jaegis_config.json": "config/system/jaegis_config.json",
            "sync-config.json": "config/system/sync-config.json",
            "squad-commands.md": "config/commands/squad-commands.md",
            
            # CLI systems
            "jaegis-cli.py": "integrations/cli/jaegis-cli.py",
            "jaegis-failsafe-cli.py": "integrations/cli/jaegis-failsafe-cli.py",
            "eJAEGIS/": "integrations/vscode/",
            
            # Deployment
            "deployment/": "deployment/",
            "Dockerfile": "Dockerfile",  # Stay at root
            "docker-compose.yml": "docker-compose.yml",  # Stay at root
            
            # Tests
            "tests/": "tests/",
            
            # Documentation
            "README.md": "README.md",  # Stay at root
            "SECURITY_SCANNER_README.md": "docs/SECURITY_SCANNER_README.md",
            "CONTRIBUTING.md": "CONTRIBUTING.md",  # Stay at root
            "CHANGELOG.md": "CHANGELOG.md",  # Stay at root
            
            # Examples
            "examples/": "examples/"
        }
    
    def generate_mapping(self):
        """Generate complete migration mapping"""
        print("🗺️ Generating migration mapping...")
        
        # Process all files in repository
        for file_path in self._get_all_files():
            if '.git' in str(file_path):
                continue
                
            relative_path = str(file_path.relative_to(self.repo_path))
            new_path = self._determine_new_path(relative_path)
            
            self.migration_mapping[relative_path] = {
                "old_path": relative_path,
                "new_path": new_path,
                "dependencies": self._analyze_dependencies(file_path),
                "risk_level": self._assess_risk_level(file_path),
                "validation_method": self._get_validation_method(file_path),
                "move_required": new_path != relative_path,
                "update_references": self._requires_reference_updates(file_path),
                "migration_phase": self._get_migration_phase(relative_path)
            }
        
        print(f"✅ Generated mapping for {len(self.migration_mapping)} files")
        
    def _get_all_files(self):
        """Get all files in repository"""
        for file_path in self.repo_path.rglob("*"):
            if file_path.is_file():
                yield file_path
    
    def _determine_new_path(self, old_path: str) -> str:
        """Determine new path for file"""
        # Check exact matches first
        if old_path in self.ideal_structure:
            return self.ideal_structure[old_path]
        
        # Check directory matches
        for old_pattern, new_pattern in self.ideal_structure.items():
            if old_pattern.endswith('/') and old_path.startswith(old_pattern):
                return old_path.replace(old_pattern, new_pattern, 1)
        
        # Pattern-based matching
        path_obj = Path(old_path)
        
        # Security files
        if 'security' in old_path.lower():
            if path_obj.suffix == '.py':
                return f"security/{path_obj.name}"
            else:
                return f"config/system/{path_obj.name}"
        
        # GitHub integration
        elif any(keyword in old_path.lower() for keyword in ['github', 'upload', 'sync']):
            return f"integrations/github/{path_obj.name}"
        
        # N.L.D.S. system
        elif 'nlds' in old_path.lower():
            return old_path.replace('nlds/', 'core/nlds/', 1)
        
        # P.I.T.C.E.S. framework
        elif 'pitces' in old_path.lower():
            return old_path.replace('pitces/', 'frameworks/pitces/', 1)
        
        # Project Chimera
        elif 'chimera' in old_path.lower():
            return old_path.replace('JAEGIS_Enhanced_System/project_chimera/', 'frameworks/project_chimera/', 1)
        
        # Cognitive pipeline
        elif 'cognitive_pipeline' in old_path.lower():
            return old_path.replace('cognitive_pipeline/', 'frameworks/cognitive_pipeline/', 1)
        
        # Configuration files
        elif path_obj.suffix in ['.json', '.yaml', '.yml', '.txt'] and 'config' in old_path.lower():
            return f"config/system/{path_obj.name}"
        
        # Agent configurations
        elif 'agent-config' in path_obj.name:
            return f"core/agents/{path_obj.name}"
        
        # CLI files
        elif any(keyword in old_path.lower() for keyword in ['cli', 'jaegis']):
            if 'ejaegis' in old_path.lower():
                return old_path.replace('eJAEGIS/', 'integrations/vscode/', 1)
            else:
                return f"integrations/cli/{path_obj.name}"
        
        # Test files
        elif 'test' in old_path.lower():
            return old_path if old_path.startswith('tests/') else f"tests/{path_obj.name}"
        
        # Documentation
        elif path_obj.suffix == '.md':
            if path_obj.name in ['README.md', 'CONTRIBUTING.md', 'CHANGELOG.md', 'LICENSE']:
                return old_path  # Stay at root
            else:
                return f"docs/{path_obj.name}"
        
        # Deployment files
        elif any(keyword in old_path.lower() for keyword in ['deploy', 'docker', 'kubernetes']):
            if path_obj.name in ['Dockerfile', 'docker-compose.yml']:
                return old_path  # Stay at root
            else:
                return old_path if old_path.startswith('deployment/') else f"deployment/{path_obj.name}"
        
        # Core Python files
        elif path_obj.suffix == '.py':
            if 'enhanced_system' in old_path.lower():
                return f"core/{path_obj.name}"
            else:
                return old_path
        
        # Default: keep in place
        else:
            return old_path
    
    def _analyze_dependencies(self, file_path: Path) -> List[str]:
        """Analyze file dependencies"""
        dependencies = []
        
        if file_path.suffix == '.py':
            dependencies = self._analyze_python_dependencies(file_path)
        elif file_path.suffix in ['.json', '.yaml', '.yml']:
            dependencies = self._analyze_config_dependencies(file_path)
        elif file_path.name in ['Dockerfile', 'docker-compose.yml']:
            dependencies = self._analyze_docker_dependencies(file_path)
        
        return dependencies
    
    def _analyze_python_dependencies(self, file_path: Path) -> List[str]:
        """Analyze Python file dependencies"""
        dependencies = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            import re
            
            # Find import statements
            imports = re.findall(r'^(?:from\s+([^\s]+)\s+)?import\s+([^\s#]+)', content, re.MULTILINE)
            for module, item in imports:
                if module:
                    dependencies.append(module)
                else:
                    dependencies.append(item)
            
            # Find file references
            file_refs = re.findall(r'["\']([^"\']*\.(?:py|json|yaml|yml|txt))["\']', content)
            dependencies.extend(file_refs)
            
        except Exception:
            pass
        
        return list(set(dependencies))
    
    def _analyze_config_dependencies(self, file_path: Path) -> List[str]:
        """Analyze configuration file dependencies"""
        dependencies = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            import re
            
            # Find file references
            file_refs = re.findall(r'["\']([^"\']*\.(?:py|json|yaml|yml|txt))["\']', content)
            dependencies.extend(file_refs)
            
            # Find path references
            path_refs = re.findall(r'["\']([^"\']*[/\\][^"\']*)["\']', content)
            dependencies.extend(path_refs)
            
        except Exception:
            pass
        
        return list(set(dependencies))
    
    def _analyze_docker_dependencies(self, file_path: Path) -> List[str]:
        """Analyze Docker file dependencies"""
        dependencies = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            import re
            
            # Find COPY instructions
            copy_refs = re.findall(r'COPY\s+([^\s]+)', content)
            dependencies.extend(copy_refs)
            
            # Find volume mounts
            volume_refs = re.findall(r'([^:]+):', content)
            dependencies.extend(volume_refs)
            
        except Exception:
            pass
        
        return list(set(dependencies))
    
    def _assess_risk_level(self, file_path: Path) -> str:
        """Assess migration risk level"""
        critical_files = {
            'security_scanner.py',
            'multi_account_github_uploader.py',
            'jaegis-auto-sync.py',
            'jaegis_enhanced_orchestrator.py',
            'docker-compose.yml',
            'Dockerfile'
        }
        
        if file_path.name in critical_files:
            return "critical"
        
        high_risk_patterns = ['config', 'agent', 'orchestrator']
        if any(pattern in str(file_path).lower() for pattern in high_risk_patterns):
            return "high"
        
        if file_path.suffix == '.py':
            return "medium"
        
        return "low"
    
    def _get_validation_method(self, file_path: Path) -> str:
        """Get validation method for file"""
        if file_path.suffix == '.py':
            module_name = file_path.stem
            return f"python -c 'import {module_name}'"
        elif file_path.suffix == '.json':
            return f"python -c 'import json; json.load(open(\"{file_path.name}\"))'"
        elif file_path.name == 'docker-compose.yml':
            return "docker-compose config"
        elif file_path.suffix in ['.yaml', '.yml']:
            return f"python -c 'import yaml; yaml.safe_load(open(\"{file_path.name}\"))'"
        else:
            return f"test -f {file_path.name}"
    
    def _requires_reference_updates(self, file_path: Path) -> bool:
        """Check if file requires reference updates"""
        # Files that are commonly referenced by others
        referenced_files = {
            'security_scanner.py',
            'multi_account_github_uploader.py',
            'agent-config.txt',
            'security_config.json'
        }
        
        return file_path.name in referenced_files
    
    def _get_migration_phase(self, file_path: str) -> int:
        """Determine migration phase for file"""
        if 'security' in file_path.lower():
            return 1
        elif any(keyword in file_path.lower() for keyword in ['config', 'agent-config']):
            return 2
        elif any(keyword in file_path.lower() for keyword in ['github', 'upload', 'sync']):
            return 3
        elif any(keyword in file_path.lower() for keyword in ['orchestrator', 'main']):
            return 4
        elif any(keyword in file_path.lower() for keyword in ['cli', 'jaegis']):
            return 5
        else:
            return 6  # Non-critical files
    
    def generate_phase_summary(self) -> Dict:
        """Generate summary by migration phase"""
        phase_summary = {}
        
        for file_info in self.migration_mapping.values():
            phase = file_info["migration_phase"]
            if phase not in phase_summary:
                phase_summary[phase] = {
                    "files": [],
                    "critical_count": 0,
                    "high_risk_count": 0,
                    "total_count": 0
                }
            
            phase_summary[phase]["files"].append(file_info["old_path"])
            phase_summary[phase]["total_count"] += 1
            
            if file_info["risk_level"] == "critical":
                phase_summary[phase]["critical_count"] += 1
            elif file_info["risk_level"] == "high":
                phase_summary[phase]["high_risk_count"] += 1
        
        return phase_summary
    
    def save_mapping(self, output_path: str = "migration_mapping.json"):
        """Save migration mapping to JSON file"""
        mapping_data = {
            "metadata": {
                "total_files": len(self.migration_mapping),
                "files_to_move": len([f for f in self.migration_mapping.values() if f["move_required"]]),
                "critical_files": len([f for f in self.migration_mapping.values() if f["risk_level"] == "critical"]),
                "high_risk_files": len([f for f in self.migration_mapping.values() if f["risk_level"] == "high"])
            },
            "migration_mapping": self.migration_mapping,
            "phase_summary": self.generate_phase_summary(),
            "validation_commands": self._generate_validation_commands()
        }
        
        with open(output_path, 'w') as f:
            json.dump(mapping_data, f, indent=2)
        
        print(f"💾 Migration mapping saved to {output_path}")
        
        # Generate human-readable summary
        self._generate_summary_report(mapping_data)
    
    def _generate_validation_commands(self) -> Dict:
        """Generate validation commands for each phase"""
        commands = {}
        
        for file_info in self.migration_mapping.values():
            phase = file_info["migration_phase"]
            if phase not in commands:
                commands[phase] = []
            
            commands[phase].append({
                "file": file_info["old_path"],
                "new_path": file_info["new_path"],
                "command": file_info["validation_method"],
                "risk_level": file_info["risk_level"]
            })
        
        return commands
    
    def _generate_summary_report(self, mapping_data: Dict):
        """Generate human-readable summary report"""
        summary = f"""# JAEGIS Repository Migration Mapping Summary

## Overview
- **Total Files**: {mapping_data['metadata']['total_files']:,}
- **Files to Move**: {mapping_data['metadata']['files_to_move']:,}
- **Critical Files**: {mapping_data['metadata']['critical_files']}
- **High Risk Files**: {mapping_data['metadata']['high_risk_files']}

## Migration Phases
"""
        
        for phase, info in mapping_data['phase_summary'].items():
            summary += f"""
### Phase {phase}
- **Total Files**: {info['total_count']}
- **Critical Files**: {info['critical_count']}
- **High Risk Files**: {info['high_risk_count']}
"""
        
        summary += """
## Key File Migrations
"""
        
        # Show important file migrations
        important_files = [
            'security_scanner.py',
            'multi_account_github_uploader.py',
            'jaegis-auto-sync.py',
            'agent-config.txt'
        ]
        
        for file_name in important_files:
            for old_path, info in mapping_data['migration_mapping'].items():
                if file_name in old_path:
                    summary += f"- **{old_path}** → **{info['new_path']}**\n"
                    break
        
        with open("migration_mapping_summary.md", 'w') as f:
            f.write(summary)
        
        print("📊 Summary report saved to migration_mapping_summary.md")

def main():
    """Main execution"""
    generator = MigrationMappingGenerator(".")
    
    # Generate mapping
    generator.generate_mapping()
    
    # Save results
    generator.save_mapping()
    
    print("🎉 Migration mapping generation complete!")

if __name__ == "__main__":
    main()
