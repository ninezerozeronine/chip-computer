"""The set operation"""

from ..definitions import (
    OPCODE_GROUPS,
    SRC_REGISTERS,
    DEST_REGISTERS,
    MODULE_CONTROL,
    FLAGS,
    instruction_byte_from_bitdefs
)
from .. import utils


def get_name():
    """
    Get the outward facing name for the OPERATION_TEMPLATE operation.

    Returns:
        str: Name of the OPERATION_TEMPLATE operation.
    """
    return "SET"


def generate_microcode_templates():
    """
    Generate datatemplates for all the SET operations.

    Returns:
        list(DataTemplate): All the datatemplates that make up the
        SET operation.
    """

    destinations = ["ACC", "A", "B", "C", "SP"]
    data_templates = []
    for dest in destinations:
        instruction_bitdefs = [
            OPCODE_GROUPS["COPY"],
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
        destination (str): The module having it's value set
    Returns:
        str: bitstring for the first byte of the SET operation.
    """

    return instruction_byte_from_bitdefs(
        OPCODE_GROUPS["COPY"],
        SRC_REGISTERS["IMM"],
        DEST_REGISTERS[destination],
        )


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
            OPERATION_TEMPLATE operation but incorrectly specified.
    """

    # Does line have any content
    if not line:
        return []

    # Does the line have any content after splitting it
    line_tokens = line.split()
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
            "to. E.g. \"SET A #123\"."
        )
        msg = not_3_tokens_message(line_tokens, op_name, followup)
        raise InstructionParsingError(msg)

    dest = line_tokens[1]
    constant = line_tokens[2]
    # Is the second token a valid module name
    destinations = ["ACC", "A", "B", "C", "SP"]
    if dest not in destinations:
        pretty_destinations = add_quotes_to_strings(destinations)
        msg = (
            "Invalid module name used for SET operation (\"{dest}\"). "
            "It must be one of: {pretty_destinations}".format(
                dest=dest,
                pretty_destinations=pretty_destinations,
            )
        )
        raise InstructionParsingError(msg)

    instruction_byte = get_instruction_byte(dest)
    mc_byte_0 = utils.get_machine_code_byte_template()
    mc_byte_0["machine_code"] = instruction_byte
    mc_byte_1 = utils.get_machine_code_byte_template()
    mc_byte_1["constant"] = constant
    return [mc_byte_0, mc_byte_1]
