"""
Process assembly code and output machine code.
"""

import copy
import re

from .validity import check_structure_validity
from ..language.operations import get_all_operations
from ..exceptions import (
    LineProcessingError,
    InstructionParsingError,
    AssemblyError,
)
from .. import numbers


def assemble(input_path, output_path=None, variable_start_offset=0):
    """
    Read an assembly file and write out equivalent machine code.

    Args:
        input_path (str): The location of the assembly file.
        output_path (str) (optional): The location to write out the
            machine code. If nothing is passed, the output path will be
            the input path with the extension changed to mc or have mc
            added if no extension was present.
        variable_start_offset (int) (optional): How far to offset the
            first variable in data memory from 0.
    """

    lines = filepath_to_lines(input_path)

    try:
        machine_code = lines_to_machine_code(
            lines, variable_start_offset=variable_start_offset
        )
    except AssemblyError:
        print AssemblyError

    if output_path is None:
        output_path = basename(input_path) + ".mc"

    write_machine_code(machine_code, output_path)


def filepath_to_lines(input_path):
    """
    Take a filepath and get all the lines of the file.

    The lines returned have the newline stripped.

    Args:
        input_path (str): Path to the file of disk to read.
    Returns:
        list(str): Lines of the file.
    """
    with open(input_path) as file:
        lines = file.read().splitlines()
    return lines


def write_machine_code(machine_code, output_path):
    """
    Write machine code to a file

    Args:
        machine_code (list(str)): List of the machine code values.
        output_path (str): Path of the file to write to.
    """
    pass


def lines_to_machine_code(lines, variable_start_offset=0):
    """
    Convert assembly lines to machine code lines.

    Args:
        lines (list(str)): The lines that made up the assembly file to
            be assembled.
        variable_start_offset (int) (optional): How far to offset the
            first variable in data memory from 0.
    Returns:
        list(str): The assembly file converted to an equivalent list of
        machine code bytes as 8 bit binary strings.
    Raises:
        AssemblyError: If there was an error assembling the machine
            code.
    """

    assembly_lines = []
    for line_no, line in enumerate(lines, start=1):
        try:
            assembly_line = process_line(line)
        except LineProcessingError as e:
            raise AssemblyError(e)
        assembly_line["line_no"] = line_no
        assembly_lines.append(assembly_line)

    check_structure_validity(assembly_lines)
    assign_labels(assembly_lines)
    resolve_labels(assembly_lines)
    resolve_numbers(assembly_lines)
    resolve_variables(
        assembly_lines, variable_start_offset=variable_start_offset
    )
    machine_code = extract_machine_code(assembly_lines)

    return machine_code


def process_line(line):
    """
    Process a single line of assembly.

    Args:
        line (str): The line of assembly to process. This line has
            already been cleaned (excess whitespace and comments
            removed).
    Returns:
        dict: A dictionary of information about this line. See the
        :data:`~LINE_INFO_TEMPLATE` documentation for more information
        about what is in the dictionary.
    """
    line_info = get_line_info_template()
    line_info["raw"] = line

    cleaned_line = clean_line(line)
    if not cleaned_line:
        return line_info
    line_info["clean"] = cleaned_line

    line_is_label = is_label(cleaned_line)
    if line_is_label:
        line_info["defined_label"] = cleaned_line

    line_is_variable = is_variable(cleaned_line)
    if line_is_variable:
        line_info["defined_variable"] = cleaned_line

    if not (line_is_variable or line_is_label):
        machine_code = machine_code_from_line(cleaned_line)
        validate_and_identify_constants(machine_code)
        line_info["machine_code"] = machine_code

    return line_info


def get_line_info_template():
    """
    Get a template for the assembly line information template.

    Template for a dictionary that contains information about this line
    of assembly code. The keys have the following meanings:

    - line_no: The line in the assembly file that this line was on.
    - raw: The line as it was in the assembly file.
    - clean: The cleaned up line, ready for parsing.
    - defined_label: The label that this line defined. Empty string
      if the line is not a label definition.
    - assigned_label: The label that has been assigned to the first
      line of the machine code generated for this line. Empty string
      if the line has no label.
    - defined_variable: The variable that this line defined. Empty
      string if the line is not a variable definition.
    - machine_code: List of machine code bytes (with constant
      expansion information) for this line. Empty list if no machine
      code is required for this line. e.g. a comment.

    Returns:
        dict: Assembly line description template.
    """

    return {
        "line_no": -1,
        "raw": "",
        "clean": "",

        "defined_label": "",
        "assigned_label": "",

        "defined_variable": "",

        "machine_code": [],
    }


