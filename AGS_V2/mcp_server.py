from fastmcp import FastMCP
import os
import subprocess

# Explicitly defining the fastMCP server instance representing local host actions
mcp = FastMCP("AGS_Local_Actuators")

@mcp.tool()
def read_file(path: str) -> str:
    """Reads the complete content of a local file."""
    if not os.path.exists(path):
        return f"Error: File {path} not found."
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

@mcp.tool()
def write_file(path: str, content: str) -> str:
    """Writes content to a file, completely overwriting it."""
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"File {path} written successfully."
    except Exception as e:
        return f"File write failed: {e}"

@mcp.tool()
def run_shell(command: str) -> str:
    """Executes a shell command in the current directory and returns stdout/stderr."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        return f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
    except Exception as e:
        return f"Execution Exception: {e}"

if __name__ == "__main__":
    print("[AGS v2.0] Starting FastMCP Server...")
    mcp.run()
