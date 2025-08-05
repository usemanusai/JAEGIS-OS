#!/usr/bin/env python3
"""
P.I.T.C.E.S. Framework Test Suite
Task 305: P.I.T.C.E.S. Framework Implementation

Comprehensive test suite for P.I.T.C.E.S. framework with >90% coverage requirement.
Tests all components: Engine, Workflow Manager, Complexity Analyzer, Sequential Waterfall,
CI/AR Mode, and N.L.D.S. Integration.
"""

import unittest
import time
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.pitces import PITCESEngine, WorkflowManager, ComplexityAnalyzer
from core.pitces import SequentialWaterfallMode, ContinuousIntegrationARMode, NLDSIntegration
from core.pitces.engine import PITCESState
from core.pitces.workflow_manager import WorkflowMode
from core.pitces.complexity_analyzer import ComplexityFactors
from core.pitces.nlds_integration import NLDSAnalysis, AnalysisDimension

class TestPITCESEngine(unittest.TestCase):
    """Test cases for P.I.T.C.E.S. Engine"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Reset singleton instance for testing
        PITCESEngine._instance = None
        self.engine = PITCESEngine()
    
    def test_singleton_pattern(self):
        """Test singleton pattern implementation"""
        engine1 = PITCESEngine.get_instance()
        engine2 = PITCESEngine.get_instance()
        self.assertIs(engine1, engine2)
    
    def test_engine_initialization(self):
        """Test engine initialization"""
        self.assertEqual(self.engine.state, PITCESState.UNINITIALIZED)
        
        # Mock component initialization
        with patch.object(WorkflowManager, 'initialize', return_value=True), \
             patch.object(ComplexityAnalyzer, 'initialize', return_value=True), \
             patch.object(NLDSIntegration, 'initialize', return_value=True):
            
            result = self.engine.initialize()
            self.assertTrue(result)
            self.assertEqual(self.engine.state, PITCESState.READY)
    
    def test_engine_initialization_failure(self):
        """Test engine initialization failure handling"""
        with patch.object(WorkflowManager, 'initialize', return_value=False):
            result = self.engine.initialize()
            self.assertFalse(result)
            self.assertEqual(self.engine.state, PITCESState.ERROR)
    
    def test_process_task_success(self):
        """Test successful task processing"""
        # Initialize engine
        with patch.object(WorkflowManager, 'initialize', return_value=True), \
             patch.object(ComplexityAnalyzer, 'initialize', return_value=True), \
             patch.object(NLDSIntegration, 'initialize', return_value=True):
            self.engine.initialize()
        
        # Mock component methods
        self.engine.complexity_analyzer.analyze_task = Mock(return_value=0.5)
        self.engine.workflow_manager.select_workflow = Mock(return_value="sequential_waterfall")
        self.engine.workflow_manager.execute_workflow = Mock(return_value={"status": "success"})
        
        task_data = {"id": "test_task", "requirements": ["req1", "req2"]}
        result = self.engine.process_task(task_data)
        
        self.assertEqual(result["status"], "success")
        self.assertIn("metadata", result)
        self.assertEqual(result["metadata"]["workflow_mode"], "sequential_waterfall")
    
    def test_process_task_not_ready(self):
        """Test task processing when engine not ready"""
        task_data = {"id": "test_task"}
        
        with self.assertRaises(RuntimeError):
            self.engine.process_task(task_data)
    
    def test_get_status(self):
        """Test engine status retrieval"""
        status = self.engine.get_status()
        
        self.assertIn("state", status)
        self.assertIn("metrics", status)
        self.assertIn("config", status)
        self.assertEqual(status["state"], PITCESState.UNINITIALIZED.value)

class TestWorkflowManager(unittest.TestCase):
    """Test cases for Workflow Manager"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_engine = Mock()
        self.workflow_manager = WorkflowManager(self.mock_engine)
    
    def test_workflow_manager_initialization(self):
        """Test workflow manager initialization"""
        with patch.object(SequentialWaterfallMode, 'initialize', return_value=True), \
             patch.object(ContinuousIntegrationARMode, 'initialize', return_value=True):
            
            result = self.workflow_manager.initialize()
            self.assertTrue(result)
            self.assertTrue(self.workflow_manager.initialized)
    
    def test_select_workflow_low_complexity(self):
        """Test workflow selection for low complexity"""
        task_data = {"team_size": 2, "timeline_pressure": 0.3}
        
        selected_mode = self.workflow_manager.select_workflow(0.2, task_data)
        self.assertEqual(selected_mode, WorkflowMode.SEQUENTIAL_WATERFALL.value)
    
    def test_select_workflow_high_complexity(self):
        """Test workflow selection for high complexity"""
        task_data = {"team_size": 8, "timeline_pressure": 0.8}
        
        selected_mode = self.workflow_manager.select_workflow(0.9, task_data)
        self.assertEqual(selected_mode, WorkflowMode.CI_AR.value)
    
    def test_select_workflow_medium_complexity_ci_ar(self):
        """Test workflow selection for medium complexity favoring CI/AR"""
        task_data = {
            "team_size": 6,
            "timeline_pressure": 0.8,
            "change_frequency": 0.7,
            "integration_complexity": 0.6
        }
        
        selected_mode = self.workflow_manager.select_workflow(0.5, task_data)
        self.assertEqual(selected_mode, WorkflowMode.CI_AR.value)
    
    def test_select_workflow_medium_complexity_waterfall(self):
        """Test workflow selection for medium complexity favoring Waterfall"""
        task_data = {
            "team_size": 2,
            "timeline_pressure": 0.3,
            "change_frequency": 0.2,
            "integration_complexity": 0.3
        }
        
        selected_mode = self.workflow_manager.select_workflow(0.5, task_data)
        self.assertEqual(selected_mode, WorkflowMode.SEQUENTIAL_WATERFALL.value)
    
    def test_execute_workflow_sequential_waterfall(self):
        """Test workflow execution for Sequential Waterfall"""
        self.workflow_manager.initialized = True
        self.workflow_manager.sequential_waterfall = Mock()
        self.workflow_manager.sequential_waterfall.execute.return_value = {"status": "success"}
        
        task_data = {"id": "test_task"}
        result = self.workflow_manager.execute_workflow("sequential_waterfall", task_data)
        
        self.assertEqual(result["status"], "success")
        self.workflow_manager.sequential_waterfall.execute.assert_called_once_with(task_data)
    
    def test_execute_workflow_ci_ar(self):
        """Test workflow execution for CI/AR"""
        self.workflow_manager.initialized = True
        self.workflow_manager.ci_ar_mode = Mock()
        self.workflow_manager.ci_ar_mode.execute.return_value = {"status": "success"}
        
        task_data = {"id": "test_task"}
        result = self.workflow_manager.execute_workflow("continuous_integration_ar", task_data)
        
        self.assertEqual(result["status"], "success")
        self.workflow_manager.ci_ar_mode.execute.assert_called_once_with(task_data)
    
    def test_execute_workflow_not_initialized(self):
        """Test workflow execution when not initialized"""
        task_data = {"id": "test_task"}
        
        with self.assertRaises(RuntimeError):
            self.workflow_manager.execute_workflow("sequential_waterfall", task_data)

