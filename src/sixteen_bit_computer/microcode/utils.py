from collections import namedtuple

from . import bitdef
from . import hardware_mapping


DataTemplate = namedtuple("DataTemplate", ["address_range", "data"])
"""
Some data and a range of addresses to store that data in

Attributes:
    address_range (str): The range of addresses to store the data in.
        0 and 1 are absolute values, X is either a 0 or 1 and the
        expectation is that the data will expand out to the parts of the
        address marked with an X. and example could be "0010XX001".
    data (str): The data to be stored at the given addresses.
"""


def assemble_instruction(instruction_bitdefs, flags_bitdefs, control_steps):
    """
    Create templates for all steps to form a complete instruction.

    Args:
        instruction_bitdefs (list(str)): List of the bitdefs that make
            up the instruction byte.
        flags_bitdefs: list(str): List of the bitdefs that make up the
            flags for this instruction.
        control_steps: list(list(str): List of list of bitdefs that
            make up the control signals for each step.
    Returns:
        list(DataTemplate): All the steps for this instruction.
    Raises:
        ValueError: If too many steps were provided.
    """

    num_steps = len(control_steps)
    if num_steps > 6:
        msg = (
            "{num_steps} control steps were passed, "
            "the maxiumum is 6.".format(num_steps=num_steps)
        )
        raise ValueError(msg)

    templates = []

    instruction_bitdef = bitdef.merge(instruction_bitdefs)
    flags_bitdef = bitdef.merge(flags_bitdefs)

    for index, current_step_controls in enumerate(control_steps, start=2):
        step_bitdef = hardware_mapping.STEPS[index]

        address_bitdef = bitdef.merge(
            [
                instruction_bitdef,
                flags_bitdef,
                step_bitdef
            ]
        )

        # If this is the last step, add a step reset
        if index == num_steps + 1:
            current_step_controls.append(
                hardware_mapping.MODULE_CONTROL["CU"]["STEP_RESET"]
            )

        control_bitdef = bitdef.merge(current_step_controls)
        control_bitdef = bitdef.fill(control_bitdef, "0")

        template = DataTemplate(
            address_range=address_bitdef, data=control_bitdef
        )

        templates.append(template)

    return templates
