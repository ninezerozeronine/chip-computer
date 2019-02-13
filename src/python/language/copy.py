"""The copy operation"""

from itertools import product

from language.definitions import SRC_REGISTERS, DST_REGISTERS, OPCODE_GROUPS, MODULE_CONTROL, FLAGS
import language.utils


def generate_datatemplates():
    """
    Gernerate datatemplates for all the copy operations.
    """

    sources = ["ACC", "A", "B", "C", "PC", "SP"]
    destinations = ["ACC", "A", "B", "C", "SP"]

    data_templates = []

    for src, dest in product(sources, destinations):
        if src != dest:
            template = create_datatemplate(src, dest)
            data_templates.append(template)

    return data_templates

def create_datatemplate(src, dest):
    """
    Create the datatemplates to define a copy from src to dest.
    """
    instruction_bitdefs = [
        OPCODE_GROUPS["COPY"],
        SRC_REGISTERS[src],
        DST_REGISTERS[dest],
    ]

    flags_bitdefs = [FLAGS["ALL"]]

    instruction_steps = [
        [
            MODULE_CONTROL[src]["OUT"],
            MODULE_CONTROL[dest]["IN"],
        ]
    ]

    return language.utils.assemble_operation_templates(
        instruction_bitdefs, flags_bitdefs, instruction_steps
    )