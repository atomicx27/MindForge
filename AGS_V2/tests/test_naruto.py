import sys
from unittest.mock import MagicMock

# --- Mocking external dependencies ---

# Mock pydantic
pydantic = MagicMock()
class MockBaseModel:
    def __init__(self, **data):
        for key, value in data.items():
            setattr(self, key, value)
    @classmethod
    def model_validate_json(cls, json_data):
        import json
        data = json.loads(json_data)
        return cls(**data)
pydantic.BaseModel = MockBaseModel
pydantic.Field = MagicMock(return_value=None)
pydantic.ConfigDict = MagicMock(return_value=None)
sys.modules['pydantic'] = pydantic

# Mock litellm
litellm = MagicMock()
sys.modules['litellm'] = litellm

# Mock chromadb
chromadb = MagicMock()
sys.modules['chromadb'] = chromadb
sys.modules['chromadb.config'] = MagicMock()

# Mock redis
redis = MagicMock()
sys.modules['redis'] = redis

# Mock sqlmodel
sqlmodel = MagicMock()
sqlmodel.SQLModel = MockBaseModel
sqlmodel.Field = MagicMock(return_value=None)
sys.modules['sqlmodel'] = sqlmodel

# --- Now we can import our modules ---
import unittest
from agents.naruto import NarutoAgent
from core.schemas import AgentResult, PersonaName, ActionTier, ActionType

class TestNarutoRetryFailure(unittest.TestCase):
    def test_retry_loop_exception_path(self):
        # Setup Naruto
        naruto = NarutoAgent()

        # Mock llm_proxy.route_completion to raise an exception
        from core.proxy import llm_proxy
        llm_proxy.route_completion = MagicMock(side_effect=Exception("LLM is down"))

        # Mock failure_memory.log_failure
        from core.memory import failure_memory
        failure_memory.log_failure = MagicMock()
        failure_memory.check_for_similar_failure = MagicMock(return_value={"matched": False})

        # Execute the retry_loop
        task_id = "test-task-123"
        failed_action = "ls -la"
        error_trace = "File not found"

        result = naruto.retry_loop(task_id, failed_action, error_trace)

        # Assertions
        # 1. Verify failure_memory.log_failure was called
        failure_memory.log_failure.assert_called_once()
        args, kwargs = failure_memory.log_failure.call_args
        self.assertEqual(args[0], task_id)
        self.assertEqual(args[1], failed_action)
        self.assertIn(error_trace, args[2])
        self.assertIn("LLM is down", args[2])

        # 2. Verify AgentResult properties
        self.assertEqual(result.task_id, task_id)
        self.assertEqual(result.persona, PersonaName.NARUTO)
        self.assertEqual(result.action_type, ActionType.escalate)
        self.assertTrue(result.requires_human)
        self.assertEqual(result.target, "orchestrator")

if __name__ == "__main__":
    unittest.main()
