"""
Tool Decorator for Mallku Agents
"""


def mcp_tool(func):
    """A simple decorator to mark a function as an MCP tool."""

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
