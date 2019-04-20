from .. import bitdef
from ..datatemplate import DataTemplate
from .definitions import MODULE_CONTROL, STEPS

import re


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
    - byte_type: The type of machine code byte. Will be instruction or
      constant.
    - constant_type: The type of the constant. Could be a label,
      variable or number.
    - constant: The constant that this byte will need to become. The
      resolution of the constant to a real machine code byte is done by
      the assembler.
    - number_value: The value of the constant as an int if it's a
      number.

    Returns:
        dict: Machine code byte description template.
    """

    return {
        "machine_code": "",
        "byte_type": "",
        "constant_type": "",
        "constant": "",
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


def extract_memory_position(token):
    """
    Extract a memory position from a token.

    A token holding a memory position is a token that starts with "[",
    ends with "]" and has at least one character in between.

    Args:
        token (str): The token to extract a memory position from.
    Returns:
        str or None: String of the token if one could be extracted, None
        otherwise.
    """

    if (token.startswith("[")
            and token.endswith("]")
            and len(token) > 2):
        return token[1:-1]
    else:
        return None


def parse_line(line, opcode, op_args_defs=None):
    """

    """

    if op_args_defs is None:
        op_args_defs = []

    line_tokens = get_tokens_from_line(line)

    # Return early if there are no tokens
    if not line_tokens:
        return None, []

    # Return early if the opcode doesn't match
    line_opcode = line_tokens[0]
    if line_opcode != opcode:
        return None, []

    # Return early if this op code has no args
    line_args = line_tokens[1:]
    if not line_args and not op_args_defs:
        return line_opcode, []

    matches = []
    for op_args_def in op_args_defs:
        match, parsed_args = match_and_parse_args_sets(line_args, op_args_def)
        if match:
            matches.append((line_opcode, parsed_args))
    if 1


def match_and_parse_args_sets(line_args, op_args_def):
    """

    """

    if len(line_args) != len(op_args_def):
        return False, []

    all_match = True
    parsed_args = []
    for line_arg, op_arg_def in zip(line_args, op_args_def):
        pass


def get_arg_template():
    """
    Get an argument template for an assembly operation argument.

    This is a set of information that describes an argument used in a
    line of assembly.

    The keys have the following meaning:

    - arg_type: What kind of argument this is. constant or module
    - is_memory_location: Whether this argument is referring to a
      location in memory.
    - value: The permitted value of the argument if it's a module.

    Returns:
        dict: Machine code byte description template.
    """

    return {
        "arg_type": "",
        "is_memory_location": False,
        "value": "",
    }



    # # COPY ACC A
    # # COPY B C
    # example_op_args_0 = [
    #     [
    #         {
    #             "arg_type": "module",
    #             "is_memory_location": False,
    #             "value": "ACC",
    #         },
    #         {
    #             "arg_type": "module",
    #             "is_memory_location": False,
    #             "value": "A",
    #         },
    #     ],
    #     [
    #         {
    #             "arg_type": "module",
    #             "is_memory_location": False,
    #             "value": "B",
    #         },
    #         {
    #             "arg_type": "module",
    #             "is_memory_location": False,
    #             "value": "C",
    #         },
    #     ],
    # ]

    # # LOAD [#123] B
    # example_op_args_1 = [
    #     [
    #         {
    #             "arg_type": "constant",
    #             "is_memory_location": True,
    #             "value": "",
    #         },
    #         {
    #             "arg_type": "module",
    #             "is_memory_location": False,
    #             "value": "B",
    #         },
    #     ],
    # ]

    # # SET B #44
    # example_op_args_2 = [
    #     [
    #         {
    #             "arg_type": "module",
    #             "is_memory_location": False,
    #             "value": "B",
    #         },
    #         {
    #             "arg_type": "constant",
    #             "is_memory_location": False,
    #             "value": "",
    #         },
    #     ],
    # ]