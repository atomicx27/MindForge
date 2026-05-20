from fastmcp import FastMCP
import os
import subprocess
from pathlib import Path

# Explicitly defining the fastMCP server instance representing local host actions
mcp = FastMCP("AGS_Local_Actuators")

def safe_path(path: str) -> Path:
    """Ensures the path is within the current working directory."""
    base = Path.cwd().resolve()
    target = Path(path).resolve()
    try:
        target.relative_to(base)
    except ValueError:
        raise PermissionError(f"Access denied: {path} is outside the allowed directory.")
    return target

@mcp.tool()
def read_file(path: str) -> str:
    """Reads the complete content of a local file."""
    try:
        target = safe_path(path)
        if not target.exists():
            return f"Error: File {path} not found."
        with open(target, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Read failed: {e}"

@mcp.tool()
def write_file(path: str, content: str) -> str:
    """Writes content to a file, completely overwriting it."""
    try:
        target = safe_path(path)
        os.makedirs(target.parent, exist_ok=True)
        with open(target, 'w', encoding='utf-8') as f:
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
