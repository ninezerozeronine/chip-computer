from copy import deepcopy

import pytest

from eight_bit_computer import operation_utils
from eight_bit_computer.data_structures import get_arg_def_template
from eight_bit_computer.exceptions import InstructionParsingError


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

    op_args_def = []

    op_arg_def = get_arg_def_template()
    op_arg_def["value_type"] = "module_name"
    op_arg_def["is_memory_location"] = False
    op_arg_def["value"] = "A"

    op_args_def.append(op_arg_def)

    expected_match = True
    expected_args = deepcopy(op_args_def)

    return (line_args, op_args_def, expected_match, expected_args)


def gen_test_match_and_parse_args_input_1():
    """
    All kinds
    """

    line_args = ["A", "[B]", "#123", "[#123]"]

    op_args_def = []

    op_arg_def = get_arg_def_template()
    op_arg_def["value_type"] = "module_name"
    op_arg_def["is_memory_location"] = False
    op_arg_def["value"] = "A"

    op_args_def.append(op_arg_def)

    op_arg_def = get_arg_def_template()
    op_arg_def["value_type"] = "module_name"
    op_arg_def["is_memory_location"] = True
    op_arg_def["value"] = "B"

    op_args_def.append(op_arg_def)

    op_arg_def = get_arg_def_template()
    op_arg_def["value_type"] = "constant"
    op_arg_def["is_memory_location"] = False
    op_arg_def["value"] = ""

    op_args_def.append(op_arg_def)

    op_arg_def = get_arg_def_template()
    op_arg_def["value_type"] = "constant"
    op_arg_def["is_memory_location"] = True
    op_arg_def["value"] = ""

    op_args_def.append(op_arg_def)

    expected_match = True
    expected_args = deepcopy(op_args_def)
    expected_args[2]["value"] = "#123"
    expected_args[3]["value"] = "#123"

    return (line_args, op_args_def, expected_match, expected_args)


def gen_test_match_and_parse_args_input_2():
    """
    Not module memref
    """

    line_args = ["A"]

    op_args_def = []

    op_arg_def = get_arg_def_template()
    op_arg_def["value_type"] = "module_name"
    op_arg_def["is_memory_location"] = True
    op_arg_def["value"] = "A"

    op_args_def.append(op_arg_def)

    expected_match = False
    expected_args = []

    return (line_args, op_args_def, expected_match, expected_args)


def gen_test_match_and_parse_args_input_3():
    """
    Not constant memref
    """

    line_args = ["#123"]

    op_args_def = []

    op_arg_def = get_arg_def_template()
    op_arg_def["value_type"] = "constant"
    op_arg_def["is_memory_location"] = True
    op_arg_def["value"] = ""

    op_args_def.append(op_arg_def)

    expected_match = False
    expected_args = []

    return (line_args, op_args_def, expected_match, expected_args)


def gen_test_match_and_parse_args_input_4():
    """
    Arg length mismatch
    """

    line_args = ["A", "B"]

    op_args_def = []

    op_arg_def = get_arg_def_template()
    op_arg_def["value_type"] = "module_name"
    op_arg_def["is_memory_location"] = False
    op_arg_def["value"] = "A"

    op_args_def.append(op_arg_def)

    expected_match = False
    expected_args = []

    return (line_args, op_args_def, expected_match, expected_args)


@pytest.mark.parametrize(
    "line_args,op_args_def,expected_match,expected_args",
    [
        gen_test_match_and_parse_args_input_0(),
        gen_test_match_and_parse_args_input_1(),
        gen_test_match_and_parse_args_input_2(),
        gen_test_match_and_parse_args_input_3(),
        gen_test_match_and_parse_args_input_4(),
    ]
)
def test_match_and_parse_args(
    line_args, op_args_def, expected_match, expected_args
):
    match, parsed_args = operation_utils.match_and_parse_args(
        line_args, op_args_def
    )
    assert match == expected_match
    assert parsed_args == expected_args


def gen_test_match_and_parse_line_input_0():
    """
    Match second args def
    """

    line = "COPY A B"
    opcode = "COPY"

    op_args_defs = []

    # Def 0
    op_args_def = []

    op_arg_def = get_arg_def_template()
    op_arg_def["value_type"] = "module_name"
    op_arg_def["is_memory_location"] = False
    op_arg_def["value"] = "C"

    op_args_def.append(op_arg_def)

    op_arg_def = get_arg_def_template()
    op_arg_def["value_type"] = "module_name"
    op_arg_def["is_memory_location"] = False
    op_arg_def["value"] = "D"

    op_args_def.append(op_arg_def)

    op_args_defs.append(op_args_def)

    # Def 1
    op_args_def = []

    op_arg_def = get_arg_def_template()
    op_arg_def["value_type"] = "module_name"
    op_arg_def["is_memory_location"] = False
    op_arg_def["value"] = "A"

    op_args_def.append(op_arg_def)

    op_arg_def = get_arg_def_template()
    op_arg_def["value_type"] = "module_name"
    op_arg_def["is_memory_location"] = False
    op_arg_def["value"] = "B"

    op_args_def.append(op_arg_def)

    op_args_defs.append(op_args_def)

    expected_match = True
    expected_args = deepcopy(op_args_defs[1])

    return (line, opcode, op_args_defs, expected_match, expected_args)


