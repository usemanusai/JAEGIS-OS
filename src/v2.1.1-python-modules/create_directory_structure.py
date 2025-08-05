#!/usr/bin/env python3
"""
JAEGIS Directory Structure Creator
Creates the ideal directory structure in staging branch
"""

import os
from pathlib import Path
from typing import Dict, List

class DirectoryStructureCreator:
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        
        # Define ideal directory structure
        self.directory_structure = {
            "core": {
                "description": "Core JAEGIS system components",
                "subdirs": {
                    "agents": "Agent implementations and configurations",
                    "orchestration": "Core orchestration systems",
                    "nlds": "N.L.D.S. Tier 0 system",
                    "brain_protocol": "Brain Protocol Suite components"
                }
            },
            "frameworks": {
                "description": "Specialized frameworks and engines",
                "subdirs": {
                    "pitces": "P.I.T.C.E.S. framework implementation",
                    "cognitive_pipeline": "Cognitive processing pipeline",
                    "project_chimera": "Advanced AI security architecture"
                }
            },
            "integrations": {
                "description": "External system integrations",
                "subdirs": {
                    "github": "GitHub integration and upload systems",
                    "openrouter": "OpenRouter.ai integration",
                    "vscode": "VS Code extension and IDE integration",
                    "cli": "Command-line interfaces"
                }
            },
            "security": {
                "description": "Security systems and scanning",
                "subdirs": {
                    "patterns": "Security pattern definitions",
                    "policies": "Security policies and configurations",
                    "audit": "Audit logging and compliance"
                }
            },
            "config": {
                "description": "Configuration management",
                "subdirs": {
                    "system": "System-wide configurations",
                    "agents": "Agent-specific configurations",
                    "commands": "Command definitions and mappings",
                    "templates": "Configuration templates"
                }
            },
            "deployment": {
                "description": "Deployment configurations and scripts",
                "subdirs": {
                    "kubernetes": "Kubernetes manifests",
                    "monitoring": "Monitoring and observability",
                    "backup": "Backup configurations",
                    "security": "Security hardening configurations"
                }
            },
            "scripts": {
                "description": "Utility and automation scripts",
                "subdirs": {
                    "services": "Background services and daemons",
                    "monitoring": "System monitoring scripts",
                    "validation": "Validation and verification scripts",
                    "utilities": "General utility scripts"
                }
            },
            "tests": {
                "description": "Testing framework and test suites",
                "subdirs": {
                    "unit": "Unit tests for individual components",
                    "integration": "Integration tests for system interactions",
                    "security": "Security and vulnerability tests",
                    "performance": "Performance and load tests",
                    "acceptance": "User acceptance tests",
                    "validation": "System validation tests"
                }
            },
            "docs": {
                "description": "Documentation and guides",
                "subdirs": {
                    "api": "API documentation and references",
                    "architecture": "System architecture documentation",
                    "tutorials": "User tutorials and guides",
                    "security": "Security documentation",
                    "diagrams": "Architecture diagrams and visuals",
                    "user-guide": "End-user documentation"
                }
            },
            "examples": {
                "description": "Usage examples and demonstrations",
                "subdirs": {
                    "basic": "Basic usage examples",
                    "advanced": "Advanced configuration examples",
                    "integrations": "Integration examples"
                }
            },
            "logs": {
                "description": "Log files (gitignored)",
                "subdirs": {}
            }
        }
    
    def create_structure(self):
        """Create the complete directory structure"""
        print("🏗️ Creating ideal directory structure...")
        
        created_dirs = []
        
        for main_dir, config in self.directory_structure.items():
            # Create main directory
            main_path = self.repo_path / main_dir
            if not main_path.exists():
                main_path.mkdir(parents=True, exist_ok=True)
                created_dirs.append(str(main_path))
                print(f"  📁 Created: {main_dir}/")
            
            # Create README for main directory
            self._create_directory_readme(main_path, main_dir, config)
            
            # Create subdirectories
            for subdir, description in config["subdirs"].items():
                sub_path = main_path / subdir
                if not sub_path.exists():
                    sub_path.mkdir(parents=True, exist_ok=True)
                    created_dirs.append(str(sub_path))
                    print(f"    📁 Created: {main_dir}/{subdir}/")
                
                # Create .gitkeep for empty directories
                gitkeep_path = sub_path / ".gitkeep"
                if not any(sub_path.iterdir()):  # If directory is empty
                    gitkeep_path.touch()
                    print(f"      📄 Created: {main_dir}/{subdir}/.gitkeep")
        
        # Create special files
        self._create_special_files()
        
        print(f"✅ Created {len(created_dirs)} directories")
        return created_dirs
    
    def _create_directory_readme(self, dir_path: Path, dir_name: str, config: Dict):
        """Create README.md for each directory"""
        readme_path = dir_path / "README.md"
        
        if readme_path.exists():
            return  # Don't overwrite existing README
        
        readme_content = f"""# {dir_name.title()} Directory

## Purpose
{config['description']}

## Structure
"""
        
        if config["subdirs"]:
            for subdir, description in config["subdirs"].items():
                readme_content += f"- **{subdir}/**: {description}\n"
        else:
            readme_content += "This directory contains files directly related to its purpose.\n"
        
        readme_content += f"""
## Usage
This directory is part of the JAEGIS ecosystem restructuring. Files in this directory should follow the established patterns and conventions.

## Contributing
When adding files to this directory:
1. Follow the naming conventions
2. Update this README if adding new subdirectories
3. Ensure proper documentation
4. Run validation tests

## Related Documentation
- [Main README](../README.md)
- [Architecture Documentation](../docs/architecture/)
- [Contributing Guidelines](../CONTRIBUTING.md)
"""
        
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        
        print(f"    📄 Created: {dir_name}/README.md")
    
    def _create_special_files(self):
        """Create special configuration files"""
        
        # Create .gitkeep for logs directory (since it should be empty)
        logs_gitkeep = self.repo_path / "logs" / ".gitkeep"
        logs_gitkeep.touch()
        
        # Create enhanced .gitignore
        self._update_gitignore()
        
        # Create directory structure documentation
        self._create_structure_documentation()
    
    def _update_gitignore(self):
        """Update .gitignore with new patterns"""
        gitignore_path = self.repo_path / ".gitignore"
        
        new_patterns = [
            "",
            "# JAEGIS Restructuring - Additional Patterns",
            "logs/",
            "security_violations.log",
            "*.tmp",
            "*.temp",
            ".cache/",
            "__pycache__/",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            ".Python",
            "build/",
            "develop-eggs/",
            "dist/",
            "downloads/",
            "eggs/",
            ".eggs/",
            "lib/",
            "lib64/",
            "parts/",
            "sdist/",
            "var/",
            "wheels/",
            "",
            "# IDE files",
            ".vscode/settings.json",
            ".idea/",
            "*.swp",
            "*.swo",
            "",
            "# OS files",
            ".DS_Store",
            "Thumbs.db",
            "",
            "# Environment files",
            ".env",
            ".env.*",
            "",
            "# Test coverage",
            ".coverage",
            "htmlcov/",
            "",
            "# Backup files",
            "*.backup",
            "*.bak",
            ""
        ]
        
        # Read existing .gitignore
        existing_content = ""
        if gitignore_path.exists():
            with open(gitignore_path, 'r') as f:
                existing_content = f.read()
        
        # Add new patterns if not already present
        with open(gitignore_path, 'a') as f:
            for pattern in new_patterns:
                if pattern and pattern not in existing_content:
                    f.write(pattern + "\n")
        
        print("    📄 Updated: .gitignore")
    
    def _create_structure_documentation(self):
        """Create documentation for the new structure"""
        structure_doc_path = self.repo_path / "docs" / "DIRECTORY_STRUCTURE.md"
        
        # Ensure docs directory exists
        structure_doc_path.parent.mkdir(parents=True, exist_ok=True)
        
        doc_content = """# JAEGIS Repository Directory Structure

This document describes the reorganized directory structure of the JAEGIS repository.

## Overview

The repository has been restructured to improve organization, maintainability, and developer experience. Each directory has a specific purpose and follows established conventions.

## Directory Structure

```
JAEGIS/
├── core/                    # Core JAEGIS system components
│   ├── agents/             # Agent implementations and configurations
│   ├── orchestration/      # Core orchestration systems
│   ├── nlds/              # N.L.D.S. Tier 0 system
│   └── brain_protocol/    # Brain Protocol Suite components
├── frameworks/             # Specialized frameworks and engines
│   ├── pitces/            # P.I.T.C.E.S. framework implementation
│   ├── cognitive_pipeline/ # Cognitive processing pipeline
│   └── project_chimera/   # Advanced AI security architecture
├── integrations/          # External system integrations
│   ├── github/            # GitHub integration and upload systems
│   ├── openrouter/        # OpenRouter.ai integration
│   ├── vscode/            # VS Code extension and IDE integration
│   └── cli/               # Command-line interfaces
├── security/              # Security systems and scanning
│   ├── patterns/          # Security pattern definitions
│   ├── policies/          # Security policies and configurations
│   └── audit/             # Audit logging and compliance
├── config/                # Configuration management
│   ├── system/            # System-wide configurations
│   ├── agents/            # Agent-specific configurations
│   ├── commands/          # Command definitions and mappings
│   └── templates/         # Configuration templates
├── deployment/            # Deployment configurations and scripts
│   ├── kubernetes/        # Kubernetes manifests
│   ├── monitoring/        # Monitoring and observability
│   ├── backup/            # Backup configurations
│   └── security/          # Security hardening configurations
├── scripts/               # Utility and automation scripts
│   ├── services/          # Background services and daemons
│   ├── monitoring/        # System monitoring scripts
│   ├── validation/        # Validation and verification scripts
│   └── utilities/         # General utility scripts
├── tests/                 # Testing framework and test suites
│   ├── unit/              # Unit tests for individual components
│   ├── integration/       # Integration tests for system interactions
│   ├── security/          # Security and vulnerability tests
│   ├── performance/       # Performance and load tests
│   ├── acceptance/        # User acceptance tests
│   └── validation/        # System validation tests
├── docs/                  # Documentation and guides
│   ├── api/               # API documentation and references
│   ├── architecture/      # System architecture documentation
│   ├── tutorials/         # User tutorials and guides
│   ├── security/          # Security documentation
│   ├── diagrams/          # Architecture diagrams and visuals
│   └── user-guide/        # End-user documentation
├── examples/              # Usage examples and demonstrations
│   ├── basic/             # Basic usage examples
│   ├── advanced/          # Advanced configuration examples
│   └── integrations/      # Integration examples
└── logs/                  # Log files (gitignored)
```

## Migration Benefits

### 1. Improved Organization
- **Logical grouping** of related components
- **Clear separation** between core, frameworks, and integrations
- **Standardized structure** for easy navigation

### 2. Enhanced Security
- **Centralized security** in dedicated `/security/` directory
- **Security scanning** integrated into CI/CD pipeline
- **Audit trails** and compliance monitoring

### 3. Better Maintainability
- **Modular architecture** with clear boundaries
- **Configuration management** in dedicated directories
- **Testing framework** with comprehensive coverage

### 4. Scalability
- **Framework-based organization** for easy extension
- **Plugin architecture** for new integrations
- **Deployment-ready** structure with Docker/K8s support

### 5. Developer Experience
- **Clear entry points** for different use cases
- **Comprehensive documentation** structure
- **Examples and tutorials** for quick onboarding

## File Naming Conventions

- **Python files**: `snake_case.py`
- **Configuration files**: `kebab-case.json/yaml`
- **Documentation**: `UPPER_CASE.md` for important docs, `Title_Case.md` for guides
- **Scripts**: `kebab-case.py/sh`
- **Directories**: `lowercase` with underscores for multi-word names

## Contributing

When adding new files or directories:

1. **Choose the appropriate directory** based on the file's purpose
2. **Follow naming conventions** established for that directory
3. **Update relevant README files** if adding new subdirectories
4. **Add appropriate documentation** for new components
5. **Include tests** for new functionality
6. **Update this document** if adding new top-level directories

## Related Documentation

- [Main README](../README.md)
- [Contributing Guidelines](../CONTRIBUTING.md)
- [Architecture Documentation](architecture/)
- [Security Documentation](security/)
"""
        
        with open(structure_doc_path, 'w') as f:
            f.write(doc_content)
        
        print("    📄 Created: docs/DIRECTORY_STRUCTURE.md")

def main():
    """Main execution"""
    creator = DirectoryStructureCreator()
    
    # Create directory structure
    created_dirs = creator.create_structure()
    
    print(f"🎉 Directory structure creation complete! Created {len(created_dirs)} directories.")

if __name__ == "__main__":
    main()
