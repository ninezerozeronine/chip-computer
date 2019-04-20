"""
The LOAD operation.

Loads a value from data memory into a module.
"""

from itertools import product

from ..definitions import (
    INSTRUCTION_GROUPS,
    SRC_REGISTERS,
    DEST_REGISTERS,
    MODULE_CONTROL,
    FLAGS,
    instruction_byte_from_bitdefs,
)
from .. import utils
from ...exceptions import InstructionParsingError


_SOURCES = ("ACC", "A", "B", "C", "PC", "SP")
_DESTINATIONS = ("ACC", "A", "B", "C")


def get_name():
    """
    Get the outward facing name for the LOAD operation.

    Returns:
        str: Name of the LOAD operation.
    """
    return "LOAD"


def generate_microcode_templates():
    """
    Generate microcode for all the LOAD instructions.

    Returns:
        list(DataTemplate): DataTemplates for all the LOAD instructions.
    """

    data_templates = []

    for src, dest in product(_SOURCES, _DESTINATIONS):
        templates = generate_instruction(src, dest)
        data_templates.extend(templates)

    for dest in _DESTINATIONS:
        templates = generate_immediate_instruction(dest)
        data_templates.extend(templates)

    return data_templates


def generate_instruction(src, dest):
    """
    Create DataTemplates to define a load from memory at src into dest.

    Returns:
        list(DataTemplate) : Datatemplates that define this load.
    """

    instruction_bitdefs = [
        INSTRUCTION_GROUPS["LOAD"],
        SRC_REGISTERS[src],
        DEST_REGISTERS[dest],
    ]

    flags_bitdefs = [FLAGS["ANY"]]

    control_steps = [
        [
           MODULE_CONTROL[src]["OUT"],
           MODULE_CONTROL["MAR"]["IN"],
        ],
        [
           MODULE_CONTROL["RAM"]["OUT"],
           MODULE_CONTROL[dest]["IN"],
        ],
    ]

    return utils.assemble_instruction(
        instruction_bitdefs, flags_bitdefs, control_steps)


def generate_immediate_instruction(dest):
    """
    Define a load from an immediate address in memory into dest.

    Returns:
        list(DataTemplate) : Datatemplates that define this load.
    """

    instruction_bitdefs = [
        INSTRUCTION_GROUPS["LOAD"],
        SRC_REGISTERS["IMM"],
        DEST_REGISTERS[dest],
    ]

    flags_bitdefs = [FLAGS["ANY"]]

    control_steps = [
        [
           MODULE_CONTROL["PC"]["OUT"],
           MODULE_CONTROL["MAR"]["IN"],
        ],
        [
           MODULE_CONTROL["PC"]["COUNT"],
           MODULE_CONTROL["RAM"]["SEL_PROG_MEM"],
           MODULE_CONTROL["RAM"]["OUT"],
           MODULE_CONTROL[dest]["IN"],
        ],
    ]

    return utils.assemble_instruction(
        instruction_bitdefs, flags_bitdefs, control_steps)


def get_instruction_byte(source, destination):
    """
    Get the instruction byte for a load from source to destination.

    Args:
        source (str): The location in memory the value is being read
            from. If this is a constante, IMM should be subbed in.
        destination (str): The module having it's value set.
    Returns:
        str: bitstring for the first byte of the LOAD operation.
    """

    return instruction_byte_from_bitdefs([
        INSTRUCTION_GROUPS["LOAD"],
        SRC_REGISTERS[source],
        DEST_REGISTERS[destination],
        ])


def parse_line(line):
    """
    Parse a line of assembly code to create machine code byte templates.

    If a line is not identifiably a LOAD assembly line, return an empty
    list instead.

    Args:
        line (str): Assembly line to be parsed.
    Returns:
        list(dict): List of instruction byte template dictionaries or an
        empty list.
    Raises:
        InstructionParsingError: If the line was identifiably a LOAD
            operation but incorrectly specified.
    """

    line_tokens = utils.get_tokens_from_line(line)
    if not line_tokens:
        return []

    # Is the first token not "LOAD"
    if line_tokens[0] != "LOAD":
        return []

    # Are there exactly 3 tokens
    num_tokens = len(line_tokens)
    if num_tokens != 3:
        op_name = "LOAD"
        followup = (
            "Exactly 2 tokens should be passed to the LOAD operation. "
            "A location in data memory and a module to write the value "
            "to. E.g. \"LOAD [A] B\" or LOAD [$variable] C."
        )
        msg = utils.not_3_tokens_message(line_tokens, op_name, followup)
        raise InstructionParsingError(msg)

    source_token = line_tokens[1]
    dest_token = line_tokens[2]

    validate_source_and_dest_tokens(source_token, dest_token)

    return generate_machine_code_templates(source_token, dest_token)


def validate_source_and_dest_tokens(source, destination):
    """
    Make sure that the source and destination tokens are valid.

    Args:
        source (str): The source location. Could be a module or
            constant.
        destination (str): The destination module.
    Raises:
        InstructionParsingError: If the source/destination pair is
            invalid.
    """

    # Is the memory location valid
    memory_position = utils.extract_memory_position(source)
    if memory_position is None:
        msg = (
            "A memory position (e.g. [A], [#123], [$variable]) must be "
            "specified as the first operand for the LOAD operation. "
            "{source} was given.".format(source=source)
            )
        raise InstructionParsingError(msg)

    # Is the destination valid
    if destination not in _DESTINATIONS:
        pretty_destinations = utils.add_quotes_to_strings(_DESTINATIONS)
        msg = (
            "Invalid destination for LOAD operation "
            "(\"{destination}\").It must be one of: "
            "{pretty_destinations}".format(
                destination=destination,
                pretty_destinations=pretty_destinations,
            )
        )
        raise InstructionParsingError(msg)


def generate_machine_code_templates(source_token, dest_token):
    """
    Generate the machine code templates for this load operation.

    Args:
        source_token (str): The source location. Could be a module or
            constant.
        dest_token (str): The destination token.
    Returns:
        list(dict): List of machine code templates.
    """

    memory_position = utils.extract_memory_position(source_token)
    machine_code = []
    # If the source is a normal module
    if memory_position in _SOURCES:
        instruction_byte = get_instruction_byte(memory_position, dest_token)
        mc_0 = utils.get_machine_code_byte_template()
        mc_0["machine_code"] = instruction_byte
        machine_code.append(mc_0)

    # Else the source is a constant
    else:
        instruction_byte = get_instruction_byte("IMM", dest_token)
        mc_0 = utils.get_machine_code_byte_template()
        mc_0["machine_code"] = instruction_byte
        machine_code.append(mc_0)

        mc_1 = utils.get_machine_code_byte_template()
        mc_1["constant"] = memory_position
        machine_code.append(mc_1)

    return machine_code
