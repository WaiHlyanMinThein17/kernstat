"""Memory statistics from /proc/meminfo."""

PROC_MEMINFO = "/proc/meminfo"

def parse_meminfo() -> dict[str, int]:
    """Parse /proc/meminfo and return memory values."""

    meminfo = {}

    with open(PROC_MEMINFO) as f:
        for line in f:
            parts = line.split()

            key = parts[0].rstrip(":")
            value = int(parts[1])

            meminfo[key] = value

    return meminfo

def mem_percent() -> float:
    """Return memory usage percentage."""

    meminfo = parse_meminfo()

    total = meminfo["MemTotal"]
    available = meminfo["MemAvailable"]

    percent = ((total - available) / total) * 100

    return round(percent, 2)
    
def kb_to_gb(kb: int) -> float:
    """Convert kilobytes to gigabytes using binary units."""

    return round(kb / (1024 ** 2), 2)

def mem_info() -> dict[str, float]:
    """Return memory information summary."""

    meminfo = parse_meminfo()
    
    total = meminfo["MemTotal"]
    available = meminfo["MemAvailable"]
    used = total - available

    return {
        "total_gb": kb_to_gb(total),
        "available_gb": kb_to_gb(available),
        "used_gb": kb_to_gb(used),
        "percent": mem_percent(),
    }
