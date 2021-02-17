import pytest
from sixteen_bit_computer.assembly_tokens import (
    ALIAS,
    NUMBER,
    OPCODE,
    MODULE,
)
from sixteen_bit_computer.assembly_patterns import (
    NullPattern,
    AliasDefinition,
    Instruction,
)
from sixteen_bit_computer.new_assembler import get_tokens
from sixteen_bit_computer.data_structures import Word
from sixteen_bit_computer import instruction_components as ics


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
def test_NullPattern_from_tokens(test_input, expected):
    assert isinstance(NullPattern.from_tokens(test_input), expected)


@pytest.mark.parametrize("test_input, expected_type, expected_attrs", [
    (
        [],
        type(None),
        tuple(),
    ),
    (
        get_tokens("NOOP"),
        type(None),
        tuple(),
    ),
    (
        get_tokens("!my_alias"),
        type(None),
        tuple(),
    ),
    (
        get_tokens("!my_alias NOOP $marker"),
        type(None),
        tuple(),
    ),
    (
        get_tokens("!num_lives #3"),
        AliasDefinition,
        ("num_lives", 3),
    ),

])
def test_AliasDefinition_from_tokens(test_input, expected_type, expected_attrs):
    res = AliasDefinition.from_tokens(test_input)
    assert isinstance(res, expected_type)
    if isinstance(res, AliasDefinition):
        assert res.name == expected_attrs[0]
        assert res.value == expected_attrs[1]


@pytest.mark.parametrize("test_input, expected_type, expected_signature, expected_machinecode", [
    (
        [],
        type(None),
        tuple(),
        tuple(),
    ),
    (
        get_tokens("$marker"),
        type(None),
        tuple(),
        tuple(),
    ),
    (
        get_tokens("NOOP"),
        Instruction,
        (ics.NOOP,),
        (Word(),),
    ),
    (
        get_tokens("SET_ZERO ACC"),
        Instruction,
        (ics.SET_ZERO, ics.ACC),
        (Word(),),
    ),
])
def test_Instruction_from_tokens(test_input, expected_type, expected_signature, expected_machinecode):
    res = Instruction.from_tokens(test_input)
    assert isinstance(res, expected_type)
    if isinstance(res, Instruction):
        assert res.signature == expected_signature
        if expected_machinecode:
            assert len(expected_machinecode) == len(res.machinecode)
            for expected_word, res_word in zip(expected_machinecode, res.machinecode):
                assert expected_word.const_token == res_word.const_token