def clean_line(line):
    """
    Clean a line of assembly ready for further processing.

    Removes leading and trailing whitespace, comments, and excess
    whitespace between tokens.

    Args:
        line (str): The line to clean.
    Returns:
        str: The cleaned line.
    """
    no_comments = remove_comments(line)
    no_excess_whitespace = remove_excess_whitespace(no_comments)
    return no_excess_whitespace


def remove_comments(line):
    """
    Remove comments from a line.

    A comment is anything on the line after and including an occurrence
    of ``//``.

    Args:
        line (str): line to remove comments from.
    Returns:
        str: The line with comments removed.
    """
    comment_index = line.find("//")
    comments_removed = line
    if comment_index >= 0:
        comments_removed = line[:comment_index]
    return comments_removed


def remove_excess_whitespace(line):
    """
    Remove excess whitespace from a line

    Args:
        line (str): line to remove excess whitespace from.
    Returns:
        str: The line with excess whitespace removed.
    """
    return " ".join(line.strip().split())


def is_label(test_string):
    """
    Test if a string is a valid label.

    Args:
        test_string (str): The string to test
    Returns:
        bool: True if the string is a valid label, false otherwise.
    """
    match = re.match(r"@[a-zA-Z_]+\w*$", test_string)
    if match:
        return True
    else:
        return False


def is_variable(test_string):
    """
    Test if a string is a valid variable.

    Args:
        test_string (str): The string to test
    Returns:
        bool: True if the string is a valid variable, false otherwise.
    """
    match = re.match(r"\$[a-zA-Z_]+\w*$", test_string)
    if match:
        return True
    else:
        return False


def machine_code_from_line(line):
    """
    Get the machine code that this assembly line is equivalent to.

    Uses all the defined instructions and defers the work of parsing to
    them. See XXX for information on machine code dictionaries from
    instructions.

    Expects the passed in line to be a valid line of machine code. That
    is, the passed in line should be translatable to valid machine code.

    Args:
        line (str): Line to parse.
    Returns:
        list(dict): Machine code byte information dictionaries.
    Raises:
        LineProcessingError: Failure to extract machine code or matching
        multiple operations.
    """
    operation_matches = []
    for operation in get_all_operations():
        try:
            machine_code = operation.parse_line(line)
        except InstructionParsingError as e:
            raise LineProcessingError(e)
        if machine_code:
            operation_matches.append(machine_code)

    num_matches = len(operation_matches)
    if num_matches == 0:
        raise LineProcessingError("Unable to match line")
    if num_matches > 1:
        raise LineProcessingError("Line matched multiple operations")

    return operation_matches[0]


def validate_and_identify_constants(machine_code):
    """
    Validate and identify constants from instruction machine code.

    Assumed constants are returned from the instruction parsers. This
    function then validates them to make sure they are correct and
    determines what kind of constant they are.

    See XXX for information on machine code dictionaries from
    instructions.

    This function modifies the passed in machine code list in place

    Args:
        machine_code (list(dict)): The machine code bytes as returned by
            an instruction line parser.
    Raises:
        LineProcessingError: Invalid constants were specified.
    """

    for instruction_byte in machine_code:
        constant = instruction_byte["constant"]
        if not constant:
            continue

        constant_is_label = is_label(constant)
        constant_is_variable = is_variable(constant)
        constant_is_number = is_number(constant)

        constants = [
            constant_is_label, constant_is_variable, constant_is_number
        ]

        if not any(constants):
            raise LineProcessingError()

        num_constants = sum([1 for _constant in constants if _constant])
        if num_constants > 1:
            raise LineProcessingError()

        if constant_is_label:
            constant_type = "label"
        elif constant_is_variable:
            constant_type = "variable"
        else:
            constant_type = "number"
            value = number_constant_value(constant)
            if not (numbers.number_is_within_bit_limit(value, bits=8)):
                raise LineProcessingError()
            instruction_byte["number_value"] = value

        instruction_byte["constant_type"] = constant_type


def is_number(test_string):
    """
    Test if a string is a valid number.

    Args:
        test_string (str): The string to test
    Returns:
        bool: True if the string is a valid number, false otherwise.
    """
    if not test_string:
        return False
    if test_string[0] == "#":
        stripped = test_string[1:]
        if not stripped:
            return False
        try:
            num = int(stripped, 0)
        except ValueError:
            return False
        return True
    else:
        return False


def number_constant_value(number_constant):
    """
    Get the value that a number constant represents.

    Args:
        number_constant (str): The constant to extract the value from.
    Returns:
        int: The value of the constant.
    """

    return int(number_constant[1:], 0)


