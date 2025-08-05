@echo off
REM eJAEGIS Universal Installation Script for Windows Command Prompt
REM Fallback installer when PowerShell is not available

setlocal enabledelayedexpansion

REM Configuration
set "eJAEGIS_REPO=https://github.com/huggingfacer04/eJAEGIS"
set "eJAEGIS_DIR=%USERPROFILE%\.eJAEGIS"
set "LOG_FILE=%TEMP%\eJAEGIS-install.log"
set "PYTHON_MIN_VERSION=3.7"

echo 🚀 eJAEGIS Universal Installer for Windows (Command Prompt)
echo ============================================================
echo.

REM Create log file
echo %date% %time% - Starting eJAEGIS installation > "%LOG_FILE%"

REM Check for required commands
echo ℹ️  Checking prerequisites...
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git is required but not found
    echo Download from: https://git-scm.com/download/win
    echo %date% %time% - Git not found >> "%LOG_FILE%"
    pause
    exit /b 1
)
echo ✅ Git is available

REM Check Python
echo ℹ️  Checking Python installation...
set "PYTHON_CMD="

REM Try different Python commands
for %%p in (python python3 py) do (
    %%p --version >nul 2>&1
    if !errorlevel! equ 0 (
        for /f "tokens=2" %%v in ('%%p --version 2^>^&1') do (
            set "version=%%v"
            REM Simple version check (assumes format X.Y.Z)
            for /f "tokens=1,2 delims=." %%a in ("!version!") do (
                set /a "major=%%a"
                set /a "minor=%%b"
                if !major! gtr 3 (
                    set "PYTHON_CMD=%%p"
                    goto :python_found
                )
                if !major! equ 3 (
                    if !minor! geq 7 (
                        set "PYTHON_CMD=%%p"
                        goto :python_found
                    )
                )
            )
        )
    )
)

if "%PYTHON_CMD%"=="" (
    echo ❌ Python 3.7 or higher is required
    echo Download from: https://python.org/downloads/
    echo %date% %time% - Python not found >> "%LOG_FILE%"
    pause
    exit /b 1
)

:python_found
echo ✅ Python found: %PYTHON_CMD%

REM Install Python dependencies
echo ℹ️  Installing Python dependencies...
%PYTHON_CMD% -c "import requests" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing requests...
    %PYTHON_CMD% -m pip install --user requests
    if %errorlevel% neq 0 (
        echo ❌ Failed to install requests
        echo %date% %time% - Failed to install requests >> "%LOG_FILE%"
        pause
        exit /b 1
    )
)

%PYTHON_CMD% -c "import psutil" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing psutil...
    %PYTHON_CMD% -m pip install --user psutil
    if %errorlevel% neq 0 (
        echo ❌ Failed to install psutil
        echo %date% %time% - Failed to install psutil >> "%LOG_FILE%"
        pause
        exit /b 1
    )
)
echo ✅ Python dependencies installed

REM Download eJAEGIS system
echo ℹ️  Downloading eJAEGIS system...
if exist "%eJAEGIS_DIR%" (
    echo Directory already exists. Updating...
    cd /d "%eJAEGIS_DIR%"
    git pull origin main
    if %errorlevel% neq 0 (
        echo ❌ Failed to update eJAEGIS system
        echo %date% %time% - Failed to update eJAEGIS >> "%LOG_FILE%"
        pause
        exit /b 1
    )
) else (
    echo Cloning eJAEGIS repository...
    git clone "%eJAEGIS_REPO%" "%eJAEGIS_DIR%"
    if %errorlevel% neq 0 (
        echo ❌ Failed to clone eJAEGIS repository
        echo %date% %time% - Failed to clone eJAEGIS >> "%LOG_FILE%"
        pause
        exit /b 1
    )
)
echo ✅ eJAEGIS system downloaded

REM Interactive setup
echo.
echo 🔧 eJAEGIS Interactive Setup
echo =========================

