"""
The simple ALU Ops
"""
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
