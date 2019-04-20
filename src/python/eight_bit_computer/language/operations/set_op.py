"""
The set operation.

Sets a module to a certain value.
"""

from ..definitions import (
    INSTRUCTION_GROUPS,
    SRC_REGISTERS,
    DEST_REGISTERS,
    MODULE_CONTROL,
    FLAGS,
    instruction_byte_from_bitdefs
)
from .. import utils
from ...exceptions import InstructionParsingError

_DESTINATIONS = ("ACC", "A", "B", "C", "SP")


def get_name():
    """
    Get the outward facing name for the SET operation.

    Returns:
        str: Name of the SET operation.
    """
    return "SET"


def generate_microcode_templates():
    """
    Generate datatemplates for all the SET operations.

    Returns:
        list(DataTemplate): All the datatemplates that make up the
        SET operation.
    """

    data_templates = []
    for dest in _DESTINATIONS:
        instruction_bitdefs = [
            INSTRUCTION_GROUPS["COPY"],
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
                MODULE_CONTROL["RAM"]["OUT"],
                MODULE_CONTROL["RAM"]["SEL_PROG_MEM"],
                MODULE_CONTROL[dest]["IN"],
            ],
        ]

        data_templates.extend(
            utils.assemble_instruction(
                instruction_bitdefs, flags_bitdefs, control_steps
            )
        )
    return data_templates


def get_instruction_byte(destination):
    """
    Get the instruction byte for this SET operation.

    Args:
        destination (str): The module having it's value set.
    Returns:
        str: bitstring for the first byte of the SET operation.
    """

    return instruction_byte_from_bitdefs([
        INSTRUCTION_GROUPS["COPY"],
        SRC_REGISTERS["IMM"],
        DEST_REGISTERS[destination],
        ])


def parse_line(line):
    """
    Parse a line of assembly code to create machine code byte templates.

    If a line is not identifiably a SET assembly line, return an empty
    list instead.

    Args:
        line (str): Assembly line to be parsed.
    Returns:
        list(dict): List of instruction byte template dictionaries or an
        empty list.
    Raises:
        InstructionParsingError: If the line was identifiably a
            SET operation but incorrectly specified.
    """

    line_tokens = utils.get_tokens_from_line(line)
    if not line_tokens:
        return []

    # Is the first token not "SET"
    if line_tokens[0] != "SET":
        return []

    # Are there exactly 3 tokens
    num_tokens = len(line_tokens)
    if num_tokens != 3:
        op_name = "SET"
        followup = (
            "Exactly 2 tokens should be passed to the SET operation. A "
            "module to have it's value set and a constant to set it "
            "to. E.g. \"SET B #123\"."
        )
        msg = utils.not_3_tokens_message(line_tokens, op_name, followup)
        raise InstructionParsingError(msg)

    dest = line_tokens[1]
    constant = line_tokens[2]

    # Is the destination token a valid module name
    if dest not in _DESTINATIONS:
        pretty_destinations = utils.add_quotes_to_strings(_DESTINATIONS)
        msg = (
            "Invalid module name used for SET operation (\"{dest}\"). "
            "It must be one of: {pretty_destinations}".format(
                dest=dest,
                pretty_destinations=pretty_destinations,
            )
        )
        raise InstructionParsingError(msg)

    instruction_byte = get_instruction_byte(dest)
    byte_template_0 = utils.get_machine_code_byte_template()
    byte_template_0["byte_type"] = "instruction"
    byte_template_0["machine_code"] = instruction_byte
    byte_template_1 = utils.get_machine_code_byte_template()
    byte_template_1["byte_type"] = "constant"
    byte_template_1["constant"] = constant
    return [byte_template_0, byte_template_1]
