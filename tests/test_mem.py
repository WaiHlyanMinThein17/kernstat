"""Tests for memory statistics reader."""

import kernstat.mem as mem_module


def test_parse_meminfo_returns_integers(tmp_path):
    original = mem_module.PROC_MEMINFO
    fake_meminfo = tmp_path / "meminfo"

    fake_meminfo.write_text(
        "MemTotal:       8000000 kB\n"
        "MemFree:        1000000 kB\n"
        "MemAvailable:   2000000 kB\n"
    )

    mem_module.PROC_MEMINFO = str(fake_meminfo)

    result = mem_module.parse_meminfo()
    mem_module.PROC_MEMINFO = original

    assert result == {
        "MemTotal": 8000000,
        "MemFree": 1000000,
        "MemAvailable": 2000000,
    }


def test_parse_meminfo_strips_kb_unit(tmp_path):
    original = mem_module.PROC_MEMINFO
    fake_meminfo = tmp_path / "meminfo"

    fake_meminfo.write_text("MemTotal:        8000000 kB\n")

    mem_module.PROC_MEMINFO = str(fake_meminfo)

    result = mem_module.parse_meminfo()
    mem_module.PROC_MEMINFO = original

    assert result["MemTotal"] == 8000000
    assert isinstance(result["MemTotal"], int)


def test_mem_percent_correct_math(mocker):
    mocker.patch(
        "kernstat.mem.parse_meminfo",
        return_value={
            "MemTotal": 8000000,
            "MemAvailable": 2000000,
        },
    )

    result = mem_module.mem_percent()

    assert result == 75.0


def test_kb_to_gb_conversion():
    result = mem_module.kb_to_gb(1048576)

    assert result == 1.0
