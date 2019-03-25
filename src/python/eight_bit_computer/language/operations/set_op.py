"""The set operation"""

from ..definitions import (
    OPCODE_GROUPS, SRC_REGISTERS, DEST_REGISTERS, MODULE_CONTROL, FLAGS
)
from .. import utils


def generate_microcode_templates():
    """
    Generate datatemplates for all the set operations.
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


def parse_line(line):
    """
    Parse a line of assembly code to generate machine code.
    """

    return []
