"""
Filesystem Tools for Mallku Agents
"""

from .tool_decorator import mcp_tool


@mcp_tool
def list_directory(path: str) -> dict[str, list[str]]:
    """Lists files and directories in a given path."""
    import os

    try:
        entries = os.listdir(path)
        files = [e for e in entries if os.path.isfile(os.path.join(path, e))]
        dirs = [e for e in entries if os.path.isdir(os.path.join(path, e))]
        return {"files": files, "directories": dirs}
    except Exception as e:
        return {"error": str(e)}


@mcp_tool
def read_file(file_path: str) -> dict[str, str]:
    """Reads the content of a file."""
    try:
        with open(file_path) as f:
            content = f.read()
        return {"content": content}
    except Exception as e:
        return {"error": str(e)}


@mcp_tool
def write_file(file_path: str, content: str) -> dict[str, str]:
    """Writes content to a file."""
    try:
        with open(file_path, "w") as f:
            f.write(content)
        return {"status": "success"}
    except Exception as e:
        return {"error": str(e)}
