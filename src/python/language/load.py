"""The load operation"""

from itertools import product

from language.definitions import REGISTERS, OPCODE_GROUPS, MODULE_CONTROL_FLAGS
import language.utils


def generate_datatemplates():
    """

    """
    sources = ["ACC", "A", "B", "C", "PC"]
    destinations = ["ACC", "A", "B", "C", "SP"]

    data_templates = []

    for src, dest in product(sources, destinations):
        template = create_datatemplate(src, dest)
        data_templates.append(template)

    for dest in destinations:
        template = create_immediate_datatemplate(dest)
        data_templates.append(template)

    return data_templates


def create_datatemplate(src, dest):
    """
    Define a load from data memory at src into dest.
    """

    instruction_bits = "{group_code}{source_code}{dest_code}".format(
        group_code = OPCODE_GROUPS["LOAD"],
        source_code = REGISTERS[src],
        dest_code = REGISTERS[dest]
    )

    flags_bits = utils.match_any_flag_bitpattern()

    steps = [
        [
           MODULE_CONTROL_FLAGS[src]["OUT"],
           MODULE_CONTROL_FLAGS["MAR"]["IN"]
        ],
        [
           MODULE_CONTROL_FLAGS["RAM"]["OUT"],
           MODULE_CONTROL_FLAGS[dst]["IN"]
        ]
    ]

    return utils.data_templates_from_steps(instruction_bits, flags_bits, steps)

def create_immediate_datatemplate(dest):
    """

    """
    pass
