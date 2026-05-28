"""Tests for network statistics reader."""

import pytest
import kernstat.net as net_module


def test_get_default_interface_returns_string(tmp_path):
    original = net_module.PROC_NET_ROUTE

    fake_route = tmp_path / "route"

    fake_route.write_text(
        "Iface\tDestination\tGateway\tFlags\tRefCnt\tUse\tMetric\tMask\tMTU\tWindow\tIRTT\n"
        "wlp1s0\t00000000\t01000A0A\t0003\t0\t0\t600\t00000000\t0\t0\t0\n"
    )

    net_module.PROC_NET_ROUTE = str(fake_route)
    result = net_module.get_default_interface()
    net_module.PROC_NET_ROUTE = original

    assert result == "wlp1s0"


def test_get_default_interface_raises_when_not_found(tmp_path):
    original = net_module.PROC_NET_ROUTE

    fake_route = tmp_path / "route"

    fake_route.write_text(
        "Iface\tDestination\tGateway\tFlags\tRefCnt\tUse\tMetric\tMask\tMTU\tWindow\tIRTT\n"
        "wlp1s0\t11111111\t01000A0A\t0003\t0\t0\t600\t00000000\t0\t0\t0\n"
    )

    net_module.PROC_NET_ROUTE = str(fake_route)
    try:
        with pytest.raises(ValueError):
            net_module.get_default_interface()
    finally:
        net_module.PROC_NET_ROUTE = original


def test_read_net_stats_return_correct_values(tmp_path):
    original = net_module.PROC_NET_DEV

    fake_dev = tmp_path / "dev"

    fake_dev.write_text(
        "Inter-|   Receive                                                |  Transmit\n"
        " face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed\n"
        "    lo:       0       0    0    0    0     0          0         0       0       0    0    0    0     0       0          0\n"
        "wlp1s0: 1000000    5000    0    0    0     0          0         0  500000    2000    0    0    0     0       0          0\n"
    )

    net_module.PROC_NET_DEV = str(fake_dev)
    result = net_module.read_net_stats("wlp1s0")
    net_module.PROC_NET_DEV = original

    assert result["rx_bytes"] == 1000000
    assert result["tx_bytes"] == 500000


def test_net_io_return_correct_rates(mocker):
    mocker.patch(
        "kernstat.net.read_net_stats",
        side_effect=[
            {
                "rx_bytes": 1000000,
                "tx_bytes": 500000,
            },
            {
                "rx_bytes": 1002000,
                "tx_bytes": 500500,
            },
        ],
    )

    result = net_module.net_io(
        interface="wlp1s0",
        interval=0.1,
    )

    assert result["rx_bytes_per_sec"] == 20000.0
    assert result["tx_bytes_per_sec"] == 5000.0
    assert result["rx_kb_per_sec"] == 19.53
    assert result["tx_kb_per_sec"] == 4.88


def test_net_info_uses_default_interface_when_none(mocker):
    mocker.patch(
        "kernstat.net.get_default_interface",
        return_value="wlp1s0",
    )

    mock_net_io = mocker.patch(
        "kernstat.net.net_io",
        return_value={
            "rx_bytes_per_sec": 1.0,
            "tx_bytes_per_sec": 1.0,
            "rx_kb_per_sec": 0.0,
            "tx_kb_per_sec": 0.0,
        },
    )

    result = net_module.net_info(interface=None)

    mock_net_io.assert_called_once_with(
        "wlp1s0",
        0.1,
    )

    assert result["rx_bytes_per_sec"] == 1.0
