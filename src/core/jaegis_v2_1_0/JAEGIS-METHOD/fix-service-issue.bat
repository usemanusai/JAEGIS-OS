@echo off
REM Quick fix for eJAEGIS service startup issues
cd /d "%~dp0"

echo 🔧 eJAEGIS Service Quick Fix
echo ========================
echo Current Directory: %CD%
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ This script must be run as Administrator
    echo Please right-click and select "Run as administrator"
    pause
    exit /b 1
)

echo ✅ Running as Administrator

REM Stop any existing service
echo 🛑 Stopping existing service (if running)...
python eJAEGIS-service-manager.py stop

REM Remove existing service
echo 🗑️ Removing existing service (if installed)...
python eJAEGIS-service-manager.py remove

echo.
echo 🔧 Installing service with improved configuration...

REM Install service with better error handling
python eJAEGIS-service-manager.py install

if %errorlevel% neq 0 (
    echo.
    echo ❌ Service installation failed. Let's try alternative approach...
    echo.
    echo 🔍 Running diagnostics...
    python troubleshoot-eJAEGIS.py
    pause
    exit /b 1
)

echo.
echo 🚀 Starting service...
python eJAEGIS-service-manager.py start

echo.
echo 📊 Final service status:
python eJAEGIS-service-manager.py status

echo.
echo 📋 Recent logs:
python eJAEGIS-service-manager.py logs

echo.
echo 🎉 Service fix completed!
echo.
echo If the service is still not working:
echo 1. Check the logs above for errors
echo 2. Try running: python eJAEGIS-auto-sync.py --test
echo 3. Run: python troubleshoot-eJAEGIS.py
echo.
pause
