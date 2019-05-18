import textwrap

import pytest

from eight_bit_computer import export


def test_bitstrings_to_logisim():
    test_data = [
        "10111110",
        "11101111",
        "11111010",
        "11001110",
    ]
    expected = textwrap.dedent(
        """\
        v2.0 raw
        BE EF FA CE
        """
    )
    assert export.bitstrings_to_logisim(test_data) == expected


def generator_tester(generator_iterator_to_test, expected_values):
    """
    https://stackoverflow.com/questions/34346182/testing-a-generator-in-python
    """
    range_index = 0
    for actual in generator_iterator_to_test:
        assert range_index + 1 <= len(expected_values), 'Too many values returned from range'
        assert expected_values[range_index] == actual
        range_index += 1

    assert range_index == len(expected_values), 'Too few values returned from range'


@pytest.mark.parametrize("seq,chunk_size,expected", [
    ([0, 1, 2, 3, 4, 5, 6, 7],   8, [[0, 1, 2, 3, 4, 5, 6, 7]]),
    ([0, 1, 2, 3, 4, 5, 6, 7],   2, [[0, 1], [2, 3], [4, 5], [6, 7]]),
    ([0, 1, 2, 3, 4, 5, 6, 7],   10, [[0, 1, 2, 3, 4, 5, 6, 7]]),
    ([0, 1, 2, 3, 4, 5, 6, 7],   3, [[0, 1, 2], [3, 4, 5], [6, 7]]),
])
def test_number_to_bitstring(seq, chunk_size, expected):
    generator = export.chunker(seq, chunk_size)
    generator_tester(generator, expected)
