import re
from copy import deepcopy

from .definitions import MODULE_CONTROL, STEPS
from ..datatemplate import DataTemplate
from ..exceptions import InstructionParsingError
from ..assembler.assembler import is_constant
from .. import bitdef


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

    - bitstring: A byte bitstring of the final byte that will make up
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
    - index: The index of this byte in program data.

    Returns:
        dict: Machine code byte description template.
    """

    return {
        "bitstring": "",
        "byte_type": "",
        "constant_type": "",
        "constant": "",
        "number_value": 0,
        "index": -1,
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


def extract_memory_position(argument):
    """
    Extract a memory position from a memory index argument.

    See :func:~`is_memory_index` for details of what a memory index is.

    Args:
        argument (str): The argument to extract a memory position from.
    Returns:
        str: The location in memory being referenced.
    """

    return argument[1:-1]


def is_memory_index(argument):
    """
    Determine whether this argument is a memory index.

    Memory indexes can be module names or constants with a ``[`` at the start
    and a ``]`` at the end. e.g.:

    - ``[A]``
    - ``[#42]``
    - ``[$variable]``

    Args:
        argument (str): The argument being used for the assembly
            operation.
    Returns:
        bool: True if the argument is a memory index, false if not.

    """
    if (argument.startswith("[")
            and argument.endswith("]")
            and len(argument) > 2):
        return True
    else:
        return False


def represent_as_memory_index(argument):
    """
    Format the argument so it appears as a memory index.

    See :func:~`is_memory_index` for details on what a memory index is.

    Args:
        argument (str): The argument to represent as a memory index.
    Returns:
        str: The formatted argument.
    """
    return "[{argument}]".format(argument=argument)


def match_and_parse_line(line, opcode, op_args_defs=None):
    """
    Examine assembly code to see if it is valid and parse the arguments.

    This is a common function used by most of the assembly operations.

    Args:
        line (str): The line of assembly code.
        opcode (str): The opcode this line is being tested to match.
        op_args_defs (list(list(dict)), optional): Data structure that
            defines the different combinations of arguments. See
            :func:`~get_arg_def_template` for more details.

    Returns:
        (bool, list(dict)): Whether or not the line matched, and if it
        did, the parsed arguments.

    Raises:
        InstructionParsingError: If multiple op_args defs matched. Or
        if no op_args defs matched if the opcode matched (i.e. the
        arguments weren't valid for that assembly operation).
    """

    if op_args_defs is None:
        op_args_defs = []

    line_tokens = get_tokens_from_line(line)

    # Return early if there are no tokens
    if not line_tokens:
        return False, []

    # Return early if the opcode doesn't match
    line_opcode = line_tokens[0]
    if line_opcode != opcode:
        return False, []

    # Return early if this op code has no args
    line_args = line_tokens[1:]
    if not line_args and not op_args_defs:
        return True, []

    match = False
    for op_args_def in op_args_defs:
        args_are_correct, parsed_args = match_and_parse_args(
            line_args, op_args_def
        )
        if args_are_correct:
            if match:
                msg = (
                    "Args matched multiple arg possibilities."
                )
                raise InstructionParsingError(msg)
            else:
                match = True
                ret_args = parsed_args

    if not match:
        poss_args_list = generate_possible_arg_list(op_args_defs)
        poss_args_quotes_list = [
            add_quotes_to_strings(poss_args) for poss_args in poss_args_list
        ]
        pretty_possible_args = "\n".join(poss_args_quotes_list)
        msg = (
            "Incorrect arguments specified for the {opcode} "
            "operation:\n\n{pretty_args}\n\nThe possible arguments "
            "are:\n\n{pretty_possible_args}.".format(
                opcode=opcode,
                pretty_args=add_quotes_to_strings(line_args),
                pretty_possible_args=pretty_possible_args,
            )
        )
        raise InstructionParsingError(msg)

    return True, ret_args


def generate_possible_arg_list(op_args_defs):
    """
    Create a readable list of all possible argument combinations.

    Args:
        op_args_defs (list(list(dict))): Data structure that defines
            the different combinations of arguments. See
            :func:`~get_arg_def_template` for more details.
    Returns:
        list(str): All possible argument combinations.
    """

    arg_possibilities = []
    for op_args_def in op_args_defs:
        args = []
        for op_arg_def in op_args_def:
            arg = ""
            if op_arg_def["value_type"] == "module_name":
                arg = op_arg_def["value"]
            if op_arg_def["value_type"] == "constant":
                arg = "<constant>"
            if op_arg_def["is_memory_location"]:
                arg = represent_as_memory_index(arg)
            args.append(arg)
        arg_possibilities.append(args)
    return arg_possibilities


def match_and_parse_args(line_args, op_args_def):
    """
    Parse assembly operation args if they match the definition.

    Take arguments supplied for the assembly operation and see if they
    match this arguments definition.

    Args:
        line_args: (list(str)): The arguments supplied for this assembly
            operation.
        op_args_def (list(dict)): Definition of a set of arguments. See
            :func:`~get_arg_def_template` for more details.

    Returns:
        (bool, list(dict)): Whether or not the arguments matched, and if
        they did, the parsed values.

    Raises:
        InstructionParsingError: If a single argument managed to match
            different kinds of argument definitions.
    """

    if len(line_args) != len(op_args_def):
        return False, []

    parsed_args = []
    for line_arg, op_arg_def in zip(line_args, op_args_def):
        num_matches = 0
        # If the argument is a plain module name
        if (op_arg_def["value_type"] == "module_name"
                and not op_arg_def["is_memory_location"]
                and not is_memory_index(line_arg)
                and line_arg == op_arg_def["value"]):
            parsed_arg = deepcopy(op_arg_def)
            parsed_args.append(parsed_arg)
            num_matches += 1

        # If the argument is a module name indexing memory
        if (op_arg_def["value_type"] == "module_name"
                and op_arg_def["is_memory_location"]
                and is_memory_index(line_arg)):
            memory_position = extract_memory_position(line_arg)
            if memory_position == op_arg_def["value"]:
                parsed_arg = deepcopy(op_arg_def)
                parsed_args.append(parsed_arg)
                num_matches += 1

        # If the argument is a plain constant
        if (op_arg_def["value_type"] == "constant"
                and not op_arg_def["is_memory_location"]
                and not is_memory_index(line_arg)
                and is_constant(line_arg)):
            parsed_arg = deepcopy(op_arg_def)
            parsed_arg["value"] = line_arg
            parsed_args.append(parsed_arg)
            num_matches += 1

        # If the argument is a constant indexing memory
        if (op_arg_def["value_type"] == "constant"
                and op_arg_def["is_memory_location"]
                and is_memory_index(line_arg)):
            memory_position = extract_memory_position(line_arg)
            if is_constant(memory_position):
                parsed_arg = deepcopy(op_arg_def)
                parsed_arg["value"] = memory_position
                parsed_args.append(parsed_arg)
                num_matches += 1

        # If this argument didn't match, then these args don't match the
        # defs
        if num_matches == 0:
            return False, []

        # If there was more than one match something strange has
        # happened, bail.
        if num_matches > 1:
            msg = (
                "The argument '{line_arg} matched more than one "
                "argument type".format(line_arg=line_arg)
            )
            raise InstructionParsingError(msg)

    # If the for loop completes successfully, we've matched all the
    # args.
    return True, parsed_args


def get_arg_def_template():
    """
    Get a definition template for an assembly operation argument.

    This is a set of information that describes an argument used in a
    line of assembly.

    The keys have the following meaning:

    - value_type: What kind of argument this is. ``constant`` or
      ``module_name``.
    - is_memory_location: Whether this argument is referring to a
      location in memory.
    - value: The permitted value of the argument if it's a module.

    These dictionaries will be grouped in a list of lists that describe
    the possible arguments for an assembly operation. E.g. if the
    possible arguments for an assembly operation were:

    - ``ACC`` ``A``
    - ``B`` ``C``
    - ``A`` ``[#123]``

    The data structure would be as follows::

        [
            [
                {
                    "value_type": "module_name",
                    "is_memory_location": False,
                    "value": "ACC",
                },
                {
                    "value_type": "module_name",
                    "is_memory_location": False,
                    "value": "A",
                },
            ],
            [
                {
                    "value_type": "module_name",
                    "is_memory_location": False,
                    "value": "B",
                },
                {
                    "value_type": "module_name",
                    "is_memory_location": True,
                    "value": "C",
                },
            ],
            [
                {
                    "value_type": "module_name",
                    "is_memory_location": False,
                    "value": "A",
                },
                {
                    "value_type": "constant",
                    "is_memory_location": True,
                    "value": "",
                },
            ],
        ]

    Returns:
        dict: Machine code byte description template.
    """

    return {
        "value_type": "",
        "is_memory_location": False,
        "value": "",
    }