class TestComplexityAnalyzer(unittest.TestCase):
    """Test cases for Complexity Analyzer"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_engine = Mock()
        self.analyzer = ComplexityAnalyzer(self.mock_engine)
        self.analyzer.initialized = True
    
    def test_analyze_task_simple(self):
        """Test complexity analysis for simple task"""
        task_data = {
            "tasks": ["task1"],
            "team_size": 1,
            "timeline_days": 30,
            "technologies": ["python"],
            "integrations": [],
            "risks": []
        }
        
        complexity = self.analyzer.analyze_task(task_data)
        self.assertIsInstance(complexity, float)
        self.assertGreaterEqual(complexity, 0.0)
        self.assertLessEqual(complexity, 1.0)
    
    def test_analyze_task_complex(self):
        """Test complexity analysis for complex task"""
        task_data = {
            "tasks": ["task" + str(i) for i in range(20)],
            "dependency_depth": 5,
            "team_size": 15,
            "timeline_days": 7,
            "technologies": ["python", "javascript", "docker", "kubernetes", "postgresql"],
            "integrations": ["api1", "api2", "api3"],
            "risks": ["risk1", "risk2"],
            "change_frequency": 0.8,
            "testing_requirements": 0.9
        }
        
        complexity = self.analyzer.analyze_task(task_data)
        self.assertGreater(complexity, 0.5)  # Should be high complexity
    
    def test_extract_complexity_factors(self):
        """Test complexity factors extraction"""
        task_data = {
            "tasks": ["task1", "task2"],
            "team_size": 5,
            "timeline_days": 14
        }
        
        factors = self.analyzer._extract_complexity_factors(task_data)
        self.assertIsInstance(factors, ComplexityFactors)
        self.assertEqual(factors.task_count, 2)
        self.assertEqual(factors.team_size, 5)
        self.assertEqual(factors.timeline_days, 14)
    
    def test_calculate_task_complexity(self):
        """Test task complexity calculation"""
        factors = ComplexityFactors(task_count=10)
        complexity = self.analyzer._calculate_task_complexity(factors)
        
        self.assertIsInstance(complexity, float)
        self.assertGreaterEqual(complexity, 0.0)
        self.assertLessEqual(complexity, 1.0)
    
    def test_calculate_team_complexity(self):
        """Test team complexity calculation"""
        # Small team
        factors_small = ComplexityFactors(team_size=2)
        complexity_small = self.analyzer._calculate_team_complexity(factors_small)
        
        # Large team
        factors_large = ComplexityFactors(team_size=15)
        complexity_large = self.analyzer._calculate_team_complexity(factors_large)
        
        self.assertGreater(complexity_large, complexity_small)

class TestSequentialWaterfallMode(unittest.TestCase):
    """Test cases for Sequential Waterfall Mode"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_workflow_manager = Mock()
        self.waterfall = SequentialWaterfallMode(self.mock_workflow_manager)
        self.waterfall.initialized = True
    
    def test_execute_success(self):
        """Test successful Sequential Waterfall execution"""
        task_data = {"id": "test_task", "requirements": ["req1", "req2"]}
        
        result = self.waterfall.execute(task_data)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["workflow_mode"], "sequential_waterfall")
        self.assertIn("phase_results", result)
        self.assertIn("total_duration", result)
    
    def test_execute_phase_requirements(self):
        """Test requirements phase execution"""
        task_data = {"requirements": ["req1", "req2"]}
        
        result = self.waterfall.execute_phase("requirements", task_data)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["phase"], "requirements")
    
    def test_quality_gate_check(self):
        """Test quality gate checking"""
        from core.pitces.sequential_waterfall import PhaseResult, WaterfallPhase
        
        phase_result = PhaseResult(
            phase=WaterfallPhase.REQUIREMENTS,
            status="completed",
            duration=100.0,
            deliverables=["doc1"],
            quality_metrics={"completeness": 0.96, "clarity": 0.92},
            issues=[],
            next_phase_ready=True
        )
        
        result = self.waterfall._check_quality_gate(WaterfallPhase.REQUIREMENTS, phase_result)
        self.assertTrue(result)
    
    def test_quality_gate_failure(self):
        """Test quality gate failure"""
        from core.pitces.sequential_waterfall import PhaseResult, WaterfallPhase
        
        phase_result = PhaseResult(
            phase=WaterfallPhase.REQUIREMENTS,
            status="completed",
            duration=100.0,
            deliverables=["doc1"],
            quality_metrics={"completeness": 0.80, "clarity": 0.85},  # Below threshold
            issues=[],
            next_phase_ready=True
        )
        
        result = self.waterfall._check_quality_gate(WaterfallPhase.REQUIREMENTS, phase_result)
        self.assertFalse(result)

