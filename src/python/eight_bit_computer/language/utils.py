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

    Args:
        strings (list(str)): List of strings to add parentheses to.
    Returns:
        str: The strings with quotes added and joined with commas.
    """
    quote_strings = []
    for _string in strings:
        quote_strings.append("\"{string}\"".format(string=_string))
    pretty_strings = ", ".join(quote_strings)
    return pretty_strings


def not_3_tokens_message(tokens, op_name, followup):
    """
    Generate the error message for when not 3 tokens are specified.

    Convenience function for generating useful error messages when an
    operator expects 3 tokens (Operator, source, dest) but too few or
    too many were supplied.

    Args:
        tokens (list(str)): The tkens on the line being parsed
        op_name (str): The name of the operators e.g. SET, LOAD
        followup (str): Extra context and example to make the error more
            useful.
    Returns:
        str: The compiled message.
    """
    num_tokens = len(tokens)
    if num_tokens == 1:
        msg = (
            "No tokens were specified for the {op_name} "
            "operation. ".format(op_name=op_name)
        )
    elif num_tokens == 2:
        msg = (
            "Only one token was specified for the {op_name} operation "
            "(\"{token}\"). ".format(token=tokens[1], op_name=op_name)
        )
    else:
        pretty_tokens = add_quotes_to_strings(tokens)
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


def get_tokens_from_line(line):
    """
    Given a line split it into tokens and return them.

    Tokens are runs of characters separated by spaces. If there are no
    tokens return an empty list.

    Args:
        line (str): line to convert to tokens
    Returns:
        list(str): The tokens
    """

    # Does line have any content
    if not line:
        return []

    # Does the line have any content after splitting it
    line_tokens = line.split()
    if not line_tokens:
        return []

    return line_tokens