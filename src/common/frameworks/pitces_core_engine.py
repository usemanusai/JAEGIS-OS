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
try:
    from core.utils.telemetry_init import get_tracer, get_langfuse_client
    from core.utils.metrics import (
        PITCES_WORKFLOWS_TOTAL,
        PITCES_TASK_DURATION,
        PITCES_WORKFLOW_SUCCESS_RATE
    )
    # JAEGIS Integration
    from core.nlds.natural_language_detection import NLDSProcessor
    from core.aegis.integration_system import get_aegis_system
    
    tracer = get_tracer(__name__)
except ImportError:
    # Fallback for standalone usage
    tracer = None

logger = logging.getLogger(__name__)

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
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4
    URGENT = 5

class ContextType(Enum):
    """Context types for task contexting"""
    TECHNICAL = "technical"
    BUSINESS = "business"
    USER_EXPERIENCE = "user_experience"
    SECURITY = "security"
    PERFORMANCE = "performance"
    COMPLIANCE = "compliance"

@dataclass
class TaskContext:
    """Context information for task execution"""
    context_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    context_type: ContextType = ContextType.TECHNICAL
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class Task:
    """P.I.T.C.E.S. Task Definition"""
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    priority: TaskPriority = TaskPriority.NORMAL
    status: TaskStatus = TaskStatus.PENDING
    
    # Task execution
    executor: Optional[Callable] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    # Context and dependencies
    contexts: List[TaskContext] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    dependents: List[str] = field(default_factory=list)
    
    # Timing and resources
    estimated_duration: Optional[int] = None  # seconds
    actual_duration: Optional[int] = None
    timeout: Optional[int] = None
    retry_count: int = 0
    max_retries: int = 3
    
    # Results and metadata
    result: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

@dataclass
class WorkflowDefinition:
    """P.I.T.C.E.S. Workflow Definition"""
    workflow_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    mode: WorkflowMode = WorkflowMode.AUTO_SELECT
    
    # Tasks and execution
    tasks: Dict[str, Task] = field(default_factory=dict)
    execution_order: List[str] = field(default_factory=list)
    
    # Configuration
    parallel_execution: bool = True
    max_parallel_tasks: int = 5
    failure_strategy: str = "stop_on_critical"  # stop_on_critical, continue, retry_failed
    
    # Context and metadata
    global_context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class WorkflowExecution:
    """P.I.T.C.E.S. Workflow Execution State"""
    execution_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    workflow_id: str = ""
    status: str = "pending"  # pending, running, completed, failed, cancelled
    
    # Execution state
    current_tasks: List[str] = field(default_factory=list)
    completed_tasks: List[str] = field(default_factory=list)
    failed_tasks: List[str] = field(default_factory=list)
    
    # Results and metrics
    results: Dict[str, Any] = field(default_factory=dict)
    metrics: Dict[str, Any] = field(default_factory=dict)
    
    # Timestamps
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # Error handling
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

