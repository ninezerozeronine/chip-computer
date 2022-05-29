"""
JUMP_IF_NEGATIVE_FLAG operation
"""

from . import jump_if_flag_base
from ..language_defs import FLAGS

_NAME = "JUMP_IF_NEGATIVE_FLAG"


def generate_microcode_templates():
    """
    Generate microcode for all the JUMP_IF_NEGATIVE_FLAG instructions.

    Returns:
        list(DataTemplate): DataTemplates for all the
        JUMP_IF_NEGATIVE_FLAG instructions.
    """

    return jump_if_flag_base.generate_microcode_templates(
        "C",
        FLAGS["NEGATIVE"]["HIGH"],
        FLAGS["NEGATIVE"]["LOW"],
    )


def parse_line(line):
    """
    Parse a line of assembly code to create machine code byte templates.

    If a line is not identifiably a JUMP_IF_NEGATIVE_FLAG assembly line,
    return an empty list instead.

    Args:
        line (str): Assembly line to be parsed.
    Returns:
        list(dict): List of machine code byte template dictionaries or
        an empty list.
    """

    return jump_if_flag_base.parse_line(line, "C", _NAME)
