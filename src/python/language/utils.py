import utils
from language.definitions import MODULE_CONTROL, MODULE_CONTROL_END, MODULE_CONTROL_START, STEPS

def assemble_instruction(instruction_bitdefs, flags_bitdefs, instruction_steps):
    """
    Create templates for all steps to form a complete instruction.
    """

    num_steps = len(instruction_steps)
    if num_steps > 6:
        msg = "{num_steps} steps were passed, the maxiumum is 6.".format(
            num_steps=num_steps)
        raise ValueError(msg)

    templates = []

    instruction_bitdef = utils.concatenate_bitdefs(instruction_bitdefs)
    flags_bitdef = utils.merge_bitdefs(flags_bitdefs)

    for index, current_step_controls in enumerate(instruction_steps, start=2):
        step_bitdef = STEPS[index]

        address_bitdef = utils.concatenate_bitdefs(
            [
                instruction_bitdef,
                flags_bitdef,
                step_bitdef
            ]
        )

        # If this is the last step, add a step reset
        if index == num_steps + 2:
            current_step_controls.append(MODULE_CONTROL["CU"]["STEP_RESET"])

        control_bitdef = utils.stack_bitdefs(
            MODULE_CONTROL_END,
            MODULE_CONTROL_START,
            current_step_controls,
            base_value = 0
        )

        template = DataTemplate(
            address_range=address_bitdef, data=control_bitdef
        )

        templates.append(template)

    return templates