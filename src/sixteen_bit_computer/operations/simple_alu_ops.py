"""
The simple ALU Ops
"""

import textwrap

from ..instruction_listings import get_instruction_index
from ..instruction_components import (
    ADD,
    SUB,
    AND,
    OR,
    XOR,
    NAND,
    NOR,
    NXOR,
    A,
    B,
    C,
    CONST,
    M_CONST,
    component_to_assembly,
)
from .. import number_utils
from . import utils
from ..data_structures import Word
from ..language_defs import (
    FLAGS,
    MODULE_CONTROL,
    ALU_CONTROL_FLAGS,
)


_SUPPORTED_SIGNATURES = (
    (ADD, A),
    (ADD, B),
    (ADD, C),
    (ADD, CONST),
    (ADD, M_CONST),
    (SUB, A),
    (SUB, B),
    (SUB, C),
    (SUB, CONST),
    (SUB, M_CONST),
    (AND, A),
    (AND, B),
    (AND, C),
    (AND, CONST),
    (AND, M_CONST),
    (OR, A),
    (OR, B),
    (OR, C),
    (OR, CONST),
    (OR, M_CONST),
    (XOR, A),
    (XOR, B),
    (XOR, C),
    (XOR, CONST),
    (XOR, M_CONST),
    (NAND, A),
    (NAND, B),
    (NAND, C),
    (NAND, CONST),
    (NAND, M_CONST),
    (NOR, A),
    (NOR, B),
    (NOR, C),
    (NOR, CONST),
    (NOR, M_CONST),
    (NXOR, A),
    (NXOR, B),
    (NXOR, C),
    (NXOR, CONST),
    (NXOR, M_CONST),
)


def generate_machinecode(signature, const_tokens):
    if signature not in _SUPPORTED_SIGNATURES:
        raise ValueError

    if signature[1] in (A, B, C):
        return [
            Word(value=get_instruction_index(signature))
        ]

    if signature[1] in (CONST, M_CONST):
        return [
            Word(value=get_instruction_index(signature)),
            Word(const_token=const_tokens[0]),
        ]


def generate_microcode_templates():
    microcode_templates = []
    for signature in _SUPPORTED_SIGNATURES:
        instr_index = get_instruction_index(signature)
        instr_index_bitdef = number_utils.number_to_bitstring(
            instr_index, bit_width=8
        )
        flags_bitdefs = [FLAGS["ANY"]]
        control_steps = _generate_control_steps(signature)
        templates = utils.assemble_instruction_steps(
            instr_index_bitdef, flags_bitdefs, control_steps
        )
        microcode_templates.extend(templates)
    return microcode_templates


_ALU_OPCODE_TO_ALU_MODE = {
    ADD: "A_PLUS_B",
    SUB: "A_MINUS_B",
    AND: "A_AND_B",
    OR: "A_OR_B",
    XOR: "A_XOR_B",
    NAND: "A_NAND_B",
    NOR: "A_NOR_B",
    NXOR: "A_NXOR_B",
}


def _alu_opcode_to_alu_mode(component):
    return _ALU_OPCODE_TO_ALU_MODE[component]


