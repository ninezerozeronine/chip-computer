from .. import utils, bitdef
from .definitions import MODULE_CONTROL, STEPS


def assemble_instruction(instruction_bitdefs, flags_bitdefs, control_steps):
    """
    Create templates for all steps to form a complete instruction.
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

    # templates.append(fetch0(instruction_bitdef, flags_bitdef))
    # templates.append(fetch1(instruction_bitdef, flags_bitdef))

    for index, current_step_controls in enumerate(control_steps, start=2):
        step_bitdef = STEPS[index]

        address_bitdef = bitdef.merge(
            [
                instruction_bitdef,
                flags_bitdef,
                step_bitdef
            ]
        )

        # If this is the last step, add a step reset
        if index == num_steps + 1:
            current_step_controls.append(MODULE_CONTROL["CU"]["STEP_RESET"])

        control_bitdef = bitdef.merge(current_step_controls)
        control_bitdef = bitdef.fill(control_bitdef, "0")

        template = utils.DataTemplate(
            address_range=address_bitdef, data=control_bitdef
        )

        templates.append(template)

    return templates
