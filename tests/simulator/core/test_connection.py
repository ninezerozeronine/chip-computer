import pytest

from eight_bit_computer.simulator import core
from eight_bit_computer.simulator.core import Connection


def gen_width_data():
    tests = []

    conn = Connection()
    tests.append((conn, 0))

    p1 = core.Port("one",  channels=[
        core.Channel(mode=core.MODE["OUTPUT"]),
        core.Channel(mode=core.MODE["INPUT"]),
    ])
    conn = Connection([p1])
    tests.append((conn, 2))

    return tests


@pytest.mark.parametrize("test_input,expected", gen_width_data())
def test_width(test_input, expected):
    assert test_input.width == expected


def gen_ports_data():
    tests = []

    conn = Connection()
    tests.append((conn, []))

    return tests


@pytest.mark.parametrize("test_input,expected", gen_ports_data())
def test_ports(test_input, expected):
    assert True


def gen_ports_in_contention_data():
    """
    Test data for the process line test
    """
    tests = []

    p1 = core.Port("one", channels=[core.Channel(mode=core.MODE["OUTPUT"])])
    p2 = core.Port("two", channels=[core.Channel(mode=core.MODE["OUTPUT"])])
    conn = Connection([p1, p2])
    tests.append((conn, True))

    p1 = core.Port("one", channels=[core.Channel(mode=core.MODE["OUTPUT"])])
    p2 = core.Port("two", channels=[core.Channel(mode=core.MODE["INPUT"])])
    conn = Connection([p1, p2])
    tests.append((conn, False))

    p1 = core.Port("one", channels=[core.Channel(mode=core.MODE["OUTPUT"])])
    p2 = core.Port("two", channels=[core.Channel(mode=core.MODE["INPUT"])])
    p3 = core.Port("three", channels=[core.Channel(mode=core.MODE["OUTPUT"])])
    p4 = core.Port("four", channels=[core.Channel(mode=core.MODE["INPUT"])])
    conn = Connection([p1, p2, p3, p4])
    tests.append((conn, True))

    p1 = core.Port("one", channels=[
        core.Channel(mode=core.MODE["OUTPUT"]),
        core.Channel(mode=core.MODE["INPUT"]),
    ])
    p2 = core.Port("two", channels=[
        core.Channel(mode=core.MODE["OUTPUT"]),
        core.Channel(mode=core.MODE["OUTPUT"]),
    ])
    conn = Connection([p1, p2])
    tests.append((conn, True))

    p1 = core.Port("one", channels=[
        core.Channel(mode=core.MODE["OUTPUT"]),
        core.Channel(mode=core.MODE["INPUT"]),
    ])
    p2 = core.Port("two", channels=[
        core.Channel(mode=core.MODE["INPUT"]),
        core.Channel(mode=core.MODE["OUTPUT"]),
    ])
    conn = Connection([p1, p2])
    tests.append((conn, False))

    return tests


@pytest.mark.parametrize("test_input,expected", gen_ports_in_contention_data())
def test_ports_in_contention(test_input, expected):
    assert test_input.ports_in_contention() is expected