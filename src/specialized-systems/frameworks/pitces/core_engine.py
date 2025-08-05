#!/usr/bin/env python3
"""
P.I.T.C.E.S. Framework Core Engine
Parallel Integrated Task Contexting Engine System

A hybrid workflow system with Sequential Waterfall and CI/AR modes,
integrating with JAEGIS v2.2 and N.L.D.S. Tier 0 component.

JAEGIS Enhanced Agent System v2.2 - Brain Protocol Suite v1.0
"""

import asyncio
import logging
import time
from typing import Dict, List, Any, Optional, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import uuid

# J.O.L.T. Observability Stack Integration
from core.utils.telemetry_init import get_tracer, get_langfuse_client
from core.utils.metrics import (
    PITCES_WORKFLOWS_TOTAL,
    PITCES_TASK_DURATION,
    PITCES_WORKFLOW_SUCCESS_RATE
)

# JAEGIS Integration
from core.nlds.natural_language_detection import NLDSProcessor
from core.aegis.integration_system import get_aegis_system

logger = logging.getLogger(__name__)
tracer = get_tracer(__name__)

class WorkflowMode(Enum):
    """P.I.T.C.E.S. Workflow Execution Modes"""
    SEQUENTIAL_WATERFALL = "sequential_waterfall"
    CI_AR = "ci_ar"  # Continuous Integration / Adaptive Response
    HYBRID = "hybrid"
    AUTO_SELECT = "auto_select"

class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    BLOCKED = "blocked"

