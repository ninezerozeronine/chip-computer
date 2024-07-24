"""
The SET operation.

Sets the given module to zero.
"""

from .. import instruction_listings
from .. import number_utils
from . import utils
from ..data_structures import Word
from ..instruction_components import (
    SET,
    ACC,
    A,
    B,
    C,
    SP,
    CONST,
    M_CONST,
)
from ..language_defs import (
    MODULE_CONTROL,
    FLAGS,
)


_SUPPORTED_SIGNATURES = (
    (SET, ACC, CONST),
    (SET, A, CONST),
    (SET, B, CONST),
    (SET, C, CONST),
    (SET, SP, CONST),
    (SET, M_CONST, CONST),
)
"""
The list of signatures this operation supports.

An instruction signature is a tuple of the :mod:`Instruction component
<.instruction_components>` s it's made up of.
"""


def generate_machinecode(signature, const_tokens):
    """
    Generate machinecode for the given SET operation.

    Args:
        signature (Tuple(:mod:`Instruction component<.instruction_components>`)):
            The signature to check.
        const_tokens (list(Token)): The tokens that represent constant
            values in the instruction.
    Returns:
        list(Word): The machinecode for the given signature.
    """
    if signature not in _SUPPORTED_SIGNATURES:
        raise ValueError

    machinecode = [
        Word(value=instruction_listings.get_instruction_index(signature))
    ]

    if signature[1] == M_CONST:
        machinecode.append(Word(const_token=const_tokens[1]))
        machinecode.append(Word(const_token=const_tokens[0]))
    else:
        machinecode.append(Word(const_token=const_tokens[0]))

    return machinecode


def generate_microcode_templates():
    """
    Generate microcode for the SET operation.

    Returns:
        list(DataTemplate): DataTemplates for all the SET microcode.
    """
    data_templates = []

    for signature in _SUPPORTED_SIGNATURES:
        instr_index = instruction_listings.get_instruction_index(signature)
        instr_index_bitdef = number_utils.number_to_bitstring(
            instr_index, bit_width=8
        )
        flags_bitdefs = [FLAGS["ANY"]]

        if signature[1] == M_CONST:
            step_0 = [
                MODULE_CONTROL["MEM"]["READ_FROM"],
                MODULE_CONTROL["SHR"]["IN"],
                MODULE_CONTROL["PC"]["COUNT"],
                MODULE_CONTROL["MAR"]["COUNT"],
            ]
            step_1 = [
                MODULE_CONTROL["MEM"]["READ_FROM"],
                MODULE_CONTROL["MAR"]["IN"],
                MODULE_CONTROL["PC"]["COUNT"],
            ]
            step_2 = [
                MODULE_CONTROL["MEM"]["WRITE_TO"],
                MODULE_CONTROL["SHR"]["OUT"],
            ]
            control_steps = [step_0, step_1, step_2]
        else:
            step_0 = [
                MODULE_CONTROL["MEM"]["READ_FROM"],
                MODULE_CONTROL[utils.component_to_module_name(signature[1])]["IN"],
                MODULE_CONTROL["PC"]["COUNT"],
            ]
            control_steps = [step_0]

        templates = utils.assemble_instruction_steps(
            instr_index_bitdef, flags_bitdefs, control_steps
        )
        data_templates.extend(templates)

    return data_templates


def supports(signature):
    """
    Whether this operation provides a definition for the given signature.

    Args:
        signature (Tuple(:mod:`Instruction component<.instruction_components>`)):
            The signature to check.
    Returns:
        bool: Whether it's supported or not.
    """
    return signature in _SUPPORTED_SIGNATURES
