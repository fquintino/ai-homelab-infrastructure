#!/usr/bin/env python3

"""
AI Homelab Infrastructure Diagnostics

Version: 0.1.0

Collects basic information about the system and produces
a simple infrastructure diagnostic report.
"""

import platform
import shutil
import socket
import sys
from datetime import datetime, timezone


def get_system_info():
    """Collect basic operating system information."""
    return {
        "hostname": socket.gethostname(),
        "operating_system": platform.system(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "timestamp": datetime.now(tz=timezone.utc).isoformat(timespec="seconds"),
    }


def get_cpu_info():
    """Collect CPU information."""
    return {
        "logical_cpus": __import__("os").cpu_count(),
    }


def get_memory_info():
    """Collect basic memory information."""
    memory = __import__("psutil").virtual_memory()

    return {
        "total_gb": round(memory.total / (1024**3), 2),
        "available_gb": round(memory.available / (1024**3), 2),
        "used_percent": memory.percent,
    }


def get_disk_info():
    """Collect information about the root filesystem."""
    disk = shutil.disk_usage("/")

    total_gb = disk.total / (1024**3)
    used_gb = disk.used / (1024**3)
    free_gb = disk.free / (1024**3)

    return {
        "total_gb": round(total_gb, 2),
        "used_gb": round(used_gb, 2),
        "free_gb": round(free_gb, 2),
        "used_percent": round((disk.used / disk.total) * 100, 1),
    }


def print_section(title, data):
    """Print a formatted diagnostic section."""
    print()
    print("=" * 50)
    print(title)
    print("=" * 50)

    for key, value in data.items():
        label = key.replace("_", " ").title()
        print(f"{label}: {value}")


def main():
    """Run the infrastructure diagnostic."""
    print()
    print("AI Homelab Infrastructure Diagnostics")
    print("Version 0.1.0")

    print_section("System", get_system_info())
    print_section("CPU", get_cpu_info())
    print_section("Memory", get_memory_info())
    print_section("Disk", get_disk_info())

    print()
    print("Diagnostic completed.")
    print()


if __name__ == "__main__":
    main()
