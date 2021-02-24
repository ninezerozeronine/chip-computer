"""
The simple ALU Ops
"""
from ..instruction_listings import get_instruction_index
from ..instruction_components import (
    ADD,
    AND,
    A,
    B,
    C,
    CONST,
    M_CONST,
)
from .. import number_utils
from . import utils
from ..language_defs import (
    FLAGS,
    MODULE_CONTROL,
    ALU_CONTROL_FLAGS,
)


_SUPPORTED_SIGNATURES = frozenset([
    (ADD, A),
    (ADD, B),
    (ADD, C),
    (ADD, CONST),
    (ADD, M_CONST),
    (AND, A),
    (AND, B),
    (AND, C),
    (AND, CONST),
    (AND, M_CONST),
])

# ADD
# SUB
# AND
# OR
# XOR
# NAND
# NOR
# NXOR


def generate_machinecode(signature, const_tokens):
    if signature not in _SUPPORTED_SIGNATURES:
        raise ValueError

    if signature[1] in (A, B, C):
        return _add_module_machinecode(signature)

    if signature[1] in (CONST, M_CONST):
        return _add_const_machinecode(signature, const_tokens)


def _add_module_machinecode(signature):
    return [
        Word(value=get_instruction_index(signature))
    ]


def _add_const_machinecode(signature, const_tokens):
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
    AND: "A_AND_B",
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
            MODULE_CONTROL["PC"]["OUT"],
            MODULE_CONTROL["MAR"]["IN"],
        ]

        step_1 = [
            MODULE_CONTROL["MEM"]["READ_FROM"],
            MODULE_CONTROL["ALU"]["STORE_RESULT"],
            MODULE_CONTROL["ALU"]["STORE_FLAGS"],
            MODULE_CONTROL["PC"]["COUNT"],
        ]
        step_1.extend(ALU_CONTROL_FLAGS[_alu_opcode_to_alu_mode(signature[0])])

        step_2 = [
            MODULE_CONTROL["ALU"]["OUT"],
            MODULE_CONTROL["ACC"]["IN"],
        ]

        control_steps = [step_0, step_1, step_2]

    elif signature[1] == M_CONST:
        step_0 = [
            MODULE_CONTROL["PC"]["OUT"],
            MODULE_CONTROL["MAR"]["IN"],
        ]

        # This is a little sketchy, on the rising clock edge we're
        # simultaneously:
        # - Reading a value from memory
        # - Changing the address in memory we're looking at
        # step_1 = [
        #     MODULE_CONTROL["MEM"]["READ_FROM"],
        #     MODULE_CONTROL["MAR"]["IN"],
        #     MODULE_CONTROL["PC"]["COUNT"],
        # ]

        # Temporarily storing the memory address in the ALU for safety
        # reasons...
        step_1 = [
            MODULE_CONTROL["MEM"]["READ_FROM"],
            MODULE_CONTROL["ALU"]["A_IS_BUS"],
            MODULE_CONTROL["ALU"]["STORE_RESULT"],
        ]
        step_1.extend(ALU_CONTROL_FLAGS["A"])

        step_2 = [
            MODULE_CONTROL["ALU"]["OUT"],
            MODULE_CONTROL["MAR"]["IN"],
        ]

        step_3 = [
            MODULE_CONTROL["MEM"]["READ_FROM"],
            MODULE_CONTROL["ALU"]["STORE_RESULT"],
            MODULE_CONTROL["ALU"]["STORE_FLAGS"],
        ]
        step_3.extend(ALU_CONTROL_FLAGS[_alu_opcode_to_alu_mode(signature[0])])

        step_4 = [
            MODULE_CONTROL["ALU"]["OUT"],
            MODULE_CONTROL["ACC"]["IN"],
        ]

        control_steps = [step_0, step_1, step_2, step_3, step_4]

    return control_steps


def supports(signature):
    return signature in _SUPPORTED_SIGNATURES
