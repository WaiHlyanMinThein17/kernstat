"""CPU statistics from /proc/stat."""

import time

PROC_STAT = "/proc/stat"

def read_cpu_line() -> list[int]:
    """Read the first cpu line from /proc/stat and return values as integers."""
    with open(PROC_STAT) as f:
        cpu, *values = f.readline().split()

    return [int(v) for v in values]
        
def calculate_cpu_percent(first: list[int], second: list[int]) -> float:
    """Calculate CPU usage percentage between two /proc/stat readings."""
    idle_diff = second[3] - first[3]
    total_diff = sum(second) - sum(first)
    if total_diff == 0:
        return 0.0
    return round(100 - ((idle_diff / total_diff) * 100), 2)

def cpu_percent(interval: float = 0.1) -> float:
    """Return CPU usage percentage over a short sampling interval."""
    start = read_cpu_line()
    time.sleep(interval)
    end = read_cpu_line()
    return calculate_cpu_percent(start, end)