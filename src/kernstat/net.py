"""Network statistics from /proc/net/dev."""

import time

PROC_NET_DEV = "/proc/net/dev"
PROC_NET_ROUTE = "/proc/net/route"


def get_default_interface() -> str:
    """Return the default network interface."""

    best_interface = None
    lowest_metric = None

    with open(PROC_NET_ROUTE) as f:
        next(f)

        for line in f:
            parts = line.split()

            if len(parts) < 7:
                continue

            iface, dest, _, flags, _, _, metric = parts[:7]

            if dest == "00000000":
                flags_int = int(flags, 16)

                if flags_int & 0x0001:
                    metric_int = int(metric)

                    if lowest_metric is None or metric_int < lowest_metric:
                        lowest_metric = metric_int
                        best_interface = iface

    if best_interface is None:
        raise ValueError("No default network interface found")

    return best_interface


def read_net_stats(interface: str) -> dict[str, int]:
    """Read network statistics for an interface."""

    with open(PROC_NET_DEV) as f:
        # Skip header lines
        next(f)
        next(f)

        for line in f:
            if ":" not in line:
                continue

            iface_part, data_part = line.split(":", 1)

            iface = iface_part.strip()

            if iface == interface:
                parts = data_part.split()

                return {
                    "rx_bytes": int(parts[0]),
                    "tx_bytes": int(parts[8]),
                }

    raise ValueError(f"Interface {interface} not found")


def net_io(
    interface: str,
    interval: float = 0.1,
) -> dict[str, float]:
    """Return network I/O statistics per second."""

    first = read_net_stats(interface)

    time.sleep(interval)

    second = read_net_stats(interface)

    # Protect against interface resets/counter rollover
    rx_bytes_diff = max(
        0,
        second["rx_bytes"] - first["rx_bytes"],
    )

    tx_bytes_diff = max(
        0,
        second["tx_bytes"] - first["tx_bytes"],
    )

    rx_bytes_per_sec = rx_bytes_diff / interval
    tx_bytes_per_sec = tx_bytes_diff / interval

    rx_kb_per_sec = rx_bytes_per_sec / 1024
    tx_kb_per_sec = tx_bytes_per_sec / 1024

    return {
        "rx_bytes_per_sec": round(rx_bytes_per_sec, 2),
        "tx_bytes_per_sec": round(tx_bytes_per_sec, 2),
        "rx_kb_per_sec": round(rx_kb_per_sec, 2),
        "tx_kb_per_sec": round(tx_kb_per_sec, 2),
    }


def net_info(
    interface: str | None = None,
    interval: float = 0.1,
) -> dict[str, float]:
    """Return network information for an interface."""

    if interface is None:
        interface = get_default_interface()

    return net_io(interface, interval)