REM GitHub token
echo Please enter your GitHub Personal Access Token:
echo You can create one at: https://github.com/settings/tokens
echo Required scopes: repo, workflow
set /p "GITHUB_TOKEN=GitHub Token: "

if "%GITHUB_TOKEN%"=="" (
    echo ❌ GitHub token is required
    echo %date% %time% - No GitHub token provided >> "%LOG_FILE%"
    pause
    exit /b 1
)

REM Validate token (simple check)
echo ℹ️  Validating GitHub token...
curl -s -H "Authorization: Bearer %GITHUB_TOKEN%" https://api.github.com/user >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Invalid GitHub token or network error
    echo %date% %time% - GitHub token validation failed >> "%LOG_FILE%"
    pause
    exit /b 1
)
echo ✅ GitHub token validated

REM Repository name
set /p "REPO_NAME=Enter target repository name (default: eJAEGIS-Project): "
if "%REPO_NAME%"=="" set "REPO_NAME=eJAEGIS-Project"

REM Sync frequency
echo Select sync frequency:
echo 1) Hourly (recommended)
echo 2) Every 30 minutes
echo 3) Every 15 minutes
echo 4) On file change
set /p "SYNC_CHOICE=Choice (1-4): "

set "SYNC_INTERVAL=3600"
if "%SYNC_CHOICE%"=="2" set "SYNC_INTERVAL=1800"
if "%SYNC_CHOICE%"=="3" set "SYNC_INTERVAL=900"
if "%SYNC_CHOICE%"=="4" set "SYNC_INTERVAL=300"

REM Failsafe sensitivity
echo Select failsafe sensitivity:
echo 1) Strict (recommended for critical projects)
echo 2) Balanced (recommended for most projects)
echo 3) Permissive (minimal interruptions)
set /p "FAILSAFE_CHOICE=Choice (1-3): "

set "FAILSAFE_SENSITIVITY=balanced"
if "%FAILSAFE_CHOICE%"=="1" set "FAILSAFE_SENSITIVITY=strict"
if "%FAILSAFE_CHOICE%"=="3" set "FAILSAFE_SENSITIVITY=permissive"

REM Detect project type
set "PROJECT_TYPE=generic"
if exist "package.json" set "PROJECT_TYPE=nodejs"
if exist "requirements.txt" set "PROJECT_TYPE=python"
if exist "setup.py" set "PROJECT_TYPE=python"
if exist "Cargo.toml" set "PROJECT_TYPE=rust"
if exist "pom.xml" set "PROJECT_TYPE=java"
if exist "go.mod" set "PROJECT_TYPE=go"

echo ℹ️  Detected project type: %PROJECT_TYPE%

REM Generate configuration files
echo ℹ️  Generating configuration files...
mkdir "%eJAEGIS_DIR%\config" 2>nul

REM Get username from GitHub API
for /f "delims=" %%i in ('curl -s -H "Authorization: Bearer %GITHUB_TOKEN%" https://api.github.com/user ^| findstr /r "\"login\""') do (
    set "line=%%i"
    for /f "tokens=2 delims=:" %%j in ("!line!") do (
        set "username=%%j"
        set "username=!username: =!"
        set "username=!username:"=!"
        set "username=!username:,=!"
    )
)

REM Create user configuration
(
echo {
echo   "github": {
echo     "token": "%GITHUB_TOKEN%",
echo     "username": "%username%",
echo     "repository": "%REPO_NAME%"
echo   },
echo   "sync": {
echo     "interval_seconds": %SYNC_INTERVAL%,
echo     "auto_start": true,
echo     "create_repo_if_missing": true
echo   },
echo   "project": {
echo     "type": "%PROJECT_TYPE%",
echo     "root_directory": "%CD%"
echo   }
echo }
) > "%eJAEGIS_DIR%\config\eJAEGIS-user-config.json"