class PITCESEngine:
    """
    P.I.T.C.E.S. Framework Core Engine
    
    Parallel Integrated Task Contexting Engine System with support for:
    - Sequential Waterfall execution
    - Continuous Integration / Adaptive Response (CI/AR)
    - Hybrid execution modes
    - Intelligent context management
    - JAEGIS v2.2 integration
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize P.I.T.C.E.S. Engine"""
        self.config = config or {}
        self.workflows: Dict[str, WorkflowDefinition] = {}
        self.executions: Dict[str, WorkflowExecution] = {}
        self.task_registry: Dict[str, Callable] = {}
        
        # Integration components
        self.nlds_processor = None
        self.aegis_system = None
        
        # Execution state
        self.running_executions: Dict[str, asyncio.Task] = {}
        self.execution_lock = asyncio.Lock()
        
        # Metrics and monitoring
        self.metrics = {
            'total_workflows': 0,
            'successful_workflows': 0,
            'failed_workflows': 0,
            'total_tasks': 0,
            'successful_tasks': 0,
            'failed_tasks': 0,
            'average_execution_time': 0.0
        }
        
        logger.info("P.I.T.C.E.S. Engine initialized")
    
    async def initialize(self) -> bool:
        """Initialize P.I.T.C.E.S. Engine with integrations"""
        try:
            # Initialize JAEGIS integrations if available
            try:
                self.nlds_processor = NLDSProcessor()
                await self.nlds_processor.initialize()
                
                self.aegis_system = get_aegis_system()
                await self.aegis_system.initialize()
                
                logger.info("JAEGIS integrations initialized successfully")
            except Exception as e:
                logger.warning(f"JAEGIS integrations not available: {e}")
            
            logger.info("P.I.T.C.E.S. Engine initialization complete")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize P.I.T.C.E.S. Engine: {e}")
            return False
    
    def register_task_executor(self, task_type: str, executor: Callable):
        """Register a task executor function"""
        self.task_registry[task_type] = executor
        logger.info(f"Registered task executor for type: {task_type}")
    
    def create_workflow(self, name: str, description: str = "", mode: WorkflowMode = WorkflowMode.AUTO_SELECT) -> WorkflowDefinition:
        """Create a new workflow definition"""
        workflow = WorkflowDefinition(
            name=name,
            description=description,
            mode=mode
        )
        
        self.workflows[workflow.workflow_id] = workflow
        logger.info(f"Created workflow: {name} ({workflow.workflow_id})")
        
        return workflow
    
    def add_task(self, workflow_id: str, task: Task) -> bool:
        """Add a task to a workflow"""
        if workflow_id not in self.workflows:
            logger.error(f"Workflow not found: {workflow_id}")
            return False
        
        workflow = self.workflows[workflow_id]
        workflow.tasks[task.task_id] = task
        
        # Add to execution order if not already present
        if task.task_id not in workflow.execution_order:
            workflow.execution_order.append(task.task_id)
        
        logger.info(f"Added task {task.name} to workflow {workflow.name}")
        return True
    
    def add_task_dependency(self, workflow_id: str, task_id: str, dependency_id: str) -> bool:
        """Add a dependency between tasks"""
        if workflow_id not in self.workflows:
            return False
        
        workflow = self.workflows[workflow_id]
        
        if task_id not in workflow.tasks or dependency_id not in workflow.tasks:
            return False
        
        task = workflow.tasks[task_id]
        dependency = workflow.tasks[dependency_id]
        
        # Add dependency
        if dependency_id not in task.dependencies:
            task.dependencies.append(dependency_id)
        
        # Add dependent
        if task_id not in dependency.dependents:
            dependency.dependents.append(task_id)
        
        logger.info(f"Added dependency: {task.name} depends on {dependency.name}")
        return True
    
    async def execute_workflow(self, workflow_id: str, context: Dict[str, Any] = None) -> WorkflowExecution:
        """Execute a workflow"""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow not found: {workflow_id}")
        
        workflow = self.workflows[workflow_id]
        
        # Create execution instance
        execution = WorkflowExecution(
            workflow_id=workflow_id,
            started_at=datetime.utcnow()
        )
        
        self.executions[execution.execution_id] = execution
        
        try:
            # Update metrics
            self.metrics['total_workflows'] += 1
            
            # Determine execution mode
            execution_mode = await self._determine_execution_mode(workflow, context)
            
            logger.info(f"Starting workflow execution: {workflow.name} in {execution_mode.value} mode")
            
            # Execute based on mode
            if execution_mode == WorkflowMode.SEQUENTIAL_WATERFALL:
                await self._execute_sequential_waterfall(workflow, execution, context)
            elif execution_mode == WorkflowMode.CI_AR:
                await self._execute_ci_ar(workflow, execution, context)
            elif execution_mode == WorkflowMode.HYBRID:
                await self._execute_hybrid(workflow, execution, context)
            else:
                raise ValueError(f"Unsupported execution mode: {execution_mode}")
            
            # Mark as completed
            execution.status = "completed"
            execution.completed_at = datetime.utcnow()
            
            # Update metrics
            self.metrics['successful_workflows'] += 1
            self._update_execution_time_metric(execution)
            
            logger.info(f"Workflow execution completed: {workflow.name}")
            
        except Exception as e:
            execution.status = "failed"
            execution.completed_at = datetime.utcnow()
            execution.errors.append(str(e))
            
            self.metrics['failed_workflows'] += 1
            
            logger.error(f"Workflow execution failed: {workflow.name} - {e}")
            raise
        
        return execution
    
    async def _determine_execution_mode(self, workflow: WorkflowDefinition, context: Dict[str, Any] = None) -> WorkflowMode:
        """Determine the optimal execution mode for a workflow"""
        if workflow.mode != WorkflowMode.AUTO_SELECT:
            return workflow.mode
        
        # Auto-select based on workflow characteristics
        task_count = len(workflow.tasks)
        has_dependencies = any(task.dependencies for task in workflow.tasks.values())
        has_parallel_tasks = workflow.parallel_execution and task_count > 1
        
        # Use NLDS for intelligent mode selection if available
        if self.nlds_processor and context:
            try:
                mode_suggestion = await self._get_nlds_mode_suggestion(workflow, context)
                if mode_suggestion:
                    return mode_suggestion
            except Exception as e:
                logger.warning(f"NLDS mode suggestion failed: {e}")
        
        # Fallback logic
        if has_dependencies and has_parallel_tasks:
            return WorkflowMode.HYBRID
        elif has_dependencies:
            return WorkflowMode.SEQUENTIAL_WATERFALL
        else:
            return WorkflowMode.CI_AR
    
    async def _get_nlds_mode_suggestion(self, workflow: WorkflowDefinition, context: Dict[str, Any]) -> Optional[WorkflowMode]:
        """Get execution mode suggestion from NLDS"""
        if not self.nlds_processor:
            return None
        
        # Prepare context for NLDS analysis
        analysis_context = {
            'workflow_name': workflow.name,
            'workflow_description': workflow.description,
            'task_count': len(workflow.tasks),
            'has_dependencies': any(task.dependencies for task in workflow.tasks.values()),
            'context': context
        }
        
        # Get NLDS suggestion
        suggestion = await self.nlds_processor.suggest_execution_mode(analysis_context)
        
        if suggestion:
            mode_map = {
                'sequential': WorkflowMode.SEQUENTIAL_WATERFALL,
                'parallel': WorkflowMode.CI_AR,
                'hybrid': WorkflowMode.HYBRID
            }
            return mode_map.get(suggestion.lower())
        
        return None
    
    async def _execute_sequential_waterfall(self, workflow: WorkflowDefinition, execution: WorkflowExecution, context: Dict[str, Any] = None):
        """Execute workflow in sequential waterfall mode"""
        execution.status = "running"
        
        # Sort tasks by dependencies
        sorted_tasks = self._topological_sort(workflow.tasks)
        
        for task_id in sorted_tasks:
            task = workflow.tasks[task_id]
            
            try:
                # Execute task
                await self._execute_task(task, workflow, execution, context)
                execution.completed_tasks.append(task_id)
                
            except Exception as e:
                execution.failed_tasks.append(task_id)
                
                # Handle failure based on strategy
                if workflow.failure_strategy == "stop_on_critical" and task.priority in [TaskPriority.CRITICAL, TaskPriority.URGENT]:
                    raise
                elif workflow.failure_strategy == "stop_on_critical":
                    execution.warnings.append(f"Task {task.name} failed but continuing: {e}")
                    continue
                else:
                    raise
    
    async def _execute_ci_ar(self, workflow: WorkflowDefinition, execution: WorkflowExecution, context: Dict[str, Any] = None):
        """Execute workflow in Continuous Integration / Adaptive Response mode"""
        execution.status = "running"
        
        # Get ready tasks (no dependencies or dependencies completed)
        ready_tasks = self._get_ready_tasks(workflow, execution)
        
        # Execute tasks in parallel with adaptive response
        while ready_tasks or execution.current_tasks:
            # Start new tasks up to parallel limit
            while ready_tasks and len(execution.current_tasks) < workflow.max_parallel_tasks:
                task_id = ready_tasks.pop(0)
                task = workflow.tasks[task_id]
                
                # Start task execution
                task_coroutine = self._execute_task(task, workflow, execution, context)
                task_future = asyncio.create_task(task_coroutine)
                
                execution.current_tasks.append(task_id)
                self.running_executions[task_id] = task_future
            
            # Wait for at least one task to complete
            if execution.current_tasks:
                done_tasks = []
                
                # Check for completed tasks
                for task_id in execution.current_tasks[:]:
                    if task_id in self.running_executions:
                        task_future = self.running_executions[task_id]
                        
                        if task_future.done():
                            try:
                                await task_future  # Get result or exception
                                execution.completed_tasks.append(task_id)
                                done_tasks.append(task_id)
                            except Exception as e:
                                execution.failed_tasks.append(task_id)
                                done_tasks.append(task_id)
                                
                                # Handle failure
                                task = workflow.tasks[task_id]
                                if workflow.failure_strategy == "stop_on_critical" and task.priority in [TaskPriority.CRITICAL, TaskPriority.URGENT]:
                                    # Cancel remaining tasks
                                    for running_task_id in execution.current_tasks:
                                        if running_task_id in self.running_executions:
                                            self.running_executions[running_task_id].cancel()
                                    raise
                
                # Remove completed tasks
                for task_id in done_tasks:
                    execution.current_tasks.remove(task_id)
                    if task_id in self.running_executions:
                        del self.running_executions[task_id]
                
                # Get newly ready tasks
                new_ready_tasks = self._get_ready_tasks(workflow, execution)
                ready_tasks.extend(new_ready_tasks)
                
                # Small delay to prevent busy waiting
                if not done_tasks:
                    await asyncio.sleep(0.1)
    
    async def _execute_hybrid(self, workflow: WorkflowDefinition, execution: WorkflowExecution, context: Dict[str, Any] = None):
        """Execute workflow in hybrid mode (combination of sequential and parallel)"""
        execution.status = "running"
        
        # Group tasks by dependency levels
        dependency_levels = self._group_tasks_by_dependency_level(workflow.tasks)
        
        # Execute each level sequentially, but tasks within each level in parallel
        for level, task_ids in dependency_levels.items():
            if not task_ids:
                continue
            
            # Execute tasks in this level in parallel
            level_tasks = []
            for task_id in task_ids:
                task = workflow.tasks[task_id]
                task_coroutine = self._execute_task(task, workflow, execution, context)
                level_tasks.append(task_coroutine)
            
            try:
                # Wait for all tasks in this level to complete
                await asyncio.gather(*level_tasks)
                execution.completed_tasks.extend(task_ids)
                
            except Exception as e:
                # Handle level failure
                for task_id in task_ids:
                    if task_id not in execution.completed_tasks:
                        execution.failed_tasks.append(task_id)
                
                # Check if we should stop
                failed_critical = any(
                    workflow.tasks[task_id].priority in [TaskPriority.CRITICAL, TaskPriority.URGENT]
                    for task_id in execution.failed_tasks
                    if task_id in task_ids
                )
                
                if workflow.failure_strategy == "stop_on_critical" and failed_critical:
                    raise
    
    async def _execute_task(self, task: Task, workflow: WorkflowDefinition, execution: WorkflowExecution, context: Dict[str, Any] = None):
        """Execute a single task"""
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        try:
            # Update metrics
            self.metrics['total_tasks'] += 1
            
            # Prepare task context
            task_context = {
                'task': task,
                'workflow': workflow,
                'execution': execution,
                'global_context': context or {},
                'task_contexts': {ctx.context_id: ctx for ctx in task.contexts}
            }
            
            # Execute task
            if task.executor:
                # Use custom executor
                result = await self._run_task_executor(task.executor, task_context)
            else:
                # Use registered executor
                task_type = task.metadata.get('type', 'default')
                if task_type in self.task_registry:
                    executor = self.task_registry[task_type]
                    result = await self._run_task_executor(executor, task_context)
                else:
                    raise ValueError(f"No executor found for task type: {task_type}")
            
            # Store result
            task.result = result
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.actual_duration = int((task.completed_at - task.started_at).total_seconds())
            
            # Update execution results
            execution.results[task.task_id] = result
            
            # Update metrics
            self.metrics['successful_tasks'] += 1
            
            logger.info(f"Task completed: {task.name}")
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.completed_at = datetime.utcnow()
            
            # Update metrics
            self.metrics['failed_tasks'] += 1
            
            logger.error(f"Task failed: {task.name} - {e}")
            raise
    
    async def _run_task_executor(self, executor: Callable, context: Dict[str, Any]) -> Any:
        """Run a task executor with proper error handling and timeout"""
        task = context['task']
        
        try:
            # Apply timeout if specified
            if task.timeout:
                result = await asyncio.wait_for(executor(context), timeout=task.timeout)
            else:
                result = await executor(context)
            
            return result
            
        except asyncio.TimeoutError:
            raise Exception(f"Task timed out after {task.timeout} seconds")
        except Exception as e:
            # Retry logic
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                logger.warning(f"Task {task.name} failed, retrying ({task.retry_count}/{task.max_retries}): {e}")
                await asyncio.sleep(2 ** task.retry_count)  # Exponential backoff
                return await self._run_task_executor(executor, context)
            else:
                raise
    
    def _topological_sort(self, tasks: Dict[str, Task]) -> List[str]:
        """Perform topological sort on tasks based on dependencies"""
        # Kahn's algorithm
        in_degree = {task_id: 0 for task_id in tasks}
        
        # Calculate in-degrees
        for task in tasks.values():
            for dep_id in task.dependencies:
                if dep_id in in_degree:
                    in_degree[task.task_id] += 1
        
        # Find tasks with no dependencies
        queue = [task_id for task_id, degree in in_degree.items() if degree == 0]
        result = []
        
        while queue:
            task_id = queue.pop(0)
            result.append(task_id)
            
            # Update in-degrees of dependent tasks
            task = tasks[task_id]
            for dependent_id in task.dependents:
                if dependent_id in in_degree:
                    in_degree[dependent_id] -= 1
                    if in_degree[dependent_id] == 0:
                        queue.append(dependent_id)
        
        # Check for cycles
        if len(result) != len(tasks):
            raise ValueError("Circular dependency detected in workflow")
        
        return result
    
    def _get_ready_tasks(self, workflow: WorkflowDefinition, execution: WorkflowExecution) -> List[str]:
        """Get tasks that are ready to execute (dependencies satisfied)"""
        ready_tasks = []
        
        for task_id, task in workflow.tasks.items():
            if (task_id not in execution.completed_tasks and 
                task_id not in execution.failed_tasks and 
                task_id not in execution.current_tasks):
                
                # Check if all dependencies are completed
                dependencies_satisfied = all(
                    dep_id in execution.completed_tasks 
                    for dep_id in task.dependencies
                )
                
                if dependencies_satisfied:
                    ready_tasks.append(task_id)
        
        # Sort by priority
        ready_tasks.sort(key=lambda tid: workflow.tasks[tid].priority.value, reverse=True)
        
        return ready_tasks
    
    def _group_tasks_by_dependency_level(self, tasks: Dict[str, Task]) -> Dict[int, List[str]]:
        """Group tasks by their dependency level"""
        levels = {}
        task_levels = {}
        
        def get_task_level(task_id: str) -> int:
            if task_id in task_levels:
                return task_levels[task_id]
            
            task = tasks[task_id]
            if not task.dependencies:
                level = 0
            else:
                level = max(get_task_level(dep_id) for dep_id in task.dependencies if dep_id in tasks) + 1
            
            task_levels[task_id] = level
            return level
        
        # Calculate levels for all tasks
        for task_id in tasks:
            level = get_task_level(task_id)
            if level not in levels:
                levels[level] = []
            levels[level].append(task_id)
        
        return levels
    
    def _update_execution_time_metric(self, execution: WorkflowExecution):
        """Update average execution time metric"""
        if execution.started_at and execution.completed_at:
            duration = (execution.completed_at - execution.started_at).total_seconds()
            
            current_avg = self.metrics['average_execution_time']
            total_workflows = self.metrics['successful_workflows']
            
            # Calculate new average
            new_avg = ((current_avg * (total_workflows - 1)) + duration) / total_workflows
            self.metrics['average_execution_time'] = new_avg
    
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a workflow"""
        if workflow_id not in self.workflows:
            return None
        
        workflow = self.workflows[workflow_id]
        
        # Find latest execution
        latest_execution = None
        for execution in self.executions.values():
            if execution.workflow_id == workflow_id:
                if not latest_execution or execution.started_at > latest_execution.started_at:
                    latest_execution = execution
        
        return {
            'workflow_id': workflow_id,
            'workflow_name': workflow.name,
            'workflow_description': workflow.description,
            'task_count': len(workflow.tasks),
            'latest_execution': {
                'execution_id': latest_execution.execution_id if latest_execution else None,
                'status': latest_execution.status if latest_execution else 'never_executed',
                'completed_tasks': len(latest_execution.completed_tasks) if latest_execution else 0,
                'failed_tasks': len(latest_execution.failed_tasks) if latest_execution else 0,
                'started_at': latest_execution.started_at.isoformat() if latest_execution and latest_execution.started_at else None,
                'completed_at': latest_execution.completed_at.isoformat() if latest_execution and latest_execution.completed_at else None
            } if latest_execution else None
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get engine metrics"""
        return {
            **self.metrics,
            'active_workflows': len(self.workflows),
            'active_executions': len([e for e in self.executions.values() if e.status == 'running']),
            'success_rate': (
                self.metrics['successful_workflows'] / 
                max(self.metrics['total_workflows'], 1)
            ) * 100,
            'task_success_rate': (
                self.metrics['successful_tasks'] / 
                max(self.metrics['total_tasks'], 1)
            ) * 100
        }


