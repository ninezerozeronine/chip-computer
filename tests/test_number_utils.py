import pytest

from sixteen_bit_computer import number_utils


@pytest.mark.parametrize("test_input,test_bitwidth,expected", [
    (0,   8, "00000000"),
    (-1,  8, "11111111"),
    (255, 8, "11111111"),
    (1,   8, "00000001"),
    (-1,  16, "1111111111111111"),
])
def test_number_to_bitstring(test_input, test_bitwidth, expected):
    assert number_utils.number_to_bitstring(
        test_input, bit_width=test_bitwidth
    ) == expected


@pytest.mark.parametrize("test_input,test_bitwidth,expected", [
    (0,    8, True),
    (-1,   8, True),
    (255,  8, True),
    (1,    8, True),
    (-128, 8, True),
    (-200, 8, False),
    (500,  8, False),
])
def test_number_is_within_bit_limit(test_input, test_bitwidth, expected):
    assert number_utils.number_is_within_bit_limit(
        test_input, bit_width=test_bitwidth
    ) == expected


@pytest.mark.parametrize("test_input,expected", [
    (0,    0),
    (-1,   255),
    (255,  255),
    (1,    1),
    (-128, 128),
])
def test_get_positive_equivalent(test_input, expected):
    assert number_utils.get_positive_equivalent(test_input) == expected


@pytest.mark.parametrize("test_input,test_bitwidth,expected", [
    (0,    8,  0),
    (-1,   16, -1),
    (200,  8,  -56),
    (-15,  8,  -15),
    (1,    8,  1),
    (3,    3,  3),
    (6,    3,  -2),
])
def test_get_signed_equivalent(test_input, test_bitwidth, expected):
    assert number_utils.get_signed_equivalent(
        test_input, bit_width=test_bitwidth
    ) == expected


@pytest.mark.parametrize("test_input,expected", [
    ("00000000", 0),
    ("11111111", 255),
    ("00000001", 1),
    ("10000000", 128),
    ("00001010", 10),
])
def test_bitstring_to_number(test_input, expected):
    assert number_utils.bitstring_to_number(test_input) == expected


@pytest.mark.parametrize("test_input,test_pad,expected", [
    ("00000000", 2, "00"),
    ("11111111", 2, "FF"),
    ("00000001", 2, "01"),
    ("10000000", 2, "80"),
    ("00001010", 2, "0A"),
    ("00001010", 3, "00A"),
])
def test_bitstring_to_hex_string(test_input, test_pad, expected):
    assert number_utils.bitstring_to_hex_string(
        test_input, zero_pad_width=test_pad) == expected


@pytest.mark.parametrize("test_input,expected", [
    (4, (-8, 15)),
    (8, (-128, 255)),
    (16, (-32768, 65535)),
])
def test_get_min_max_values(test_input, expected):
    assert number_utils.get_min_max_values(test_input) == expected




























