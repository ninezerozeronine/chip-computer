from .. import (
    bitdef,
    language_defs,
    number_utils
)
from ..data_structures import DataTemplate
from ..instruction_components import ACC, A, B, C, PC, SP


def assemble_instruction_steps(instruction_bitdef, flags_bitdefs, control_steps):
    """
    Create templates for all steps to form a complete instruction.

    All steps will be given the same flag bitdefs.

    Args:
        instruction_bitdef (str): Bitdef of the instruction index.
        flags_bitdefs: list(str): List of the bitdefs that make up the
            flags for this instruction.
        control_steps: list(list(str)): List of list of bitdefs that
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


def assemble_explicit_instruction_steps(instruction_index, microcode_defs):
    """
    Generate DataTemplates give explicit instruction steps.

    In contrast to assemble_instruction_steps, the flags can vary 
    between steps. It will also not add a step reset to the last step.

    Args:
        microcode_defs (list(dict)): List of dictionaries that define
            the microcode that will make up this instruction. Generally
            they will define the entire instruction, but not always.

            Each dictionary has the form:

            .. code-block:: none

                {
                    "step": Integer step number, starting at zero.
                    "flags": List of bitdefs defining the flags for
                        this step
                    "module_controls": List of bitdefs the define the
                        module controls to set.
                }

        instruction_index (int): The index of this instruction.
    Returns:
        list(DataTemplate): Data templates representing the passed in
        microcode defs.
    """

    check_max_step(microcode_defs)

    instr_index_bitdef = number_utils.number_to_bitstring(
        instruction_index, bit_width=8
    )
    padded_instruction_bitdef = "{instr}.......".format(
        instr=instr_index_bitdef
    )

    data_templates = []

    for mc_def in microcode_defs:
        flags_bitdef = bitdef.merge(mc_def["flags"])
        # Add 2 here to make way for the fetch steps at the start of
        # every instruction.
        step_bitdef = language_defs.STEPS[mc_def["step"] + 2]
        mc_address_bitdef = bitdef.merge(
            [
                padded_instruction_bitdef,
                flags_bitdef,
                step_bitdef
            ]
        )

        control_bitdef = bitdef.merge(mc_def["module_controls"])
        control_bitdef = bitdef.fill(control_bitdef, "0")

        data_template = DataTemplate(
            address_range=mc_address_bitdef, data=control_bitdef
        )

        data_templates.append(data_template)

    return data_templates


def check_max_step(microcode_defs):
    """
    Check all the step indecies are within range.

    Args:
        microcode_defs (list(dict)): List of dictionaries that define
            the microcode that will make up this instruction. See
            :func:`assemble_explicit_instruction_steps` for more
            details.
    Raises:
        ValueError: If too many steps were provided.
    """

    max_step = max([mc_defn["step"] for mc_defn in microcode_defs])
    if max_step > 5:
        raise ValueError(
            "A control step with an index greater than 5 was specified"
        )


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
