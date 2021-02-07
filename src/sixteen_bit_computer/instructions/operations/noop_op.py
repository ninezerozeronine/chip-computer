from .. import listings
from ..machinecode import Word
from ..components import NOOP
from .. import number_utils
from ..microcode.hardware_mapping import (
    MODULE_CONTROLS_NONE,
    FLAGS,
)
from ..microcode.utils import assemble_instruction

_SUPPORTED_SIGNATURES = frozenset([
    (NOOP,),
])


def generate_machinecode(signature, const_tokens):
    """

    """
    if signature not in _SUPPORTED_SIGNATURES:
        raise ValueError

    return [
        Word(value=listings.get_instruction_index(signature))
    ]


def generate_microcode():
    """

    """
    data_templates = []

    for signature in _SUPPORTED_SIGNATURES:
        instr_index = listings.get_instruction_index(signature)
        instr_index_bitdef = number_utils.number_to_bitstring(
            instr_index, width=8
        )
        flags_bitdefs = [FLAGS["ANY"]]
        control_steps = [[MODULE_CONTROLS_NONE]]

        templates = assemble_instruction(
            instr_index_bitdef, flags_bitdefs, control_steps
        )
        data_templates.extend(templates)

    return data_templates


def supports(signature):
    return signature in _SUPPORTED_SIGNATURES
