"""Command-line interface for kernstat."""

import json
import click

from kernstat import __version__
from kernstat.cpu import cpu_percent
from kernstat.mem import mem_info
from kernstat.disk import disk_info
from kernstat.net import net_info, get_default_interface


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """Report Linux kernel statistics from /proc interfaces."""


@main.command()
@click.option(
    "--format",
    "fmt",
    type=click.Choice(["text", "json"]),
    default="text",
    help="Output format.",
)
def cpu(fmt: str) -> None:
    """Show CPU usage percentage."""

    result = {
        "cpu_percent": cpu_percent(),
    }

    if fmt == "json":
        click.echo(json.dumps(result, indent=2))
    else:
        click.echo(f"CPU Usage:    {result['cpu_percent']}%")


@main.command()
@click.option(
    "--format",
    "fmt",
    type=click.Choice(["text", "json"]),
    default="text",
    help="Output format.",
)
def memory(fmt: str) -> None:
    """Show memory usage statistics."""

    result = mem_info()

    if fmt == "json":
        click.echo(json.dumps(result, indent=2))
    else:
        click.echo("Memory")
        click.echo(f"  Total:      {result['total_gb']} GB")
        click.echo(f"  Used:       {result['used_gb']} GB")
        click.echo(f"  Available:  {result['available_gb']} GB")
        click.echo(f"  Usage:      {result['percent']}%")


@main.command()
@click.option(
    "--format",
    "fmt",
    type=click.Choice(["text", "json"]),
    default="text",
    help="Output format.",
)
def disk(fmt: str) -> None:
    """Show disk I/O and space statistics."""

    result = disk_info()

    if fmt == "json":
        click.echo(json.dumps(result, indent=2))
    else:
        space = result["space"]
        io = result["io"]

        click.echo("Disk")
        click.echo(f"  Total:      {space['total_gb']} GB")
        click.echo(f"  Used:       {space['used_gb']} GB")
        click.echo(f"  Free:       {space['free_gb']} GB")
        click.echo(f"  Usage:      {space['percent']}%")
        click.echo(f"  Reads:      {io['reads_per_sec']}/sec")
        click.echo(f"  Writes:     {io['writes_per_sec']}/sec")


@main.command()
@click.option(
    "--format",
    "fmt",
    type=click.Choice(["text", "json"]),
    default="text",
    help="Output format.",
)
def network(fmt: str) -> None:
    """Show network I/O statistics."""

    result = net_info()

    if fmt == "json":
        click.echo(json.dumps(result, indent=2))
    else:
        interface = get_default_interface()

        click.echo(f"Network ({interface})")
        click.echo(f"  Download:   {result['rx_kb_per_sec']} KB/s")
        click.echo(f"  Upload:     {result['tx_kb_per_sec']} KB/s")


@main.command()
@click.option(
    "--format",
    "fmt",
    type=click.Choice(["text", "json"]),
    default="text",
    help="Output format.",
)
def report(fmt: str) -> None:
    """Show full system statistics report."""

    cpu_result = {
        "cpu_percent": cpu_percent(),
    }

    memory_result = mem_info()
    disk_result = disk_info()
    network_result = net_info()

    result = {
        "cpu": cpu_result,
        "memory": memory_result,
        "disk": disk_result,
        "network": network_result,
    }

    if fmt == "json":
        click.echo(json.dumps(result, indent=2))
    else:
        click.echo(f"CPU Usage:    {cpu_result['cpu_percent']}%")
        click.echo()

        click.echo("Memory")
        click.echo(f"  Total:      {memory_result['total_gb']} GB")
        click.echo(f"  Used:       {memory_result['used_gb']} GB")
        click.echo(f"  Available:  {memory_result['available_gb']} GB")
        click.echo(f"  Usage:      {memory_result['percent']}%")
        click.echo()

        space = disk_result["space"]
        io = disk_result["io"]

        click.echo("Disk")
        click.echo(f"  Total:      {space['total_gb']} GB")
        click.echo(f"  Used:       {space['used_gb']} GB")
        click.echo(f"  Free:       {space['free_gb']} GB")
        click.echo(f"  Usage:      {space['percent']}%")
        click.echo(f"  Reads:      {io['reads_per_sec']}/sec")
        click.echo(f"  Writes:     {io['writes_per_sec']}/sec")
        click.echo()

        interface = get_default_interface()

        click.echo(f"Network ({interface})")
        click.echo(f"  Download:   {network_result['rx_kb_per_sec']} KB/s")
        click.echo(f"  Upload:     {network_result['tx_kb_per_sec']} KB/s")