class TestContinuousIntegrationARMode(unittest.TestCase):
    """Test cases for CI/AR Mode"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_workflow_manager = Mock()
        self.ci_ar = ContinuousIntegrationARMode(self.mock_workflow_manager)
        self.ci_ar.initialized = True
    
    def test_plan_sprints(self):
        """Test sprint planning"""
        task_data = {
            "features": ["feature1", "feature2", "feature3", "feature4"]
        }
        
        sprints = self.ci_ar._plan_sprints(task_data)
        
        self.assertIsInstance(sprints, list)
        self.assertGreater(len(sprints), 0)
        self.assertIn("sprint_id", sprints[0])
        self.assertIn("features", sprints[0])
    
    def test_execute_sprint_planning(self):
        """Test sprint planning execution"""
        sprint_plan = {
            "sprint_id": "sprint_1",
            "features": ["feature1", "feature2"],
            "story_points": 6
        }
        task_data = {"id": "test_task"}
        
        result = self.ci_ar._execute_sprint_planning(sprint_plan, task_data)
        
        self.assertEqual(result["phase"], "sprint_planning")
        self.assertTrue(result["success"])
        self.assertEqual(result["planned_features"], ["feature1", "feature2"])
    
    def test_execute_development_phase(self):
        """Test development phase execution"""
        sprint_plan = {
            "features": ["feature1", "feature2"]
        }
        task_data = {"id": "test_task"}
        
        result = self.ci_ar._execute_development_phase(sprint_plan, task_data)
        
        self.assertEqual(result["phase"], "development")
        self.assertTrue(result["success"])
        self.assertEqual(len(result["features_completed"]), 2)
    
    def test_execute_continuous_integration(self):
        """Test CI phase execution"""
        development_result = {
            "features_completed": ["feature1", "feature2"]
        }
        
        result = self.ci_ar._execute_continuous_integration(development_result)
        
        self.assertEqual(result["phase"], "continuous_integration")
        self.assertTrue(result["build_success"])
        self.assertIn("build_time", result)

class TestNLDSIntegration(unittest.TestCase):
    """Test cases for N.L.D.S. Integration"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_engine = Mock()
        self.nlds = NLDSIntegration(self.mock_engine)
        self.nlds.initialized = True
        self.nlds._compile_keyword_patterns()
    
    def test_analyze_logical_text(self):
        """Test analysis of logical text"""
        text = "We need systematic requirements analysis and formal documentation process"
        
        analysis = self.nlds.analyze_natural_language(text)
        
        self.assertIsInstance(analysis, NLDSAnalysis)
        self.assertGreater(analysis.logical_score, analysis.emotional_score)
        self.assertGreater(analysis.logical_score, analysis.creative_score)
    
    def test_analyze_emotional_text(self):
        """Test analysis of emotional text"""
        text = "Our team needs better collaboration and user experience feedback"
        
        analysis = self.nlds.analyze_natural_language(text)
        
        self.assertGreater(analysis.emotional_score, 0.0)
    
    def test_analyze_creative_text(self):
        """Test analysis of creative text"""
        text = "We want to explore innovative design and experimental prototype"
        
        analysis = self.nlds.analyze_natural_language(text)
        
        self.assertGreater(analysis.creative_score, 0.0)
    
    def test_preprocess_text(self):
        """Test text preprocessing"""
        text = "Hello, World! This is a TEST."
        processed = self.nlds._preprocess_text(text)
        
        self.assertEqual(processed, "hello world this is a test")
    
    def test_confidence_threshold(self):
        """Test confidence threshold handling"""
        # Mock low confidence scenario
        with patch.object(self.nlds, '_determine_dominant_dimension', return_value=("logical", 0.5)):
            text = "simple text"
            analysis = self.nlds.analyze_natural_language(text)
            
            self.assertEqual(analysis.recommended_mode, "hybrid")  # Fallback for low confidence

if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestPITCESEngine,
        TestWorkflowManager,
        TestComplexityAnalyzer,
        TestSequentialWaterfallMode,
        TestContinuousIntegrationARMode,
        TestNLDSIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print coverage summary
    print(f"\nTest Results:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    # Exit with appropriate code
    exit_code = 0 if result.wasSuccessful() else 1
    exit(exit_code)
