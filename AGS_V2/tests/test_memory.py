import pytest
from core.memory import FailureMemoryEngine
import os
import shutil

@pytest.fixture
def memory_engine():
    persist_dir = "./test_memory_data"
    engine = FailureMemoryEngine(persist_directory=persist_dir)
    yield engine
    shutil.rmtree(persist_dir, ignore_errors=True)

def test_memory_logging_and_retrieval(memory_engine):
    task_id = "test_task"
    error_msg = "test_error"
    stack = "test_stack"
    resolution = "test_resolution"

    memory_engine.log_failure(task_id, error_msg, stack, resolution)

    # Check for same exact error
    result = memory_engine.check_for_similar_failure(error_msg, stack)
    assert result["matched"] is True
    assert result["resolution_note"] == resolution

def test_memory_no_match(memory_engine):
    result = memory_engine.check_for_similar_failure("different error", "different stack")
    assert result["matched"] is False
