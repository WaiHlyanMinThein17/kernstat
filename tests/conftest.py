"""Shared pytest fixtures for kernstat tests."""

from pathlib import Path

import pytest


@pytest.fixture
def proc_stat_path(tmp_path):
    """Return a factory for creating fake /proc/stat files."""

    def _make(content: str) -> Path:
        fake = tmp_path / "stat"
        fake.write_text(content)
        return fake

    return _make


@pytest.fixture
def proc_meminfo_path(tmp_path):
    """Return a factory for creating fake /proc/meminfo files."""

    def _make(content: str) -> Path:
        fake = tmp_path / "meminfo"
        fake.write_text(content)
        return fake

    return _make


@pytest.fixture
def proc_diskstats_path(tmp_path):
    """Return a factory for creating fake /proc/diskstats files."""

    def _make(content: str) -> Path:
        fake = tmp_path / "diskstats"
        fake.write_text(content)
        return fake

    return _make


@pytest.fixture
def proc_net_dev_path(tmp_path):
    """Return a factory for creating fake /proc/net/dev files."""

    def _make(content: str) -> Path:
        fake = tmp_path / "dev"
        fake.write_text(content)
        return fake

    return _make


@pytest.fixture
def proc_net_route_path(tmp_path):
    """Return a factory for creating fake /proc/net/route files."""

    def _make(content: str) -> Path:
        fake = tmp_path / "route"
        fake.write_text(content)
        return fake

    return _make