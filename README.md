# kernstat

![CI](https://github.com/WaiHlyanMinThein17/kernstat/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-GPL--3.0-blue)
![Python](https://img.shields.io/badge/python-3.14+-blue)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)

Lightweight Linux system statistics CLI built directly on `/proc` and `/sys`
interfaces. `kernstat` reports CPU, memory, disk, and network metrics without
external monitoring daemons or subprocess wrappers, with both human-readable
and JSON output modes for scripting and automation.

---

## Basic usage

Show CPU usage:

```bash
kernstat cpu
```
CPU Usage:    12.4%

Show memory statistics:

```bash
kernstat memory
```
Memory
Total:      7.62 GB
Used:       4.11 GB
Available:  3.51 GB
Usage:      53.94%

Show full system report:

```bash
kernstat report
```
CPU Usage:    10.8%
Memory
Total:      7.62 GB
Used:       4.09 GB
Available:  3.53 GB
Usage:      53.67%
Disk
Total:      238.47 GB
Used:       121.84 GB
Free:       116.63 GB
Usage:      51.09%
Reads:      0.0/sec
Writes:     2.0/sec
Network (wlp1s0)
Download:   4.82 KB/s
Upload:     0.31 KB/s

JSON output for scripting:

```bash
kernstat report --format json
```

```json
{
  "cpu": {
    "cpu_percent": 10.8
  },
  "memory": {
    "total_gb": 7.62,
    "available_gb": 3.53,
    "used_gb": 4.09,
    "percent": 53.67
  },
  "disk": {
    "io": {
      "reads_per_sec": 0.0,
      "writes_per_sec": 2.0,
      "read_bytes_per_sec": 0.0,
      "write_bytes_per_sec": 1024.0
    },
    "space": {
      "total_gb": 238.47,
      "free_gb": 116.63,
      "used_gb": 121.84,
      "percent": 51.09
    }
  },
  "network": {
    "rx_bytes_per_sec": 4935.68,
    "tx_bytes_per_sec": 317.44,
    "rx_kb_per_sec": 4.82,
    "tx_kb_per_sec": 0.31
  }
}
```

---

## Installation

Install from PyPI:

```bash
pip install kernstat
```

Run the CLI:

```bash
kernstat report
```

For development:

```bash
git clone https://github.com/WaiHlyanMinThein17/kernstat.git
cd kernstat
pip install -e .
```

---

## Commands

| Command | Description |
|---------|-------------|
| `kernstat cpu` | CPU usage percentage |
| `kernstat memory` | Memory usage statistics |
| `kernstat disk` | Disk I/O and space statistics |
| `kernstat network` | Network I/O statistics |
| `kernstat report` | Full system report |

All commands accept `--format json` for structured output.

---

## Design notes

**Direct `/proc` and `/sys` parsing**

`kernstat` reads Linux kernel interfaces directly instead of shelling out to
tools like `top`, `free`, or `iostat`. This avoids subprocess overhead, removes
dependencies on external utilities, and keeps the implementation portable across
minimal Linux environments and containers. Parsing kernel interfaces directly
also provides predictable structured data and exposes how Linux system metrics
are actually represented internally.

**Sampling with two readings**

CPU and network usage are calculated from differences between two cumulative
kernel readings over a short interval. Linux counters in `/proc` continuously
increase since boot, so a single reading cannot represent utilization or
throughput by itself. Taking two samples and calculating the delta produces
accurate rates such as CPU utilization percentages and network transfer speeds.

**JSON output for automation**

All commands support structured JSON output in addition to human-readable
terminal output. This allows `kernstat` to integrate cleanly with shell
scripts, monitoring pipelines, CI systems, and other automation tooling.
The JSON mode provides stable machine-readable output while preserving a
concise CLI experience for interactive use.

---

## Contributing

Contributions, bug reports, and suggestions are welcome.

Run tests:

```bash
uv run pytest
```

Run linting:

```bash
uvx ruff check src tests
```

---

## License

`kernstat` is released under the [GPL-3.0 license](LICENSE).