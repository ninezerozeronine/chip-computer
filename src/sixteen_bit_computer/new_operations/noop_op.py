from .. import instruction_listings
from ..data_structures import Word
from ..instruction_components import NOOP
from .. import number_utils
from ..language_defs import (
    MODULE_CONTROLS_NONE,
    FLAGS,
)
from . import utils

_SUPPORTED_SIGNATURES = frozenset([
    (NOOP,),
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
        instr_index = instruction_listings.get_instruction_index(signature)
        instr_index_bitdef = number_utils.number_to_bitstring(
            instr_index, bit_width=8
        )
        flags_bitdefs = [FLAGS["ANY"]]
        control_steps = [[MODULE_CONTROLS_NONE]]

        templates = utils.assemble_instruction_steps(
            instr_index_bitdef, flags_bitdefs, control_steps
        )
        data_templates.extend(templates)

    return data_templates


def supports(signature):
    return signature in _SUPPORTED_SIGNATURES
