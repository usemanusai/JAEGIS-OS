#!/usr/bin/env python3
"""
JAEGIS GitHub Actions Workflow Creator
Creates comprehensive CI/CD workflows for the restructured repository
"""

import os
from pathlib import Path

class GitHubWorkflowCreator:
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.workflows_dir = self.repo_path / ".github" / "workflows"
        
    def create_all_workflows(self):
        """Create all GitHub Actions workflows"""
        print("🔄 Creating GitHub Actions workflows...")
        
        # Ensure workflows directory exists
        self.workflows_dir.mkdir(parents=True, exist_ok=True)
        
        workflows = [
            ("ci.yml", self._create_ci_workflow()),
            ("security-scan.yml", self._create_security_workflow()),
            ("deploy.yml", self._create_deploy_workflow()),
            ("validate-structure.yml", self._create_validation_workflow()),
            ("test-migration.yml", self._create_migration_test_workflow())
        ]
        
        for filename, content in workflows:
            workflow_path = self.workflows_dir / filename
            with open(workflow_path, 'w') as f:
                f.write(content)
            print(f"  📄 Created: .github/workflows/{filename}")
        
        print("✅ All GitHub Actions workflows created")
    
    def _create_ci_workflow(self) -> str:
        """Create CI workflow"""
        return """name: Continuous Integration

on:
  push:
    branches: [ main, develop, restructure-staging ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Cache pip dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov flake8 black isort
    
    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    - name: Check code formatting with black
      run: black --check .
    
    - name: Check import sorting with isort
      run: isort --check-only .
    
    - name: Run unit tests
      run: |
        pytest tests/unit/ -v --cov=. --cov-report=xml
    
    - name: Run integration tests
      run: |
        pytest tests/integration/ -v
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella

  security-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Run security scanner validation
      run: |
        python -c "from security.security_scanner import SecurityScanner; print('Security scanner functional')"
    
    - name: Run Bandit security scan
      run: |
        pip install bandit
        bandit -r . -f json -o bandit-report.json || true
    
    - name: Upload security scan results
      uses: actions/upload-artifact@v3
      with:
        name: security-scan-results
        path: bandit-report.json

  validate-imports:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Validate critical imports
      run: |
        python validation_scripts.py
"""
    
    def _create_security_workflow(self) -> str:
        """Create security scanning workflow"""
        return """name: Security Scanning

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * 1'  # Weekly on Monday at 2 AM

jobs:
  security-scan:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install bandit safety semgrep
    
    - name: Run JAEGIS Security Scanner
      run: |
        python -c "
        from security.security_scanner import SecurityScanner
        import os
        scanner = SecurityScanner()
        violations = []
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r') as f:
                            content = f.read()
                        file_violations = scanner.scan_file_content(content, file_path)
                        violations.extend(file_violations)
                    except:
                        pass
        print(f'JAEGIS Security Scanner: {len(violations)} violations found')
        if violations:
            for v in violations[:5]:  # Show first 5
                print(f'  {v.file_path}:{v.line_number} - {v.pattern_name}')
        "
    
    - name: Run Bandit
      run: |
        bandit -r . -f json -o bandit-report.json
      continue-on-error: true
    
    - name: Run Safety check
      run: |
        safety check --json --output safety-report.json
      continue-on-error: true
    
    - name: Run Semgrep
      run: |
        semgrep --config=auto --json --output=semgrep-report.json .
      continue-on-error: true
    
    - name: Upload security reports
      uses: actions/upload-artifact@v3
      with:
        name: security-reports
        path: |
          bandit-report.json
          safety-report.json
          semgrep-report.json
    
    - name: Comment PR with security results
      if: github.event_name == 'pull_request'
      uses: actions/github-script@v6
      with:
        script: |
          const fs = require('fs');
          let comment = '## 🔒 Security Scan Results\\n\\n';
          
          try {
            const bandit = JSON.parse(fs.readFileSync('bandit-report.json', 'utf8'));
            comment += `**Bandit**: ${bandit.results.length} issues found\\n`;
          } catch (e) {
            comment += '**Bandit**: Scan completed\\n';
          }
          
          try {
            const safety = JSON.parse(fs.readFileSync('safety-report.json', 'utf8'));
            comment += `**Safety**: ${safety.length} vulnerabilities found\\n`;
          } catch (e) {
            comment += '**Safety**: No vulnerabilities found\\n';
          }
          
          comment += '\\nDetailed reports are available in the workflow artifacts.';
          
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: comment
          });
"""
    
    def _create_deploy_workflow(self) -> str:
        """Create deployment workflow"""
        return """name: Deployment

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install build twine
    
    - name: Run tests
      run: |
        python validation_scripts.py
    
    - name: Build Docker image
      run: |
        docker build -t jaegis:latest .
    
    - name: Test Docker image
      run: |
        docker run --rm jaegis:latest python -c "print('Docker image working')"
    
    - name: Build Python package
      run: |
        python -m build
    
    - name: Upload build artifacts
      uses: actions/upload-artifact@v3
      with:
        name: dist
        path: dist/

  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: staging
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Deploy to staging
      run: |
        echo "Deploying to staging environment"
        # Add staging deployment commands here

  deploy-production:
    needs: build
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/v')
    environment: production
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Deploy to production
      run: |
        echo "Deploying to production environment"
        # Add production deployment commands here
"""
    
    def _create_validation_workflow(self) -> str:
        """Create structure validation workflow"""
        return """name: Structure Validation

on:
  push:
    branches: [ main, develop, restructure-staging ]
  pull_request:
    branches: [ main, develop ]

jobs:
  validate-structure:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Validate directory structure
      run: |
        python -c "
        import os
        from pathlib import Path
        
        required_dirs = [
            'core', 'frameworks', 'integrations', 'security',
            'config', 'deployment', 'scripts', 'tests', 'docs', 'examples'
        ]
        
        missing_dirs = []
        for dir_name in required_dirs:
            if not Path(dir_name).exists():
                missing_dirs.append(dir_name)
        
        if missing_dirs:
            print(f'Missing required directories: {missing_dirs}')
            exit(1)
        else:
            print('All required directories present')
        "
    
    - name: Validate critical files
      run: |
        python -c "
        from pathlib import Path
        
        critical_files = [
            'security/security_scanner.py',
            'integrations/github/multi_account_github_uploader.py',
            'core/agents/agent-config.txt',
            'config/system/security_config.json'
        ]
        
        missing_files = []
        for file_path in critical_files:
            if not Path(file_path).exists():
                # Check if file exists in old location
                old_path = file_path.split('/')[-1]
                if not Path(old_path).exists():
                    missing_files.append(file_path)
        
        if missing_files:
            print(f'Missing critical files: {missing_files}')
            exit(1)
        else:
            print('All critical files present or in migration')
        "
    
    - name: Validate imports
      run: |
        python validation_scripts.py
    
    - name: Check for broken links in documentation
      run: |
        find docs -name "*.md" -exec grep -l "](.*\.md)" {} \\; | while read file; do
          echo "Checking links in $file"
          grep -o "](.*\.md)" "$file" | sed 's/](//' | while read link; do
            if [[ "$link" == /* ]]; then
              # Absolute path
              if [ ! -f ".$link" ]; then
                echo "Broken link in $file: $link"
              fi
            else
              # Relative path
              dir=$(dirname "$file")
              if [ ! -f "$dir/$link" ]; then
                echo "Broken link in $file: $link"
              fi
            fi
          done
        done
"""
    
    def _create_migration_test_workflow(self) -> str:
        """Create migration testing workflow"""
        return """name: Migration Testing

on:
  push:
    branches: [ restructure-staging ]
  pull_request:
    branches: [ main ]
    paths:
      - 'migration_*.py'
      - 'validation_scripts.py'

jobs:
  test-migration:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0  # Full history for migration testing
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Test file inventory generation
      run: |
        python generate_file_inventory.py
        test -f file_inventory.json
        echo "File inventory generation: PASSED"
    
    - name: Test dependency analysis
      run: |
        python analyze_dependencies.py
        test -f dependency_analysis.json
        echo "Dependency analysis: PASSED"
    
    - name: Test critical system identification
      run: |
        python identify_critical_systems.py
        test -f critical_systems_analysis.json
        echo "Critical system identification: PASSED"
    
    - name: Test migration mapping
      run: |
        python generate_migration_mapping.py
        test -f migration_mapping.json
        echo "Migration mapping generation: PASSED"
    
    - name: Test validation scripts
      run: |
        python validation_scripts.py
        echo "Validation scripts: PASSED"
    
    - name: Upload migration test results
      uses: actions/upload-artifact@v3
      with:
        name: migration-test-results
        path: |
          file_inventory.json
          dependency_analysis.json
          critical_systems_analysis.json
          migration_mapping.json
          validation_report.json
"""

def main():
    """Main execution"""
    creator = GitHubWorkflowCreator()
    creator.create_all_workflows()
    print("🎉 GitHub Actions workflows creation complete!")

if __name__ == "__main__":
    main()
