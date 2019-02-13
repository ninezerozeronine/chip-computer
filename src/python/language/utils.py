import utils
from language.definitions import MODULE_CONTROL_FLAGS

def steps_to_data_templates(instruction_bits, flags_bits, steps):
    """
    Create templates for all steps to form a complete instruction.
    """

    num_steps = len(steps)
    if num_steps > 6:
        msg = "{num_steps} steps were passed, the maxiumum is 6.".format(
            num_steps=num_steps)
        raise RuntimeError(msg)

    templates = []

    for index, control_signals in enumerate(steps):
        step_bits = utils.value_to_binary_string(index, width=3)

        # If this is the last step, add a step reset
        if index == num_steps + 2:
            control_signals.append(MODULE_CONTROL_FLAGS["CU"]["STEP_RESET"])

        address = "{instr}{flags}{step}".format(
            instr = instruction_bits,
            flags = flags_bits,
            step = step_bits
        )

        control_bits = combine_control_signals(control_signals)

        template = DataTemplate(
            address_range=address, data=control_bits
        )

        templates.append(template)

    return templates

def step_bits_to_bitdef(step_bits):
    """

    """
    pass

def flags_to_bitpattern(flags):
    """
    Generate the bit template that matches the desired flags
    """
    pass

def match_any_flag_bitpattern():
    """
    Get a bit pattern that will match any flag
    """

    return "XXXX"

def combine_control_signals(control_signals):
    """

    """
    pass