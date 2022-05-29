import pytest
from sixteen_bit_computer.assembly_tokens import (
    ALIAS,
    NUMBER,
    OPCODE,
    MODULE,
)
from sixteen_bit_computer.assembly_patterns import (
    NullPattern,
    AliasDef,
    Anchor,
    Label,
    Variable,
    VariableDef,
    Instruction,
)
from sixteen_bit_computer.new_assembler import get_tokens
from sixteen_bit_computer.data_structures import Word
from sixteen_bit_computer import instruction_components as ics

# Null
@pytest.mark.parametrize("test_input, expected", [
    (
        [],
        NullPattern
    ),
    (
        get_tokens("NOOP"),
        type(None)
    ),
    (
        get_tokens("#123"),
        type(None)
    ),
])
def test_NullPattern(test_input, expected):
    assert isinstance(NullPattern.from_tokens(test_input), expected)

# Alias
@pytest.mark.parametrize("test_input, expected_type, expected_attrs", [
    (
        "",
        type(None),
        tuple(),
    ),
    (
        "NOOP",
        type(None),
        tuple(),
    ),
    (
        "!my_alias",
        type(None),
        tuple(),
    ),
    (
        "!my_alias NOOP $marker",
        type(None),
        tuple(),
    ),
    (
        "!num_lives #3",
        AliasDef,
        ("num_lives", 3),
    ),
])
def test_AliasDef(test_input, expected_type, expected_attrs):
    tokens = get_tokens(test_input)
    res = AliasDef.from_tokens(tokens)
    assert isinstance(res, expected_type)
    if isinstance(res, AliasDef):
        assert res.name == expected_attrs[0]
        assert res.value == expected_attrs[1]


# Anchor
@pytest.mark.parametrize("test_input, is_anchor", [
    ("", False),
    ("NOOP", False),
    ("!my_alias", False),
    ("@", False),
    ("@ NOOP", False),
    ("@ !myalias", False),
    ("@ #23", True),
    ("@ #0b01001", True),
])
def test_Anchor(test_input, is_anchor):
    tokens = get_tokens(test_input)
    res = Anchor.from_tokens(tokens)
    if is_anchor:
        assert isinstance(res, Anchor)


@pytest.mark.parametrize("test_input, location", [
    ("@ #23", 23),
    ("@ #0xFF", 255),
])
def test_Anchor_location(test_input, location):
    tokens = get_tokens(test_input)
    res = Anchor.from_tokens(tokens)
    assert res.location == location


# Label
@pytest.mark.parametrize("test_input, is_label", [
    ("", False),
    ("NOOP", False),
    ("!my_alias", False),
    ("$variable", False),
    ("AND &label", False),
    ("&mylabel", True),
    ("&loop_start2", True),
])
def test_Label(test_input, is_label):
    tokens = get_tokens(test_input)
    res = Label.from_tokens(tokens)
    if is_label:
        assert isinstance(res, Label)


@pytest.mark.parametrize("test_input, label_name", [
    ("&mylabel", "mylabel"),
    ("&loop_start2", "loop_start2"),
])
def test_Label_name(test_input, label_name):
    tokens = get_tokens(test_input)
    res = Label.from_tokens(tokens)
    assert res.name == label_name


# Variable
@pytest.mark.parametrize("test_input, is_variable", [
    ("", False),
    ("NOOP", False),
    ("!my_alias", False),
    ("&foo AND", False),
    ("NOOP [$variable] ACC", False),
    ("$myvar", True),
    ("$VAR_2", True),
])
def test_Variable(test_input, is_variable):
    tokens = get_tokens(test_input)
    res = Variable.from_tokens(tokens)
    if is_variable:
        assert isinstance(res, Variable)


@pytest.mark.parametrize("test_input, variable_name", [
    ("$myvariable", "myvariable"),
    ("$NUM_LIVES", "NUM_LIVES"),
])
def test_Variable_name(test_input, variable_name):
    tokens = get_tokens(test_input)
    res = Variable.from_tokens(tokens)
    assert res.name == variable_name


