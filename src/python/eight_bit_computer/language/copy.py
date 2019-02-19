"""The copy operation"""

from itertools import product

from .definitions import (
    OPCODE_GROUPS, SRC_REGISTERS, DEST_REGISTERS, MODULE_CONTROL, FLAGS
)
from . import utils


def generate_microcode_templates():
    """
    Gernerate datatemplates for all the copy operations.
    """

    sources = ["ACC", "A", "B", "C", "PC", "SP"]
    destinations = ["ACC", "A", "B", "C", "SP"]

    data_templates = []

    for src, dest in product(sources, destinations):
        if src != dest:
            templates = generate_instruction(src, dest)
            data_templates.extend(templates)

    return data_templates


def generate_instruction(src, dest):
    """
    Create the datatemplates to define a copy from src to dest.
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
