"""Tests for disk I/O statistics reader."""

import pytest
import kernstat.disk as disk_module


def test_read_diskstats_returns_correct_fields(tmp_path):
    original = disk_module.PROC_DISKSTATS

    fake_diskstats = tmp_path / "diskstats"

    fake_diskstats.write_text(
        " 259       0 nvme0n1 100 50 800 10 200 75 1600 20 0 30 30 0 0 0 0 0 0\n"
    )

    disk_module.PROC_DISKSTATS = str(fake_diskstats)
    result = disk_module.read_diskstats()
    disk_module.PROC_DISKSTATS = original

    assert result["reads_completed"] == 100
    assert result["sectors_read"] == 800
    assert result["writes_completed"] == 200
    assert result["sectors_written"] == 1600


def test_read_diskstats_raise_for_unknown_device(tmp_path):
    original = disk_module.PROC_DISKSTATS

    fake_diskstats = tmp_path / "diskstats"

    fake_diskstats.write_text(
        " 259       0 nvme0n1 100 50 800 10 200 75 1600 20 0 30 30 0 0 0 0 0 0\n"
    )

    disk_module.PROC_DISKSTATS = str(fake_diskstats)
    try:
        with pytest.raises(ValueError):
            disk_module.read_diskstats("nonexistent")
    finally:
        disk_module.PROC_DISKSTATS = original


def test_disk_io_returns_correct_rates(mocker):
    mocker.patch(
        "kernstat.disk.read_diskstats",
        side_effect=[
            {
                "reads_completed": 100,
                "writes_completed": 200,
                "sectors_read": 800,
                "sectors_written": 1600,
            },
            {
                "reads_completed": 110,
                "writes_completed": 210,
                "sectors_read": 900,
                "sectors_written": 1700,
            },
        ],
    )

    result = disk_module.disk_io(interval=0.1)

    assert result["reads_per_sec"] == 100.0
    assert result["writes_per_sec"] == 100.0
    assert result["read_bytes_per_sec"] == 512000.0
    assert result["write_bytes_per_sec"] == 512000.0


def test_disk_bytes_to_gb_conversion():
    result = disk_module.bytes_to_gb(1073741824)

    assert result == 1.0


def test_disk_space_returns_sensible_values():
    result = disk_module.disk_space("/")

    assert 0.0 <= result["percent"] <= 100.0
    assert result["total_gb"] > 0
