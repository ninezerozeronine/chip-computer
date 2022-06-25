"""
The simple ALU Ops
"""
from ..instruction_listings import get_instruction_index
from ..instruction_components import (
    COPY,
    ACC,
    A,
    B,
    C,
    PC,
    SP,
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
    (COPY, ACC, A),
    (COPY, ACC, B),
    (COPY, ACC, C),
    (COPY, ACC, SP),
    (COPY, A, ACC),
    (COPY, A, B),
    (COPY, A, C),
    (COPY, A, SP),
    (COPY, B, ACC),
    (COPY, B, A),
    (COPY, B, C),
    (COPY, B, SP),
    (COPY, C, ACC),
    (COPY, C, A),
    (COPY, C, B),
    (COPY, C, SP),
    (COPY, PC, ACC),
    (COPY, PC, A),
    (COPY, PC, B),
    (COPY, PC, C),
    (COPY, PC, SP),
    (COPY, SP, ACC),
    (COPY, SP, A),
    (COPY, SP, B),
    (COPY, SP, C),
)


def generate_machinecode(signature, const_tokens):
    if signature not in _SUPPORTED_SIGNATURES:
        raise ValueError

    return [
        Word(value=get_instruction_index(signature))
    ]


def generate_microcode_templates():
    microcode_templates = []
    for signature in _SUPPORTED_SIGNATURES:
        instr_index = get_instruction_index(signature)
        instr_index_bitdef = number_utils.number_to_bitstring(
            instr_index, bit_width=8
        )
        flags_bitdefs = [FLAGS["ANY"]]

        control_steps = [
            [
                MODULE_CONTROL[utils.component_to_module_name(signature[1])]["OUT"],
                MODULE_CONTROL[utils.component_to_module_name(signature[2])]["IN"],
            ]
        ]
        templates = utils.assemble_instruction_steps(
            instr_index_bitdef, flags_bitdefs, control_steps
        )
        microcode_templates.extend(templates)
    return microcode_templates


def supports(signature):
    return signature in _SUPPORTED_SIGNATURES
