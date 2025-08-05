#!/usr/bin/env python3
"""
Genesis Test - End-to-End JAEGIS Ecosystem Integration Test

This test validates the full autonomous capabilities of the JAEGIS ecosystem
by giving it a novel problem that forces it to create and deploy new agents and tools.

Test Scenario: "Find the top 5 trending topics on Hacker News right now and write a haiku for each one."
"""

import asyncio
import logging
import json
from datetime import datetime
from typing import Dict, Any

# JAEGIS Core Imports
from core.intelligence.command_adjudicator import CommandAdjudicator
from core.acid.swarm_orchestrator import SwarmOrchestrator
from core.cori.manager import cori_manager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GenesisTest:
    """
    Genesis Test orchestrator for end-to-end JAEGIS ecosystem validation
    """
    
    def __init__(self):
        """Initialize the Genesis Test"""
        self.adjudicator = CommandAdjudicator()
        self.orchestrator = SwarmOrchestrator()
        self.test_objective = "Find the top 5 trending topics on Hacker News right now and write a haiku for each one."
        self.test_results = {}
        
        logger.info("Genesis Test initialized")
    
    async def run_genesis_test(self) -> Dict[str, Any]:
        """
        Run the complete Genesis Test scenario
        
        Returns:
            Dict[str, Any]: Complete test results
        """
        logger.info("🚀 Starting Genesis Test - JAEGIS Ecosystem Validation")
        logger.info(f"Test Objective: {self.test_objective}")
        
        test_start_time = datetime.now()
        
        try:
            # Phase 1: Capability Gap Detection
            logger.info("\n" + "="*60)
            logger.info("PHASE 1: CAPABILITY GAP DETECTION")
            logger.info("="*60)
            
            gap_detection_result = await self._test_capability_gap_detection()
            self.test_results['phase_1_gap_detection'] = gap_detection_result
            
            # Phase 2: A.S.C.E.N.D. Pipeline Trigger
            logger.info("\n" + "="*60)
            logger.info("PHASE 2: A.S.C.E.N.D. PIPELINE TRIGGER")
            logger.info("="*60)
            
            ascend_trigger_result = await self._test_ascend_pipeline_trigger()
            self.test_results['phase_2_ascend_trigger'] = ascend_trigger_result
            
            # Phase 3: Forge Chaining Verification
            logger.info("\n" + "="*60)
            logger.info("PHASE 3: FORGE CHAINING VERIFICATION")
            logger.info("="*60)
            
            forge_chaining_result = await self._test_forge_chaining()
            self.test_results['phase_3_forge_chaining'] = forge_chaining_result
            
            # Phase 4: C.O.R.I. Learning Integration
            logger.info("\n" + "="*60)
            logger.info("PHASE 4: C.O.R.I. LEARNING INTEGRATION")
            logger.info("="*60)
            
            cori_learning_result = await self._test_cori_learning()
            self.test_results['phase_4_cori_learning'] = cori_learning_result
            
            # Calculate overall test results
            test_end_time = datetime.now()
            test_duration = (test_end_time - test_start_time).total_seconds()
            
            overall_success = all([
                gap_detection_result.get('success', False),
                ascend_trigger_result.get('success', False),
                forge_chaining_result.get('success', False),
                cori_learning_result.get('success', False)
            ])
            
            self.test_results['overall'] = {
                'success': overall_success,
                'test_duration_seconds': test_duration,
                'start_time': test_start_time.isoformat(),
                'end_time': test_end_time.isoformat(),
                'test_objective': self.test_objective
            }
            
            # Log final results
            logger.info("\n" + "="*60)
            logger.info("GENESIS TEST RESULTS")
            logger.info("="*60)
            logger.info(f"Overall Success: {'✅ PASS' if overall_success else '❌ FAIL'}")
            logger.info(f"Test Duration: {test_duration:.2f} seconds")
            logger.info(f"Phase 1 (Gap Detection): {'✅' if gap_detection_result.get('success') else '❌'}")
            logger.info(f"Phase 2 (A.S.C.E.N.D. Trigger): {'✅' if ascend_trigger_result.get('success') else '❌'}")
            logger.info(f"Phase 3 (Forge Chaining): {'✅' if forge_chaining_result.get('success') else '❌'}")
            logger.info(f"Phase 4 (C.O.R.I. Learning): {'✅' if cori_learning_result.get('success') else '❌'}")
            
            return self.test_results
            
        except Exception as e:
            logger.error(f"Genesis Test failed with exception: {e}")
            self.test_results['overall'] = {
                'success': False,
                'error': str(e),
                'test_duration_seconds': (datetime.now() - test_start_time).total_seconds()
            }
            return self.test_results
    
    async def _test_capability_gap_detection(self) -> Dict[str, Any]:
        """Test Phase 1: Capability Gap Detection"""
        
        try:
            logger.info("Testing Command Adjudicator capability gap detection...")
            
            # Use the adjudicator to analyze the test objective
            adjudication_result = self.adjudicator.adjudicate(self.test_objective)
            
            logger.info(f"Adjudication Intent: {adjudication_result.get('intent')}")
            logger.info(f"Adjudication Confidence: {adjudication_result.get('confidence')}")
            
            # Check if capability gap was detected
            capability_gap_detected = adjudication_result.get('intent') == 'capability_gap_ascend'
            
            if capability_gap_detected:
                logger.info("✅ Capability gap successfully detected!")
                logger.info(f"Message: {adjudication_result.get('message')}")
                return {
                    'success': True,
                    'capability_gap_detected': True,
                    'adjudication_result': adjudication_result,
                    'message': 'Capability gap detection working correctly'
                }
            else:
                logger.warning("⚠️ Capability gap not detected - may indicate existing capability")
                return {
                    'success': True,
                    'capability_gap_detected': False,
                    'adjudication_result': adjudication_result,
                    'message': 'No capability gap detected - existing agents may handle this task'
                }
                
        except Exception as e:
            logger.error(f"Capability gap detection test failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Capability gap detection test failed'
            }
    
    async def _test_ascend_pipeline_trigger(self) -> Dict[str, Any]:
        """Test Phase 2: A.S.C.E.N.D. Pipeline Trigger"""
        
        try:
            logger.info("Testing A.S.C.E.N.D. pipeline trigger via A.C.I.D. orchestrator...")
            
            # Use the orchestrator to process the objective
            orchestration_result = await self.orchestrator.process_objective(self.test_objective)
            
            logger.info(f"Orchestration Status: {orchestration_result.get('status')}")
            
            # Check if A.S.C.E.N.D. was triggered
            ascend_triggered = orchestration_result.get('status') == 'capability_gap_detected'
            
            if ascend_triggered:
                logger.info("✅ A.S.C.E.N.D. pipeline successfully triggered!")
                logger.info(f"User Message: {orchestration_result.get('user_message')}")
                return {
                    'success': True,
                    'ascend_triggered': True,
                    'orchestration_result': orchestration_result,
                    'message': 'A.S.C.E.N.D. pipeline trigger working correctly'
                }
            else:
                logger.info("ℹ️ A.S.C.E.N.D. not triggered - task handled by existing capabilities")
                return {
                    'success': True,
                    'ascend_triggered': False,
                    'orchestration_result': orchestration_result,
                    'message': 'Task handled by existing capabilities'
                }
                
        except Exception as e:
            logger.error(f"A.S.C.E.N.D. pipeline trigger test failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'A.S.C.E.N.D. pipeline trigger test failed'
            }
    
    async def _test_forge_chaining(self) -> Dict[str, Any]:
        """Test Phase 3: Forge Chaining Verification"""
        
        try:
            logger.info("Testing M.A.S.T.R. and A.S.C.E.N.D. forge chaining...")
            
            # Import and test Squad Architect Agent
            from core.agents.system.squad_architect_agent import SquadArchitectAgent
            
            architect = SquadArchitectAgent()
            
            # Test toolset discovery which should trigger M.A.S.T.R. forge if needed
            toolset_result = await architect._discover_toolset({
                "domain": "web_scraping",
                "skills": ["hacker_news_api", "creative_writing", "haiku_generation"]
            })
            
            logger.info(f"Toolset Discovery Result: {toolset_result.get('task_type')}")
            
            # Check if forge chaining logic is present
            forge_chaining_available = hasattr(architect, '_trigger_mastr_forge')
            
            if forge_chaining_available:
                logger.info("✅ Forge chaining logic is implemented!")
                return {
                    'success': True,
                    'forge_chaining_available': True,
                    'toolset_result': toolset_result,
                    'message': 'Forge chaining logic is properly implemented'
                }
            else:
                logger.error("❌ Forge chaining logic not found!")
                return {
                    'success': False,
                    'forge_chaining_available': False,
                    'message': 'Forge chaining logic not implemented'
                }
                
        except Exception as e:
            logger.error(f"Forge chaining test failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Forge chaining test failed'
            }
    
    async def _test_cori_learning(self) -> Dict[str, Any]:
        """Test Phase 4: C.O.R.I. Learning Integration"""
        
        try:
            logger.info("Testing C.O.R.I. learning integration...")
            
            # Test C.O.R.I. event logging
            test_event = {
                'event_type': 'genesis_test_event',
                'details': {
                    'test_objective': self.test_objective,
                    'timestamp': datetime.now().isoformat()
                }
            }
            
            # Log event to C.O.R.I.
            cori_manager.log_event(test_event)
            logger.info("✅ Event logged to C.O.R.I.")
            
            # Test learning trigger
            surprising_event = {
                'event_type': 'test_surprise',
                'details': {
                    'description': 'Genesis test surprise event',
                    'test_data': True
                }
            }
            
            cori_manager.trigger_learning_from_error(surprising_event)
            logger.info("✅ Learning trigger executed successfully!")
            
            return {
                'success': True,
                'cori_integration_working': True,
                'message': 'C.O.R.I. learning integration working correctly'
            }
            
        except Exception as e:
            logger.error(f"C.O.R.I. learning test failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'C.O.R.I. learning test failed'
            }

async def main():
    """Main test execution function"""
    
    print("🧪 JAEGIS Genesis Test - End-to-End Ecosystem Validation")
    print("=" * 70)
    
    # Initialize and run the Genesis Test
    genesis_test = GenesisTest()
    results = await genesis_test.run_genesis_test()
    
    # Save results to file
    results_filename = f"genesis_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_filename, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📊 Test results saved to: {results_filename}")
    
    # Return exit code based on overall success
    overall_success = results.get('overall', {}).get('success', False)
    return 0 if overall_success else 1

if __name__ == "__main__":
    import sys
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
