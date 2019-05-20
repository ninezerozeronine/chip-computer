"""
Example and explanation of required functions for an operation module.
"""

from ..language_defs import (
    INSTRUCTION_GROUPS,
    SRC_REGISTERS,
    DEST_REGISTERS,
    MODULE_CONTROL,
    FLAGS,
)
from ..operation_utils import assemble_instruction, match_and_parse_line
from ..data_structures import (
    get_arg_def_template, get_machine_code_byte_template
)

_NAME = "JUMP"


def generate_microcode_templates():
    """
    Generate microcode for all the JUMP instructions.

    Returns:
        list(DataTemplate): DataTemplates for all the JUMP instructions.
    """

    data_templates = []

    signatures = generate_signatures()
    for signature in signatures:
        templates = generate_operation_templates(signature)
        data_templates.extend(templates)

    return data_templates


def generate_signatures():
    """
    Generate all the argument signatures for the jump operation.

    Returns:
        list(list(dict)): All possible signatures, See
        :func:`~.get_arg_def_template` for more information on an
        argument definition dictionary.
    """

    signatures = []
    direct_modules = ("ACC", "A", "B", "C", "SP")
    memory_refs = ("ACC", "A", "B", "C", "PC", "SP")

    for module in direct_modules:
        arg_def = get_arg_def_template()
        arg_def["value_type"] = "module_name"
        arg_def["is_memory_location"] = False
        arg_def["value"] = module
        signatures.append([arg_def])

    for module in memory_refs:
        arg_def = get_arg_def_template()
        arg_def["value_type"] = "module_name"
        arg_def["is_memory_location"] = True
        arg_def["value"] = module
        signatures.append([arg_def])

    arg_def = get_arg_def_template()
    arg_def["value_type"] = "constant"
    arg_def["is_memory_location"] = False
    signatures.append([arg_def])

    arg_def = get_arg_def_template()
    arg_def["value_type"] = "constant"
    arg_def["is_memory_location"] = True
    signatures.append([arg_def])

    return signatures


def generate_operation_templates(signature):
    """
    Create the DataTemplates to define a load with the given args.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular load operation to generate
            templates for.
    Returns:
        list(DataTemplate) : Datatemplates that define this load.
    """

    instruction_byte_bitdefs = generate_instruction_byte_bitdefs(signature)

    flags_bitdefs = [FLAGS["ANY"]]

    control_steps = generate_control_steps(signature)

    return assemble_instruction(
        instruction_byte_bitdefs, flags_bitdefs, control_steps
    )



def parse_line(line):
    """
    Parse a line of assembly code to create machine code byte templates.

    If a line is not identifiably a OPERATION_TEMPLATE assembly line,
    return an empty list instead.

    Args:
        line (str): Assembly line to be parsed.
    Returns:
        list(dict): List of instruction byte template dictionaries or an
        empty list.
    Raises:
        OperationParsingError: If the line was identifiably a
            OPERATION_TEMPLATE operation but incorrectly specified.
    """
    pass
