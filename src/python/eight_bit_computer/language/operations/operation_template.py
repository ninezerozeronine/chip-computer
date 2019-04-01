"""
Example and explanation of required functions for an operation module.
"""

from ..definitions import (
    OPCODE_GROUPS,
    SRC_REGISTERS,
    DEST_REGISTERS,
    MODULE_CONTROL,
    FLAGS,
)
from .. import utils


def get_name():
    """
    The outward facing name for the OPERATION_TEMPLATE operation.

    Returns:
        str: Name of the OPERATION_TEMPLATE operation.
    """
    pass


def generate_microcode_templates():
    """
    Generate datatemplates for all the OPERATION_TEMPLATE operations.

    Returns:
        list(DataTemplate): All the datatemplates that make up the
        OPERATION_TEMPLATE operation.
    """
    pass


def parse_line(line):
    """
    Parse a line of assembly code to create machine code byte templates.

    If a line is not identifiable a OPERATION_TEMPLATE assembly line,
    return an empty list instead.

    Args:
        line (str): Assembly line to be parsed.
    Returns:
        list(dict): List of instruction byte template dictionaries or an
        empty list.
    Raises:
        InstructionParsingError: If the line was identifiably a
            OPERATION_TEMPLATE operation but incorrectly specified.
    """
    pass
