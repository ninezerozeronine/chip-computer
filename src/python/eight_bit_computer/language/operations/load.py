"""The load operation"""

from itertools import product

from ..definitions import (
    OPCODE_GROUPS,
    SRC_REGISTERS,
    DEST_REGISTERS,
    MODULE_CONTROL,
    FLAGS,
)
from .. import utils


def generate_microcode_templates():
    """
    Generate microcode for all the load intructions
    """

    sources = ["ACC", "A", "B", "C", "PC"]
    destinations = ["ACC", "A", "B", "C", "SP"]

    data_templates = []

    for src, dest in product(sources, destinations):
        templates = generate_instruction(src, dest)
        data_templates.extend(templates)

    for dest in destinations:
        templates = generate_immediate_instruction(dest)
        data_templates.extend(templates)

    return data_templates


def generate_instruction(src, dest):
    """
    Define a load from data memory at src into dest.
    """

    instruction_bitdefs = [
        OPCODE_GROUPS["LOAD"],
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
    Define a load from an immediate address in memory into dest
    """

    instruction_bitdefs = [
        OPCODE_GROUPS["LOAD"],
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


def parse_line(line):
    """
    Parse a line of assembly code to generate machine code.
    """

    return []
