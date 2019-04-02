from .. import bitdef
from ..datatemplate import DataTemplate
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

        template = DataTemplate(
            address_range=address_bitdef, data=control_bitdef
        )

        templates.append(template)

    return templates


def get_machine_code_byte_template():
    """
    Get the template used to describe a machine code byte.

    This is a set of information that describes the byte (of which there
    could be many) of machine code that an operation (e.g. LOAD
    [$variable] A) results in.

    The keys have the following meaning:

    - machine_code: A byte bitstring of the final byte that will make up
      the machine code.
    - constant: The constant that this byte may optionally need to
      become. The resolution of the constant to a real machine come byte
      is done by the assembler.
    - constant_type: The type of the constant. Could be a label,
      variable or number.
    - number_value: The value of the constant as an int if it's a
      number.

    Returns:
        dict: Machine code byte description template.
    """

    return {
        "machine_code": "",
        "constant": "",
        "constant_type": "",
        "number_value": 0,
    }


def add_quotes_to_strings(strings):
    """
    Add double quotes strings in a list then join with commas.
    """
    quote_strings = []
    for _string in strings:
        quote_strings.append("(\"{string}\").".format(sring=_string))
    pretty_strings = ", ".join(pretty_strings)
    return pretty_strings


def not_3_tokens_message(tokens, op_name, followup):
    """
    Generate the error message for when not 3 tokens are used specified.
    """
    num_tokens = len(tokens)
    if num_tokens == 1:
        msg = (
            "No tokens were specified for the {op_name} "
            "operation. ".format(op_name)
        )
    elif num_tokens == 2:
        msg = (
            "Only one token was specified for the {op_name} operation "
            "(\"{token}\"). ".format(token=tokens[1], op_name=op_name)
        )
    else:
        pretty_tokens = add_quotes_to_strings(line_tokens)
        msg = (
            "{num_tokens} tokens were specified for the {op_name} "
            "operation ({pretty_tokens}). ".format(
                num_tokens=num_tokens,
                op_name=op_name,
                pretty_tokens=pretty_tokens,
            )
        )
    msg += followup
    return msg
