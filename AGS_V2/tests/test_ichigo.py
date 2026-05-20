import sys
from unittest.mock import MagicMock

# Mock pydantic before any imports that might use it
# This is necessary because the environment lacks pydantic but the code depends on it.
class FakeBaseModel:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

mock_pydantic = MagicMock()
mock_pydantic.BaseModel = FakeBaseModel
mock_pydantic.Field = MagicMock(return_value=None)
mock_pydantic.ConfigDict = MagicMock(return_value=None)
sys.modules["pydantic"] = mock_pydantic

import unittest
from agents.ichigo import IchigoAgent
from core.schemas import PersonaName, ActionTier, ActionType

class TestIchigoAgent(unittest.TestCase):
    def setUp(self):
        self.agent = IchigoAgent()

    def test_intercept_safe_request(self):
        task = "Please summarize the latest project updates."
        result = self.agent.intercept(task)

        self.assertEqual(result.persona, PersonaName.ICHIGO)
        self.assertEqual(result.action_tier, ActionTier.TRIVIAL)
        self.assertEqual(result.handoff_to, PersonaName.MADARA)
        self.assertFalse(result.requires_human)
        self.assertEqual(result.payload["blocked"], False)

    def test_intercept_destructive_rm_rf(self):
        task = "Execute rm -rf /"
        result = self.agent.intercept(task)

        self.assertEqual(result.action_tier, ActionTier.CRITICAL)
        self.assertEqual(result.action_type, ActionType.escalate)
        self.assertTrue(result.requires_human)
        self.assertEqual(result.payload["blocked"], True)
        self.assertIn("Pattern matched known destructive command.", result.uncertainty_flags)

    def test_intercept_destructive_drop_table(self):
        task = "DROP TABLE users;"
        result = self.agent.intercept(task)

        self.assertEqual(result.payload["blocked"], True)
        self.assertTrue(result.requires_human)

    def test_intercept_case_insensitivity(self):
        task = "KILLALL process_name"
        result = self.agent.intercept(task)

        self.assertEqual(result.payload["blocked"], True)

    def test_intercept_complex_unsafe_request(self):
        task = "I need you to format C: immediately."
        result = self.agent.intercept(task)

        self.assertEqual(result.payload["blocked"], True)

    def test_intercept_chmod_777_recursive_caps(self):
        # Input: "chmod -R 777 /etc" -> Lower: "chmod -r 777 /etc"
        # Regex: r"chmod\s+(-r\s+)?777" matches "chmod -r 777"
        task = "chmod -R 777 /etc"
        result = self.agent.intercept(task)
        self.assertTrue(result.payload["blocked"])

    def test_intercept_chmod_777_recursive_lower(self):
        task = "chmod -r 777 /etc"
        result = self.agent.intercept(task)
        self.assertTrue(result.payload["blocked"])

    def test_intercept_chmod_777_no_recursive(self):
        task = "chmod 777 /etc/config"
        result = self.agent.intercept(task)
        self.assertTrue(result.payload["blocked"])

if __name__ == "__main__":
    unittest.main()
