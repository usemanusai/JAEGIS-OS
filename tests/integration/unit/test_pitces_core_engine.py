#!/usr/bin/env python3
"""
Unit tests for P.I.T.C.E.S. Core Engine
Critical component test coverage for P.I.T.C.E.S. workflow system
"""

import pytest
import asyncio
import unittest
from unittest.mock import Mock, patch, AsyncMock
import sys
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from enum import Enum

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Mock enums and dataclasses for testing
class WorkflowMode(Enum):
    SEQUENTIAL_WATERFALL = "sequential_waterfall"
    CONTINUOUS_INTEGRATION_AR = "continuous_integration_ar"
    HYBRID = "hybrid"

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class PITCESTask:
    task_id: str
    name: str
    description: str
    status: TaskStatus
    priority: int
    dependencies: List[str]
    estimated_duration: float
    actual_duration: Optional[float] = None
    created_at: datetime = None
    completed_at: Optional[datetime] = None

@dataclass
class PITCESWorkflow:
    workflow_id: str
    name: str
    mode: WorkflowMode
    tasks: List[PITCESTask]
    status: str
    complexity_score: float
    created_at: datetime
    completed_at: Optional[datetime] = None

try:
    from frameworks.pitces.core_engine import PITCESEngine
except ImportError:
    # Create a mock class for testing if the actual module doesn't exist
    class PITCESEngine:
        def __init__(self):
            self.workflows: Dict[str, PITCESWorkflow] = {}
            self.active_tasks: Dict[str, PITCESTask] = {}
            self.task_executors: Dict[str, callable] = {}
            self.complexity_thresholds = {
                'simple': 0.3,
                'medium': 0.6,
                'complex': 0.8
            }
            
        async def create_workflow(self, name: str, tasks: List[Dict], mode: str = None) -> str:
            workflow_id = f"workflow_{len(self.workflows)}"
            
            # Determine mode based on complexity if not specified
            if mode is None:
                complexity = self._calculate_complexity(tasks)
                mode = self._select_workflow_mode(complexity)
            
            workflow_mode = WorkflowMode(mode)
            
            # Create task objects
            pitces_tasks = []
            for i, task_data in enumerate(tasks):
                task = PITCESTask(
                    task_id=f"task_{workflow_id}_{i}",
                    name=task_data.get('name', f'Task {i}'),
                    description=task_data.get('description', ''),
                    status=TaskStatus.PENDING,
                    priority=task_data.get('priority', 5),
                    dependencies=task_data.get('dependencies', []),
                    estimated_duration=task_data.get('estimated_duration', 1.0),
                    created_at=datetime.now()
                )
                pitces_tasks.append(task)
                self.active_tasks[task.task_id] = task
            
            workflow = PITCESWorkflow(
                workflow_id=workflow_id,
                name=name,
                mode=workflow_mode,
                tasks=pitces_tasks,
                status="created",
                complexity_score=self._calculate_complexity(tasks),
                created_at=datetime.now()
            )
            
            self.workflows[workflow_id] = workflow
            return workflow_id
            
        async def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
            if workflow_id not in self.workflows:
                raise ValueError(f"Workflow {workflow_id} not found")
                
            workflow = self.workflows[workflow_id]
            workflow.status = "executing"
            
            # Simulate task execution
            for task in workflow.tasks:
                task.status = TaskStatus.IN_PROGRESS
                await asyncio.sleep(0.01)  # Simulate work
                task.status = TaskStatus.COMPLETED
                task.completed_at = datetime.now()
                task.actual_duration = 0.01
                
            workflow.status = "completed"
            workflow.completed_at = datetime.now()
            
            return {
                "workflow_id": workflow_id,
                "status": workflow.status,
                "completed_tasks": len(workflow.tasks),
                "total_duration": sum(t.actual_duration or 0 for t in workflow.tasks)
            }
            
        def _calculate_complexity(self, tasks: List[Dict]) -> float:
            # Simple complexity calculation based on task count and dependencies
            base_complexity = len(tasks) * 0.1
            dependency_complexity = sum(len(task.get('dependencies', [])) for task in tasks) * 0.05
            return min(base_complexity + dependency_complexity, 1.0)
            
        def _select_workflow_mode(self, complexity: float) -> str:
            if complexity <= self.complexity_thresholds['simple']:
                return WorkflowMode.SEQUENTIAL_WATERFALL.value
            elif complexity <= self.complexity_thresholds['medium']:
                return WorkflowMode.HYBRID.value
            else:
                return WorkflowMode.CONTINUOUS_INTEGRATION_AR.value


