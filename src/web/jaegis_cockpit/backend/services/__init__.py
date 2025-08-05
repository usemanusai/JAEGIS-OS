"""
JAEGIS Cockpit Backend Services - Real System Integration

Real services for the JAEGIS Cockpit backend API including:
- Real A.C.I.D. Swarm Orchestrator integration
- Real JAEGIS Agent System monitoring
- Real N.L.D.S. Language Processing integration
- Real Enhanced Chat System monitoring
- Live system telemetry and monitoring
"""

from .real_jaegis_service import RealJAEGISService
from .real_agent_service import RealAgentService
from .real_nlds_service import RealNLDSService
from .real_chat_service import RealChatService

__all__ = [
    "RealJAEGISService",
    "RealAgentService",
    "RealNLDSService",
    "RealChatService"
]