# VariableDef
@pytest.mark.parametrize("test_input, is_variabledef", [
    ("", False),
    ("NOOP", False),
    ("!my_alias", False),
    ("&foo AND", False),
    ("NOOP [$variable] ACC", False),
    ("$myvar #32", True),
    ("$VAR_2 #0x12", True),
    ("$VAR_2 #0xFF #23 !myalias", True),
])
def test_VariableDef(test_input, is_variabledef):
    tokens = get_tokens(test_input)
    res = VariableDef.from_tokens(tokens)
    if is_variabledef:
        assert isinstance(res, VariableDef)


@pytest.mark.parametrize("test_input, variabledef_name", [
    ("$myvar #32", "myvar"),
    ("$VAR_2 #0x12", "VAR_2"),
    ("$VAR_2 #0xFF #23 !myalias", "VAR_2"),
])
def test_VariableDef_name(test_input, variabledef_name):
    tokens = get_tokens(test_input)
    res = VariableDef.from_tokens(tokens)
    assert res.name == variabledef_name


@pytest.mark.parametrize("test_input, expected_machinecode", [
    (
        "$var #12",
        (Word(const_token=get_tokens("#12")[0],),)
    ),
    (
        "$var #12 #0b101",
        (
            Word(const_token=get_tokens("#12")[0],),
            Word(const_token=get_tokens("#0b101")[0],)
        )
    ),
    (
        "$var #12 #0b101 !myalias",
        (
            Word(const_token=get_tokens("#12")[0],),
            Word(const_token=get_tokens("#0b101")[0],),
            Word(const_token=get_tokens("!myalias")[0],),
        )
    ),
])
def test_VariableDef_machinecode(test_input, expected_machinecode):
    tokens = get_tokens(test_input)
    res = VariableDef.from_tokens(tokens)
    assert len(expected_machinecode) == len(res.machinecode)
    for expected_word, res_word in zip(expected_machinecode, res.machinecode):
        assert expected_word.const_token.value == res_word.const_token.value


# Instruction
@pytest.mark.parametrize("test_input, expected_type", [
    (
        "",
        type(None),
    ),
    (
        "$variable",
        type(None),
    ),
    (
        "NOOP",
        Instruction,
    ),
    (
        "SET_ZERO ACC",
        Instruction,
    ),
    (
        "ADD A",
        Instruction,
    ),
    (
        "AND #12",
        Instruction,
    ),
    (
        "AND [!my_alias]",
        Instruction,
    ),
])
def test_Instruction(test_input, expected_type):
    tokens = get_tokens(test_input)
    res = Instruction.from_tokens(tokens)
    assert isinstance(res, expected_type)


@pytest.mark.parametrize("test_input, expected_signature", [
    (
        "NOOP",
        (ics.NOOP,),
    ),
    (
        "SET_ZERO ACC",
        (ics.SET_ZERO, ics.ACC),
    ),
    (
        "ADD A",
        (ics.ADD, ics.A),
    ),
    (
        "AND #12",
        (ics.AND, ics.CONST),
    ),
    (
        "AND [!my_alias]",
        (ics.AND, ics.M_CONST),
    ),
])
def test_Instruction_signature(test_input, expected_signature):
    tokens = get_tokens(test_input)
    res = Instruction.from_tokens(tokens)
    assert res.signature == expected_signature


@pytest.mark.parametrize("test_input, expected_machinecode", [
    (
        "NOOP",
        (Word(),),
    ),
    (
        "SET_ZERO ACC",
        (Word(),),
    ),
    (
        "ADD A",
        (Word(),),
    ),
    (
        "AND #12",
        (Word(), Word(const_token=get_tokens("#12")[0])),
    ),
    (
        "AND [!my_alias]",
        (Word(), Word(const_token=get_tokens("!my_alias")[0])),
    ),
])
def test_Instruction_machinecode(test_input, expected_machinecode):
    tokens = get_tokens(test_input)
    res = Instruction.from_tokens(tokens)
    assert len(expected_machinecode) == len(res.machinecode)
    for expected_word, res_word in zip(expected_machinecode, res.machinecode):
        if expected_word.const_token is not None:
            assert expected_word.const_token.value == res_word.const_token.value