def _generate_control_steps(signature):
    if signature[1] in (A, B, C):
        step_0 = [
            MODULE_CONTROL[utils.component_to_module_name(signature[1])]["OUT"],
            MODULE_CONTROL["ALU"]["STORE_RESULT"],
            MODULE_CONTROL["ALU"]["STORE_FLAGS"],
        ]
        step_0.extend(ALU_CONTROL_FLAGS[_alu_opcode_to_alu_mode(signature[0])])

        step_1 = [
            MODULE_CONTROL["ALU"]["OUT"],
            MODULE_CONTROL["ACC"]["IN"],
        ]

        control_steps = [step_0, step_1]

    elif signature[1] == CONST:
        step_0 = [
            MODULE_CONTROL["MEM"]["READ_FROM"],
            MODULE_CONTROL["ALU"]["STORE_RESULT"],
            MODULE_CONTROL["ALU"]["STORE_FLAGS"],
            MODULE_CONTROL["PC"]["COUNT"],
        ]
        step_0.extend(ALU_CONTROL_FLAGS[_alu_opcode_to_alu_mode(signature[0])])

        step_1 = [
            MODULE_CONTROL["ALU"]["OUT"],
            MODULE_CONTROL["ACC"]["IN"],
        ]

        control_steps = [step_0, step_1]

    elif signature[1] == M_CONST:
        step_0 = [
            MODULE_CONTROL["MEM"]["READ_FROM"],
            MODULE_CONTROL["MAR"]["IN"],
            MODULE_CONTROL["PC"]["COUNT"]
        ]

        step_1 = [
            MODULE_CONTROL["MEM"]["READ_FROM"],
            MODULE_CONTROL["ALU"]["STORE_RESULT"],
            MODULE_CONTROL["ALU"]["STORE_FLAGS"],
        ]
        step_1.extend(ALU_CONTROL_FLAGS[_alu_opcode_to_alu_mode(signature[0])])

        step_2 = [
            MODULE_CONTROL["ALU"]["OUT"],
            MODULE_CONTROL["ACC"]["IN"],
        ]

        control_steps = [step_0, step_1, step_2]

    return control_steps


def supports(signature):
    return signature in _SUPPORTED_SIGNATURES


