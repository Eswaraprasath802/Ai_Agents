from mcp.server.mcpserver import MCPServer
from datetime import datetime
import platform
import os

mcp = MCPServer("My Tools")


# 1. Calculator
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


# 2. Text tool
@mcp.tool()
def reverse_text(text: str) -> str:
    """Reverse the given text."""
    return text[::-1]


@mcp.tool()
def count_words(text: str) -> int:
    """Count the number of words."""
    return len(text.split())


# 3. Time tool
@mcp.tool()
def get_time() -> str:
    """Get the current local time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 4. System information
@mcp.tool()
def system_info() -> str:
    """Get basic system information."""
    return (
        f"OS: {platform.system()}\n"
        f"Release: {platform.release()}\n"
        f"Machine: {platform.machine()}\n"
        f"Python: {platform.python_version()}"
    )


# 5. Username
@mcp.tool()
def get_username() -> str:
    """Get the current username."""
    return os.getlogin()


if __name__ == "__main__":
    mcp.run()