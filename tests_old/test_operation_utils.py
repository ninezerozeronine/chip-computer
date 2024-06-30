from copy import deepcopy

import pytest

from sixteen_bit_computer import operation_utils
from sixteen_bit_computer.data_structures import get_arg_def_template
from sixteen_bit_computer.exceptions import OperationParsingError


@pytest.mark.parametrize("test_input,expected", [
    (
        [
        ],
        "",
    ),
    (
        [
            "hello",
        ],
        "\"hello\"",
    ),
    (
        [
            "foo",
            "bar",
        ],
        "\"foo\", \"bar\"",
    ),
    (
        [
            "foo",
            "bar",
            "   ",
        ],
        "\"foo\", \"bar\", \"   \"",
    ),
])
def test_add_quotes_to_strings(test_input, expected):
    assert operation_utils.add_quotes_to_strings(test_input) == expected


def gen_test_match_and_parse_args_input_0():
    """
    Single module arg
    """

    line_args = ["A"]

    signature = []

    arg_def = get_arg_def_template()
    arg_def["value_type"] = "module_name"
    arg_def["is_memory_location"] = False
    arg_def["value"] = "A"

    signature.append(arg_def)

    expected_match = True
    expected_args = deepcopy(signature)

    return (line_args, signature, expected_match, expected_args)


def gen_test_match_and_parse_args_input_1():
    """
    All kinds
    """

    line_args = ["A", "[B]", "#123", "[#123]"]

    signature = []

    arg_def = get_arg_def_template()
    arg_def["value_type"] = "module_name"
    arg_def["is_memory_location"] = False
    arg_def["value"] = "A"

    signature.append(arg_def)

    arg_def = get_arg_def_template()
    arg_def["value_type"] = "module_name"
    arg_def["is_memory_location"] = True
    arg_def["value"] = "B"

    signature.append(arg_def)

    arg_def = get_arg_def_template()
    arg_def["value_type"] = "constant"
    arg_def["is_memory_location"] = False
    arg_def["value"] = ""

    signature.append(arg_def)

    arg_def = get_arg_def_template()
    arg_def["value_type"] = "constant"
    arg_def["is_memory_location"] = True
    arg_def["value"] = ""

    signature.append(arg_def)

    expected_match = True
    expected_args = deepcopy(signature)
    expected_args[2]["value"] = "#123"
    expected_args[3]["value"] = "#123"

    return (line_args, signature, expected_match, expected_args)


def gen_test_match_and_parse_args_input_2():
    """
    Not module memref
    """

    line_args = ["A"]

    signature = []

    arg_def = get_arg_def_template()
    arg_def["value_type"] = "module_name"
    arg_def["is_memory_location"] = True
    arg_def["value"] = "A"

    signature.append(arg_def)

    expected_match = False
    expected_args = []

    return (line_args, signature, expected_match, expected_args)


def gen_test_match_and_parse_args_input_3():
    """
    Not constant memref
    """

    line_args = ["#123"]

    signature = []

    arg_def = get_arg_def_template()
    arg_def["value_type"] = "constant"
    arg_def["is_memory_location"] = True
    arg_def["value"] = ""

    signature.append(arg_def)

    expected_match = False
    expected_args = []

    return (line_args, signature, expected_match, expected_args)


def gen_test_match_and_parse_args_input_4():
    """
    Arg length mismatch
    """

    line_args = ["A", "B"]

    signature = []

    arg_def = get_arg_def_template()
    arg_def["value_type"] = "module_name"
    arg_def["is_memory_location"] = False
    arg_def["value"] = "A"

    signature.append(arg_def)

    expected_match = False
    expected_args = []

    return (line_args, signature, expected_match, expected_args)


@pytest.mark.parametrize(
    "line_args,signature,expected_match,expected_args",
    [
        gen_test_match_and_parse_args_input_0(),
        gen_test_match_and_parse_args_input_1(),
        gen_test_match_and_parse_args_input_2(),
        gen_test_match_and_parse_args_input_3(),
        gen_test_match_and_parse_args_input_4(),
    ]
)
def test_match_and_parse_args(
    line_args, signature, expected_match, expected_args
):
    match, parsed_args = operation_utils.match_and_parse_args(
        line_args, signature
    )
    assert match == expected_match
    assert parsed_args == expected_args


def gen_test_match_and_parse_line_input_0():
    """
    Match second args def
    """

    line = "COPY A B"
    opcode = "COPY"

    signatures = []

    # Def 0
    signature = []

    arg_def = get_arg_def_template()
    arg_def["value_type"] = "module_name"
    arg_def["is_memory_location"] = False
    arg_def["value"] = "C"

    signature.append(arg_def)

    arg_def = get_arg_def_template()
    arg_def["value_type"] = "module_name"
    arg_def["is_memory_location"] = False
    arg_def["value"] = "D"

    signature.append(arg_def)

    signatures.append(signature)

    # Def 1
    signature = []

    arg_def = get_arg_def_template()
    arg_def["value_type"] = "module_name"
    arg_def["is_memory_location"] = False
    arg_def["value"] = "A"

    signature.append(arg_def)

    arg_def = get_arg_def_template()
    arg_def["value_type"] = "module_name"
    arg_def["is_memory_location"] = False
    arg_def["value"] = "B"

    signature.append(arg_def)

    signatures.append(signature)

    expected_match = True
    expected_args = deepcopy(signatures[1])

    return (line, opcode, signatures, expected_match, expected_args)


def gen_test_match_and_parse_line_input_1():
    """
    No args
    """
    line = "NOOP"
    opcode = "NOOP"

    signatures = []

    expected_match = True
    expected_args = []

    return (line, opcode, signatures, expected_match, expected_args)


