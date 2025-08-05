#!/usr/bin/env python3
"""
Framework Integration and Coordination Layer
JAEGIS Enhanced Agent System v2.2 - Brain Protocol Suite v1.0

Unified coordination layer for all frameworks ensuring seamless integration
with A.E.G.I.S. components and comprehensive system orchestration.
"""

import asyncio
import logging
import time
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import uuid

# J.O.L.T. Observability Stack Integration
from core.utils.telemetry_init import get_tracer, get_langfuse_client
from core.utils.metrics import (
    FRAMEWORK_COORDINATION_EVENTS,
    FRAMEWORK_INTEGRATION_LATENCY,
    FRAMEWORK_HEALTH_STATUS
)

# Framework Imports
from frameworks.pitces.core_engine import get_pitces_controller
from frameworks.cognitive.pipeline_framework import get_cognitive_pipeline
from frameworks.chimera.security_framework import get_chimera_security
from core.aegis.integration_system import get_aegis_system

logger = logging.getLogger(__name__)
tracer = get_tracer(__name__)

class FrameworkType(Enum):
    """Types of integrated frameworks"""
    PITCES = "pitces"
    COGNITIVE = "cognitive"
    CHIMERA_SECURITY = "chimera_security"
    AEGIS = "aegis"
    ACID = "acid"
    AURA = "aura"
    PHALANX = "phalanx"
    ODIN = "odin"

class CoordinationEvent(Enum):
    """Framework coordination events"""
    FRAMEWORK_STARTUP = "framework_startup"
    FRAMEWORK_SHUTDOWN = "framework_shutdown"
    CROSS_FRAMEWORK_REQUEST = "cross_framework_request"
    RESOURCE_ALLOCATION = "resource_allocation"
    CONFLICT_RESOLUTION = "conflict_resolution"
    HEALTH_CHECK = "health_check"

@dataclass
class FrameworkRequest:
    """Request between frameworks"""
    id: str
    source_framework: FrameworkType
    target_framework: FrameworkType
    operation: str
    parameters: Dict[str, Any]
    priority: int = 5  # 1-10, 10 being highest
    timeout: int = 30
    callback: Optional[Callable] = None
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class FrameworkResponse:
    """Response from framework operation"""
    request_id: str
    success: bool
    result: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    processing_time: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class FrameworkStatus:
    """Status of a framework"""
    framework_type: FrameworkType
    status: str  # operational, degraded, offline
    health_score: float  # 0.0 to 1.0
    last_heartbeat: datetime
    active_requests: int
    error_count: int
    metadata: Dict[str, Any] = field(default_factory=dict)