def assign_labels(assembly_lines):
    """
    Assign labels to the lines for later reference

    This modifies the passed in list of assembly lines, adding data to
    it.

    Args:
        assembly_lines (list(dict)): Lines of assembly to add label
        information to.
    """

    label = None
    for assembly_line in assembly_lines:
        if label is None:
            label = assembly_line["defined_label"] or None
        if assembly_line["machine_code"] and label is not None:
            assembly_line["assigned_label"] = label
            label = None
        else:
            assembly_line["assigned_label"] = ""


def resolve_labels(assembly_lines):
    """
    Resolve labels to indexes in the machine code bytes.

    This modifies the passed in list of assembly line dictionaries.

    Args:
        assembly_lines (list(dict)): List of assembly lines to resolve
            label references in.
    """

    label_map = create_label_map(assembly_lines)
    for assembly_line in assembly_lines:
        for instruction_byte in assembly_line["machine_code"]:
            constant = instruction_byte["constant"]
            if not constant:
                continue
            if instruction_byte["constant_type"] != "label":
                continue
            instruction_byte["machine_code"] = label_map[constant]


def create_label_map(assembly_lines):
    """
    Create a map of labels to machine code byte indexes.

    Args:
        assembly_lines (list(dict)): List of assembly lines to create a
            label map for.
    Returns:
        dict(str:str): Dictionary of label names to machine code
        indexes.
    """

    label_map = {}
    byte_index = 0
    for assembly_line in assembly_lines:
        assigned_label = assembly_line["assigned_label"]
        if assigned_label:
            index_bit_string = number_to_bitstring(byte_index)
            label_map[assigned_label] = index_bit_string
        machine_code = assembly_line["machine_code"]
        byte_index += len(machine_code)
    return label_map


def resolve_numbers(assembly_lines):
    """
    Resolve number constants to machine code byte values.

    This modifies the passed in list of assembly line dictionaries.

    Args:
        assembly_lines (list(dict)): List of assembly lines to create a
            label map for.
    """
    for assembly_line in assembly_lines:
        for instruction_byte in assembly_line["machine_code"]:
            constant = instruction_byte["constant"]
            if not constant:
                continue
            if instruction_byte["constant_type"] != "number":
                continue
            number = instruction_byte["number_value"]
            instruction_byte["machine_code"] = number_to_bitstring(number)


def resolve_variables(assembly_lines, variable_start_offset=0):
    """
    Resolve variable constants to indexes in data memory.

    This modifies the passed in list of assembly line dictionaries.

    Args:
        assembly_lines (list(dict)): List of assembly lines to resolve
            variables in.
        variable_start_offset (int) (optional): An offset into data
            memory for where to start storing the variables.
    """
    variable_map = create_variable_map(assembly_lines)
    for assembly_line in assembly_lines:
        for instruction_byte in assembly_line["machine_code"]:
            constant = instruction_byte["constant"]
            if not constant:
                continue
            if instruction_byte["constant_type"] != "variable":
                continue
            instruction_byte["machine_code"] = variable_map[constant]


def create_variable_map(assembly_lines, variable_start_offset=0):
    """
    Create a map of variables to indexes in data memory.

    Args:
        assembly_lines (list(dict)): List of assembly lines to create a
            variable map for.
        variable_start_offset (int) (optional): An offset into data
            memory for where to start storing the variables.
    Returns:
        dict(str:str): Dictionary of variable names to machine code
        indexes.
    """

    variable_map = {}
    variable_index = variable_start_offset
    for assembly_line in assembly_lines:

        # Check for defined variable
        variable = assembly_line["defined_variable"]
        if variable:
            if variable in variable_map:
                continue
            variable_map[variable] = number_to_bitstring(variable_index)
            continue

        # Check for variable in machine code
        for instruction_byte in assembly_line["machine_code"]:
            constant = instruction_byte["constant"]
            if not constant:
                continue
            if instruction_byte["constant_type"] != "variable":
                continue
            if constant in variable_map:
                continue
            variable_map[constant] = number_to_bitstring(variable_index)
            variable_index += 1
    return variable_map


def extract_machine_code(assembly_lines):
    """
    Extract machine code from assembly line dictionaries.

    Args:
        assembly_lines (list(dict)): List of assembly lines to extract
            machine code from.
    Returns:
        list(str): List of bit strings for the machine code.
    """
    machine_code = []
    for assembly_line in assembly_lines:
        for instruction_byte in assembly_line["machine_code"]:
            machine_code.append(instruction_byte["machine_code"])
    return machine_code
