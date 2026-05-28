"""Disk I/O statistics from /proc/diskstats."""

import os
import time

PROC_DISKSTATS = "/proc/diskstats"
DEFAULT_DEVICE = "nvme0n1"


def read_diskstats(device: str = DEFAULT_DEVICE) -> dict[str, int]:
    """Read disk statistics for a device."""

    with open(PROC_DISKSTATS) as f:
        for line in f:
            parts = line.split()

            if parts[2] == device:
                return {
                    "reads_completed": int(parts[3]),
                    "writes_completed": int(parts[7]),
                    "sectors_read": int(parts[5]),
                    "sectors_written": int(parts[9]),
                }

    raise ValueError(f"Device {device} not found")


def disk_io(
    device: str = DEFAULT_DEVICE,
    interval: float = 0.1,
) -> dict[str, float]:
    """Return disk I/O statistics per second."""

    first = read_diskstats(device)

    time.sleep(interval)

    second = read_diskstats(device)

    reads_per_sec = (second["reads_completed"] - first["reads_completed"]) / interval
    writes_per_sec = (second["writes_completed"] - first["writes_completed"]) / interval
    read_bytes_per_sec = (
        (second["sectors_read"] - first["sectors_read"]) * 512
    ) / interval
    write_bytes_per_sec = (
        (second["sectors_written"] - first["sectors_written"]) * 512
    ) / interval

    return {
        "reads_per_sec": round(reads_per_sec, 2),
        "writes_per_sec": round(writes_per_sec, 2),
        "read_bytes_per_sec": round(read_bytes_per_sec, 2),
        "write_bytes_per_sec": round(write_bytes_per_sec, 2),
    }


def bytes_to_gb(value: int) -> float:
    """Convert bytes to gigabytes."""

    return round(value / (1024**3), 2)


def disk_space(path: str = "/") -> dict[str, float]:
    """Return filesystem disk space statistics."""

    stats = os.statvfs(path)

    total_bytes = stats.f_blocks * stats.f_frsize
    free_bytes = stats.f_bfree * stats.f_frsize
    used_bytes = total_bytes - free_bytes

    percent = (used_bytes / total_bytes) * 100

    return {
        "total_gb": bytes_to_gb(total_bytes),
        "free_gb": bytes_to_gb(free_bytes),
        "used_gb": bytes_to_gb(used_bytes),
        "percent": round(percent, 2),
    }


def disk_info(
    device: str = DEFAULT_DEVICE,
    path: str = "/",
    interval: float = 0.1,
) -> dict[str, dict]:
    """Return combined disk I/O and space information."""

    return {
        "io": disk_io(device, interval),
        "space": disk_space(path),
    }