def gen_test_assembly():
    """
    Generate assembly code that verifies the instructions work as expected.
    """

    test_assembly = """\
        ////////////////////////////////////////////////////////////////
        // ADD
        ////////////////////////////////////////////////////////////////

    &add_0
        SET ACC #1
        SET A #2
        ADD A
        JUMP_IF_ACC_EQ #3 &add_1
        HALT

    &add_1
        SET ACC #456
        SET B #111
        ADD B
        JUMP_IF_ACC_EQ #567 &add_2
        HALT

    &add_2
        SET ACC #3333
        SET C #2222
        ADD C
        JUMP_IF_ACC_EQ #5555 &add_3
        HALT

    &add_3
        SET ACC #123
        ADD #-23
        JUMP_IF_ACC_EQ #100 &add_4
        HALT

    $v_add_0 #42
    &add_4
        SET ACC #42
        ADD [$v_add_0]
        JUMP_IF_ACC_EQ #84 &add_5
        HALT

    &add_5
        // Test carry flag
        SET ACC #60000
        ADD #60000
        JUMP_IF_CARRY &add_6
        HALT

    &add_6
        // Test no carry flag
        SET ACC #5
        ADD #10
        JUMP_IF_NOT_CARRY &sub_0
        HALT

        ////////////////////////////////////////////////////////////////
        // SUB
        ////////////////////////////////////////////////////////////////

    &sub_0
        SET ACC #1
        SET A #2
        SUB A
        JUMP_IF_ACC_EQ #-1 &sub_1
        HALT

    &sub_1
        SET ACC #456
        SET B #111
        SUB B
        JUMP_IF_ACC_EQ #345 &sub_2
        HALT

    &sub_2
        SET ACC #3333
        SET C #2222
        SUB C
        JUMP_IF_ACC_EQ #1111 &sub_3
        HALT

    &sub_3
        SET_ZERO ACC
        SUB #1
        JUMP_IF_ACC_EQ #0xFFFF &sub_4
        HALT

    $v_sub_0 #42
    &sub_4
        SET ACC #42
        SUB [$v_sub_0]
        JUMP_IF_EQ_ZERO ACC &sub_5
        HALT

    &sub_5
        // Test borrow flag
        SET ACC #34
        SUB #500
        JUMP_IF_BORROW &sub_6
        HALT

    &sub_6
        // Test no carry flag
        SET ACC #34
        SUB #3
        JUMP_IF_NOT_BORROW &and_0
        HALT
        
        ////////////////////////////////////////////////////////////////
        // AND
        ////////////////////////////////////////////////////////////////

    &and_0
        SET ACC        #0b1111
        SET A          #0b0101
        AND A
        JUMP_IF_ACC_EQ #0b0101 &and_1
        HALT

    &and_1
        SET ACC        #0b1111_0000_1111_0000
        SET B          #0b1111_1111_1111_1111
        AND B
        JUMP_IF_ACC_EQ #0b1111_0000_1111_0000 &and_2
        HALT

    &and_2
        SET ACC        #0b1100_1111
        SET C          #0b0000_0000
        AND C
        JUMP_IF_ACC_EQ #0b0000_0000 &and_3
        HALT

    &and_3
        SET ACC        #0b0011_1100_1111_0000
        AND            #0b1111_1111_0000_1111
        JUMP_IF_ACC_EQ #0b0011_1100_0000_0000 &and_4
        HALT

    $v_and_0           #0b1
    &and_4
        SET ACC        #0b1
        AND [$v_and_0]
        JUMP_IF_ACC_EQ #0b1 &nand_0
        HALT

        ////////////////////////////////////////////////////////////////
        // NAND
        ////////////////////////////////////////////////////////////////

    &nand_0
        SET ACC        #0b0000_0000_0000_1111
        SET A          #0b1111_1111_1111_0101
        NAND A
        JUMP_IF_ACC_EQ #0b1111_1111_1111_1010 &nand_1
        HALT

    &nand_1
        SET ACC        #0b1111_0000_1111_0000
        SET B          #0b1111_1111_1111_1111
        NAND B
        JUMP_IF_ACC_EQ #0b0000_1111_0000_1111 &nand_2
        HALT

    &nand_2
        SET ACC        #0b1111_1111_1100_1111
        SET C          #0b1111_1111_0000_0000
        NAND C
        JUMP_IF_ACC_EQ #0b0000_0000_1111_1111 &nand_3
        HALT

    &nand_3
        SET ACC        #0b0011_1100_1111_0000
        NAND           #0b1111_1111_0000_1111
        JUMP_IF_ACC_EQ #0b1100_0011_1111_1111 &nand_4
        HALT

    $v_nand_0          #0b0000_0000_0000_0001
    &nand_4
        SET ACC        #0b0000_0000_0000_0001
        NAND [$v_nand_0]
        JUMP_IF_ACC_EQ #0b1111_1111_1111_1110 &or_0
        HALT

        ////////////////////////////////////////////////////////////////
        // OR
        ////////////////////////////////////////////////////////////////

    &or_0
        SET ACC        #0b1111
        SET A          #0b0101
        OR A
        JUMP_IF_ACC_EQ #0b1111 &or_1
        HALT

    &or_1
        SET ACC        #0b1111_0000_1111_0000
        SET B          #0b1111_1111_1111_1111
        OR B
        JUMP_IF_ACC_EQ #0b1111_1111_1111_1111 &or_2
        HALT

    &or_2
        SET ACC        #0b1100_1111
        SET C          #0b0000_0000
        OR C
        JUMP_IF_ACC_EQ #0b1100_1111 &or_3
        HALT

    &or_3
        SET ACC        #0b0011_1100_1111_0000
        OR             #0b1111_1111_0000_1111
        JUMP_IF_ACC_EQ #0b1111_1111_1111_1111 &or_4
        HALT

    $v_or_0            #0b1
    &or_4
        SET ACC        #0b1
        OR [$v_or_0]
        JUMP_IF_ACC_EQ #0b1 &nor_0
        HALT

        ////////////////////////////////////////////////////////////////
        // NOR
        ////////////////////////////////////////////////////////////////

    &nor_0
        SET ACC        #0b1111_0101_0000_1111
        SET A          #0b0010_0010_1111_0101
        NOR A
        JUMP_IF_ACC_EQ #0b0000_1000_0000_0000 &nor_1
        HALT

    &nor_1
        SET ACC        #0b1111_0000_1111_0000
        SET B          #0b1111_1111_1111_1111
        NOR B
        JUMP_IF_ACC_EQ #0b0000_0000_0000_0000 &nor_2
        HALT

    &nor_2
        SET ACC        #0b0000_0000_1100_1111
        SET C          #0b0000_1111_0000_0000
        NOR C
        JUMP_IF_ACC_EQ #0b1111_0000_0011_0000 &nor_3
        HALT

    &nor_3
        SET ACC        #0b0011_1100_1111_0000
        NOR            #0b0111_1110_0000_1110
        JUMP_IF_ACC_EQ #0b1000_0001_0000_0001 &nor_4
        HALT

    $v_nor_0           #0b0100_0000_0000_0001
    &nor_4
        SET ACC        #0b0000_0010_0000_0001
        NOR [$v_nor_0]
        JUMP_IF_ACC_EQ #0b1011_1101_1111_1110 &xor_0
        HALT

        ////////////////////////////////////////////////////////////////
        // XOR
        ////////////////////////////////////////////////////////////////

    &xor_0
        SET ACC        #0b1111
        SET A          #0b0101
        XOR A
        JUMP_IF_ACC_EQ #0b1010 &xor_1
        HALT

    &xor_1
        SET ACC        #0b0011
        SET B          #0b0101
        XOR B
        JUMP_IF_ACC_EQ #0b0110 &xor_2
        HALT

    &xor_2
        SET ACC        #0b1100_1111
        SET C          #0b0000_0000
        XOR C
        JUMP_IF_ACC_EQ #0b1100_1111 &xor_3
        HALT

    &xor_3
        SET ACC        #0b0011_1100_1011_0001
        XOR            #0b1111_1111_0000_1111
        JUMP_IF_ACC_EQ #0b1100_0011_1011_1110 &xor_4
        HALT

    $v_xor_0           #0b1
    &xor_4
        SET ACC        #0b1
        XOR [$v_xor_0]
        JUMP_IF_ACC_EQ #0b0 &nxor_0
        HALT

        ////////////////////////////////////////////////////////////////
        // NXOR
        ////////////////////////////////////////////////////////////////

    &nxor_0
        SET ACC        #0b1111_1111_1111_1111
        SET A          #0b0000_0000_0000_0101
        NXOR A
        JUMP_IF_ACC_EQ #0b0000_0000_0000_0101 &nxor_1
        HALT

    &nxor_1
        SET ACC        #0b1111_1111_1111_0011
        SET B          #0b1111_1111_1111_0101
        NXOR B
        JUMP_IF_ACC_EQ #0b1111_1111_1111_1001 &nxor_2
        HALT

    &nxor_2
        SET ACC        #0b0111_1100_1100_1111
        SET C          #0b1011_0000_0000_0000
        NXOR C
        JUMP_IF_ACC_EQ #0b0011_0011_0011_0000 &nxor_3
        HALT

    &nxor_3
        SET ACC        #0b0011_1100_1011_0001
        NXOR           #0b1111_1111_0000_1111
        JUMP_IF_ACC_EQ #0b0011_1100_0100_0001 &nxor_4
        HALT

    $v_nxor_0          #0b1110_1111_1110_1111
    &nxor_4
        SET ACC        #0b1111_1110_1110_1111
        NXOR [$v_nxor_0]
        JUMP_IF_ACC_EQ #0b1110_1110_1111_1111 &nxor_done
        HALT

    &nxor_done
        NOOP
    """
    
    return textwrap.dedent(test_assembly)


def gen_all_assembly():
    """
    Generate assembly lines for all the instructions this module supports.

    Returns:
        list(str): The assembly lines.
    """
    ret = []
    for signature in _SUPPORTED_SIGNATURES:
        ret.append(" ".join(
            [component_to_assembly(component) for component in signature]
        ))
    return ret
