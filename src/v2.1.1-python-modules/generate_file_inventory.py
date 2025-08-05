#!/usr/bin/env python3
"""
JAEGIS Repository File Inventory Generator
Creates comprehensive catalog of all files with metadata for migration planning
"""

import os
import json
from common.utils import calculate_string_hash
from pathlib import Path
from datetime import datetime
import subprocess

class FileInventoryGenerator:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.inventory = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "repo_path": str(self.repo_path),
                "total_files": 0,
                "total_size_bytes": 0
            },
            "files": [],
            "directories": [],
            "critical_files": [],
            "dependencies": {}
        }
    
    def generate_inventory(self):
        """Generate complete file inventory"""
        print("🔍 Generating comprehensive file inventory...")
        
        # Walk through all files
        for root, dirs, files in os.walk(self.repo_path):
            # Skip .git directory
            if '.git' in root:
                continue
                
            root_path = Path(root)
            relative_root = root_path.relative_to(self.repo_path)
            
            # Add directory info
            if str(relative_root) != '.':
                self.inventory["directories"].append({
                    "path": str(relative_root),
                    "absolute_path": str(root_path),
                    "file_count": len(files),
                    "subdirs": len(dirs)
                })
            
            # Process each file
            for file in files:
                file_path = root_path / file
                relative_path = file_path.relative_to(self.repo_path)
                
                file_info = self._analyze_file(file_path, relative_path)
                self.inventory["files"].append(file_info)
                
                # Track critical files
                if self._is_critical_file(file_path):
                    self.inventory["critical_files"].append(str(relative_path))
        
        # Update metadata
        self.inventory["metadata"]["total_files"] = len(self.inventory["files"])
        self.inventory["metadata"]["total_size_bytes"] = sum(f["size_bytes"] for f in self.inventory["files"])
        
        print(f"✅ Inventory complete: {self.inventory['metadata']['total_files']} files")
        return self.inventory
    
    def _analyze_file(self, file_path: Path, relative_path: Path):
        """Analyze individual file"""
        try:
            stat = file_path.stat()
            
            # Calculate file hash
            file_hash = calculate_string_hash(str(file_path))
            
            # Determine file type and category
            file_type = self._get_file_type(file_path)
            category = self._get_file_category(file_path)
            
            return {
                "relative_path": str(relative_path),
                "absolute_path": str(file_path),
                "size_bytes": stat.st_size,
                "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "file_type": file_type,
                "category": category,
                "hash": file_hash,
                "is_critical": self._is_critical_file(file_path),
                "migration_priority": self._get_migration_priority(file_path)
            }
        except Exception as e:
            return {
                "relative_path": str(relative_path),
                "error": str(e),
                "is_critical": False,
                "migration_priority": "low"
            }
    
    def _get_file_type(self, file_path: Path):
        """Determine file type"""
        suffix = file_path.suffix.lower()
        type_map = {
            '.py': 'python',
            '.json': 'json_config',
            '.yaml': 'yaml_config',
            '.yml': 'yaml_config',
            '.txt': 'text_config',
            '.md': 'documentation',
            '.dockerfile': 'docker',
            '.sh': 'shell_script',
            '.ps1': 'powershell_script',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.html': 'html',
            '.css': 'css',
            '.log': 'log_file'
        }
        return type_map.get(suffix, 'other')
    
    def _get_file_category(self, file_path: Path):
        """Categorize file by purpose"""
        path_str = str(file_path).lower()
        
        if 'security' in path_str:
            return 'security'
        elif 'github' in path_str or 'upload' in path_str:
            return 'github_integration'
        elif 'nlds' in path_str:
            return 'nlds_system'
        elif 'pitces' in path_str:
            return 'pitces_framework'
        elif 'chimera' in path_str:
            return 'project_chimera'
        elif 'config' in path_str or file_path.suffix in ['.json', '.yaml', '.yml']:
            return 'configuration'
        elif 'test' in path_str:
            return 'testing'
        elif 'doc' in path_str or file_path.suffix == '.md':
            return 'documentation'
        elif 'deploy' in path_str or 'docker' in path_str:
            return 'deployment'
        elif file_path.suffix == '.py':
            return 'core_system'
        else:
            return 'other'
    
    def _is_critical_file(self, file_path: Path):
        """Identify critical files that require special handling"""
        critical_files = {
            'security_scanner.py',
            'multi_account_github_uploader.py',
            'jaegis-auto-sync.py',
            'jaegis_enhanced_orchestrator.py',
            'jaegis_v2_enhanced_orchestrator.py',
            'agent-config.txt',
            'enhanced-agent-config.txt',
            'docker-compose.yml',
            'Dockerfile',
            'requirements.txt',
            'README.md'
        }
        
        return file_path.name in critical_files or 'config' in str(file_path).lower()
    
    def _get_migration_priority(self, file_path: Path):
        """Determine migration priority"""
        if self._is_critical_file(file_path):
            return 'critical'
        elif file_path.suffix == '.py':
            return 'high'
        elif file_path.suffix in ['.json', '.yaml', '.yml', '.txt']:
            return 'medium'
        else:
            return 'low'
    
    def analyze_dependencies(self):
        """Analyze file dependencies"""
        print("🔗 Analyzing file dependencies...")
        
        for file_info in self.inventory["files"]:
            if file_info.get("file_type") == "python":
                deps = self._analyze_python_dependencies(file_info["absolute_path"])
                self.inventory["dependencies"][file_info["relative_path"]] = deps
        
        print(f"✅ Analyzed dependencies for {len(self.inventory['dependencies'])} Python files")
    
    def _analyze_python_dependencies(self, file_path: str):
        """Analyze Python file dependencies"""
        dependencies = {
            "imports": [],
            "relative_imports": [],
            "file_references": [],
            "config_references": []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find import statements
            import re
            
            # Standard imports
            imports = re.findall(r'^(?:from\s+(\S+)\s+)?import\s+(.+)$', content, re.MULTILINE)
            for module, items in imports:
                if module:
                    dependencies["imports"].append(f"from {module} import {items}")
                else:
                    dependencies["imports"].append(f"import {items}")
            
            # Relative imports
            rel_imports = re.findall(r'from\s+\.+(\S*)\s+import\s+(.+)', content)
            dependencies["relative_imports"] = [f"from .{module} import {items}" for module, items in rel_imports]
            
            # File path references
            file_refs = re.findall(r'["\']([^"\']*\.(?:py|json|yaml|yml|txt|md))["\']', content)
            dependencies["file_references"] = list(set(file_refs))
            
            # Config file references
            config_refs = re.findall(r'["\']([^"\']*config[^"\']*)["\']', content)
            dependencies["config_references"] = list(set(config_refs))
            
        except Exception as e:
            dependencies["error"] = str(e)
        
        return dependencies
    
    def save_inventory(self, output_path: str = "file_inventory.json"):
        """Save inventory to JSON file"""
        with open(output_path, 'w') as f:
            json.dump(self.inventory, f, indent=2)
        
        print(f"💾 Inventory saved to {output_path}")
        
        # Generate summary report
        self._generate_summary_report()
    
    def _generate_summary_report(self):
        """Generate human-readable summary"""
        summary = f"""
# JAEGIS Repository File Inventory Summary

## Overview
- **Total Files**: {self.inventory['metadata']['total_files']:,}
- **Total Size**: {self.inventory['metadata']['total_size_bytes'] / (1024*1024):.1f} MB
- **Critical Files**: {len(self.inventory['critical_files'])}
- **Directories**: {len(self.inventory['directories'])}

## File Categories
"""
        
        # Count by category
        categories = {}
        for file_info in self.inventory["files"]:
            cat = file_info.get("category", "unknown")
            categories[cat] = categories.get(cat, 0) + 1
        
        for category, count in sorted(categories.items()):
            summary += f"- **{category.title()}**: {count} files\n"
        
        summary += f"""
## Migration Priorities
"""
        
        # Count by priority
        priorities = {}
        for file_info in self.inventory["files"]:
            priority = file_info.get("migration_priority", "unknown")
            priorities[priority] = priorities.get(priority, 0) + 1
        
        for priority, count in sorted(priorities.items()):
            summary += f"- **{priority.title()}**: {count} files\n"
        
        with open("inventory_summary.md", 'w') as f:
            f.write(summary)
        
        print("📊 Summary report saved to inventory_summary.md")

def main():
    """Main execution"""
    repo_path = "."  # Current directory
    
    generator = FileInventoryGenerator(repo_path)
    
    # Generate inventory
    inventory = generator.generate_inventory()
    
    # Analyze dependencies
    generator.analyze_dependencies()
    
    # Save results
    generator.save_inventory()
    
    print("🎉 File inventory generation complete!")

if __name__ == "__main__":
    main()
