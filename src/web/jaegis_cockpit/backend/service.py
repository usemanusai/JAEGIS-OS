#!/usr/bin/env python3
"""
JAEGIS Cockpit Service
======================

Service wrapper for the JAEGIS Cockpit backend using JAEGIS common base classes.
Provides the main control interface for the JAEGIS ecosystem.
"""

import asyncio
import logging
import uvicorn
from typing import Dict, Any, Optional
from pathlib import Path

# Import common base classes
import sys
sys.path.append(str(Path(__file__).parent.parent.parent / "common"))
from common.core.base_classes import BaseJAEGISService, ServiceStatus

from .main import app
from .services.taskmaster_service import taskmaster_service
from .services.governance import governance_service
from .services.treasury_service import treasury_service

logger = logging.getLogger(__name__)


class JAEGISCockpitService(BaseJAEGISService):
    """
    JAEGIS Cockpit Service implementation.
    
    Provides the main control interface for the JAEGIS ecosystem with:
    - Operations dashboard for system monitoring
    - Forge console for M.A.S.T.R. and A.S.C.E.N.D. operations
    - Governance interface for human-in-the-loop approvals
    - Treasury dashboard for budget and spending monitoring
    - Real-time WebSocket connections
    - RESTful API interface
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize JAEGIS Cockpit service"""
        super().__init__("jaegis_cockpit", config)
        
        # Service-specific configuration
        self.host = self.config.get('host', '127.0.0.1')
        self.port = self.config.get('port', 8090)
        self.log_level = self.config.get('log_level', 'info')
        self.reload = self.config.get('reload', False)
        
        # FastAPI app
        self.app = app
        self.server: Optional[uvicorn.Server] = None
        
        # Sub-services
        self.taskmaster = taskmaster_service
        self.governance = governance_service
        self.treasury = treasury_service
        
        logger.info("JAEGIS Cockpit service initialized")
    
    async def initialize(self) -> bool:
        """
        Initialize the JAEGIS Cockpit service.
        
        Returns:
            bool: True if initialization successful
        """
        try:
            # Initialize sub-services
            logger.info("Initializing Cockpit sub-services...")
            
            # Taskmaster service is already initialized as a singleton
            # Governance service is already initialized as a singleton
            # Treasury service is already initialized as a singleton
            
            # Configure uvicorn server
            config = uvicorn.Config(
                app=self.app,
                host=self.host,
                port=self.port,
                log_level=self.log_level,
                reload=self.reload
            )
            self.server = uvicorn.Server(config)
            
            logger.info("JAEGIS Cockpit service initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize JAEGIS Cockpit service: {e}")
            return False
    
    async def start(self) -> bool:
        """
        Start the JAEGIS Cockpit service.
        
        Returns:
            bool: True if start successful
        """
        try:
            if not self.server:
                logger.error("Server not initialized")
                return False
            
            # Start the FastAPI server
            logger.info(f"Starting JAEGIS Cockpit server on {self.host}:{self.port}")
            
            # Run server in background task
            asyncio.create_task(self.server.serve())
            
            # Wait a moment for server to start
            await asyncio.sleep(1)
            
            logger.info("JAEGIS Cockpit service started successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start JAEGIS Cockpit service: {e}")
            return False
    
    async def stop(self) -> bool:
        """
        Stop the JAEGIS Cockpit service.
        
        Returns:
            bool: True if stop successful
        """
        try:
            if self.server:
                logger.info("Stopping JAEGIS Cockpit server...")
                self.server.should_exit = True
                
                # Wait for server to stop
                await asyncio.sleep(2)
            
            logger.info("JAEGIS Cockpit service stopped successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop JAEGIS Cockpit service: {e}")
            return False
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform health check.
        
        Returns:
            Dict[str, Any]: Health status information
        """
        health_status = {
            'service': 'jaegis_cockpit',
            'status': self.status.value,
            'healthy': True,
            'components': {},
            'timestamp': asyncio.get_event_loop().time()
        }
        
        try:
            # Check server status
            if self.server and hasattr(self.server, 'started') and self.server.started:
                health_status['components']['fastapi_server'] = {
                    'status': 'healthy',
                    'host': self.host,
                    'port': self.port
                }
            else:
                health_status['components']['fastapi_server'] = {
                    'status': 'unhealthy',
                    'error': 'Server not running'
                }
                health_status['healthy'] = False
            
            # Check sub-services
            try:
                # Check taskmaster service
                taskmaster_status = self.taskmaster.get_status()
                health_status['components']['taskmaster'] = {
                    'status': 'healthy' if taskmaster_status else 'unhealthy'
                }
            except Exception as e:
                health_status['components']['taskmaster'] = {
                    'status': 'unhealthy',
                    'error': str(e)
                }
                health_status['healthy'] = False
            
            try:
                # Check governance service
                governance_status = await self.governance.get_pending_approvals()
                health_status['components']['governance'] = {
                    'status': 'healthy',
                    'pending_approvals': len(governance_status) if governance_status else 0
                }
            except Exception as e:
                health_status['components']['governance'] = {
                    'status': 'unhealthy',
                    'error': str(e)
                }
                health_status['healthy'] = False
            
            try:
                # Check treasury service
                treasury_status = self.treasury.get_status()
                health_status['components']['treasury'] = {
                    'status': 'healthy' if treasury_status else 'unhealthy',
                    'budget_info': treasury_status if treasury_status else None
                }
            except Exception as e:
                health_status['components']['treasury'] = {
                    'status': 'unhealthy',
                    'error': str(e)
                }
                health_status['healthy'] = False
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            health_status['healthy'] = False
            health_status['error'] = str(e)
        
        return health_status
    
    # Service-specific methods
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get current system status.
        
        Returns:
            Dict[str, Any]: System status information
        """
        return {
            'cockpit': self.get_metrics(),
            'taskmaster': self.taskmaster.get_status(),
            'treasury': self.treasury.get_status(),
            'timestamp': asyncio.get_event_loop().time()
        }
    
    async def get_governance_status(self) -> Dict[str, Any]:
        """
        Get governance status.
        
        Returns:
            Dict[str, Any]: Governance status information
        """
        try:
            pending_approvals = await self.governance.get_pending_approvals()
            return {
                'pending_approvals': len(pending_approvals) if pending_approvals else 0,
                'approvals': pending_approvals[:10] if pending_approvals else [],  # Latest 10
                'healthy': True
            }
        except Exception as e:
            logger.error(f"Failed to get governance status: {e}")
            return {
                'pending_approvals': 0,
                'approvals': [],
                'healthy': False,
                'error': str(e)
            }
    
    def get_treasury_status(self) -> Dict[str, Any]:
        """
        Get treasury status.
        
        Returns:
            Dict[str, Any]: Treasury status information
        """
        try:
            return self.treasury.get_status()
        except Exception as e:
            logger.error(f"Failed to get treasury status: {e}")
            return {
                'monthly_budget': 0,
                'current_spend': 0,
                'usage_percent': 0,
                'healthy': False,
                'error': str(e)
            }
    
    async def submit_forge_request(self, request_type: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Submit a forge request (M.A.S.T.R. or A.S.C.E.N.D.).
        
        Args:
            request_type: Type of request ('mastr_toolset' or 'ascend_agent')
            request_data: Request data
            
        Returns:
            Dict[str, Any]: Request submission result
        """
        try:
            # Submit to governance for approval
            if request_type == 'mastr_toolset':
                item_type = 'MASTR_Toolset'
            elif request_type == 'ascend_agent':
                item_type = 'ASCEND_Agent'
            else:
                raise ValueError(f"Unknown request type: {request_type}")
            
            request_id = await self.governance.submit_approval_request(
                item_type=item_type,
                item_details=request_data,
                requester_id='cockpit_user'
            )
            
            return {
                'success': True,
                'request_id': request_id,
                'message': f'{request_type} request submitted for approval'
            }
            
        except Exception as e:
            logger.error(f"Failed to submit forge request: {e}")
            return {
                'success': False,
                'error': str(e)
            }


# Global service instance
_cockpit_service: Optional[JAEGISCockpitService] = None


def get_cockpit_service(config: Optional[Dict[str, Any]] = None) -> JAEGISCockpitService:
    """
    Get the global JAEGIS Cockpit service instance.
    
    Args:
        config: Service configuration (only used on first call)
        
    Returns:
        JAEGISCockpitService: Global service instance
    """
    global _cockpit_service
    if _cockpit_service is None:
        _cockpit_service = JAEGISCockpitService(config)
    return _cockpit_service
