import pytest

from eight_bit_computer import bitdef


@pytest.mark.parametrize("test_input,expected", [
    (
        [
            ".",
            "0",
            "1",
        ],
        True,
    ),
    (
        [
            "...",
            "0.1",
            "1..",
        ],
        True,
    ),
    (
        [
            "",
            "",
        ],
        True,
    ),
    (
        [
            "..",
            "0",
            "1111",
        ],
        False,
    ),
    (
        [
            "...",
            "0.1",
            "1...",
        ],
        False,
    ),
    (
        [
            "...",
            "0.1",
            "",
        ],
        False,
    )
])
def test_same_length(test_input, expected):
    assert bitdef.same_length(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [
    ("00010", 5),
    ("", 0),
    (".", 1),
    ("01.100", 6),
])
def test_length(test_input, expected):
    assert bitdef.length(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [
    (
        [
            "0",
            "0",
        ],
        True,
    ),
    (
        [
            "0.",
            "1.",
        ],
        True,
    ),
    (
        [
            "..0.",
            "1.1.",
        ],
        True,
    ),
    (
        [
            "....0.",
            "....1.",
        ],
        True,
    ),
    (
        [
            "......",
            "....0.",
            "....1.",
        ],
        True,
    ),
    (
        [
            "",
        ],
        False,
    ),
    (
        [
            "",
            "",
            "",
        ],
        False,
    ),
    (
        [
            ".",
            "1",
            ".",
        ],
        False,
    ),
    (
        [
            "...0.",
            "1....",
            "..1..",
        ],
        False,
    ),
    (
        [
            "...",
            "...",
            "...",
        ],
        False,
    )
])
def test_have_overlapping_bits(test_input, expected):
    assert bitdef.have_overlapping_bits(test_input) == expected


@pytest.mark.parametrize('test_input', [
    [
        ".10",
        "010.",
    ],
    [
        ".",
        "",
    ],
])
def test_have_overlapping_bits_raises(test_input):
    with pytest.raises(ValueError):
        bitdef.have_overlapping_bits(test_input)


@pytest.mark.parametrize("test_input,expected", [
    (
        [
            "",
        ],
        "",
    ),
    (
        [
            ".",
        ],
        ".",
    ),
    (
        [
            "0",
        ],
        "0",
    ),
    (
        [
            "1",
        ],
        "1",
    ),
    (
        [
            "0...",
            ".1..",
            "..0.",
        ],
        "010.",
    ),
])
def test_merge(test_input, expected):
    assert bitdef.merge(test_input) == expected


@pytest.mark.parametrize('test_input', [
    [
        "0",
        "1",
    ],
    [
        "..0",
        "..1",
    ],
    [
        "00",
        "1",
    ],
])
def test_merge_raises(test_input):
    with pytest.raises(ValueError):
        bitdef.merge(test_input)


@pytest.mark.parametrize("test_input,expected", [
    (
        "",
        [
            "",
        ],
    ),
    (
        ".",
        [
            "0",
            "1"
        ],
    ),
    (
        "..",
        [
            "00",
            "01",
            "10",
            "11",
        ],
    ),
    (
        "1..0",
        [
            "1000",
            "1010",
            "1100",
            "1110",
        ],
    ),
])
def test_collapse(test_input, expected):
    assert bitdef.collapse(test_input) == expected


@pytest.mark.parametrize("test_input,fill,expected", [
    ("", "1", ""),
    (".", "0", "0"),
    (".10.", "1", "1101"),
    ("1010", "0", "1010"),
])
def test_fill(test_input, fill, expected):
    assert bitdef.fill(test_input, fill) == expected


@pytest.mark.parametrize("test_input,end,start,expected", [
    (
        "001010.",
        6,
        0,
        "001010.",
    ),
    (
        "10..11",
        5,
        3,
        "10.",
    ),
    (
        "..01.010",
        1,
        1,
        "1",
    ),
])
def test_extract_bits(test_input, end, start, expected):
    assert bitdef.extract_bits(test_input, end, start) == expected


@pytest.mark.parametrize("test_input,expected", [
    ("", ""),
    ("0", "0"),
    ("00 01", "0001"),
    ("  ..  00  1  ", "..001"),
])
def test_remove_whitespace(test_input, expected):
    assert bitdef.remove_whitespace(test_input) == expected


@pytest.mark.parametrize("test_input,length,expected", [
    (0, 6, 5,),
    (0, 1, 0,),
    (1, 4, 2,),
    (3, 4, 0,),
])
def test_reverse_index(test_input, length, expected):
    assert bitdef.reverse_index(test_input, length) == expected
