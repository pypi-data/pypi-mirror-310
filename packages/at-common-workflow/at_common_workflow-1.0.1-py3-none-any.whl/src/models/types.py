from enum import Enum
from typing import Any, Dict, List, Set, Callable

class TaskStatus(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class TaskProgressStatus(Enum):
    STARTED = "STARTED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

TaskParameters = Dict[str, Any]

TaskFunction = Callable[['Context'], Any]