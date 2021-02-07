from .. import listings
from ..machinecode import Word
from ..components import SET_ZERO, ACC, A, B, C

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
        Word(value=listings.get_instruction_index(signature))
    ]


def generate_microcode():
    """

    """
    data_templates = []

    for signature in _SUPPORTED_SIGNATURES:
        templates = _generate_microcode_for_sig(signature)
        data_templates.extend(templates)

    return data_templates


def _generate_microcode_for_sig(signature):
    """

    """
    instr_index = listings.get_instruction_index(signature)
    instr_index_bitdef = number_utils.number_to_bitstring(
        instr_index, width=8
    )
    flags_bitdefs = [FLAGS["ANY"]]

    step_0 = [
        MODULE_CONTROL["ALU"]["STORE_RESULT"],
    ]
    step_0.extend(ALU_CONTROL_FLAGS["ZERO"])

    step_1 = [
        MODULE_CONTROL["ALU"]["OUT"],
        MODULE_CONTROL[component_to_module_name(signaure[1])]["IN"],
    ]

    control_steps = [step_0, step_1]

    return assemble_instruction(
        instr_index_bitdef, flags_bitdefs, control_steps
    )


def supports(signature):
    return signature in _SUPPORTED_SIGNATURES
