#!/usr/bin/env python3
"""
JAEGIS Dependency Analysis Tool
Analyzes all file dependencies to create migration mapping
"""

import os
import json
import re
import ast
from pathlib import Path
from typing import Dict, List, Set, Tuple

class DependencyAnalyzer:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.dependencies = {}
        self.reverse_dependencies = {}
        self.migration_mapping = {}
        self.critical_paths = set()
        
    def analyze_all_dependencies(self):
        """Analyze dependencies for all files"""
        print("🔍 Analyzing file dependencies...")
        
        # Analyze Python files
        self._analyze_python_files()
        
        # Analyze configuration files
        self._analyze_config_files()
        
        # Analyze documentation files
        self._analyze_documentation_files()
        
        # Analyze Docker files
        self._analyze_docker_files()
        
        # Build reverse dependency map
        self._build_reverse_dependencies()
        
        print(f"✅ Analyzed {len(self.dependencies)} files")
        
    def _analyze_python_files(self):
        """Analyze Python file dependencies"""
        python_files = list(self.repo_path.rglob("*.py"))
        
        for py_file in python_files:
            if '.git' in str(py_file):
                continue
                
            relative_path = py_file.relative_to(self.repo_path)
            deps = self._extract_python_dependencies(py_file)
            
            self.dependencies[str(relative_path)] = {
                "type": "python",
                "imports": deps["imports"],
                "relative_imports": deps["relative_imports"],
                "file_references": deps["file_references"],
                "config_references": deps["config_references"],
                "risk_level": self._assess_risk_level(py_file, deps)
            }
    
    def _extract_python_dependencies(self, file_path: Path) -> Dict:
        """Extract dependencies from Python file"""
        deps = {
            "imports": [],
            "relative_imports": [],
            "file_references": [],
            "config_references": []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST for accurate import analysis
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            deps["imports"].append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        module = node.module or ""
                        if module.startswith('.'):
                            deps["relative_imports"].append({
                                "module": module,
                                "names": [alias.name for alias in node.names],
                                "level": node.level
                            })
                        else:
                            deps["imports"].append(module)
            except SyntaxError:
                # Fallback to regex if AST parsing fails
                pass
            
            # Find file path references
            file_patterns = [
                r'["\']([^"\']*\.(?:py|json|yaml|yml|txt|md|log))["\']',
                r'Path\(["\']([^"\']+)["\']',
                r'open\(["\']([^"\']+)["\']',
                r'load\(["\']([^"\']+)["\']'
            ]
            
            for pattern in file_patterns:
                matches = re.findall(pattern, content)
                deps["file_references"].extend(matches)
            
            # Find configuration references
            config_patterns = [
                r'["\']([^"\']*config[^"\']*\.(?:json|yaml|yml|txt))["\']',
                r'getenv\(["\']([^"\']+)["\']',
                r'environ\[["\']([^"\']+)["\']'
            ]
            
            for pattern in config_patterns:
                matches = re.findall(pattern, content)
                deps["config_references"].extend(matches)
            
            # Remove duplicates
            for key in deps:
                if isinstance(deps[key], list):
                    deps[key] = list(set(deps[key]))
                    
        except Exception as e:
            deps["error"] = str(e)
        
        return deps
    
    def _analyze_config_files(self):
        """Analyze configuration file dependencies"""
        config_patterns = ["*.json", "*.yaml", "*.yml", "*.txt"]
        
        for pattern in config_patterns:
            for config_file in self.repo_path.rglob(pattern):
                if '.git' in str(config_file) or 'node_modules' in str(config_file):
                    continue
                
                relative_path = config_file.relative_to(self.repo_path)
                deps = self._extract_config_dependencies(config_file)
                
                self.dependencies[str(relative_path)] = {
                    "type": "configuration",
                    "file_references": deps["file_references"],
                    "path_references": deps["path_references"],
                    "risk_level": self._assess_config_risk(config_file, deps)
                }
    
    def _extract_config_dependencies(self, file_path: Path) -> Dict:
        """Extract dependencies from configuration files"""
        deps = {
            "file_references": [],
            "path_references": []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find file references
            file_refs = re.findall(r'["\']([^"\']*\.(?:py|json|yaml|yml|txt|md))["\']', content)
            deps["file_references"] = list(set(file_refs))
            
            # Find path references
            path_refs = re.findall(r'["\']([^"\']*[/\\][^"\']*)["\']', content)
            deps["path_references"] = list(set(path_refs))
            
        except Exception as e:
            deps["error"] = str(e)
        
        return deps
    
    def _analyze_documentation_files(self):
        """Analyze documentation file dependencies"""
        doc_files = list(self.repo_path.rglob("*.md"))
        
        for doc_file in doc_files:
            if '.git' in str(doc_file):
                continue
                
            relative_path = doc_file.relative_to(self.repo_path)
            deps = self._extract_doc_dependencies(doc_file)
            
            self.dependencies[str(relative_path)] = {
                "type": "documentation",
                "file_links": deps["file_links"],
                "code_references": deps["code_references"],
                "risk_level": "low"
            }
    
    def _extract_doc_dependencies(self, file_path: Path) -> Dict:
        """Extract dependencies from documentation files"""
        deps = {
            "file_links": [],
            "code_references": []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find markdown links to files
            file_links = re.findall(r'\[([^\]]+)\]\(([^)]+\.(?:py|json|yaml|yml|txt|md))\)', content)
            deps["file_links"] = [link[1] for link in file_links]
            
            # Find code references
            code_refs = re.findall(r'`([^`]*\.(?:py|json|yaml|yml))`', content)
            deps["code_references"] = list(set(code_refs))
            
        except Exception as e:
            deps["error"] = str(e)
        
        return deps
    
    def _analyze_docker_files(self):
        """Analyze Docker file dependencies"""
        docker_files = ["Dockerfile", "docker-compose.yml", "docker-compose.yaml"]
        
        for docker_file in docker_files:
            file_path = self.repo_path / docker_file
            if file_path.exists():
                relative_path = file_path.relative_to(self.repo_path)
                deps = self._extract_docker_dependencies(file_path)
                
                self.dependencies[str(relative_path)] = {
                    "type": "docker",
                    "copy_paths": deps["copy_paths"],
                    "volume_mounts": deps["volume_mounts"],
                    "workdir": deps["workdir"],
                    "risk_level": "high"
                }
    
    def _extract_docker_dependencies(self, file_path: Path) -> Dict:
        """Extract dependencies from Docker files"""
        deps = {
            "copy_paths": [],
            "volume_mounts": [],
            "workdir": []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find COPY instructions
            copy_matches = re.findall(r'COPY\s+([^\s]+)\s+([^\s]+)', content)
            deps["copy_paths"] = [{"source": src, "dest": dst} for src, dst in copy_matches]
            
            # Find volume mounts
            volume_matches = re.findall(r'volumes?:\s*\n((?:\s+-\s+[^\n]+\n?)+)', content, re.MULTILINE)
            for volume_block in volume_matches:
                volumes = re.findall(r'-\s+([^:\n]+):([^:\n]+)', volume_block)
                deps["volume_mounts"].extend([{"host": host, "container": container} for host, container in volumes])
            
            # Find WORKDIR
            workdir_matches = re.findall(r'WORKDIR\s+([^\s]+)', content)
            deps["workdir"] = workdir_matches
            
        except Exception as e:
            deps["error"] = str(e)
        
        return deps
    
    def _assess_risk_level(self, file_path: Path, deps: Dict) -> str:
        """Assess migration risk level for Python files"""
        # Critical files
        critical_files = {
            'security_scanner.py',
            'multi_account_github_uploader.py',
            'jaegis-auto-sync.py',
            'jaegis_enhanced_orchestrator.py'
        }
        
        if file_path.name in critical_files:
            return "critical"
        
        # High risk if many dependencies
        total_deps = len(deps.get("imports", [])) + len(deps.get("relative_imports", [])) + len(deps.get("file_references", []))
        
        if total_deps > 10:
            return "high"
        elif total_deps > 5:
            return "medium"
        else:
            return "low"
    
    def _assess_config_risk(self, file_path: Path, deps: Dict) -> str:
        """Assess migration risk level for config files"""
        critical_configs = {
            'agent-config.txt',
            'enhanced-agent-config.txt',
            'security_config.json',
            'docker-compose.yml'
        }
        
        if file_path.name in critical_configs:
            return "critical"
        
        total_refs = len(deps.get("file_references", [])) + len(deps.get("path_references", []))
        
        if total_refs > 5:
            return "high"
        elif total_refs > 2:
            return "medium"
        else:
            return "low"
    
    def _build_reverse_dependencies(self):
        """Build reverse dependency mapping"""
        for file_path, deps in self.dependencies.items():
            # Process different dependency types
            all_refs = []
            
            if "imports" in deps:
                all_refs.extend(deps["imports"])
            if "file_references" in deps:
                all_refs.extend(deps["file_references"])
            if "config_references" in deps:
                all_refs.extend(deps["config_references"])
            
            for ref in all_refs:
                if ref not in self.reverse_dependencies:
                    self.reverse_dependencies[ref] = []
                self.reverse_dependencies[ref].append(file_path)
    
    def generate_migration_mapping(self, ideal_structure: Dict):
        """Generate migration mapping based on ideal structure"""
        print("🗺️ Generating migration mapping...")
        
        # Define migration rules based on file types and categories
        migration_rules = {
            "security_scanner.py": "security/security_scanner.py",
            "security_config.json": "config/system/security_config.json",
            "multi_account_github_uploader.py": "integrations/github/multi_account_github_uploader.py",
            "jaegis-auto-sync.py": "integrations/github/jaegis-auto-sync.py",
            "agent-config.txt": "core/agents/agent-config.txt",
            "enhanced-agent-config.txt": "core/agents/enhanced-agent-config.txt",
            "openrouter-config.json": "integrations/openrouter/openrouter-config.json",
            "jaegis_config.json": "config/system/jaegis_config.json"
        }
        
        # Apply migration rules
        for old_path, deps in self.dependencies.items():
            file_name = Path(old_path).name
            
            if file_name in migration_rules:
                new_path = migration_rules[file_name]
            else:
                new_path = self._determine_new_path(old_path, deps)
            
            self.migration_mapping[old_path] = {
                "new_path": new_path,
                "dependencies": self._get_file_dependencies(old_path),
                "reverse_dependencies": self.reverse_dependencies.get(old_path, []),
                "risk_level": deps.get("risk_level", "medium"),
                "validation_method": self._get_validation_method(old_path, deps)
            }
        
        print(f"✅ Generated migration mapping for {len(self.migration_mapping)} files")
    
    def _determine_new_path(self, old_path: str, deps: Dict) -> str:
        """Determine new path based on file analysis"""
        path_obj = Path(old_path)
        
        # Categorize by directory patterns
        if "nlds" in old_path.lower():
            return f"core/nlds/{path_obj.name}"
        elif "pitces" in old_path.lower():
            return f"frameworks/pitces/{path_obj.name}"
        elif "chimera" in old_path.lower():
            return f"frameworks/project_chimera/{path_obj.name}"
        elif "github" in old_path.lower() or "upload" in old_path.lower():
            return f"integrations/github/{path_obj.name}"
        elif "security" in old_path.lower():
            return f"security/{path_obj.name}"
        elif "config" in old_path.lower() or path_obj.suffix in ['.json', '.yaml', '.yml']:
            return f"config/system/{path_obj.name}"
        elif "test" in old_path.lower():
            return f"tests/{path_obj.name}"
        elif "doc" in old_path.lower() or path_obj.suffix == '.md':
            return f"docs/{path_obj.name}"
        elif "deploy" in old_path.lower() or "docker" in old_path.lower():
            return f"deployment/{path_obj.name}"
        elif path_obj.suffix == '.py':
            return f"core/{path_obj.name}"
        else:
            return old_path  # Keep in place if uncertain
    
    def _get_file_dependencies(self, file_path: str) -> List[str]:
        """Get all dependencies for a file"""
        deps = self.dependencies.get(file_path, {})
        all_deps = []
        
        for key in ["imports", "file_references", "config_references"]:
            if key in deps:
                all_deps.extend(deps[key])
        
        return list(set(all_deps))
    
    def _get_validation_method(self, file_path: str, deps: Dict) -> str:
        """Determine validation method for file"""
        if deps.get("type") == "python":
            return f"python -c 'import {Path(file_path).stem}'"
        elif deps.get("type") == "configuration":
            return f"validate_config {file_path}"
        elif deps.get("type") == "docker":
            return "docker-compose config"
        else:
            return f"test -f {file_path}"
    
    def save_analysis(self, output_path: str = "dependency_analysis.json"):
        """Save dependency analysis results"""
        analysis_data = {
            "dependencies": self.dependencies,
            "reverse_dependencies": self.reverse_dependencies,
            "migration_mapping": self.migration_mapping,
            "summary": {
                "total_files": len(self.dependencies),
                "critical_files": len([f for f, d in self.dependencies.items() if d.get("risk_level") == "critical"]),
                "high_risk_files": len([f for f, d in self.dependencies.items() if d.get("risk_level") == "high"])
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(analysis_data, f, indent=2)
        
        print(f"💾 Dependency analysis saved to {output_path}")

def main():
    """Main execution"""
    analyzer = DependencyAnalyzer(".")
    
    # Analyze all dependencies
    analyzer.analyze_all_dependencies()
    
    # Generate migration mapping
    analyzer.generate_migration_mapping({})
    
    # Save results
    analyzer.save_analysis()
    
    print("🎉 Dependency analysis complete!")

if __name__ == "__main__":
    main()
