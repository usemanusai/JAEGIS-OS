#!/usr/bin/env python3
"""
Real JAEGIS Service Integration
==============================

Integrates with actual JAEGIS A.C.I.D. Swarm Orchestrator and core systems
to provide live operational data for the Cockpit dashboard.

This replaces all mock data with real system integrations.
"""

import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

# Add JAEGIS core paths
JAEGIS_ROOT = Path(__file__).parent.parent.parent.parent.parent
JAEGIS_CORE_PATH = JAEGIS_ROOT / "src" / "core"
sys.path.insert(0, str(JAEGIS_CORE_PATH))

logger = logging.getLogger(__name__)

class RealJAEGISService:
    """
    Real JAEGIS service integration for A.C.I.D. Swarm Orchestrator
    and core system monitoring.
    """
    
    def __init__(self):
        """Initialize real JAEGIS service connections"""
        self.swarm_orchestrator = None
        self.system_config = None
        self.system_status = None
        
        # Initialize connections to real JAEGIS systems
        self._initialize_connections()
    
    def _initialize_connections(self):
        """Initialize connections to real JAEGIS systems"""
        try:
            # Try to import and initialize A.C.I.D. Swarm Orchestrator
            from core.acid.swarm_orchestrator import SwarmOrchestrator
            self.swarm_orchestrator = SwarmOrchestrator()
            logger.info("✅ Connected to A.C.I.D. Swarm Orchestrator")
        except ImportError as e:
            logger.warning(f"⚠️ Could not import A.C.I.D. Swarm Orchestrator: {e}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize A.C.I.D. Swarm Orchestrator: {e}")
        
        # Load system configuration
        try:
            config_path = JAEGIS_ROOT / "src" / "core" / "agents" / "config" / "system_status.json"
            if config_path.exists():
                with open(config_path, 'r') as f:
                    self.system_status = json.load(f)
                logger.info("✅ Loaded JAEGIS system status configuration")
        except Exception as e:
            logger.error(f"❌ Failed to load system status: {e}")
        
        # Load core configuration
        try:
            core_config_path = JAEGIS_ROOT / "src" / "core" / "agents" / "config" / "core_config.json"
            if core_config_path.exists():
                with open(core_config_path, 'r') as f:
                    self.system_config = json.load(f)
                logger.info("✅ Loaded JAEGIS core configuration")
        except Exception as e:
            logger.error(f"❌ Failed to load core config: {e}")
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get real JAEGIS system status"""
        try:
            status = {
                "timestamp": datetime.utcnow().isoformat(),
                "service_available": True,
                "swarm_orchestrator_available": self.swarm_orchestrator is not None
            }
            
            # Add real system status if available
            if self.system_status:
                status.update({
                    "system_status": self.system_status.get("status", "UNKNOWN"),
                    "version": self.system_status.get("version", "Unknown"),
                    "components": self.system_status.get("components", {}),
                    "capabilities": self.system_status.get("capabilities", {}),
                    "initialization_time": self.system_status.get("initialization_time_seconds", 0)
                })
            
            # Add core configuration if available
            if self.system_config:
                status.update({
                    "core_components": self.system_config.get("core_components", {}),
                    "integration_points": self.system_config.get("integration_points", {})
                })
            
            return status
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "service_available": False,
                "error": str(e)
            }
    
    async def get_active_swarms(self) -> List[Dict[str, Any]]:
        """Get active A.C.I.D. swarms"""
        try:
            if not self.swarm_orchestrator:
                return []
            
            # Get active swarms from real orchestrator
            active_swarms = []
            if hasattr(self.swarm_orchestrator, 'active_swarms'):
                for swarm_id, swarm_config in self.swarm_orchestrator.active_swarms.items():
                    swarm_data = {
                        "swarm_id": swarm_id,
                        "task_id": getattr(swarm_config, 'task_id', 'unknown'),
                        "selected_agents": getattr(swarm_config, 'selected_agents', []),
                        "coordination_strategy": getattr(swarm_config, 'coordination_strategy', 'unknown'),
                        "created_at": getattr(swarm_config, 'created_at', datetime.now()).isoformat(),
                        "estimated_completion": getattr(swarm_config, 'estimated_completion', datetime.now()).isoformat(),
                        "performance_targets": getattr(swarm_config, 'performance_targets', {})
                    }
                    active_swarms.append(swarm_data)
            
            return active_swarms
        except Exception as e:
            logger.error(f"Error getting active swarms: {e}")
            return []
    
    async def get_swarm_details(self, swarm_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific swarm"""
        try:
            if not self.swarm_orchestrator:
                return None
            
            if hasattr(self.swarm_orchestrator, 'active_swarms'):
                swarm_config = self.swarm_orchestrator.active_swarms.get(swarm_id)
                if swarm_config:
                    return {
                        "swarm_id": swarm_id,
                        "task_id": getattr(swarm_config, 'task_id', 'unknown'),
                        "selected_agents": getattr(swarm_config, 'selected_agents', []),
                        "coordination_strategy": getattr(swarm_config, 'coordination_strategy', 'unknown'),
                        "communication_protocol": getattr(swarm_config, 'communication_protocol', 'unknown'),
                        "created_at": getattr(swarm_config, 'created_at', datetime.now()).isoformat(),
                        "estimated_completion": getattr(swarm_config, 'estimated_completion', datetime.now()).isoformat(),
                        "performance_targets": getattr(swarm_config, 'performance_targets', {}),
                        "status": "active"
                    }
            
            return None
        except Exception as e:
            logger.error(f"Error getting swarm details: {e}")
            return None
    
    async def get_task_queue(self) -> List[Dict[str, Any]]:
        """Get current A.C.I.D. task queue"""
        try:
            if not self.swarm_orchestrator:
                return []
            
            tasks = []
            if hasattr(self.swarm_orchestrator, 'task_queue'):
                for task in self.swarm_orchestrator.task_queue:
                    task_data = {
                        "task_id": getattr(task, 'task_id', 'unknown'),
                        "description": getattr(task, 'description', 'No description'),
                        "complexity": str(getattr(task, 'complexity', 'unknown')),
                        "priority": getattr(task, 'priority', 5),
                        "estimated_duration": getattr(task, 'estimated_duration', 0),
                        "required_capabilities": getattr(task, 'required_capabilities', []),
                        "success_criteria": getattr(task, 'success_criteria', {}),
                        "created_at": getattr(task, 'created_at', datetime.now()).isoformat(),
                        "status": "queued"
                    }
                    tasks.append(task_data)
            
            return tasks
        except Exception as e:
            logger.error(f"Error getting task queue: {e}")
            return []
    
    async def get_performance_metrics(self) -> Dict[str, Any]:
        """Get A.C.I.D. performance metrics"""
        try:
            if not self.swarm_orchestrator:
                return {}
            
            metrics = {
                "timestamp": datetime.utcnow().isoformat(),
                "active_swarms_count": len(getattr(self.swarm_orchestrator, 'active_swarms', {})),
                "queued_tasks_count": len(getattr(self.swarm_orchestrator, 'task_queue', [])),
                "max_concurrent_swarms": getattr(self.swarm_orchestrator, 'max_concurrent_swarms', 5),
                "agent_selection_algorithm": getattr(self.swarm_orchestrator, 'agent_selection_algorithm', 'unknown'),
                "optimization_cycles": getattr(self.swarm_orchestrator, 'optimization_cycles', 3)
            }
            
            # Add performance history if available
            if hasattr(self.swarm_orchestrator, 'performance_history'):
                metrics["performance_history_available"] = len(self.swarm_orchestrator.performance_history)
            
            return metrics
        except Exception as e:
            logger.error(f"Error getting performance metrics: {e}")
            return {}
    
    def is_available(self) -> bool:
        """Check if JAEGIS service is available"""
        return self.swarm_orchestrator is not None or self.system_status is not None
