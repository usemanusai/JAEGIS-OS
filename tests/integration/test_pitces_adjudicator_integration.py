#!/usr/bin/env python3
"""
P.I.T.C.E.S. Command Adjudicator Integration Test
Task 306: P.I.T.C.E.S. Integration with JAEGIS Command Adjudicator

Test suite for P.I.T.C.E.S. integration with JAEGIS Command Adjudicator,
demonstrating automatic workflow selection and intelligent task routing.
"""

import unittest
import asyncio
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.intelligence.pitces_adjudicator_integration import PITCESAdjudicatorIntegration
from core.intelligence.command_adjudicator import CommandAdjudicator

class TestPITCESAdjudicatorIntegration(unittest.TestCase):
    """Test cases for P.I.T.C.E.S. Command Adjudicator Integration"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_adjudicator = Mock()
        self.integration = PITCESAdjudicatorIntegration(self.mock_adjudicator)
    
    def test_integration_initialization(self):
        """Test integration initialization"""
        self.assertFalse(self.integration.initialized)
        self.assertEqual(self.integration.command_adjudicator, self.mock_adjudicator)
        self.assertIsNotNone(self.integration.config)
        self.assertIsNotNone(self.integration.metrics)
    
    @patch('core.pitces.PITCESEngine')
    async def test_async_initialization(self, mock_engine_class):
        """Test async initialization of integration"""
        # Mock P.I.T.C.E.S. engine
        mock_engine = Mock()
        mock_engine.initialize.return_value = True
        mock_engine_class.get_instance.return_value = mock_engine
        
        # Test initialization
        result = await self.integration.initialize()
        
        self.assertTrue(result)
        self.assertTrue(self.integration.initialized)
        mock_engine.initialize.assert_called_once()
    
    def test_workflow_potential_analysis_high(self):
        """Test workflow potential analysis for high-potential commands"""
        text = "create a project to build a web application with team collaboration"
        base_result = {"intent": "create_agent", "confidence": 0.8}
        
        analysis = self.integration._analyze_workflow_potential(text, base_result)
        
        self.assertTrue(analysis["has_workflow_potential"])
        self.assertGreater(analysis["potential_score"], 0.4)
        self.assertIn("project", analysis["matched_keywords"])
        self.assertIn("build", analysis["matched_keywords"])
        self.assertIn("team", analysis["matched_keywords"])
    
    def test_workflow_potential_analysis_low(self):
        """Test workflow potential analysis for low-potential commands"""
        text = "get the current time"
        base_result = {"intent": "unknown", "confidence": 0.2}
        
        analysis = self.integration._analyze_workflow_potential(text, base_result)
        
        self.assertFalse(analysis["has_workflow_potential"])
        self.assertLess(analysis["potential_score"], 0.4)
    
    def test_task_information_extraction(self):
        """Test task information extraction from commands"""
        text = "create a team project to develop a Python API with database integration"
        base_result = {
            "intent": "create_agent",
            "entities": {"goal": "develop API"},
            "confidence": 0.9
        }
        
        task_info = self.integration._extract_task_information(text, base_result)
        
        self.assertEqual(task_info["description"], text)
        self.assertEqual(task_info["intent"], "create_agent")
        self.assertGreater(task_info["team_size"], 1)  # Should detect "team"
        self.assertIn("python", task_info["technologies"])
        self.assertIn("external_api", task_info["integrations"])  # Should detect "integration"
    
    @patch('core.pitces.PITCESEngine')
    def test_enhance_adjudication_with_workflow_potential(self, mock_engine_class):
        """Test adjudication enhancement for commands with workflow potential"""
        # Setup mocks
        mock_engine = Mock()
        mock_nlds = Mock()
        mock_complexity = Mock()
        
        mock_engine.nlds_integration = mock_nlds
        mock_engine.complexity_analyzer = mock_complexity
        
        # Mock N.L.D.S. analysis
        from core.pitces.nlds_integration import NLDSAnalysis
        mock_analysis = NLDSAnalysis(
            logical_score=0.8,
            emotional_score=0.3,
            creative_score=0.2,
            confidence=0.9,
            recommended_mode="sequential_waterfall",
            reasoning="High logical score indicates structured approach"
        )
        mock_nlds.analyze_natural_language.return_value = mock_analysis
        
        # Mock complexity analysis
        mock_complexity.analyze_task.return_value = 0.4
        
        mock_engine_class.get_instance.return_value = mock_engine
        self.integration.pitces_engine = mock_engine
        self.integration.initialized = True
        
        # Test enhancement
        text = "create a systematic project to build documentation system"
        base_result = {
            "intent": "create_agent",
            "confidence": 0.8,
            "entities": {"goal": "build documentation"}
        }
        
        enhanced_result = self.integration.enhance_adjudication(text, base_result)
        
        # Verify enhancement
        self.assertIn("pitces_analysis", enhanced_result)
        pitces_analysis = enhanced_result["pitces_analysis"]
        
        self.assertTrue(pitces_analysis["workflow_potential"])
        self.assertIn("nlds_analysis", pitces_analysis)
        self.assertIn("complexity_analysis", pitces_analysis)
        self.assertIn("workflow_recommendation", pitces_analysis)
        
        # Verify N.L.D.S. analysis
        nlds_result = pitces_analysis["nlds_analysis"]
        self.assertEqual(nlds_result["recommended_mode"], "sequential_waterfall")
        self.assertEqual(nlds_result["confidence"], 0.9)
        
        # Verify workflow recommendation
        workflow_rec = pitces_analysis["workflow_recommendation"]
        self.assertIn("recommended_mode", workflow_rec)
        self.assertIn("reasoning", workflow_rec)
    
    def test_enhance_adjudication_without_workflow_potential(self):
        """Test adjudication enhancement for commands without workflow potential"""
        self.integration.initialized = True
        
        text = "get system status"
        base_result = {
            "intent": "status",
            "confidence": 0.9,
            "success": True
        }
        
        enhanced_result = self.integration.enhance_adjudication(text, base_result)
        
        # Should have P.I.T.C.E.S. analysis but no workflow potential
        self.assertIn("pitces_analysis", enhanced_result)
        self.assertFalse(enhanced_result["pitces_analysis"]["workflow_potential"])
    
    def test_workflow_mode_recommendation_high_confidence(self):
        """Test workflow mode recommendation with high N.L.D.S. confidence"""
        from core.pitces.nlds_integration import NLDSAnalysis
        
        nlds_analysis = NLDSAnalysis(
            logical_score=0.9,
            emotional_score=0.2,
            creative_score=0.1,
            confidence=0.95,
            recommended_mode="sequential_waterfall",
            reasoning="High logical score"
        )
        
        complexity_analysis = {"complexity_score": 0.6, "complexity_category": "medium"}
        task_info = {"intent": "create_agent"}
        
        recommendation = self.integration._recommend_workflow_mode(
            nlds_analysis, complexity_analysis, task_info
        )
        
        self.assertEqual(recommendation["recommended_mode"], "sequential_waterfall")
        self.assertEqual(recommendation["confidence"], 0.95)
        self.assertTrue(recommendation["agreement"])  # N.L.D.S. and complexity agree
    
    def test_workflow_mode_recommendation_low_confidence(self):
        """Test workflow mode recommendation with low N.L.D.S. confidence"""
        from core.pitces.nlds_integration import NLDSAnalysis
        
        nlds_analysis = NLDSAnalysis(
            logical_score=0.4,
            emotional_score=0.4,
            creative_score=0.4,
            confidence=0.6,  # Below threshold
            recommended_mode="hybrid",
            reasoning="Balanced scores"
        )
        
        complexity_analysis = {"complexity_score": 0.8, "complexity_category": "high"}
        task_info = {"intent": "create_agent"}
        
        recommendation = self.integration._recommend_workflow_mode(
            nlds_analysis, complexity_analysis, task_info
        )
        
        # Should fall back to complexity-based recommendation
        self.assertEqual(recommendation["recommended_mode"], "ci_ar")
        self.assertIn("complexity", recommendation["reasoning"].lower())
    
    def test_workflow_actions_generation(self):
        """Test generation of workflow actions"""
        workflow_recommendation = {
            "recommended_mode": "sequential_waterfall",
            "confidence": 0.9,
            "should_execute": True
        }
        
        task_info = {
            "description": "Build documentation system",
            "intent": "create_agent"
        }
        
        actions = self.integration._generate_workflow_actions(workflow_recommendation, task_info)
        
        self.assertIsInstance(actions, list)
        self.assertGreater(len(actions), 0)
        
        # Check for initialization action
        init_action = next((a for a in actions if a["action"] == "initialize_workflow"), None)
        self.assertIsNotNone(init_action)
        self.assertEqual(init_action["workflow_mode"], "sequential_waterfall")
        
        # Check for Sequential Waterfall specific actions
        requirements_action = next((a for a in actions if a["action"] == "requirements_gathering"), None)
        self.assertIsNotNone(requirements_action)
    
    def test_metrics_update(self):
        """Test metrics updating"""
        initial_total = self.integration.metrics["total_commands_processed"]
        initial_successful = self.integration.metrics["successful_integrations"]
        
        # Update with successful processing
        self.integration._update_metrics(True, 1.5)
        
        self.assertEqual(
            self.integration.metrics["total_commands_processed"], 
            initial_total + 1
        )
        self.assertEqual(
            self.integration.metrics["successful_integrations"], 
            initial_successful + 1
        )
        self.assertGreater(self.integration.metrics["average_processing_time"], 0)
    
    def test_integration_status(self):
        """Test integration status retrieval"""
        status = self.integration.get_integration_status()
        
        self.assertIn("initialized", status)
        self.assertIn("config", status)
        self.assertIn("metrics", status)
        self.assertIn("framework_info", status)
        self.assertEqual(status["active_workflows"], 0)

class TestCommandAdjudicatorWithPITCES(unittest.TestCase):
    """Test Command Adjudicator with P.I.T.C.E.S. integration"""
    
    @patch('core.intelligence.command_adjudicator.PITCES_INTEGRATION_AVAILABLE', True)
    @patch('core.intelligence.command_adjudicator.PITCESAdjudicatorIntegration')
    def test_adjudicator_with_pitces_integration(self, mock_integration_class):
        """Test Command Adjudicator initialization with P.I.T.C.E.S."""
        mock_integration = Mock()
        mock_integration_class.return_value = mock_integration
        
        adjudicator = CommandAdjudicator()
        
        self.assertIsNotNone(adjudicator.pitces_integration)
        mock_integration_class.assert_called_once_with(adjudicator)
    
    @patch('core.intelligence.command_adjudicator.PITCES_INTEGRATION_AVAILABLE', False)
    def test_adjudicator_without_pitces_integration(self):
        """Test Command Adjudicator initialization without P.I.T.C.E.S."""
        adjudicator = CommandAdjudicator()
        
        self.assertIsNone(adjudicator.pitces_integration)

def run_integration_demo():
    """Run a demonstration of P.I.T.C.E.S. integration"""
    print("🚀 P.I.T.C.E.S. Command Adjudicator Integration Demo")
    print("=" * 60)
    
    try:
        # Create integration instance
        integration = PITCESAdjudicatorIntegration()
        
        # Test commands with different workflow potentials
        test_commands = [
            "create a project to build a REST API with team collaboration",
            "develop a systematic documentation system with requirements analysis",
            "build an innovative prototype for creative data visualization",
            "get the current system status",
            "set github.token my-secret-token"
        ]
        
        for i, command in enumerate(test_commands, 1):
            print(f"\n{i}. Testing command: '{command}'")
            print("-" * 40)
            
            # Simulate base adjudication result
            base_result = {
                "intent": "create_agent" if "create" in command or "build" in command or "develop" in command else "unknown",
                "confidence": 0.8 if "create" in command else 0.5,
                "entities": {"goal": command.split()[-3:]} if "create" in command else {}
            }
            
            # Analyze workflow potential
            workflow_analysis = integration._analyze_workflow_potential(command, base_result)
            
            print(f"Workflow Potential: {workflow_analysis['has_workflow_potential']}")
            print(f"Potential Score: {workflow_analysis['potential_score']:.3f}")
            
            if workflow_analysis["has_workflow_potential"]:
                print(f"Matched Keywords: {', '.join(workflow_analysis['matched_keywords'])}")
                
                # Extract task information
                task_info = integration._extract_task_information(command, base_result)
                print(f"Estimated Team Size: {task_info['team_size']}")
                print(f"Technologies Detected: {', '.join(task_info['technologies']) if task_info['technologies'] else 'None'}")
        
        print(f"\n✅ P.I.T.C.E.S. Integration Demo completed successfully")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")

if __name__ == '__main__':
    # Run tests
    print("Running P.I.T.C.E.S. Integration Tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    print("\n" + "="*60)
    
    # Run demo
    run_integration_demo()