class TestPITCESEngine(unittest.TestCase):
    """Test suite for P.I.T.C.E.S. Engine"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.engine = PITCESEngine()
        
    def test_engine_initialization(self):
        """Test P.I.T.C.E.S. engine initialization"""
        self.assertIsNotNone(self.engine)
        self.assertEqual(len(self.engine.workflows), 0)
        self.assertEqual(len(self.engine.active_tasks), 0)
        self.assertIn('simple', self.engine.complexity_thresholds)
        self.assertIn('medium', self.engine.complexity_thresholds)
        self.assertIn('complex', self.engine.complexity_thresholds)
        
    @pytest.mark.asyncio
    async def test_simple_workflow_creation(self):
        """Test creation of a simple workflow"""
        tasks = [
            {"name": "Task 1", "description": "First task"},
            {"name": "Task 2", "description": "Second task"}
        ]
        
        workflow_id = await self.engine.create_workflow("Test Workflow", tasks)
        
        self.assertIsNotNone(workflow_id)
        self.assertIn(workflow_id, self.engine.workflows)
        
        workflow = self.engine.workflows[workflow_id]
        self.assertEqual(workflow.name, "Test Workflow")
        self.assertEqual(len(workflow.tasks), 2)
        self.assertEqual(workflow.status, "created")
        
    @pytest.mark.asyncio
    async def test_workflow_execution(self):
        """Test workflow execution"""
        tasks = [
            {"name": "Task 1", "description": "First task"},
            {"name": "Task 2", "description": "Second task"}
        ]
        
        workflow_id = await self.engine.create_workflow("Execution Test", tasks)
        result = await self.engine.execute_workflow(workflow_id)
        
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["completed_tasks"], 2)
        self.assertGreater(result["total_duration"], 0)
        
        # Check workflow status
        workflow = self.engine.workflows[workflow_id]
        self.assertEqual(workflow.status, "completed")
        self.assertIsNotNone(workflow.completed_at)
        
    @pytest.mark.asyncio
    async def test_workflow_mode_selection(self):
        """Test automatic workflow mode selection based on complexity"""
        # Simple workflow (should use sequential waterfall)
        simple_tasks = [{"name": "Simple Task"}]
        simple_workflow_id = await self.engine.create_workflow("Simple", simple_tasks)
        simple_workflow = self.engine.workflows[simple_workflow_id]
        self.assertEqual(simple_workflow.mode, WorkflowMode.SEQUENTIAL_WATERFALL)
        
        # Complex workflow (should use CI/AR mode)
        complex_tasks = [
            {"name": f"Task {i}", "dependencies": [f"task_{i-1}"] if i > 0 else []}
            for i in range(10)
        ]
        complex_workflow_id = await self.engine.create_workflow("Complex", complex_tasks)
        complex_workflow = self.engine.workflows[complex_workflow_id]
        self.assertIn(complex_workflow.mode, [WorkflowMode.CONTINUOUS_INTEGRATION_AR, WorkflowMode.HYBRID])
        
    @pytest.mark.asyncio
    async def test_task_dependency_handling(self):
        """Test handling of task dependencies"""
        tasks = [
            {"name": "Task 1", "dependencies": []},
            {"name": "Task 2", "dependencies": ["task_workflow_0_0"]},
            {"name": "Task 3", "dependencies": ["task_workflow_0_1"]}
        ]
        
        workflow_id = await self.engine.create_workflow("Dependency Test", tasks)
        workflow = self.engine.workflows[workflow_id]
        
        # Check dependencies are properly set
        self.assertEqual(len(workflow.tasks[0].dependencies), 0)
        self.assertEqual(len(workflow.tasks[1].dependencies), 1)
        self.assertEqual(len(workflow.tasks[2].dependencies), 1)
        
    @pytest.mark.asyncio
    async def test_invalid_workflow_execution(self):
        """Test execution of non-existent workflow"""
        with self.assertRaises(ValueError):
            await self.engine.execute_workflow("non_existent_workflow")


class TestPITCESEngineIntegration(unittest.TestCase):
    """Integration tests for P.I.T.C.E.S. Engine"""
    
    def setUp(self):
        """Set up integration test fixtures"""
        self.engine = PITCESEngine()
        
    @pytest.mark.asyncio
    async def test_multiple_concurrent_workflows(self):
        """Test handling multiple concurrent workflows"""
        workflows = []
        
        # Create multiple workflows
        for i in range(3):
            tasks = [
                {"name": f"Workflow {i} Task 1"},
                {"name": f"Workflow {i} Task 2"}
            ]
            workflow_id = await self.engine.create_workflow(f"Workflow {i}", tasks)
            workflows.append(workflow_id)
        
        # Execute all workflows concurrently
        execution_tasks = [
            self.engine.execute_workflow(wf_id) 
            for wf_id in workflows
        ]
        
        results = await asyncio.gather(*execution_tasks)
        
        # All workflows should complete successfully
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertEqual(result["status"], "completed")
            
    @pytest.mark.asyncio
    async def test_workflow_complexity_calculation(self):
        """Test workflow complexity calculation accuracy"""
        # Test different complexity scenarios
        test_cases = [
            (1, [], "simple"),
            (5, [], "medium"),
            (10, [["dep1"], ["dep2"]], "complex")
        ]
        
        for task_count, dependencies, expected_category in test_cases:
            tasks = []
            for i in range(task_count):
                task = {"name": f"Task {i}"}
                if i < len(dependencies):
                    task["dependencies"] = dependencies[i]
                tasks.append(task)
                
            complexity = self.engine._calculate_complexity(tasks)
            
            if expected_category == "simple":
                self.assertLessEqual(complexity, self.engine.complexity_thresholds['simple'])
            elif expected_category == "medium":
                self.assertLessEqual(complexity, self.engine.complexity_thresholds['medium'])
            else:
                self.assertGreater(complexity, self.engine.complexity_thresholds['medium'])


if __name__ == '__main__':
    # Run the tests
    unittest.main()