class FrameworkCoordinationLayer:
    """
    Framework Integration and Coordination Layer
    
    Provides unified coordination for all JAEGIS frameworks ensuring
    seamless integration and optimal resource utilization.
    """
    
    def __init__(self):
        self.langfuse_client = get_langfuse_client()
        
        # Framework instances
        self.frameworks: Dict[FrameworkType, Any] = {}
        self.framework_status: Dict[FrameworkType, FrameworkStatus] = {}
        
        # Request management
        self.pending_requests: Dict[str, FrameworkRequest] = {}
        self.request_queue: asyncio.Queue = asyncio.Queue()
        self.response_callbacks: Dict[str, Callable] = {}
        
        # Coordination state
        self.resource_allocations: Dict[str, Dict[str, Any]] = {}
        self.conflict_resolutions: List[Dict[str, Any]] = []
        self.coordination_metrics: Dict[str, Any] = {}
        
        # Initialize coordination layer
        self._initialize_frameworks()
        self._start_coordination_loop()
        
        logger.info("🔗 Framework Coordination Layer initialized")

    def _initialize_frameworks(self):
        """Initialize all framework instances"""
        try:
            # Initialize P.I.T.C.E.S. Framework
            self.frameworks[FrameworkType.PITCES] = get_pitces_controller()
            self._update_framework_status(FrameworkType.PITCES, "operational", 1.0)
            
            # Initialize Cognitive Pipeline
            self.frameworks[FrameworkType.COGNITIVE] = get_cognitive_pipeline()
            self._update_framework_status(FrameworkType.COGNITIVE, "operational", 1.0)
            
            # Initialize Chimera Security
            self.frameworks[FrameworkType.CHIMERA_SECURITY] = get_chimera_security()
            self._update_framework_status(FrameworkType.CHIMERA_SECURITY, "operational", 1.0)
            
            # Initialize A.E.G.I.S. System
            self.frameworks[FrameworkType.AEGIS] = get_aegis_system()
            self._update_framework_status(FrameworkType.AEGIS, "operational", 1.0)
            
            logger.info(f"✅ Initialized {len(self.frameworks)} frameworks")
            
        except Exception as e:
            logger.error(f"❌ Framework initialization failed: {e}")
            raise

    def _start_coordination_loop(self):
        """Start the coordination event loop"""
        asyncio.create_task(self._coordination_event_loop())
        asyncio.create_task(self._health_monitoring_loop())

    async def _coordination_event_loop(self):
        """Main coordination event processing loop"""
        while True:
            try:
                # Process pending requests
                if not self.request_queue.empty():
                    request = await self.request_queue.get()
                    await self._process_framework_request(request)
                
                # Brief pause to prevent busy waiting
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"❌ Coordination loop error: {e}")
                await asyncio.sleep(1)

    async def _health_monitoring_loop(self):
        """Health monitoring loop for all frameworks"""
        while True:
            try:
                await self._perform_health_checks()
                await asyncio.sleep(30)  # Health check every 30 seconds
                
            except Exception as e:
                logger.error(f"❌ Health monitoring error: {e}")
                await asyncio.sleep(5)

    async def coordinate_framework_request(
        self,
        source: FrameworkType,
        target: FrameworkType,
        operation: str,
        parameters: Dict[str, Any],
        priority: int = 5,
        timeout: int = 30
    ) -> FrameworkResponse:
        """
        Coordinate a request between frameworks
        
        Args:
            source: Source framework making the request
            target: Target framework to handle the request
            operation: Operation to perform
            parameters: Operation parameters
            priority: Request priority (1-10)
            timeout: Request timeout in seconds
            
        Returns:
            Framework response
        """
        with tracer.start_as_current_span("framework_coordination") as span:
            span.set_attribute("source", source.value)
            span.set_attribute("target", target.value)
            span.set_attribute("operation", operation)
            
            start_time = time.time()
            
            try:
                # Create request
                request = FrameworkRequest(
                    id=str(uuid.uuid4()),
                    source_framework=source,
                    target_framework=target,
                    operation=operation,
                    parameters=parameters,
                    priority=priority,
                    timeout=timeout
                )
                
                # Validate request
                if not await self._validate_framework_request(request):
                    return FrameworkResponse(
                        request_id=request.id,
                        success=False,
                        error="Request validation failed"
                    )
                
                # Check security clearance
                security_check = await self._check_security_clearance(request)
                if not security_check['allowed']:
                    return FrameworkResponse(
                        request_id=request.id,
                        success=False,
                        error=f"Security check failed: {security_check['reason']}"
                    )
                
                # Queue request for processing
                self.pending_requests[request.id] = request
                await self.request_queue.put(request)
                
                # Wait for response
                response = await self._wait_for_response(request.id, timeout)
                
                # Record metrics
                processing_time = time.time() - start_time
                
                FRAMEWORK_COORDINATION_EVENTS.labels(
                    source=source.value,
                    target=target.value,
                    operation=operation,
                    status="success" if response.success else "failed"
                ).inc()
                
                FRAMEWORK_INTEGRATION_LATENCY.labels(
                    source=source.value,
                    target=target.value
                ).observe(processing_time)
                
                logger.info(f"🔗 Framework coordination completed: {source.value} -> {target.value}")
                return response
                
            except Exception as e:
                processing_time = time.time() - start_time
                
                FRAMEWORK_COORDINATION_EVENTS.labels(
                    source=source.value,
                    target=target.value,
                    operation=operation,
                    status="error"
                ).inc()
                
                logger.error(f"❌ Framework coordination failed: {e}")
                return FrameworkResponse(
                    request_id="",
                    success=False,
                    error=str(e)
                )

    async def _process_framework_request(self, request: FrameworkRequest) -> FrameworkResponse:
        """Process a framework request"""
        try:
            target_framework = self.frameworks.get(request.target_framework)
            if not target_framework:
                return FrameworkResponse(
                    request_id=request.id,
                    success=False,
                    error=f"Target framework {request.target_framework.value} not available"
                )
            
            # Route request to appropriate handler
            response = await self._route_request_to_framework(request, target_framework)
            
            # Store response for callback
            if request.callback:
                await request.callback(response)
            
            # Clean up
            self.pending_requests.pop(request.id, None)
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Framework request processing failed: {e}")
            return FrameworkResponse(
                request_id=request.id,
                success=False,
                error=str(e)
            )

    async def _route_request_to_framework(
        self,
        request: FrameworkRequest,
        framework: Any
    ) -> FrameworkResponse:
        """Route request to specific framework"""
        start_time = time.time()
        
        try:
            # Route based on framework type
            if request.target_framework == FrameworkType.PITCES:
                result = await self._handle_pitces_request(framework, request)
            elif request.target_framework == FrameworkType.COGNITIVE:
                result = await self._handle_cognitive_request(framework, request)
            elif request.target_framework == FrameworkType.CHIMERA_SECURITY:
                result = await self._handle_security_request(framework, request)
            elif request.target_framework == FrameworkType.AEGIS:
                result = await self._handle_aegis_request(framework, request)
            else:
                result = {'success': False, 'error': 'Unknown framework type'}
            
            processing_time = time.time() - start_time
            
            return FrameworkResponse(
                request_id=request.id,
                success=result.get('success', False),
                result=result.get('result'),
                error=result.get('error'),
                processing_time=processing_time,
                metadata=result.get('metadata', {})
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            return FrameworkResponse(
                request_id=request.id,
                success=False,
                error=str(e),
                processing_time=processing_time
            )

    # Framework-specific request handlers
    async def _handle_pitces_request(self, framework: Any, request: FrameworkRequest) -> Dict[str, Any]:
        """Handle P.I.T.C.E.S. framework request"""
        operation = request.operation
        params = request.parameters
        
        if operation == "select_workflow":
            result = framework.select_workflow(params.get('project_specs', {}))
            return {'success': True, 'result': result}
        elif operation == "get_status":
            result = await framework.get_system_status()
            return {'success': True, 'result': result}
        else:
            return {'success': False, 'error': f'Unknown P.I.T.C.E.S. operation: {operation}'}

    async def _handle_cognitive_request(self, framework: Any, request: FrameworkRequest) -> Dict[str, Any]:
        """Handle Cognitive Pipeline request"""
        operation = request.operation
        params = request.parameters
        
        if operation == "process_input":
            from frameworks.cognitive.pipeline_framework import CognitiveInput, CognitiveMode
            
            input_data = CognitiveInput(
                id=params.get('id', str(uuid.uuid4())),
                content=params.get('content'),
                modality=params.get('modality', 'text'),
                context=params.get('context', {}),
                metadata=params.get('metadata', {})
            )
            
            mode = CognitiveMode(params.get('mode', 'analytical'))
            pipeline = params.get('pipeline', 'analytical')
            
            result = await framework.process_cognitive_input(input_data, pipeline, mode)
            return {'success': True, 'result': result.__dict__}
        elif operation == "get_status":
            result = await framework.get_pipeline_status()
            return {'success': True, 'result': result}
        else:
            return {'success': False, 'error': f'Unknown Cognitive operation: {operation}'}

    async def _handle_security_request(self, framework: Any, request: FrameworkRequest) -> Dict[str, Any]:
        """Handle Chimera Security request"""
        operation = request.operation
        params = request.parameters
        
        if operation == "assess_threat":
            result = await framework.assess_security_threat(
                params.get('source'),
                params.get('action'),
                params.get('context', {})
            )
            return {'success': True, 'result': result.__dict__}
        elif operation == "enforce_policy":
            result = await framework.enforce_security_policy(
                params.get('policy_id'),
                params.get('source'),
                params.get('action'),
                params.get('data')
            )
            return {'success': True, 'result': result}
        elif operation == "get_status":
            result = await framework.get_security_status()
            return {'success': True, 'result': result}
        else:
            return {'success': False, 'error': f'Unknown Security operation: {operation}'}

    async def _handle_aegis_request(self, framework: Any, request: FrameworkRequest) -> Dict[str, Any]:
        """Handle A.E.G.I.S. system request"""
        operation = request.operation
        params = request.parameters
        
        if operation == "route_request":
            result = await framework.route_request(
                params.get('component'),
                params.get('operation'),
                params.get('data', {})
            )
            return {'success': True, 'result': result}
        elif operation == "get_status":
            result = await framework.get_system_status()
            return {'success': True, 'result': result}
        else:
            return {'success': False, 'error': f'Unknown A.E.G.I.S. operation: {operation}'}

    async def _validate_framework_request(self, request: FrameworkRequest) -> bool:
        """Validate framework request"""
        try:
            # Check if target framework is available
            if request.target_framework not in self.frameworks:
                return False
            
            # Check framework status
            status = self.framework_status.get(request.target_framework)
            if not status or status.status != "operational":
                return False
            
            # Validate operation parameters
            if not request.operation or not isinstance(request.parameters, dict):
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Request validation error: {e}")
            return False

    async def _check_security_clearance(self, request: FrameworkRequest) -> Dict[str, Any]:
        """Check security clearance for framework request"""
        try:
            # Use Chimera Security for clearance check
            security_framework = self.frameworks.get(FrameworkType.CHIMERA_SECURITY)
            if security_framework:
                return await security_framework.enforce_security_policy(
                    "core_security",
                    request.source_framework.value,
                    request.operation,
                    request.parameters
                )
            
            # Default allow if security framework not available
            return {'allowed': True, 'reason': 'Security framework not available'}
            
        except Exception as e:
            logger.error(f"Security clearance check error: {e}")
            return {'allowed': False, 'reason': f'Security check error: {e}'}

    async def _wait_for_response(self, request_id: str, timeout: int) -> FrameworkResponse:
        """Wait for framework response"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            # Check if request is still pending
            if request_id not in self.pending_requests:
                # Request completed, but we need to find the response
                # For now, return a timeout response
                break
            
            await asyncio.sleep(0.1)
        
        # Timeout occurred
        return FrameworkResponse(
            request_id=request_id,
            success=False,
            error="Request timeout"
        )

    async def _perform_health_checks(self):
        """Perform health checks on all frameworks"""
        for framework_type, framework in self.frameworks.items():
            try:
                # Basic health check
                health_score = 1.0
                status = "operational"
                
                # Framework-specific health checks
                if hasattr(framework, 'get_health_status'):
                    health_result = await framework.get_health_status()
                    health_score = health_result.get('health_score', 1.0)
                    status = health_result.get('status', 'operational')
                
                self._update_framework_status(framework_type, status, health_score)
                
                # Record metrics
                FRAMEWORK_HEALTH_STATUS.labels(
                    framework=framework_type.value
                ).set(health_score)
                
            except Exception as e:
                logger.error(f"Health check failed for {framework_type.value}: {e}")
                self._update_framework_status(framework_type, "degraded", 0.5)

    def _update_framework_status(self, framework_type: FrameworkType, status: str, health_score: float):
        """Update framework status"""
        current_status = self.framework_status.get(framework_type)
        
        if current_status:
            current_status.status = status
            current_status.health_score = health_score
            current_status.last_heartbeat = datetime.now()
        else:
            self.framework_status[framework_type] = FrameworkStatus(
                framework_type=framework_type,
                status=status,
                health_score=health_score,
                last_heartbeat=datetime.now(),
                active_requests=0,
                error_count=0
            )

    async def get_coordination_status(self) -> Dict[str, Any]:
        """Get comprehensive coordination status"""
        return {
            'coordination_layer_status': 'operational',
            'frameworks_count': len(self.frameworks),
            'frameworks_status': {
                ft.value: {
                    'status': status.status,
                    'health_score': status.health_score,
                    'last_heartbeat': status.last_heartbeat.isoformat(),
                    'active_requests': status.active_requests,
                    'error_count': status.error_count
                }
                for ft, status in self.framework_status.items()
            },
            'pending_requests': len(self.pending_requests),
            'queue_size': self.request_queue.qsize(),
            'resource_allocations': len(self.resource_allocations),
            'timestamp': datetime.now().isoformat()
        }

# Global Coordination Layer instance
_coordination_layer_instance = None

def get_coordination_layer() -> FrameworkCoordinationLayer:
    """Get global Framework Coordination Layer instance"""
    global _coordination_layer_instance
    if _coordination_layer_instance is None:
        _coordination_layer_instance = FrameworkCoordinationLayer()
    return _coordination_layer_instance
