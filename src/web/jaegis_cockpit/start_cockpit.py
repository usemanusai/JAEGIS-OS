#!/usr/bin/env python3
"""
JAEGIS Cockpit Startup Script

This script starts both the backend API server and provides instructions
for starting the frontend development server.
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path

def print_banner():
    """Print the JAEGIS Cockpit banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                   JAEGIS COCKPIT - REAL                     ║
    ║                                                              ║
    ║         Live Operational Dashboard for JAEGIS               ║
    ║    A.C.I.D. Swarms • Agents • N.L.D.S. • Chat System      ║
    ║                                                              ║
    ║                        Version 2.0.0                        ║
    ║                   REAL SYSTEM INTEGRATION                   ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies and JAEGIS system connections...")

    # Check Python dependencies
    try:
        import fastapi
        import uvicorn
        import websockets
        import psutil
        print("✅ Python dependencies found")
    except ImportError as e:
        print(f"❌ Missing Python dependency: {e}")
        print("💡 Run: pip install -r backend/requirements.txt")
        return False

    # Check JAEGIS system availability
    print("🔍 Checking JAEGIS system connections...")

    # Check for A.C.I.D. Swarm Orchestrator
    try:
        jaegis_root = Path(__file__).parent.parent.parent.parent
        acid_path = jaegis_root / "src" / "core" / "core" / "acid" / "swarm_orchestrator.py"
        if acid_path.exists():
            print("✅ A.C.I.D. Swarm Orchestrator found")
        else:
            print("⚠️  A.C.I.D. Swarm Orchestrator not found at expected path")
    except Exception as e:
        print(f"⚠️  Could not check A.C.I.D. Swarm Orchestrator: {e}")

    # Check for Agent System
    try:
        agent_path = jaegis_root / "src" / "core" / "core" / "agents" / "base_agent.py"
        if agent_path.exists():
            print("✅ JAEGIS Agent System found")
        else:
            print("⚠️  JAEGIS Agent System not found at expected path")
    except Exception as e:
        print(f"⚠️  Could not check Agent System: {e}")

    # Check for N.L.D.S.
    try:
        nlds_path = jaegis_root / "src" / "core" / "nlds" / "nlp" / "language_detector.py"
        if nlds_path.exists():
            print("✅ N.L.D.S. Language Detection found")
        else:
            print("⚠️  N.L.D.S. not found at expected path")
    except Exception as e:
        print(f"⚠️  Could not check N.L.D.S.: {e}")

    # Check for Enhanced Chat System
    try:
        chat_path = jaegis_root / "src" / "cli" / "enhanced_chat_interface.py"
        if chat_path.exists():
            print("✅ Enhanced Chat System found")
        else:
            print("⚠️  Enhanced Chat System not found at expected path")
    except Exception as e:
        print(f"⚠️  Could not check Enhanced Chat System: {e}")

    # Check if Node.js is available for frontend
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js found: {result.stdout.strip()}")
        else:
            print("❌ Node.js not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found")
        print("💡 Install Node.js from https://nodejs.org/")
        return False

    print("✅ Dependency check complete - JAEGIS Cockpit ready for real system integration!")
    return True

def start_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting JAEGIS Cockpit Backend...")
    
    backend_dir = Path(__file__).parent / "backend"
    
    # Add the JAEGIS root to Python path
    jaegis_root = Path(__file__).parent.parent
    env = os.environ.copy()
    env['PYTHONPATH'] = str(jaegis_root) + os.pathsep + env.get('PYTHONPATH', '')
    
    try:
        # Start uvicorn server
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8090", 
            "--reload"
        ], cwd=backend_dir, env=env)
        
        print("✅ Backend server starting on http://localhost:8090")
        print("📚 API Documentation: http://localhost:8090/docs")
        
        return process
        
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def print_frontend_instructions():
    """Print instructions for starting the frontend"""
    print("\n" + "="*60)
    print("🎨 FRONTEND SETUP INSTRUCTIONS")
    print("="*60)
    print()
    print("To start the frontend development server:")
    print()
    print("1. Open a new terminal window")
    print("2. Navigate to the frontend directory:")
    print("   cd jaegis_cockpit/frontend")
    print()
    print("3. Install dependencies (first time only):")
    print("   npm install")
    print()
    print("4. Start the development server:")
    print("   npm run dev")
    print()
    print("5. Open your browser to:")
    print("   http://localhost:5173")
    print()
    print("="*60)

def main():
    """Main startup function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependency check failed. Please install missing dependencies.")
        sys.exit(1)
    
    print("\n🎯 Starting JAEGIS Cockpit services...")
    
    # Start backend
    backend_process = start_backend()
    
    if not backend_process:
        print("❌ Failed to start backend server")
        sys.exit(1)
    
    # Wait a moment for backend to start
    time.sleep(2)
    
    # Print frontend instructions
    print_frontend_instructions()
    
    # Setup signal handlers for graceful shutdown
    def signal_handler(signum, frame):
        print("\n🛑 Shutting down JAEGIS Cockpit...")
        if backend_process:
            backend_process.terminate()
            backend_process.wait()
        print("✅ Shutdown complete")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("\n🎮 JAEGIS Cockpit - Real Operational Dashboard is running!")
    print("📊 Live Dashboard: http://localhost:5173 (after starting frontend)")
    print("🔗 Real System Integrations:")
    print("   • A.C.I.D. Swarm Orchestrator: Live swarm monitoring")
    print("   • Agent System: Real agent status and coordination")
    print("   • N.L.D.S.: Live language processing statistics")
    print("   • Enhanced Chat: Real chat session monitoring")
    print("🔄 Press Ctrl+C to stop the backend server")
    
    try:
        # Keep the main thread alive
        backend_process.wait()
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    main()
