import asyncio
import json
import psutil
import sys
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Add JAEGIS core paths to Python path
JAEGIS_ROOT = Path(__file__).parent.parent.parent.parent
JAEGIS_CORE_PATH = JAEGIS_ROOT / "src" / "core"
JAEGIS_CLI_PATH = JAEGIS_ROOT / "src" / "cli"

sys.path.insert(0, str(JAEGIS_ROOT))
sys.path.insert(0, str(JAEGIS_CORE_PATH))
sys.path.insert(0, str(JAEGIS_CLI_PATH))

# Import real JAEGIS services
from services.real_jaegis_service import RealJAEGISService
from services.real_agent_service import RealAgentService
from services.real_nlds_service import RealNLDSService
from services.real_chat_service import RealChatService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- FastAPI App Initialization ---
app = FastAPI(
    title="JAEGIS Cockpit - Real Operational Dashboard",
    description="Live operational dashboard for the JAEGIS ecosystem",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize real JAEGIS services
try:
    jaegis_service = RealJAEGISService()
    agent_service = RealAgentService()
    nlds_service = RealNLDSService()
    chat_service = RealChatService()
    logger.info("✅ All real JAEGIS services initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize JAEGIS services: {e}")
    jaegis_service = None
    agent_service = None
    nlds_service = None
    chat_service = None

# --- WebSocket for Real-time JAEGIS System Status ---
@app.websocket("/ws/system-status")
async def system_status_ws(websocket: WebSocket):
    """
    WebSocket endpoint to stream real-time JAEGIS system status.
    Connects to actual JAEGIS systems for live data.
    """
    await websocket.accept()
    logger.info("Client connected to JAEGIS system status WebSocket")

    try:
        while True:
            # Gather real system metrics
            cpu_percent = psutil.cpu_percent()
            memory_info = psutil.virtual_memory()

            # Get real JAEGIS system status
            system_status = {}
            if jaegis_service:
                system_status = await jaegis_service.get_system_status()

            # Get real agent activity
            agent_activity = {}
            if agent_service:
                agent_activity = await agent_service.get_live_activity()

            # Get real NLDS processing data
            nlds_activity = {}
            if nlds_service:
                nlds_activity = await nlds_service.get_processing_stats()

            # Get real chat system status
            chat_status = {}
            if chat_service:
                chat_status = await chat_service.get_session_status()

            # Prepare real data payload
            payload = {
                "timestamp": datetime.utcnow().isoformat(),
                "system_metrics": {
                    "cpu_usage": cpu_percent,
                    "memory_usage": memory_info.percent,
                    "disk_usage": psutil.disk_usage('/').percent if hasattr(psutil, 'disk_usage') else 0
                },
                "jaegis_status": system_status,
                "agent_activity": agent_activity,
                "nlds_activity": nlds_activity,
                "chat_status": chat_status,
                "services_online": {
                    "jaegis_core": jaegis_service is not None,
                    "agent_system": agent_service is not None,
                    "nlds_system": nlds_service is not None,
                    "chat_system": chat_service is not None
                }
            }

            # Send real data to the client
            await websocket.send_text(json.dumps(payload, default=str))

            # Wait for 2 seconds before sending the next update
            await asyncio.sleep(2)

    except WebSocketDisconnect:
        logger.info("Client disconnected from JAEGIS system status WebSocket")
    except Exception as e:
        logger.error(f"Error in JAEGIS system status WebSocket: {e}")
        await websocket.close(code=1011, reason="Server error")

# --- Real JAEGIS A.C.I.D. Swarm Orchestrator API ---
@app.get("/api/acid/swarms")
async def get_active_swarms():
    """Get all active A.C.I.D. swarms and their status"""
    if not jaegis_service:
        raise HTTPException(status_code=503, detail="JAEGIS service not available")

    try:
        swarms = await jaegis_service.get_active_swarms()
        return {"swarms": swarms, "count": len(swarms)}
    except Exception as e:
        logger.error(f"Error getting active swarms: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/acid/swarms/{swarm_id}")
async def get_swarm_details(swarm_id: str):
    """Get detailed information about a specific swarm"""
    if not jaegis_service:
        raise HTTPException(status_code=503, detail="JAEGIS service not available")

    try:
        swarm = await jaegis_service.get_swarm_details(swarm_id)
        if not swarm:
            raise HTTPException(status_code=404, detail="Swarm not found")
        return swarm
    except Exception as e:
        logger.error(f"Error getting swarm details: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/acid/tasks")
async def get_task_queue():
    """Get current A.C.I.D. task queue"""
    if not jaegis_service:
        raise HTTPException(status_code=503, detail="JAEGIS service not available")

    try:
        tasks = await jaegis_service.get_task_queue()
        return {"tasks": tasks, "count": len(tasks)}
    except Exception as e:
        logger.error(f"Error getting task queue: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- Real Agent System API ---
@app.get("/api/agents")
async def get_all_agents():
    """Get all registered JAEGIS agents"""
    if not agent_service:
        raise HTTPException(status_code=503, detail="Agent service not available")

    try:
        agents = await agent_service.get_all_agents()
        return {"agents": agents, "count": len(agents)}
    except Exception as e:
        logger.error(f"Error getting agents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/agents/active")
async def get_active_agents():
    """Get currently active agents"""
    if not agent_service:
        raise HTTPException(status_code=503, detail="Agent service not available")

    try:
        agents = await agent_service.get_active_agents()
        return {"active_agents": agents, "count": len(agents)}
    except Exception as e:
        logger.error(f"Error getting active agents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/agents/tiers")
async def get_agent_tiers():
    """Get agent distribution by tiers"""
    if not agent_service:
        raise HTTPException(status_code=503, detail="Agent service not available")

    try:
        tiers = await agent_service.get_agent_tiers()
        return {"tiers": tiers}
    except Exception as e:
        logger.error(f"Error getting agent tiers: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- Real N.L.D.S. Language Processing API ---
@app.get("/api/nlds/stats")
async def get_nlds_stats():
    """Get N.L.D.S. processing statistics"""
    if not nlds_service:
        raise HTTPException(status_code=503, detail="N.L.D.S. service not available")

    try:
        stats = await nlds_service.get_processing_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting N.L.D.S. stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/nlds/languages")
async def get_supported_languages():
    """Get supported languages and detection capabilities"""
    if not nlds_service:
        raise HTTPException(status_code=503, detail="N.L.D.S. service not available")

    try:
        languages = await nlds_service.get_supported_languages()
        return {"supported_languages": languages}
    except Exception as e:
        logger.error(f"Error getting supported languages: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- Real Enhanced Chat System API ---
@app.get("/api/chat/sessions")
async def get_chat_sessions():
    """Get active chat sessions"""
    if not chat_service:
        raise HTTPException(status_code=503, detail="Chat service not available")

    try:
        sessions = await chat_service.get_active_sessions()
        return {"sessions": sessions, "count": len(sessions)}
    except Exception as e:
        logger.error(f"Error getting chat sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chat/models")
async def get_chat_models():
    """Get available chat models and their status"""
    if not chat_service:
        raise HTTPException(status_code=503, detail="Chat service not available")

    try:
        models = await chat_service.get_available_models()
        return {"models": models}
    except Exception as e:
        logger.error(f"Error getting chat models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/system/status")
async def get_system_status():
    """Get overall JAEGIS system status"""
    try:
        status = {
            "timestamp": datetime.utcnow().isoformat(),
            "services": {
                "jaegis_core": jaegis_service is not None,
                "agent_system": agent_service is not None,
                "nlds_system": nlds_service is not None,
                "chat_system": chat_service is not None
            },
            "system_info": {
                "cpu_usage": psutil.cpu_percent(),
                "memory_usage": psutil.virtual_memory().percent,
                "uptime": "N/A"  # Can be implemented later
            }
        }

        if jaegis_service:
            jaegis_status = await jaegis_service.get_system_status()
            status["jaegis_status"] = jaegis_status

        return status
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {
        "status": "JAEGIS Cockpit - Real Operational Dashboard",
        "version": "2.0.0",
        "description": "Live operational dashboard for the JAEGIS ecosystem",
        "services_available": {
            "jaegis_core": jaegis_service is not None,
            "agent_system": agent_service is not None,
            "nlds_system": nlds_service is not None,
            "chat_system": chat_service is not None
        }
    }


