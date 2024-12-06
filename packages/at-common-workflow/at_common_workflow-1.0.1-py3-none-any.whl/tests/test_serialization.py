import pytest
from src import (
    Workflow, 
    Context, 
    TaskStatus,
    WorkflowException
)
from src.serialization.workflow_serializer import WorkflowSerializer
import tempfile
import os
import json

# Test tasks defined at module level
async def simple_task(context: 'Context'):
    context.set("output", "simple task complete")

async def task_with_params(context: 'Context', multiplier: int):
    value = context.get("input", 0)
    context.set("output", value * multiplier)

async def task_with_deps(context: 'Context'):
    input_data = context.get("input_data")
    context.set("processed_data", f"processed_{input_data}")

async def task_with_error(context: 'Context'):
    raise ValueError("Task error")

async def provider_task(context: 'Context'):
    context.set("input_data", "raw_data")

async def first_task(context: 'Context'):
    first_task.execution_order.append("first")
    context.set("first", "done")

async def second_task(context: 'Context'):
    second_task.execution_order.append("second")
    context.set("second", "done")

# Initialize the execution order list as a class attribute
first_task.execution_order = []
second_task.execution_order = []

@pytest.fixture
def temp_filepath():
    """Fixture to provide a temporary file path."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        filepath = tmp.name
    yield filepath
    # Cleanup after test
    if os.path.exists(filepath):
        os.unlink(filepath)

async def test_simple_workflow_serialization(temp_filepath):
    """Test serialization of a simple workflow with one task."""
    context = Context()
    workflow = Workflow("simple_workflow", context)
    workflow.task(provides={"output"})(simple_task)

    WorkflowSerializer.save_workflow(workflow, temp_filepath)
    loaded_workflow = WorkflowSerializer.load_workflow(temp_filepath, Context())

    assert loaded_workflow.name == workflow.name
    assert len(loaded_workflow.tasks) == 1
    assert "simple_task" in loaded_workflow.tasks

    async for _ in loaded_workflow.execute():
        pass

    assert loaded_workflow.context.get("output") == "simple task complete"

async def test_workflow_with_parameters(temp_filepath):
    context = Context()
    workflow = Workflow("param_workflow", context)
    workflow.task(
        requires={"input"},
        provides={"output"},
        parameters={"multiplier": 2}
    )(task_with_params)

    WorkflowSerializer.save_workflow(workflow, temp_filepath)
    loaded_workflow = WorkflowSerializer.load_workflow(temp_filepath, Context())

    loaded_workflow.context.set("input", 5)
    async for _ in loaded_workflow.execute():
        pass

    assert loaded_workflow.context.get("output") == 10

async def test_workflow_with_dependencies(temp_filepath):
    context = Context()
    workflow = Workflow("dep_workflow", context)

    workflow.task(provides={"input_data"})(provider_task)
    workflow.task(
        requires={"input_data"},
        provides={"processed_data"}
    )(task_with_deps)

    WorkflowSerializer.save_workflow(workflow, temp_filepath)
    loaded_workflow = WorkflowSerializer.load_workflow(temp_filepath, Context())

    async for _ in loaded_workflow.execute():
        pass

    assert loaded_workflow.context.get("processed_data") == "processed_raw_data"

def test_invalid_file_loading():
    with pytest.raises(FileNotFoundError):
        WorkflowSerializer.load_workflow("nonexistent_file.json", Context())

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"invalid json content")
        filepath = tmp.name

    try:
        with pytest.raises(json.JSONDecodeError):
            WorkflowSerializer.load_workflow(filepath, Context())
    finally:
        os.unlink(filepath)

async def test_error_handling_in_loaded_workflow(temp_filepath):
    context = Context()
    workflow = Workflow("error_workflow", context)
    workflow.task()(task_with_error)

    WorkflowSerializer.save_workflow(workflow, temp_filepath)
    loaded_workflow = WorkflowSerializer.load_workflow(temp_filepath, Context())

    with pytest.raises(ValueError, match="Task error"):
        async for _ in loaded_workflow.execute():
            pass

def test_serialized_file_format(temp_filepath):
    context = Context()
    workflow = Workflow("test_workflow", context)
    workflow.task(
        requires={"input"},
        provides={"output"},
        parameters={"multiplier": 2}
    )(task_with_params)

    WorkflowSerializer.save_workflow(workflow, temp_filepath)

    with open(temp_filepath, 'r') as f:
        data = json.load(f)

    assert "name" in data
    assert "tasks" in data
    assert "task_with_params" in data["tasks"]
    
    task_data = data["tasks"]["task_with_params"]
    required_fields = {"name", "parameters", "requires", "provides", 
                      "status", "func_module", "func_name"}
    for field in required_fields:
        assert field in task_data

async def test_multiple_tasks_order(temp_filepath):
    # Reset execution order
    first_task.execution_order = []
    second_task.execution_order = []
    
    context = Context()
    workflow = Workflow("order_workflow", context)

    workflow.task(provides={"first"})(first_task)
    workflow.task(requires={"first"}, provides={"second"})(second_task)

    WorkflowSerializer.save_workflow(workflow, temp_filepath)
    loaded_workflow = WorkflowSerializer.load_workflow(temp_filepath, Context())

    async for _ in loaded_workflow.execute():
        pass

    assert first_task.execution_order == ["first"]
    assert second_task.execution_order == ["second"]