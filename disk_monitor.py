import os
import shutil
import subprocess
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

    return f"CPU cores: {cpu_count}\nLoad average: {load}"


@mcp.tool()
def get_memory_info() -> str:
    """Get Linux memory information."""
    memory = {}

    with open("/proc/meminfo") as f:
        for line in f:
            key, value = line.split(":", 1)
            if key in ["MemTotal", "MemAvailable", "SwapTotal", "SwapFree"]:
                memory[key] = value.strip()

    return "\n".join(f"{key}: {value}" for key, value in memory.items())


@mcp.tool()
def get_disk_usage(path: str = "/") -> str:
    """Get disk usage for a path (default: root)."""
    total, used, free = shutil.disk_usage(path)
    gb = 1024 ** 3
    return (
        f"Path: {path}\n"
        f"Total: {total / gb:.1f} GB\n"
        f"Used : {used / gb:.1f} GB ({used / total * 100:.0f}%)\n"
        f"Free : {free / gb:.1f} GB"
    )


@mcp.tool()
def get_top_processes(count: int = 5) -> str:
    """Get top processes by CPU and memory usage."""
    count = max(1, min(count, 20))

    def top(sort_key: str) -> str:
        out = subprocess.run(
            ["ps", "-eo", "pid,pcpu,pmem,comm", f"--sort=-{sort_key}"],
            capture_output=True, text=True, check=True,
        ).stdout.splitlines()
        return "\n".join(out[: count + 1])

    return f"Top by CPU:\n{top('pcpu')}\n\nTop by memory:\n{top('pmem')}"


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

    return (
        "Linux System Status\n"
        "===================\n"
        f"Uptime: {uptime:.0f} seconds\n"
        f"CPU: {os.cpu_count()} cores\n"
        f"Load: {load[0]} (1m), {load[1]} (5m), {load[2]} (15m)\n"
        f"Memory total: {memory.get('MemTotal')}\n"
        f"Memory available: {memory.get('MemAvailable')}"
    )


if __name__ == "__main__":
    mcp.run()