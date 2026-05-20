import sys
from unittest.mock import MagicMock

# Mock fastmcp and its tool decorator
class MockMCP:
    def tool(self):
        def decorator(func):
            return func
        return decorator
    def run(self):
        pass

mock_fastmcp = MagicMock()
mock_fastmcp.FastMCP.return_value = MockMCP()
sys.modules["fastmcp"] = mock_fastmcp

import os
from AGS_V2.mcp_server import read_file, write_file

def test_vulnerability():
    # Intended usage: write a file within the current directory
    print("Testing intended usage...")
    result = write_file("test_safe.txt", "hello")
    print(f"Result: {result}")
    if "written successfully" in result:
        print("Intended write SUCCESS")
    else:
        print(f"Intended write FAILED: {result}")

    # Path Traversal: try to write outside the current directory
    print("\nTesting path traversal write...")
    result = write_file("../traversal_write_blocked.txt", "pwned")
    print(f"Result: {result}")

    if "Access denied" in result:
        print("VULNERABILITY FIXED: write_file blocked traversal.")
    else:
        print("VULNERABILITY STILL PRESENT or unexpected result.")
        if os.path.exists("../traversal_write_blocked.txt"):
            print("File actually written outside!")
            os.remove("../traversal_write_blocked.txt")

    # Path Traversal: try to read outside the current directory
    # Create a dummy file in parent to attempt reading
    parent_file = "../traversal_read_blocked.txt"
    try:
        with open(parent_file, "w") as f:
            f.write("secret")

        print("\nTesting path traversal read...")
        result = read_file(parent_file)
        print(f"Result: {result}")

        if "Access denied" in result:
            print("VULNERABILITY FIXED: read_file blocked traversal.")
        elif result == "secret":
             print("VULNERABILITY STILL PRESENT: read_file allowed reading outside.")
        else:
             print(f"Unexpected read result: {result}")
    except PermissionError:
        print("Could not create parent file for test (Permission Denied).")
        # If we can't create it, we can still test if read_file blocks it
        print("\nTesting path traversal read (even if file doesn't exist)...")
        result = read_file(parent_file)
        print(f"Result: {result}")
        if "Access denied" in result:
            print("VULNERABILITY FIXED: read_file blocked traversal.")
    finally:
        if os.path.exists(parent_file):
            os.remove(parent_file)
        if os.path.exists("test_safe.txt"):
            os.remove("test_safe.txt")

if __name__ == "__main__":
    test_vulnerability()
