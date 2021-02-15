from .. import instruction_listings
from .. import number_utils
from .utils import assemble_instruction_steps
from ..data_structures import Word
from ..instruction_components import SET_ZERO, ACC, A, B, C
from ..language_defs import (
    component_to_module_name,
    MODULE_CONTROL,
    ALU_CONTROL_FLAGS,
    FLAGS,
)


_SUPPORTED_SIGNATURES = frozenset([
    (SET_ZERO, ACC),
    (SET_ZERO, A),
    (SET_ZERO, B),
    (SET_ZERO, C),
])


def generate_machinecode(signature, const_tokens):
    """

    """
    if signature not in _SUPPORTED_SIGNATURES:
        raise ValueError

    return [
        Word(value=instruction_listings.get_instruction_index(signature))
    ]


def generate_microcode_templates():
    """

    """
    data_templates = []

    for signature in _SUPPORTED_SIGNATURES:
        templates = _generate_microcode_templates_for_sig(signature)
        data_templates.extend(templates)

    return data_templates


def _generate_microcode_templates_for_sig(signature):
    """

    """
    instr_index = instruction_listings.get_instruction_index(signature)
    instr_index_bitdef = number_utils.number_to_bitstring(
        instr_index, bit_width=8
    )
    flags_bitdefs = [FLAGS["ANY"]]

    step_0 = [
        MODULE_CONTROL["ALU"]["STORE_RESULT"],
    ]
    step_0.extend(ALU_CONTROL_FLAGS["ZERO"])

    step_1 = [
        MODULE_CONTROL["ALU"]["OUT"],
        MODULE_CONTROL[component_to_module_name(signature[1])]["IN"],
    ]

    control_steps = [step_0, step_1]

    return assemble_instruction_steps(
        instr_index_bitdef, flags_bitdefs, control_steps
    )


def supports(signature):
    return signature in _SUPPORTED_SIGNATURES
