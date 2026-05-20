import sys
from unittest.mock import MagicMock

# Mock dependencies
class FakeBaseModel:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

mock_pydantic = MagicMock()
mock_pydantic.BaseModel = FakeBaseModel
sys.modules['pydantic'] = mock_pydantic

# Import IchigoAgent
try:
    from agents.ichigo import IchigoAgent
except ImportError:
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from agents.ichigo import IchigoAgent

def test_ichigo():
    agent = IchigoAgent()

    # Test cases: (task, expected_blocked)
    test_cases = [
        ("Safe task", False),
        ("rm -rf /", True),
        ("drop table users", True),
        ("format c:", True),
        ("chmod -r 777", True),
        ("killall python", True),
        ("RM -RF /", True), # case insensitivity check
        ("Just a normal request to delete a file is NOT rm -rf", True),
    ]

    all_passed = True
    for task, expected_blocked in test_cases:
        result = agent.intercept(task)
        is_blocked = result.payload.get("blocked", False)
        if is_blocked == expected_blocked:
            original_print(f"PASS: Task='{task}', Blocked={is_blocked}")
        else:
            original_print(f"FAIL: Task='{task}', Blocked={is_blocked}, Expected={expected_blocked}")
            all_passed = False

    if all_passed:
        original_print("\nAll functional tests passed!")
    else:
        original_print("\nSome functional tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    # Suppress print statements from the agent
    import builtins
    global original_print
    original_print = builtins.print
    builtins.print = lambda *args, **kwargs: None

    try:
        test_ichigo()
    finally:
        builtins.print = original_print