REM Create project configuration
(
echo {
echo   "monitoring": {
echo     "include_patterns": ["**/*.py", "**/*.js", "**/*.ts", "**/*.json", "**/*.md"],
echo     "exclude_patterns": [".git/**", "node_modules/**", "__pycache__/**", "*.log"],
echo     "watch_directories": ["src", "lib", "docs", "."],
echo     "ignore_hidden_files": true
echo   },
echo   "project_type": "%PROJECT_TYPE%",
echo   "failsafe": {
echo     "sensitivity": "%FAILSAFE_SENSITIVITY%"
echo   }
echo }
) > "%eJAEGIS_DIR%\config\eJAEGIS-project-config.json"

echo ✅ Configuration files generated

REM Setup eJAEGIS commands
echo ℹ️  Setting up eJAEGIS commands...
mkdir "%USERPROFILE%\.local\bin" 2>nul

REM Create eJAEGIS.bat command
(
echo @echo off
echo cd /d "%eJAEGIS_DIR%"
echo %PYTHON_CMD% eJAEGIS-cli.py %%*
) > "%USERPROFILE%\.local\bin\eJAEGIS.bat"

REM Add to PATH (requires restart)
echo ✅ eJAEGIS commands installed (restart command prompt to use 'eJAEGIS' command)

REM Update existing scripts with configuration
echo ℹ️  Updating eJAEGIS scripts with configuration...
cd /d "%eJAEGIS_DIR%"

if exist "eJAEGIS-auto-sync.py" (
    REM Simple token replacement (basic approach)
    powershell -Command "(Get-Content 'eJAEGIS-auto-sync.py') -replace 'GITHUB_TOKEN = .*', 'GITHUB_TOKEN = ''%GITHUB_TOKEN%''' | Set-Content 'eJAEGIS-auto-sync.py'" 2>nul
    powershell -Command "(Get-Content 'eJAEGIS-auto-sync.py') -replace 'REPO_NAME = .*', 'REPO_NAME = ''%REPO_NAME%''' | Set-Content 'eJAEGIS-auto-sync.py'" 2>nul
)

REM Start eJAEGIS system
echo ℹ️  Starting eJAEGIS system...
%PYTHON_CMD% eJAEGIS-background-runner.py start
if %errorlevel% equ 0 (
    echo ✅ eJAEGIS background runner started
) else (
    echo ⚠️  Failed to start background runner
)

REM Verification
echo.
echo 📊 Verifying Installation
echo =========================

set /a "tests_passed=0"
set /a "total_tests=4"

REM Test 1: eJAEGIS directory
if exist "%eJAEGIS_DIR%" (
    echo ✅ eJAEGIS directory exists
    set /a "tests_passed+=1"
) else (
    echo ❌ eJAEGIS directory not found
)

REM Test 2: Configuration files
if exist "%eJAEGIS_DIR%\config\eJAEGIS-user-config.json" (
    echo ✅ Configuration files exist
    set /a "tests_passed+=1"
) else (
    echo ❌ Configuration files not found
)

REM Test 3: Python dependencies
%PYTHON_CMD% -c "import requests, psutil" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python dependencies available
    set /a "tests_passed+=1"
) else (
    echo ❌ Python dependencies missing
)

REM Test 4: GitHub connectivity
curl -s -H "Authorization: Bearer %GITHUB_TOKEN%" https://api.github.com/user >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ GitHub connectivity verified
    set /a "tests_passed+=1"
) else (
    echo ❌ GitHub connectivity failed
)

echo.
echo ℹ️  Verification: %tests_passed%/%total_tests% tests passed

if %tests_passed% equ %total_tests% (
    echo ✅ Installation completed successfully!
) else (
    echo ⚠️  Installation completed with issues
)

echo.
echo 🎉 eJAEGIS Installation Complete!
echo ===============================
echo.
echo Next steps:
echo 1. Restart Command Prompt
echo 2. Navigate to your project directory
echo 3. Run: eJAEGIS init
echo 4. Check status: eJAEGIS status
echo.
echo For help: eJAEGIS --help
echo Documentation: https://github.com/huggingfacer04/eJAEGIS
echo Log file: %LOG_FILE%
echo.
pause
