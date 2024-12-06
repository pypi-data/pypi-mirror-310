from typing import Dict, List, Set, Any
from functools import wraps
import asyncio
from .context import Context
from .task import Task
from ..models.types import TaskFunction, TaskStatus, TaskProgressStatus, TaskParameters
from ..utils.validation import validate_dag
from ..utils.logging import setup_logger
from ..models.progress import TaskProgress
import inspect

logger = setup_logger(__name__)

class Workflow:
    """Manages the execution of tasks in a DAG."""
    def __init__(self, name: str, context: Context):
        self.name = name
        self.tasks: Dict[str, Task] = {}
        self.context = context
        logger.info(f"Created workflow: {name}")
    
    def task(
        self,
        requires: Set[str] = None,
        provides: Set[str] = None,
        parameters: TaskParameters = None
    ) -> callable:
        """Decorator to register a task in the workflow."""
        def decorator(func: TaskFunction) -> callable:
            # Add function signature validation
            sig = inspect.signature(func)
            params = list(sig.parameters.keys())
            
            if not params or params[0] != 'context':
                raise ValueError(
                    f"Task function '{func.__name__}' must have 'context' as its first parameter"
                )
                
            # Create and register the task
            task = Task(
                func=func,
                requires=requires,
                provides=provides,
                parameters=parameters
            )
            
            # Check for duplicate provides
            for existing_task in self.tasks.values():
                duplicate_provides = set(task.provides) & set(existing_task.provides)
                if duplicate_provides:
                    raise ValueError(
                        f"Multiple tasks provide the same data: {duplicate_provides}. "
                        f"Tasks: {task.name} and {existing_task.name}"
                    )
            
            self.tasks[task.name] = task
            logger.debug(f"Registered task: {task.name}")
            
            return func
        return decorator
    
    def _get_ready_tasks(self, completed: Set[str]) -> List[Task]:
        """Get tasks whose dependencies are satisfied."""
        ready = []
        for task in self.tasks.values():
            # Check if task is pending
            if task.status != TaskStatus.PENDING:
                continue
                
            # Get all provided data keys from completed tasks AND existing context data
            available_data = set(self.context.keys())
            for completed_task in self.tasks.values():
                if completed_task.name in completed:
                    available_data.update(completed_task.provides)
                    
            # Check if all required data is available
            if task.requires.issubset(available_data):
                ready.append(task)
                
        return ready
    
    async def execute(self) -> None:
        """Execute the workflow and yield progress updates."""
        logger.info(f"Starting workflow execution: {self.name}")
        validate_dag(self.tasks, self.context)
        completed_tasks: Set[str] = set()
        
        while len(completed_tasks) < len(self.tasks):
            ready_tasks = self._get_ready_tasks(completed_tasks)
            if not ready_tasks:
                remaining = [t.name for t in self.tasks.values() 
                           if t.status != TaskStatus.COMPLETED]
                logger.error(f"No tasks ready to execute. Remaining: {remaining}")
                raise RuntimeError(f"No tasks ready to execute. Remaining: {remaining}")
            
            # Yield starting tasks
            for task in ready_tasks:
                yield TaskProgress(task.name, TaskProgressStatus.STARTED)
            
            try:
                tasks = [task.execute(self.context) for task in ready_tasks]
                await asyncio.gather(*tasks)
                
                # Yield completed tasks
                for task in ready_tasks:
                    task.status = TaskStatus.COMPLETED
                    completed_tasks.add(task.name)
                    yield TaskProgress(task.name, TaskProgressStatus.COMPLETED)
                    
            except Exception as e:
                # Yield failed tasks
                for task in ready_tasks:
                    if task.status != TaskStatus.COMPLETED:
                        task.status = TaskStatus.FAILED
                        yield TaskProgress(task.name, TaskProgressStatus.FAILED)
                raise
        
        logger.info(f"Completed workflow execution: {self.name}")
    
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cleanup()
        
    async def cleanup(self):
        """Cleanup workflow resources."""
        self.context.clear()
        # Add any additional cleanup