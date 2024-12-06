from typing import List, Set, Dict, Any
import asyncio
from ..models.types import TaskStatus, TaskFunction, TaskParameters
from ..utils.logging import setup_logger
from .context import Context
import inspect

logger = setup_logger(__name__)

class Task:
    """Represents a single task in the workflow."""
    def __init__(
        self,
        func: TaskFunction,
        parameters: TaskParameters = None,
        requires: Set[str] = None,
        provides: Set[str] = None
    ):
        self.name: str = func.__name__
        self.func: TaskFunction = func
        self.parameters: TaskParameters = parameters or {}
        self.requires: Set[str] = requires or set()
        self.provides: Set[str] = provides or set()
        self.status: TaskStatus = TaskStatus.PENDING
    
    async def execute(self, context: Context) -> None:
        """Execute the task function."""
        try:
            self.status = TaskStatus.RUNNING
            logger.info(f"Starting task: {self.name}")
            
            if not asyncio.iscoroutinefunction(self.func):
                raise ValueError(f"Task {self.name} must be an async function")
            
            sig = inspect.signature(self.func)
            for param_name, param in sig.parameters.items():
                if param_name not in ['self', 'context']:  # Skip self and context parameters
                    if param.default == inspect.Parameter.empty and param_name not in self.parameters:
                        raise ValueError(f"Required parameter '{param_name}' not provided for task '{self.name}'")
            
            await self.func(context, **self.parameters)
            
            self.status = TaskStatus.COMPLETED
            logger.info(f"Completed task: {self.name}")
            
        except Exception as e:
            self.status = TaskStatus.FAILED
            logger.error(f"Task {self.name} failed: {str(e)}")
            raise