def gen_test_match_and_parse_line_input_2():
    """
    Module mem ref
    """

    line = "JUMP [A]"
    opcode = "JUMP"

    signatures = []

    # Def 0
    signature = []

    arg_def = get_arg_def_template()
    arg_def["value_type"] = "module_name"
    arg_def["is_memory_location"] = True
    arg_def["value"] = "A"

    signature.append(arg_def)

    signatures.append(signature)

    expected_match = True
    expected_args = deepcopy(signatures[0])

    return (line, opcode, signatures, expected_match, expected_args)


def gen_test_match_and_parse_line_input_3():
    """
    constant mem ref
    """

    line = "JUMP [$variable]"
    opcode = "JUMP"

    signatures = []

    # Def 0
    signature = []

    arg_def = get_arg_def_template()
    arg_def["value_type"] = "constant"
    arg_def["is_memory_location"] = True
    arg_def["value"] = ""

    signature.append(arg_def)

    signatures.append(signature)

    expected_match = True
    expected_args = deepcopy(signatures[0])
    expected_args[0]["value"] = "$variable"

    return (line, opcode, signatures, expected_match, expected_args)


def gen_test_match_and_parse_line_input_4():
    """
    constant
    """

    line = "JUMP @label"
    opcode = "JUMP"

    signatures = []

    # Def 0
    signature = []

    arg_def = get_arg_def_template()
    arg_def["value_type"] = "constant"
    arg_def["is_memory_location"] = False
    arg_def["value"] = ""

    signature.append(arg_def)

    signatures.append(signature)

    expected_match = True
    expected_args = deepcopy(signatures[0])
    expected_args[0]["value"] = "@label"

    return (line, opcode, signatures, expected_match, expected_args)


@pytest.mark.parametrize(
    "line,opcode,signatures,expected_match,expected_args",
    [
        gen_test_match_and_parse_line_input_0(),
        gen_test_match_and_parse_line_input_1(),
        gen_test_match_and_parse_line_input_2(),
        gen_test_match_and_parse_line_input_3(),
        gen_test_match_and_parse_line_input_4(),

    ]
)
def test_match_and_parse_line(
    line, opcode, signatures, expected_match, expected_args
):
    match, parsed_args = operation_utils.match_and_parse_line(
        line, opcode, signatures
    )
    assert match == expected_match
    assert parsed_args == expected_args


def gen_test_match_and_parse_line_raises_input_0():
    """
    Incorrect args specified
    """

    line = "LOAD A C"
    opcode = "LOAD"

    signatures = []

    # Def 0
    signature = []

    arg_def = get_arg_def_template()
    arg_def["value_type"] = "module_name"
    arg_def["is_memory_location"] = False
    arg_def["value"] = "A"

    signature.append(arg_def)

    arg_def = get_arg_def_template()
    arg_def["value_type"] = "module_name"
    arg_def["is_memory_location"] = False
    arg_def["value"] = "B"

    signature.append(arg_def)

    signatures.append(signature)

    return (line, opcode, signatures)


def gen_test_match_and_parse_line_raises_input_1():
    """
    Matches multiple arg possibilities
    """

    line = "LOAD A B"
    opcode = "LOAD"

    signatures = []

    # Def 0
    signature = []

    arg_def = get_arg_def_template()
    arg_def["value_type"] = "module_name"
    arg_def["is_memory_location"] = False
    arg_def["value"] = "A"

    signature.append(arg_def)

    arg_def = get_arg_def_template()
    arg_def["value_type"] = "module_name"
    arg_def["is_memory_location"] = False
    arg_def["value"] = "B"

    signature.append(arg_def)

    signatures.append(signature)

    # Def 1
    signature = []

    arg_def = get_arg_def_template()
    arg_def["value_type"] = "module_name"
    arg_def["is_memory_location"] = False
    arg_def["value"] = "A"

    signature.append(arg_def)

    arg_def = get_arg_def_template()
    arg_def["value_type"] = "module_name"
    arg_def["is_memory_location"] = False
    arg_def["value"] = "B"

    signature.append(arg_def)

    signatures.append(signature)

    return (line, opcode, signatures)


@pytest.mark.parametrize(
    "line,opcode,signatures",
    [
        gen_test_match_and_parse_line_raises_input_0(),
        gen_test_match_and_parse_line_raises_input_1(),
    ]
)
def test_match_and_parse_line_raises(line, opcode, signatures):
    with pytest.raises(OperationParsingError):
        operation_utils.match_and_parse_line(line, opcode, signatures)


def test_generate_possible_signatures_list():
    test_input = [
        [
            {
                "value_type": "module_name",
                "is_memory_location": False,
                "value": "A",
            },
        ],
        [
            {
                "value_type": "module_name",
                "is_memory_location": False,
                "value": "A",
            },
            {
                "value_type": "module_name",
                "is_memory_location": False,
                "value": "B",
            },
        ],
        [
            {
                "value_type": "module_name",
                "is_memory_location": False,
                "value": "A",
            },
            {
                "value_type": "module_name",
                "is_memory_location": False,
                "value": "B",
            },
            {
                "value_type": "module_name",
                "is_memory_location": False,
                "value": "C",
            },
        ],
        [
            {
                "value_type": "module_name",
                "is_memory_location": True,
                "value": "A",
            },
        ],
        [
            {
                "value_type": "constant",
                "is_memory_location": False,
                "value": "",
            },
        ],
        [
            {
                "value_type": "constant",
                "is_memory_location": True,
                "value": "",
            },
        ],
    ]
    expected = [
        ["A"],
        ["A", "B"],
        ["A", "B", "C"],
        ["[A]"],
        ["<constant>"],
        ["[<constant>]"],
    ]
    assert operation_utils.generate_possible_signatures_list(test_input) == expected
