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
    Marker,
    MarkerDefinition,
    DataSet,
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

# This is really over engineered :(
# Need to do some smarter mocking or maybe test generate machinecode seperately
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
                if expected_word.const_token is not None:
                    assert expected_word.const_token.value == res_word.const_token.value


@pytest.mark.parametrize("test_input, expected", [
    (
        [],
        type(None)
    ),
    (
        get_tokens("NOOP"),
        type(None)
    ),
    (
        get_tokens("$hello"),
        Marker
    ),
])
def test_Marker_from_tokens(test_input, expected):
    assert isinstance(Marker.from_tokens(test_input), expected)


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
        get_tokens("$my_marker"),
        type(None),
        tuple(),
    ),
    (
        get_tokens("$my_marker NOOP $marker"),
        type(None),
        tuple(),
    ),
    (
        get_tokens("$loop_start #3"),
        MarkerDefinition,
        ("loop_start", 3),
    ),

])
def test_MarkerDefinition_from_tokens(test_input, expected_type, expected_attrs):
    res = MarkerDefinition.from_tokens(test_input)
    assert isinstance(res, expected_type)
    if isinstance(res, MarkerDefinition):
        assert res.name == expected_attrs[0]
        assert res.value == expected_attrs[1]



@pytest.mark.parametrize("test_input, expected_type, expected_machinecode", [
    (
        [],
        type(None),
        tuple(),
    ),
    (
        get_tokens("$marker"),
        type(None),
        tuple(),
    ),
    (
        get_tokens("SET_ZERO"),
        type(None),
        tuple(),
    ),
    (
        get_tokens("DATA ACC"),
        type(None),
        tuple(),
    ),
    (
        get_tokens("DATA #1"),
        DataSet,
        (
            Word(const_token=get_tokens("#1")[0]),
        ),
    ),
    (
        get_tokens("DATA #12 $marker !alias"),
        DataSet,
        (
            Word(const_token=get_tokens("#12")[0]),
            Word(const_token=get_tokens("$marker")[0]),
            Word(const_token=get_tokens("!alias")[0]),
        ),
    ),
])
def test_DataSet_from_tokens(test_input, expected_type, expected_machinecode):
    res = DataSet.from_tokens(test_input)
    assert isinstance(res, expected_type)
    if isinstance(res, DataSet):
        assert len(expected_machinecode) == len(res.machinecode)
        for expected_word, res_word in zip(expected_machinecode, res.machinecode):
            assert expected_word.const_token.value == res_word.const_token.value
