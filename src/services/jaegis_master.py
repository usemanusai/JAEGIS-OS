#!/usr/bin/env python3
"""
JAEGIS Master Orchestrator
==========================

Master service orchestrator for the complete JAEGIS ecosystem.
Manages all core services and provides the Genesis Test implementation.
"""

import asyncio
import logging
import signal
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List

# Add paths for local imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
# Add the common directory from the root JAEGIS directory
common_dir = current_dir.parent.parent / "common"
sys.path.insert(0, str(common_dir))
from common.core.base_classes import BaseJAEGISService, service_lifecycle

# Import all JAEGIS services
from core.script.service import get_script_service
from core.atlas.service import get_atlas_service
from core.helm.service import get_helm_service
from core.mastr.service import get_mastr_service
from core.ascend.service import get_ascend_service
from common.core.cori.service import get_cori_service
from jaegis_cockpit.backend.service import get_cockpit_service

# Import core orchestrator for Genesis Test
from core.acid.swarm_orchestrator import SwarmOrchestrator

logger = logging.getLogger(__name__)


class JAEGISMaster(BaseJAEGISService):
    """
    JAEGIS Master Orchestrator.
    
    Manages the complete JAEGIS ecosystem and provides the Genesis Test
    to validate end-to-end autonomous capability expansion.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize JAEGIS Master"""
        super().__init__("jaegis_master", config)
        
        # Core services
        self.services: Dict[str, BaseJAEGISService] = {}
        
        # Genesis Test components
        self.swarm_orchestrator: Optional[SwarmOrchestrator] = None
        
        # Service startup order (dependencies first)
        self.service_order = [
            'script',    # Configuration and secrets
            'atlas',     # Resource synchronization
            'cori',      # Cognitive operations
            'helm',      # Benchmarking
            'mastr',     # Tool forging
            'ascend',    # Agent synthesis
            'cockpit'    # Control interface
        ]
        
        logger.info("JAEGIS Master initialized")
    
    async def initialize(self) -> bool:
        """
        Initialize all JAEGIS services.
        
        Returns:
            bool: True if initialization successful
        """
        try:
            # Initialize services in dependency order
            service_configs = {
                'script': self.config.get('script', {}),
                'atlas': self.config.get('atlas', {}),
                'cori': self.config.get('cori', {}),
                'helm': self.config.get('helm', {}),
                'mastr': self.config.get('mastr', {}),
                'ascend': self.config.get('ascend', {}),
                'cockpit': self.config.get('cockpit', {})
            }
            
            # Get service instances
            self.services = {
                'script': get_script_service(service_configs['script']),
                'atlas': get_atlas_service(service_configs['atlas']),
                'cori': get_cori_service(service_configs['cori']),
                'helm': get_helm_service(service_configs['helm']),
                'mastr': get_mastr_service(service_configs['mastr']),
                'ascend': get_ascend_service(service_configs['ascend']),
                'cockpit': get_cockpit_service(service_configs['cockpit'])
            }
            
            # Initialize each service
            for service_name in self.service_order:
                service = self.services[service_name]
                logger.info(f"Initializing {service_name} service...")
                
                if not await service.initialize():
                    logger.error(f"Failed to initialize {service_name} service")
                    return False
                
                logger.info(f"{service_name} service initialized successfully")
            
            # Initialize Genesis Test components
            self.swarm_orchestrator = SwarmOrchestrator()
            
            logger.info("JAEGIS Master initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize JAEGIS Master: {e}")
            return False
    
    async def start(self) -> bool:
        """
        Start all JAEGIS services.
        
        Returns:
            bool: True if start successful
        """
        try:
            # Start services in dependency order
            for service_name in self.service_order:
                service = self.services[service_name]
                logger.info(f"Starting {service_name} service...")
                
                if not await service.start():
                    logger.error(f"Failed to start {service_name} service")
                    return False
                
                logger.info(f"{service_name} service started successfully")
            
            logger.info("JAEGIS Master started successfully")
            logger.info("🚀 JAEGIS Ecosystem is now fully operational!")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start JAEGIS Master: {e}")
            return False
    
    async def stop(self) -> bool:
        """
        Stop all JAEGIS services.
        
        Returns:
            bool: True if stop successful
        """
        try:
            # Stop services in reverse order
            for service_name in reversed(self.service_order):
                service = self.services[service_name]
                logger.info(f"Stopping {service_name} service...")
                
                if not await service.stop():
                    logger.warning(f"Failed to stop {service_name} service cleanly")
                else:
                    logger.info(f"{service_name} service stopped successfully")
            
            logger.info("JAEGIS Master stopped successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop JAEGIS Master: {e}")
            return False
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform comprehensive health check.
        
        Returns:
            Dict[str, Any]: Health status information
        """
        health_status = {
            'service': 'jaegis_master',
            'status': self.status.value,
            'healthy': True,
            'services': {},
            'timestamp': asyncio.get_event_loop().time()
        }
        
        try:
            # Check all services
            for service_name, service in self.services.items():
                service_health = await service.health_check()
                health_status['services'][service_name] = service_health
                
                if not service_health.get('healthy', False):
                    health_status['healthy'] = False
            
            # Add ecosystem metrics
            health_status['ecosystem_metrics'] = {
                'total_services': len(self.services),
                'healthy_services': sum(1 for s in health_status['services'].values() if s.get('healthy', False)),
                'service_uptime': self.metrics.uptime_seconds
            }
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            health_status['healthy'] = False
            health_status['error'] = str(e)
        
        return health_status
    
    async def genesis_test(self) -> Dict[str, Any]:
        """
        Execute the Genesis Test - the "Hacker News haiku" scenario.
        
        This test validates the complete autonomous loop:
        1. Capability gap detection
        2. Tool/agent forging
        3. Human approval workflow
        4. Deployment and learning
        
        Returns:
            Dict[str, Any]: Genesis Test results
        """
        logger.info("🧪 Starting Genesis Test - 'Hacker News haiku' scenario")
        
        test_results = {
            'test_name': 'Genesis Test - Hacker News Haiku',
            'start_time': asyncio.get_event_loop().time(),
            'stages': {},
            'success': False
        }
        
        try:
            # Stage 1: Submit the objective that will trigger capability gap
            objective = "Write a haiku about the top story on Hacker News"
            task_id = "genesis_test_001"
            
            logger.info(f"Stage 1: Submitting objective - {objective}")
            test_results['stages']['objective_submission'] = {
                'objective': objective,
                'task_id': task_id,
                'timestamp': asyncio.get_event_loop().time()
            }
            
            # Stage 2: Process through A.C.I.D. Orchestrator (should detect capability gap)
            logger.info("Stage 2: Processing through A.C.I.D. Orchestrator")
            orchestrator_result = self.swarm_orchestrator.process_objective(objective, task_id)
            
            test_results['stages']['acid_processing'] = {
                'result': orchestrator_result,
                'timestamp': asyncio.get_event_loop().time()
            }
            
            # Check if capability gap was detected
            if orchestrator_result.get('status') == 'pending_synthesis':
                logger.info("✅ Stage 2 Success: Capability gap detected, A.S.C.E.N.D. triggered")
                test_results['stages']['capability_gap_detection'] = {
                    'detected': True,
                    'details': orchestrator_result.get('details'),
                    'timestamp': asyncio.get_event_loop().time()
                }
            else:
                logger.warning("⚠️ Stage 2: No capability gap detected - test may not proceed as expected")
                test_results['stages']['capability_gap_detection'] = {
                    'detected': False,
                    'result': orchestrator_result,
                    'timestamp': asyncio.get_event_loop().time()
                }
            
            # Stage 3: Simulate A.S.C.E.N.D. agent synthesis
            logger.info("Stage 3: Simulating A.S.C.E.N.D. agent synthesis")
            
            job_description = {
                'name': 'Hacker News Haiku Agent',
                'description': 'An agent that can fetch Hacker News stories and write haikus about them',
                'required_capabilities': [
                    'web_scraping',
                    'api_access',
                    'creative_writing',
                    'haiku_composition'
                ],
                'required_tools': [
                    'A tool to access Hacker News API',
                    'A tool for generating creative poetry'
                ]
            }
            
            ascend_service = self.services['ascend']
            synthesis_result = await ascend_service.synthesize_agent(job_description)
            
            test_results['stages']['agent_synthesis'] = {
                'result': synthesis_result,
                'timestamp': asyncio.get_event_loop().time()
            }
            
            if synthesis_result.get('success'):
                logger.info("✅ Stage 3 Success: Agent synthesis completed")
            else:
                logger.error(f"❌ Stage 3 Failed: Agent synthesis failed - {synthesis_result.get('error')}")
            
            # Stage 4: Simulate M.A.S.T.R. tool forging
            logger.info("Stage 4: Simulating M.A.S.T.R. tool forging")
            
            tool_requirements = {
                'name': 'Hacker News API Client',
                'description': 'A tool for accessing Hacker News API and fetching stories',
                'capabilities': [
                    'fetch_top_stories',
                    'get_story_details',
                    'search_stories'
                ],
                'api_endpoints': [
                    'https://hacker-news.firebaseio.com/v0/topstories.json',
                    'https://hacker-news.firebaseio.com/v0/item/{id}.json'
                ]
            }
            
            mastr_service = self.services['mastr']
            forge_result = await mastr_service.forge_toolset(tool_requirements)
            
            test_results['stages']['tool_forging'] = {
                'result': forge_result,
                'timestamp': asyncio.get_event_loop().time()
            }
            
            if forge_result.get('success'):
                logger.info("✅ Stage 4 Success: Tool forging completed")
            else:
                logger.error(f"❌ Stage 4 Failed: Tool forging failed - {forge_result.get('error')}")
            
            # Stage 5: Check governance workflow
            logger.info("Stage 5: Checking governance workflow")
            
            cockpit_service = self.services['cockpit']
            governance_status = await cockpit_service.get_governance_status()
            
            test_results['stages']['governance_check'] = {
                'status': governance_status,
                'timestamp': asyncio.get_event_loop().time()
            }
            
            if governance_status.get('pending_approvals', 0) > 0:
                logger.info("✅ Stage 5 Success: Governance workflow active with pending approvals")
            else:
                logger.info("ℹ️ Stage 5: No pending approvals (may be expected in test environment)")
            
            # Stage 6: Simulate learning and adaptation
            logger.info("Stage 6: Simulating learning and adaptation")
            
            cori_service = self.services['cori']
            
            # Log the test event for learning
            test_event = {
                'event_type': 'genesis_test_execution',
                'objective': objective,
                'capability_gap_detected': test_results['stages']['capability_gap_detection']['detected'],
                'agent_synthesized': synthesis_result.get('success', False),
                'tool_forged': forge_result.get('success', False),
                'timestamp': asyncio.get_event_loop().time()
            }
            
            learning_result = await cori_service.log_event(test_event)
            
            test_results['stages']['learning_adaptation'] = {
                'event_logged': learning_result,
                'timestamp': asyncio.get_event_loop().time()
            }
            
            if learning_result:
                logger.info("✅ Stage 6 Success: Learning event logged")
            else:
                logger.warning("⚠️ Stage 6: Failed to log learning event")
            
            # Final assessment
            test_results['end_time'] = asyncio.get_event_loop().time()
            test_results['duration'] = test_results['end_time'] - test_results['start_time']
            
            # Determine overall success
            critical_stages = [
                test_results['stages']['capability_gap_detection']['detected'],
                synthesis_result.get('success', False),
                forge_result.get('success', False)
            ]
            
            test_results['success'] = all(critical_stages)
            
            if test_results['success']:
                logger.info("🎉 Genesis Test PASSED! JAEGIS autonomous loop validated successfully!")
            else:
                logger.warning("⚠️ Genesis Test completed with some failures - review results for details")
            
            return test_results
            
        except Exception as e:
            logger.error(f"Genesis Test failed with exception: {e}")
            test_results['error'] = str(e)
            test_results['success'] = False
            test_results['end_time'] = asyncio.get_event_loop().time()
            return test_results


async def main():
    """Main entry point for JAEGIS Master"""
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Default configuration
    config = {
        'script': {'enable_api': True, 'api_port': 8080},
        'atlas': {'enable_api': True, 'api_port': 8081},
        'helm': {'enable_api': True, 'api_port': 8082},
        'mastr': {'enable_api': True, 'api_port': 8083},
        'ascend': {'enable_api': True, 'api_port': 8084},
        'cori': {'enable_htm': True, 'enable_cognitive_map': True},
        'cockpit': {'host': '127.0.0.1', 'port': 8090}
    }
    
    # Create and start JAEGIS Master
    jaegis_master = JAEGISMaster(config)
    
    # Handle shutdown gracefully
    def signal_handler(signum, frame):
        logger.info("Shutdown signal received")
        asyncio.create_task(jaegis_master.shutdown())
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Use service lifecycle context manager
        async with service_lifecycle(jaegis_master):
            logger.info("JAEGIS Master is running...")
            
            # Run Genesis Test
            if len(sys.argv) > 1 and sys.argv[1] == '--genesis-test':
                logger.info("Genesis Test mode activated")
                await asyncio.sleep(5)  # Allow services to fully start
                
                test_results = await jaegis_master.genesis_test()
                
                print("\n" + "="*80)
                print("GENESIS TEST RESULTS")
                print("="*80)
                print(f"Test: {test_results['test_name']}")
                print(f"Duration: {test_results.get('duration', 0):.2f} seconds")
                print(f"Success: {'✅ PASSED' if test_results['success'] else '❌ FAILED'}")
                
                if test_results.get('error'):
                    print(f"Error: {test_results['error']}")
                
                print("\nStage Results:")
                for stage_name, stage_data in test_results.get('stages', {}).items():
                    print(f"  {stage_name}: {stage_data}")
                
                print("="*80)
                
                return 0 if test_results['success'] else 1
            else:
                # Normal operation mode
                logger.info("Normal operation mode - JAEGIS ecosystem running")
                logger.info("Access the JAEGIS Cockpit at: http://localhost:8090")
                logger.info("Press Ctrl+C to shutdown")
                
                # Keep running until shutdown
                while True:
                    await asyncio.sleep(60)
                    
                    # Periodic health check
                    health = await jaegis_master.health_check()
                    if not health['healthy']:
                        logger.warning("Health check failed - some services may be unhealthy")
    
    except KeyboardInterrupt:
        logger.info("Shutdown requested by user")
    except Exception as e:
        logger.error(f"JAEGIS Master failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)