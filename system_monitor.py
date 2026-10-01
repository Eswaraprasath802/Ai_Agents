import os
import time
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("System Monitor")


@mcp.tool()
def get_uptime() -> str:
    """Get Linux system uptime."""
    with open("/proc/uptime") as f:
        seconds = float(f.read().split()[0])

    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)

    return f"{days}d {hours}h {minutes}m"


@mcp.tool()
def get_cpu_info() -> str:
    """Get CPU count and CPU statistics."""
    cpu_count = os.cpu_count()

    with open("/proc/loadavg") as f:
        load = f.read().strip()

    return f"""
CPU cores: {cpu_count}
Load average: {load}
"""


@mcp.tool()
def get_memory_info() -> str:
    """Get Linux memory information."""
    memory = {}

    with open("/proc/meminfo") as f:
        for line in f:
            key, value = line.split(":", 1)

            if key in ["MemTotal", "MemAvailable", "SwapTotal", "SwapFree"]:
                memory[key] = value.strip()

    return "\n".join(
        f"{key}: {value}"
        for key, value in memory.items()
    )


@mcp.tool()
def system_status() -> str:
    """Get overall Linux system status."""

    with open("/proc/uptime") as f:
        uptime = float(f.read().split()[0])

    with open("/proc/loadavg") as f:
        load = f.read().split()

    memory = {}

    with open("/proc/meminfo") as f:
        for line in f:
            key, value = line.split(":", 1)

            if key in ["MemTotal", "MemAvailable"]:
                memory[key] = value.strip()

    return f"""
Linux System Status
===================

Uptime:
{uptime:.0f} seconds

CPU:
{os.cpu_count()} cores

Load Average:
1 min  : {load[0]}
5 min  : {load[1]}
15 min : {load[2]}

Memory:
Total     : {memory.get("MemTotal")}
Available : {memory.get("MemAvailable")}
"""


if __name__ == "__main__":
    mcp.run()