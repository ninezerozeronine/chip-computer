"""
The COPY operation.

Copies a value from one module into another.
"""

from itertools import product

from ..definitions import (
    OPCODE_GROUPS,
    SRC_REGISTERS,
    DEST_REGISTERS,
    MODULE_CONTROL,
    FLAGS,
    instruction_byte_from_bitdefs,
)
from .. import utils
from ...exceptions import InstructionParsingError

_SOURCES = ("ACC", "A", "B", "C", "PC", "SP")
_DESTINATIONS = ("ACC", "A", "B", "C", "SP")


def get_name():
    """
    Get the outward facing name for the COPY operation.

    Returns:
        str: Name of the COPY operation.
    """
    return "COPY"


def generate_microcode_templates():
    """
    Generate microcode for all the COPY instructions.

    Returns:
        list(DataTemplate): DataTemplates for all the COPY microcode..
    """

    data_templates = []

    for src, dest in product(_SOURCES, _DESTINATIONS):
        if src != dest:
            templates = generate_instruction(src, dest)
            data_templates.extend(templates)

    return data_templates


def generate_instruction(src, dest):
    """
    Create the DataTemplates to define a copy from src to dest.

    Returns:
        list(DataTemplate) : Datatemplates that define this copy.
    """
    instruction_bitdefs = [
        OPCODE_GROUPS["COPY"],
        SRC_REGISTERS[src],
        DEST_REGISTERS[dest],
    ]

    flags_bitdefs = [FLAGS["ANY"]]

    control_steps = [
        [
            MODULE_CONTROL[src]["OUT"],
            MODULE_CONTROL[dest]["IN"],
        ]
    ]

    return utils.assemble_instruction(
        instruction_bitdefs, flags_bitdefs, control_steps
    )


def get_instruction_byte(source, destination):
    """
    Get the instruction byte for a copy from source to destination.

    Args:
        source (str): The module the value is being copied from.
        destination (str): The module having it's value set.
    Returns:
        str: bitstring for the first byte of the COPY operation.
    """

    return instruction_byte_from_bitdefs([
        OPCODE_GROUPS["COPY"],
        SRC_REGISTERS[source],
        DEST_REGISTERS[destination],
        ])


def parse_line(line):
    """
    Parse a line of assembly code to create machine code byte templates.

    If a line is not identifiably a COPY assembly line, return an empty
    list instead.

    Args:
        line (str): Assembly line to be parsed.
    Returns:
        list(dict): List of instruction byte template dictionaries or an
        empty list.
    Raises:
        InstructionParsingError: If the line was identifiably a COPY
            operation but incorrectly specified.
    """

    line_tokens = utils.get_tokens_from_line(line)
    if not line_tokens:
        return []

    # Is the first token not "COPY"
    if line_tokens[0] != "COPY":
        return []

    # Are there exactly 3 tokens
    num_tokens = len(line_tokens)
    if num_tokens != 3:
        op_name = "COPY"
        followup = (
            "Exactly 2 tokens should be passed to the COPY operation. "
            "A module to copy the data from and a module to write to. "
            "E.g. \"COPY A B\"."
        )
        msg = utils.not_3_tokens_message(line_tokens, op_name, followup)
        raise InstructionParsingError(msg)

    source = line_tokens[1]
    destination = line_tokens[2]

    validate_source_and_dest(source, destination)

    instruction_byte = get_instruction_byte(source, destination)
    machine_code = utils.get_machine_code_byte_template()
    machine_code["machine_code"] = instruction_byte
    return [machine_code]


def validate_source_and_dest(source, destination):
    """
    Make sure that the source and destination are valid.

    Args:
        source (str): The source module.
        destination (str): The destination module.
    Raises:
        InstructionParsingError: If the source/destination pair is
            invalid.
    """

    # Is the source valid
    if source not in _SOURCES:
        pretty_sources = utils.add_quotes_to_strings(_SOURCES)
        msg = (
            "Invalid source for COPY operation (\"{source}\"). "
            "It must be one of: {pretty_sources}".format(
                source=source,
                pretty_sources=pretty_sources,
            )
        )
        raise InstructionParsingError(msg)

    # Is the destination valid
    if destination not in _DESTINATIONS:
        pretty_destinations = utils.add_quotes_to_strings(_DESTINATIONS)
        msg = (
            "Invalid destination for COPY operation (\"{destination}\"). "
            "It must be one of: {pretty_destinations}".format(
                destination=destination,
                pretty_destinations=pretty_destinations,
            )
        )
        raise InstructionParsingError(msg)

    # Is the destination equal to the source
    if source == destination:
        msg = (
            "Source and destination cannot be the same for a COPY "
            "operation. \"{source}\" was given.".format(source=source)
        )
        raise InstructionParsingError(msg)
