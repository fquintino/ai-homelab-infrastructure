#!/usr/bin/env python3

"""
AI Homelab Infrastructure Diagnostics

Version: 0.1.0

Collects basic information about the system and produces
a simple infrastructure diagnostic report.
"""

import os
import platform
import shutil
import socket
import subprocess
import json
from datetime import datetime, timezone

import psutil

APPLE_CONTAINER_HOST = "aiserver@192.168.1.20"
APPLE_CONTAINER_SSH_KEY = os.path.expanduser("~/.ssh/id_ed25519_homelab")
APPLE_CONTAINER_CLI = (
    "/Users/aiserver/Library/Application Support/"
    "dev.wouter.davit/platform/1.3.1/bin/container"
)


def run_remote_command(command):
    """Run a command on the Apple Container host via SSH."""
    try:
        result = subprocess.run(
            [
                "ssh",
                "-i",
                APPLE_CONTAINER_SSH_KEY,
                "-o",
                "BatchMode=yes",
                APPLE_CONTAINER_HOST,
                command,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as error:

        error_message = (
            error.stderr.strip() or "remote command returned a non-zero exit status"
        )

        raise RuntimeError(
            f"Failed to execute remote command on {APPLE_CONTAINER_HOST}: "
            f"{error_message}"
        ) from error

    return result.stdout.strip()


def get_apple_container_info():
    """Collect Apple Container information from the remote host."""
    output = run_remote_command(f"'{APPLE_CONTAINER_CLI}' list --format json")

    return json.loads(output)


def get_apple_container_summary():
    """Return a concise summary of Apple Containers."""
    containers = get_apple_container_info()

    summary = []

    for container in containers:
        configuration = container.get("configuration", {})
        status = container.get("status", {})

        summary.append(
            {
                "id": container.get("id"),
                "state": status.get("state"),
                "image": configuration.get("image", {}).get("reference"),
                "ports": configuration.get("publishedPorts", []),
            }
        )

    return summary


def get_apple_container_stats():
    """Collect resource usage statistics from Apple Containers."""
    output = run_remote_command(
        f"'{APPLE_CONTAINER_CLI}' stats --no-stream --format json"
    )

    return json.loads(output)


def get_apple_container_stats_summary():
    """Return a concise summary of Apple Container resource usage."""
    stats = get_apple_container_stats()

    summary = []

    for container in stats:
        memory_limit = container.get("memoryLimitBytes", 0)
        memory_usage = container.get("memoryUsageBytes", 0)

        memory_usage_gb = memory_usage / (1024**3)
        memory_limit_gb = memory_limit / (1024**3)

        memory_percent = (memory_usage / memory_limit) * 100 if memory_limit else 0

        summary.append(
            {
                "id": container.get("id"),
                "memory_usage_gb": round(memory_usage_gb, 2),
                "memory_limit_gb": round(memory_limit_gb, 2),
                "memory_percent": round(memory_percent, 1),
                "cpu_usage_seconds": round(
                    container.get("cpuUsageUsec", 0) / 1_000_000,
                    1,
                ),
                "processes": container.get("numProcesses", 0),
            }
        )

    return summary


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
        "logical_cpus": os.cpu_count(),
    }


def get_network_info():
    """Collect network interface information."""
    interfaces = []

    for name, addresses in psutil.net_if_addrs().items():
        stats = psutil.net_if_stats().get(name)

        ipv4_addresses = []
        ipv6_addresses = []

        for address in addresses:
            if address.family == socket.AF_INET:
                ipv4_addresses.append(address.address)
            elif address.family == socket.AF_INET6:
                ipv6_addresses.append(address.address)

        if ipv4_addresses or ipv6_addresses:
            interfaces.append(
                {
                    "name": name,
                    "is_up": stats.isup if stats else None,
                    "ipv4": ipv4_addresses,
                    "ipv6": ipv6_addresses,
                }
            )

    return interfaces


def get_default_route():
    """Collect the default gateway and network interface."""
    output = subprocess.check_output(
        ["route", "-n", "get", "default"],
        text=True,
    )

    gateway = None
    interface = None

    for line in output.splitlines():
        line = line.strip()

        if line.startswith("gateway:"):
            gateway = line.split(":", 1)[1].strip()
        elif line.startswith("interface:"):
            interface = line.split(":", 1)[1].strip()

    return {
        "gateway": gateway,
        "interface": interface,
    }


def check_gateway_connectivity(gateway):
    """Check connectivity to the default gateway."""
    if not gateway:
        return False

    result = subprocess.run(
        ["ping", "-c", "1", gateway],
        capture_output=True,
        text=True,
    )

    return result.returncode == 0


def check_dns_resolution(hostname):
    """Check DNS resolution for a hostname."""
    try:
        socket.gethostbyname(hostname)
        return True
    except socket.gaierror:
        return False


def check_network_reachability(hostname):
    """Check network reachability for a hostname."""
    result = subprocess.run(
        ["ping", "-c", "1", hostname],
        capture_output=True,
        text=True,
    )

    return result.returncode == 0


def get_memory_info():
    """Collect basic memory information."""
    memory = psutil.virtual_memory()

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

    print()
    print("=" * 50)
    print("Network")
    print("=" * 50)
    route = get_default_route()
    print(f"Default Gateway: {route['gateway']}")
    print(f"Gateway Interface: {route['interface']}")
    gateway_reachable = check_gateway_connectivity(route["gateway"])
    print(f"Gateway Reachable: {'YES' if gateway_reachable else 'NO'}")
    dns_working = check_dns_resolution("github.com")
    print(f"DNS Resolution: {'YES' if dns_working else 'NO'}")
    network_reachable = check_network_reachability("github.com")
    print(f"Network Reachability: {'YES' if network_reachable else 'NO'}")
    print()

    for interface in get_network_info():
        status = "UP" if interface["is_up"] else "DOWN"
        print(f"Interface: {interface['name']}")
        print(f"  Status: {status}")

        if interface["ipv4"]:
            print(f"  IPv4: {', '.join(interface['ipv4'])}")

        if interface["ipv6"]:
            print(f"  IPv6: {', '.join(interface['ipv6'])}")

    print()

    print_section("Memory", get_memory_info())
    print_section("Disk", get_disk_info())
    print()
    print("=" * 50)
    print("Apple Containers")
    print("=" * 50)

    stats = get_apple_container_stats_summary()
    for container in get_apple_container_summary():
        print(f"Container: {container['id']}")
        print(f"  State: {container['state']}")
        print(f"  Image: {container['image']}")
        ports = container["ports"]
        port_text = (
            ", ".join(
                f"{port['hostPort']} -> {port['containerPort']}/{port['proto']}"
                for port in ports
            )
            if ports
            else "None"
        )
        print(f"  Published Ports: {port_text}")

        container_stats = next(
            (item for item in stats if item["id"] == container["id"]),
            None,
        )

        if container_stats:
            print(
                f"  Memory: {container_stats['memory_usage_gb']} GB "
                f"/ {container_stats['memory_limit_gb']} GB "
                f"({container_stats['memory_percent']}%)"
            )
            print(f"  CPU Time: {container_stats['cpu_usage_seconds']} seconds")
            print(f"  Processes: {container_stats['processes']}")

    print()
    print("Diagnostic completed.")
    print()


if __name__ == "__main__":
    main()
