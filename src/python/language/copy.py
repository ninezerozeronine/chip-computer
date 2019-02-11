"""The copy operation"""

from itertools import product

from definitions import REGISTERS, OPCODE_GROUPS


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
    Create a datatemplate to define the copy from src to dest.
    """
    instruction_bits = "{group}{source_code}{dest_code}".format(
        group = OPCODE_GROUPS["COPY"],
        source_code = REGISTERS[src],
        dest_code = REGISTERS[dest]
    )
    flags_bits = get_flag_pattern()
    step_bits = "010"
    address = "{instr}{flags}{step}".format(
        instr = instruction_bits,
        flags = flags_bits,
        step = step_bits
    )

    control_sigs = [
        MODULE_CONTROL_FLAGS[src]["OUT"],
        MODULE_CONTROL_FLAGS[dest]["IN"],
        MODULE_CONTROL_FLAGS["CU"]["MC_STEP_RESET"]
    ]
    control_value = combine_control_sigs(control_sigs)
    template = DataTemplate(
        address_range=address, data=control_value
    )