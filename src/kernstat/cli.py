"""Command-line interface for kernstat."""

import click

from kernstat import __version__


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """Report Linux kernel statistics from /proc interfaces."""