class TaskPriority(Enum):
    """Task priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class PITCESTask:
    """Individual task in P.I.T.C.E.S. workflow"""
    id: str
    name: str
    description: str
    executor: str  # Component or agent responsible
    dependencies: List[str] = field(default_factory=list)
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    timeout: int = 300  # seconds
    retry_count: int = 0
    max_retries: int = 3
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PITCESWorkflow:
    """P.I.T.C.E.S. Workflow Definition"""
    id: str
    name: str
    description: str
    mode: WorkflowMode
    tasks: List[PITCESTask]
    context: Dict[str, Any] = field(default_factory=dict)
    complexity_score: float = 0.0
    estimated_duration: int = 0  # seconds
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: str = "created"
    success_rate: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

class PITCESEngine:
    """
    P.I.T.C.E.S. Core Engine
    
    Manages parallel integrated task contexting with intelligent workflow selection
    based on project complexity metrics and N.L.D.S. analysis.
    """
    
    def __init__(self):
        self.workflows: Dict[str, PITCESWorkflow] = {}
        self.active_tasks: Dict[str, PITCESTask] = {}
        self.task_executors: Dict[str, Callable] = {}
        self.nlds_processor = NLDSProcessor()
        self.aegis_system = get_aegis_system()
        self.langfuse_client = get_langfuse_client()
        
        # Workflow selection thresholds
        self.complexity_thresholds = {
            'simple': 0.3,
            'medium': 0.6,
            'complex': 0.8
        }
        
        self._register_default_executors()
        logger.info("🔧 P.I.T.C.E.S. Engine initialized")

    def _register_default_executors(self):
        """Register default task executors"""
        self.task_executors.update({
            'acid_code_generation': self._execute_acid_task,
            'aura_ui_design': self._execute_aura_task,
            'phalanx_app_creation': self._execute_phalanx_task,
            'odin_development_support': self._execute_odin_task,
            'analysis': self._execute_analysis_task,
            'validation': self._execute_validation_task,
            'deployment': self._execute_deployment_task,
            'testing': self._execute_testing_task
        })

    async def create_workflow(
        self,
        name: str,
        description: str,
        tasks: List[Dict[str, Any]],
        mode: Optional[WorkflowMode] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create a new P.I.T.C.E.S. workflow
        
        Args:
            name: Workflow name
            description: Workflow description
            tasks: List of task definitions
            mode: Execution mode (auto-selected if None)
            context: Additional context for workflow
            
        Returns:
            Workflow ID
        """
        workflow_id = str(uuid.uuid4())
        
        with tracer.start_as_current_span("pitces_workflow_creation") as span:
            span.set_attribute("workflow.id", workflow_id)
            span.set_attribute("workflow.name", name)
            
            try:
                # Convert task definitions to PITCESTask objects
                pitces_tasks = []
                for task_def in tasks:
                    task = PITCESTask(
                        id=task_def.get('id', str(uuid.uuid4())),
                        name=task_def['name'],
                        description=task_def['description'],
                        executor=task_def['executor'],
                        dependencies=task_def.get('dependencies', []),
                        inputs=task_def.get('inputs', {}),
                        priority=TaskPriority(task_def.get('priority', 'medium')),
                        timeout=task_def.get('timeout', 300),
                        max_retries=task_def.get('max_retries', 3),
                        metadata=task_def.get('metadata', {})
                    )
                    pitces_tasks.append(task)
                
                # Analyze complexity and select mode if not specified
                complexity_score = self._calculate_complexity(pitces_tasks, context or {})
                if mode is None:
                    mode = self._select_optimal_mode(complexity_score, description)
                
                # Estimate duration
                estimated_duration = self._estimate_workflow_duration(pitces_tasks)
                
                # Create workflow
                workflow = PITCESWorkflow(
                    id=workflow_id,
                    name=name,
                    description=description,
                    mode=mode,
                    tasks=pitces_tasks,
                    context=context or {},
                    complexity_score=complexity_score,
                    estimated_duration=estimated_duration,
                    metadata={
                        'task_count': len(pitces_tasks),
                        'auto_selected_mode': mode if mode else True
                    }
                )
                
                self.workflows[workflow_id] = workflow
                
                # Record metrics
                PITCES_WORKFLOWS_TOTAL.labels(
                    mode=mode.value,
                    complexity=self._get_complexity_category(complexity_score)
                ).inc()
                
                logger.info(f"✅ P.I.T.C.E.S. workflow created: {name} ({workflow_id})")
                return workflow_id
                
            except Exception as e:
                logger.error(f"❌ Failed to create P.I.T.C.E.S. workflow: {e}")
                raise

    def _calculate_complexity(self, tasks: List[PITCESTask], context: Dict[str, Any]) -> float:
        """Calculate workflow complexity score (0.0 - 1.0)"""
        complexity = 0.0
        
        # Task count factor
        task_count_factor = min(len(tasks) / 20, 1.0) * 0.3
        complexity += task_count_factor
        
        # Dependency complexity
        total_dependencies = sum(len(task.dependencies) for task in tasks)
        dependency_factor = min(total_dependencies / (len(tasks) * 3), 1.0) * 0.2
        complexity += dependency_factor
        
        # Executor diversity
        unique_executors = len(set(task.executor for task in tasks))
        executor_factor = min(unique_executors / 8, 1.0) * 0.2
        complexity += executor_factor
        
        # Priority distribution
        high_priority_tasks = sum(1 for task in tasks if task.priority in [TaskPriority.HIGH, TaskPriority.CRITICAL])
        priority_factor = min(high_priority_tasks / len(tasks), 1.0) * 0.15
        complexity += priority_factor
        
        # Context complexity
        context_factor = min(len(context) / 10, 1.0) * 0.15
        complexity += context_factor
        
        return min(complexity, 1.0)

    def _select_optimal_mode(self, complexity_score: float, description: str) -> WorkflowMode:
        """Select optimal workflow mode based on complexity and N.L.D.S. analysis"""
        try:
            # Use N.L.D.S. to analyze description
            nlds_result = self.nlds_processor.analyze_text(description)
            
            # Simple workflows -> Sequential Waterfall
            if complexity_score < self.complexity_thresholds['simple']:
                return WorkflowMode.SEQUENTIAL_WATERFALL
            
            # Complex workflows with high creative/emotional content -> CI/AR
            if (complexity_score > self.complexity_thresholds['complex'] and 
                nlds_result.get('creative_score', 0) > 0.7):
                return WorkflowMode.CI_AR
            
            # Medium complexity -> Hybrid
            if complexity_score < self.complexity_thresholds['complex']:
                return WorkflowMode.HYBRID
            
            # Default to CI/AR for complex workflows
            return WorkflowMode.CI_AR
            
        except Exception as e:
            logger.warning(f"⚠️ Mode selection fallback due to error: {e}")
            return WorkflowMode.HYBRID

    def _estimate_workflow_duration(self, tasks: List[PITCESTask]) -> int:
        """Estimate workflow duration in seconds"""
        total_duration = 0
        
        for task in tasks:
            # Base duration from timeout
            base_duration = task.timeout
            
            # Adjust based on priority
            if task.priority == TaskPriority.CRITICAL:
                base_duration *= 1.5
            elif task.priority == TaskPriority.HIGH:
                base_duration *= 1.2
            
            # Add retry overhead
            retry_overhead = base_duration * 0.1 * task.max_retries
            
            total_duration += base_duration + retry_overhead
        
        # Adjust for parallelization potential
        parallelization_factor = 0.7  # Assume 30% time savings from parallel execution
        return int(total_duration * parallelization_factor)

    def _get_complexity_category(self, score: float) -> str:
        """Get complexity category from score"""
        if score < self.complexity_thresholds['simple']:
            return 'simple'
        elif score < self.complexity_thresholds['medium']:
            return 'medium'
        elif score < self.complexity_thresholds['complex']:
            return 'complex'
        else:
            return 'very_complex'

    async def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """
        Execute a P.I.T.C.E.S. workflow
        
        Args:
            workflow_id: ID of workflow to execute
            
        Returns:
            Execution results
        """
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        with tracer.start_as_current_span("pitces_workflow_execution") as span:
            span.set_attribute("workflow.id", workflow_id)
            span.set_attribute("workflow.mode", workflow.mode.value)
            span.set_attribute("workflow.task_count", len(workflow.tasks))
            
            start_time = time.time()
            workflow.started_at = datetime.now()
            workflow.status = "running"
            
            try:
                # Execute based on mode
                if workflow.mode == WorkflowMode.SEQUENTIAL_WATERFALL:
                    results = await self._execute_sequential_waterfall(workflow)
                elif workflow.mode == WorkflowMode.CI_AR:
                    results = await self._execute_ci_ar(workflow)
                elif workflow.mode == WorkflowMode.HYBRID:
                    results = await self._execute_hybrid(workflow)
                else:
                    raise ValueError(f"Unsupported workflow mode: {workflow.mode}")
                
                # Calculate success metrics
                completed_tasks = sum(1 for task in workflow.tasks if task.status == TaskStatus.COMPLETED)
                workflow.success_rate = completed_tasks / len(workflow.tasks)
                workflow.completed_at = datetime.now()
                workflow.status = "completed" if workflow.success_rate > 0.8 else "partial"
                
                # Record metrics
                duration = time.time() - start_time
                PITCES_TASK_DURATION.labels(
                    mode=workflow.mode.value,
                    status=workflow.status
                ).observe(duration)
                
                PITCES_WORKFLOW_SUCCESS_RATE.labels(
                    mode=workflow.mode.value
                ).set(workflow.success_rate)
                
                logger.info(f"✅ P.I.T.C.E.S. workflow {workflow_id} completed with {workflow.success_rate:.2%} success rate")
                
                return {
                    'workflow_id': workflow_id,
                    'status': workflow.status,
                    'success_rate': workflow.success_rate,
                    'duration': duration,
                    'results': results,
                    'task_results': {task.id: task.outputs for task in workflow.tasks}
                }
                
            except Exception as e:
                workflow.status = "failed"
                workflow.completed_at = datetime.now()
                
                duration = time.time() - start_time
                PITCES_TASK_DURATION.labels(
                    mode=workflow.mode.value,
                    status="failed"
                ).observe(duration)
                
                logger.error(f"❌ P.I.T.C.E.S. workflow {workflow_id} failed: {e}")
                raise

    async def _execute_sequential_waterfall(self, workflow: PITCESWorkflow) -> Dict[str, Any]:
        """Execute workflow in sequential waterfall mode"""
        results = {}
        
        # Build dependency graph
        task_order = self._resolve_dependencies(workflow.tasks)
        
        for task in task_order:
            try:
                task_result = await self._execute_task(task, workflow.context)
                results[task.id] = task_result
                
                # Update workflow context with task outputs
                workflow.context.update(task.outputs)
                
            except Exception as e:
                logger.error(f"❌ Task {task.id} failed in sequential mode: {e}")
                task.status = TaskStatus.FAILED
                task.error_message = str(e)
                
                # Stop execution on failure in waterfall mode
                break
        
        return results

    async def _execute_ci_ar(self, workflow: PITCESWorkflow) -> Dict[str, Any]:
        """Execute workflow in CI/AR (Continuous Integration / Adaptive Response) mode"""
        results = {}
        
        # Group tasks by dependency level for parallel execution
        task_levels = self._group_tasks_by_level(workflow.tasks)
        
        for level, tasks in task_levels.items():
            # Execute tasks in parallel within each level
            level_tasks = []
            for task in tasks:
                level_tasks.append(self._execute_task_with_retry(task, workflow.context))
            
            # Wait for all tasks in this level to complete
            level_results = await asyncio.gather(*level_tasks, return_exceptions=True)
            
            # Process results and update context
            for i, result in enumerate(level_results):
                task = tasks[i]
                if isinstance(result, Exception):
                    logger.error(f"❌ Task {task.id} failed in CI/AR mode: {result}")
                    task.status = TaskStatus.FAILED
                    task.error_message = str(result)
                else:
                    results[task.id] = result
                    workflow.context.update(task.outputs)
        
        return results

    async def _execute_hybrid(self, workflow: PITCESWorkflow) -> Dict[str, Any]:
        """Execute workflow in hybrid mode (combination of sequential and parallel)"""
        results = {}
        
        # Identify critical path and parallel branches
        critical_tasks, parallel_tasks = self._identify_critical_path(workflow.tasks)
        
        # Execute critical path sequentially
        for task in critical_tasks:
            try:
                task_result = await self._execute_task(task, workflow.context)
                results[task.id] = task_result
                workflow.context.update(task.outputs)
            except Exception as e:
                logger.error(f"❌ Critical task {task.id} failed: {e}")
                task.status = TaskStatus.FAILED
                task.error_message = str(e)
        
        # Execute parallel tasks concurrently
        if parallel_tasks:
            parallel_task_coroutines = [
                self._execute_task_with_retry(task, workflow.context) 
                for task in parallel_tasks
            ]
            
            parallel_results = await asyncio.gather(*parallel_task_coroutines, return_exceptions=True)
            
            for i, result in enumerate(parallel_results):
                task = parallel_tasks[i]
                if isinstance(result, Exception):
                    logger.error(f"❌ Parallel task {task.id} failed: {result}")
                    task.status = TaskStatus.FAILED
                    task.error_message = str(result)
                else:
                    results[task.id] = result
                    workflow.context.update(task.outputs)
        
        return results

    async def _execute_task(self, task: PITCESTask, context: Dict[str, Any]) -> Any:
        """Execute a single task"""
        task.started_at = datetime.now()
        task.status = TaskStatus.RUNNING
        
        try:
            # Get executor function
            executor = self.task_executors.get(task.executor)
            if not executor:
                raise ValueError(f"Unknown executor: {task.executor}")
            
            # Execute task with timeout
            result = await asyncio.wait_for(
                executor(task, context),
                timeout=task.timeout
            )
            
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            task.outputs.update(result if isinstance(result, dict) else {'result': result})
            
            return result
            
        except asyncio.TimeoutError:
            task.status = TaskStatus.FAILED
            task.error_message = f"Task timed out after {task.timeout} seconds"
            raise
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error_message = str(e)
            raise

    async def _execute_task_with_retry(self, task: PITCESTask, context: Dict[str, Any]) -> Any:
        """Execute task with retry logic"""
        for attempt in range(task.max_retries + 1):
            try:
                return await self._execute_task(task, context)
            except Exception as e:
                task.retry_count = attempt + 1
                
                if attempt < task.max_retries:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.warning(f"⚠️ Task {task.id} failed (attempt {attempt + 1}), retrying in {wait_time}s: {e}")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"❌ Task {task.id} failed after {task.max_retries + 1} attempts: {e}")
                    raise

    # Task executor implementations
    async def _execute_acid_task(self, task: PITCESTask, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute A.C.I.D. task"""
        from core.aegis.integration_system import process_aegis_request
        
        response = await process_aegis_request(
            component="acid",
            request_type="code_generation",
            payload=task.inputs,
            priority=task.priority.value
        )
        
        if response.success:
            return response.data
        else:
            raise Exception(response.error)

    async def _execute_aura_task(self, task: PITCESTask, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute A.U.R.A. task"""
        from core.aegis.integration_system import process_aegis_request
        
        response = await process_aegis_request(
            component="aura",
            request_type="ui_design",
            payload=task.inputs,
            priority=task.priority.value
        )
        
        if response.success:
            return response.data
        else:
            raise Exception(response.error)

    async def _execute_phalanx_task(self, task: PITCESTask, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute P.H.A.L.A.N.X. task"""
        from core.aegis.integration_system import process_aegis_request
        
        response = await process_aegis_request(
            component="phalanx",
            request_type="app_creation",
            payload=task.inputs,
            priority=task.priority.value
        )
        
        if response.success:
            return response.data
        else:
            raise Exception(response.error)

    async def _execute_odin_task(self, task: PITCESTask, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute O.D.I.N. task"""
        from core.aegis.integration_system import process_aegis_request
        
        response = await process_aegis_request(
            component="odin",
            request_type="development_support",
            payload=task.inputs,
            priority=task.priority.value
        )
        
        if response.success:
            return response.data
        else:
            raise Exception(response.error)

    async def _execute_analysis_task(self, task: PITCESTask, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute analysis task"""
        # Implement analysis logic
        return {"analysis_result": "completed", "insights": []}

    async def _execute_validation_task(self, task: PITCESTask, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute validation task"""
        # Implement validation logic
        return {"validation_result": "passed", "issues": []}

    async def _execute_deployment_task(self, task: PITCESTask, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute deployment task"""
        # Implement deployment logic
        return {"deployment_result": "success", "url": "https://example.com"}

    async def _execute_testing_task(self, task: PITCESTask, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute testing task"""
        # Implement testing logic
        return {"test_result": "passed", "coverage": 95}

    def _resolve_dependencies(self, tasks: List[PITCESTask]) -> List[PITCESTask]:
        """Resolve task dependencies and return execution order"""
        # Simple topological sort implementation
        task_map = {task.id: task for task in tasks}
        visited = set()
        result = []
        
        def visit(task_id: str):
            if task_id in visited:
                return
            
            task = task_map.get(task_id)
            if not task:
                return
            
            for dep_id in task.dependencies:
                visit(dep_id)
            
            visited.add(task_id)
            result.append(task)
        
        for task in tasks:
            visit(task.id)
        
        return result

    def _group_tasks_by_level(self, tasks: List[PITCESTask]) -> Dict[int, List[PITCESTask]]:
        """Group tasks by dependency level for parallel execution"""
        task_map = {task.id: task for task in tasks}
        levels = {}
        task_levels = {}
        
        def get_level(task_id: str) -> int:
            if task_id in task_levels:
                return task_levels[task_id]
            
            task = task_map.get(task_id)
            if not task or not task.dependencies:
                task_levels[task_id] = 0
                return 0
            
            max_dep_level = max(get_level(dep_id) for dep_id in task.dependencies)
            task_levels[task_id] = max_dep_level + 1
            return max_dep_level + 1
        
        for task in tasks:
            level = get_level(task.id)
            if level not in levels:
                levels[level] = []
            levels[level].append(task)
        
        return levels

    def _identify_critical_path(self, tasks: List[PITCESTask]) -> tuple[List[PITCESTask], List[PITCESTask]]:
        """Identify critical path and parallel tasks"""
        # Simplified critical path identification
        # In a real implementation, this would use more sophisticated algorithms
        
        critical_tasks = [task for task in tasks if task.priority in [TaskPriority.CRITICAL, TaskPriority.HIGH]]
        parallel_tasks = [task for task in tasks if task not in critical_tasks]
        
        return critical_tasks, parallel_tasks

    async def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get workflow execution status"""
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        return {
            'id': workflow.id,
            'name': workflow.name,
            'status': workflow.status,
            'mode': workflow.mode.value,
            'complexity_score': workflow.complexity_score,
            'success_rate': workflow.success_rate,
            'task_count': len(workflow.tasks),
            'completed_tasks': sum(1 for task in workflow.tasks if task.status == TaskStatus.COMPLETED),
            'failed_tasks': sum(1 for task in workflow.tasks if task.status == TaskStatus.FAILED),
            'estimated_duration': workflow.estimated_duration,
            'actual_duration': (
                (workflow.completed_at - workflow.started_at).total_seconds()
                if workflow.started_at and workflow.completed_at else None
            ),
            'created_at': workflow.created_at.isoformat(),
            'started_at': workflow.started_at.isoformat() if workflow.started_at else None,
            'completed_at': workflow.completed_at.isoformat() if workflow.completed_at else None
        }

# Global P.I.T.C.E.S. instance
_pitces_instance = None

def get_pitces_engine() -> PITCESEngine:
    """Get global P.I.T.C.E.S. Engine instance"""
    global _pitces_instance
    if _pitces_instance is None:
        _pitces_instance = PITCESEngine()
    return _pitces_instance
