from .. import bitdef
from .. import language_defs
from ..data_structures import DataTemplate
from ..instruction_components import ACC, A, B, C, PC, SP


def assemble_instruction_steps(instruction_bitdef, flags_bitdefs, control_steps):
    """
    Create templates for all steps to form a complete instruction.

    Args:
        instruction_bitdef (str): Bitdef of the instruction index.
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

    flags_bitdef = bitdef.merge(flags_bitdefs)

    for index, current_step_controls in enumerate(control_steps, start=2):
        step_bitdef = language_defs.STEPS[index]
        # This brings the 8 bits of the instruction bitdef up to the 15
        # in an address
        padded_instruction_bitdef = "{instr}.......".format(
            instr=instruction_bitdef
        )
        address_bitdef = bitdef.merge(
            [
                padded_instruction_bitdef,
                flags_bitdef,
                step_bitdef
            ]
        )

        # If this is the last step, add a step reset
        if index == num_steps + 1:
            current_step_controls.append(
                language_defs.MODULE_CONTROL["CU"]["STEP_RESET"]
            )

        control_bitdef = bitdef.merge(current_step_controls)
        control_bitdef = bitdef.fill(control_bitdef, "0")

        template = DataTemplate(
            address_range=address_bitdef, data=control_bitdef
        )

        templates.append(template)

    return templates


_COMPONENT_TO_MODULE_NAME = {
    ACC: "ACC",
    A: "A",
    B: "B",
    C: "C",
    SP: "SP",
    PC: "PC",
}


def component_to_module_name(component):
    """

    """
    module_name = _COMPONENT_TO_MODULE_NAME.get(component)
    if module_name is None:
        raise ValueError("Component has no mapping to a module")
    else:
        return module_name
