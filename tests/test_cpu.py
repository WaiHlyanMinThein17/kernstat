"""Tests for CPU statistics reader."""

import kernstat.cpu as cpu_module


def test_read_cpu_line_returns_integers(tmp_path):
    original = cpu_module.PROC_STAT
    fake_stat = tmp_path / "stat"
    fake_stat.write_text("cpu 100 50 25 800 10 5 0 0 0 0\n")
    cpu_module.PROC_STAT = str(fake_stat)
    result = cpu_module.read_cpu_line()
    cpu_module.PROC_STAT = original

    assert result == [100, 50, 25, 800, 10, 5, 0, 0, 0, 0]


def test_calculate_cpu_percent_correct_math():
    first = [4705, 356, 584, 3699, 23, 23, 0, 0, 0, 0]
    second = [4760, 370, 600, 3750, 25, 24, 0, 0, 0, 0]
    result = cpu_module.calculate_cpu_percent(first, second)

    assert result == 63.31


def test_cpu_percent_returns_float_between_0_and_100():
    result = cpu_module.cpu_percent()

    assert isinstance(result, float)
    assert 0.0 <= result <= 100.0