# Factory Functions

def create_pitces_engine(config: Dict[str, Any] = None) -> PITCESEngine:
    """Factory function to create P.I.T.C.E.S. Engine"""
    return PITCESEngine(config)

def create_task(name: str, description: str = "", priority: TaskPriority = TaskPriority.NORMAL, 
               executor: Optional[Callable] = None, **kwargs) -> Task:
    """Factory function to create a task"""
    return Task(
        name=name,
        description=description,
        priority=priority,
        executor=executor,
        **kwargs
    )

def create_task_context(context_type: ContextType, description: str = "", **kwargs) -> TaskContext:
    """Factory function to create task context"""
    return TaskContext(
        context_type=context_type,
        description=description,
        **kwargs
    )


# Example Usage and Default Executors

async def default_task_executor(context: Dict[str, Any]) -> str:
    """Default task executor for demonstration"""
    task = context['task']
    logger.info(f"Executing task: {task.name}")
    
    # Simulate work
    await asyncio.sleep(1)
    
    return f"Task {task.name} completed successfully"

async def example_workflow():
    """Example workflow demonstrating P.I.T.C.E.S. usage"""
    # Create engine
    engine = create_pitces_engine()
    await engine.initialize()
    
    # Register default executor
    engine.register_task_executor('default', default_task_executor)
    
    # Create workflow
    workflow = engine.create_workflow(
        name="Example Workflow",
        description="Demonstration of P.I.T.C.E.S. capabilities",
        mode=WorkflowMode.HYBRID
    )
    
    # Create tasks
    task1 = create_task(
        name="Initialize System",
        description="Initialize the system components",
        priority=TaskPriority.HIGH
    )
    task1.metadata['type'] = 'default'
    
    task2 = create_task(
        name="Process Data",
        description="Process the input data",
        priority=TaskPriority.NORMAL
    )
    task2.metadata['type'] = 'default'
    
    task3 = create_task(
        name="Generate Report",
        description="Generate final report",
        priority=TaskPriority.NORMAL
    )
    task3.metadata['type'] = 'default'
    
    # Add tasks to workflow
    engine.add_task(workflow.workflow_id, task1)
    engine.add_task(workflow.workflow_id, task2)
    engine.add_task(workflow.workflow_id, task3)
    
    # Add dependencies
    engine.add_task_dependency(workflow.workflow_id, task2.task_id, task1.task_id)
    engine.add_task_dependency(workflow.workflow_id, task3.task_id, task2.task_id)
    
    # Execute workflow
    execution = await engine.execute_workflow(workflow.workflow_id)
    
    print(f"Workflow execution completed: {execution.status}")
    print(f"Completed tasks: {len(execution.completed_tasks)}")
    print(f"Failed tasks: {len(execution.failed_tasks)}")
    
    return execution


if __name__ == "__main__":
    # Run example
    asyncio.run(example_workflow())