def gen_test_match_and_parse_line_input_1():
    """
    No args
    """
    line = "NOOP"
    opcode = "NOOP"

    op_args_defs = []

    expected_match = True
    expected_args = []

    return (line, opcode, op_args_defs, expected_match, expected_args)


def gen_test_match_and_parse_line_input_2():
    """
    Module mem ref
    """

    line = "JUMP [A]"
    opcode = "JUMP"

    op_args_defs = []

    # Def 0
    op_args_def = []

    op_arg_def = get_arg_def_template()
    op_arg_def["value_type"] = "module_name"
    op_arg_def["is_memory_location"] = True
    op_arg_def["value"] = "A"

    op_args_def.append(op_arg_def)

    op_args_defs.append(op_args_def)

    expected_match = True
    expected_args = deepcopy(op_args_defs[0])

    return (line, opcode, op_args_defs, expected_match, expected_args)


def gen_test_match_and_parse_line_input_3():
    """
    constant mem ref
    """

    line = "JUMP [$variable]"
    opcode = "JUMP"

    op_args_defs = []

    # Def 0
    op_args_def = []

    op_arg_def = get_arg_def_template()
    op_arg_def["value_type"] = "constant"
    op_arg_def["is_memory_location"] = True
    op_arg_def["value"] = ""

    op_args_def.append(op_arg_def)

    op_args_defs.append(op_args_def)

    expected_match = True
    expected_args = deepcopy(op_args_defs[0])
    expected_args[0]["value"] = "$variable"

    return (line, opcode, op_args_defs, expected_match, expected_args)


def gen_test_match_and_parse_line_input_4():
    """
    constant
    """

    line = "JUMP @label"
    opcode = "JUMP"

    op_args_defs = []

    # Def 0
    op_args_def = []

    op_arg_def = get_arg_def_template()
    op_arg_def["value_type"] = "constant"
    op_arg_def["is_memory_location"] = False
    op_arg_def["value"] = ""

    op_args_def.append(op_arg_def)

    op_args_defs.append(op_args_def)

    expected_match = True
    expected_args = deepcopy(op_args_defs[0])
    expected_args[0]["value"] = "@label"

    return (line, opcode, op_args_defs, expected_match, expected_args)


@pytest.mark.parametrize(
    "line,opcode,op_args_defs,expected_match,expected_args",
    [
        gen_test_match_and_parse_line_input_0(),
        gen_test_match_and_parse_line_input_1(),
        gen_test_match_and_parse_line_input_2(),
        gen_test_match_and_parse_line_input_3(),
        gen_test_match_and_parse_line_input_4(),

    ]
)
def test_match_and_parse_line(
    line, opcode, op_args_defs, expected_match, expected_args
):
    match, parsed_args = operation_utils.match_and_parse_line(
        line, opcode, op_args_defs
    )
    assert match == expected_match
    assert parsed_args == expected_args


def gen_test_match_and_parse_line_raises_input_0():
    """
    Incorrect args specified
    """

    line = "LOAD A C"
    opcode = "LOAD"

    op_args_defs = []

    # Def 0
    op_args_def = []

    op_arg_def = get_arg_def_template()
    op_arg_def["value_type"] = "module_name"
    op_arg_def["is_memory_location"] = False
    op_arg_def["value"] = "A"

    op_args_def.append(op_arg_def)

    op_arg_def = get_arg_def_template()
    op_arg_def["value_type"] = "module_name"
    op_arg_def["is_memory_location"] = False
    op_arg_def["value"] = "B"

    op_args_def.append(op_arg_def)

    op_args_defs.append(op_args_def)

    return (line, opcode, op_args_defs)


def gen_test_match_and_parse_line_raises_input_1():
    """
    Matches multiple arg possibilities
    """

    line = "LOAD A B"
    opcode = "LOAD"

    op_args_defs = []

    # Def 0
    op_args_def = []

    op_arg_def = get_arg_def_template()
    op_arg_def["value_type"] = "module_name"
    op_arg_def["is_memory_location"] = False
    op_arg_def["value"] = "A"

    op_args_def.append(op_arg_def)

    op_arg_def = get_arg_def_template()
    op_arg_def["value_type"] = "module_name"
    op_arg_def["is_memory_location"] = False
    op_arg_def["value"] = "B"

    op_args_def.append(op_arg_def)

    op_args_defs.append(op_args_def)

    # Def 1
    op_args_def = []

    op_arg_def = get_arg_def_template()
    op_arg_def["value_type"] = "module_name"
    op_arg_def["is_memory_location"] = False
    op_arg_def["value"] = "A"

    op_args_def.append(op_arg_def)

    op_arg_def = get_arg_def_template()
    op_arg_def["value_type"] = "module_name"
    op_arg_def["is_memory_location"] = False
    op_arg_def["value"] = "B"

    op_args_def.append(op_arg_def)

    op_args_defs.append(op_args_def)

    return (line, opcode, op_args_defs)


@pytest.mark.parametrize(
    "line,opcode,op_args_defs",
    [
        gen_test_match_and_parse_line_raises_input_0(),
        gen_test_match_and_parse_line_raises_input_1(),
    ]
)
def test_match_and_parse_line_raises(line, opcode, op_args_defs):
    with pytest.raises(InstructionParsingError):
        operation_utils.match_and_parse_line(line, opcode, op_args_defs)


def test_generate_possible_arg_list():
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
    assert operation_utils.generate_possible_arg_list(test_input) == expected
