"""
Process assembly code and output machine code.

Attributes:
    LINE_INFO_TEMPLATE (dict): Template for a dictionary that contains
        information about this line of assembly code. The keys have the
        following meanings:

        - line_no: The line in the assembly file that this line was on.
        - raw: The line as it was in the assembly file.
        - clean: The cleaned up line, ready for parsing.
        - defined_label: The label that this line defined. Empty string
          if the line is not a label definition.
        - asinged_label: The label that has been assigned to the first
          line of the machine code generated for this line. Empty string
          if the line has no label.
        - defined_variable: The variable that this line defined. Empty
          string if the line is not a variable definition.
        - machine_code: List of machine code bytes (with constant
          expansion information) for this line. Empty list if no machine
          code is required for this line. e.g. a comment.
        - used_labels: Any labels used in this line. A convenience and
          computation saving for later processing.
        - used_variables Any variables used in this line. A convenience
          and computation saving for later processing.
        - used_numbers: Any numbers used in this line. A convenience and
          computation saving for later processing.
"""

import copy

LINE_INFO_TEMPLATE = {
    "line_no": 0,
    "raw": "",
    "clean": "",

    "defined_label": "",
    "assigned_label": ""

    "defined_variable" "",

    "machine_code": [],

    "used_labels": [],
    "used_variables": [],
    "used_numbers": [],
}


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

    # Assign labels to machine_code
    label = None
    for assembly_line in assembly_lines:
        if label is None:
            label = assembly_line["defined_label"] or None
        if assembly_line["machine_code"] and label is not None:
            assembly_line["assigned_label"] = label
            label = None
        else:
            assembly_line["assigned_label"] = []

    label_mapping = create_label_mapping(assembly_lines)
    variable_mapping = create_variable_mapping(
        assembly_lines, variable_start_offset=variable_start_offset)

    machine_code = assembly_lines_to_machine_code(
        assembly_lines, label_mapping, variable_mapping
    )

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
    line_info = copy.deepcopy(LINE_INFO_TEMPLATE)
    line_info["raw"] = line
    cleaned_line = clean_line(line)
    line_info["clean"] = cleaned_line
    line_info["defined_label"] = extract_label(cleaned_line)
    line_info["defined_variable"] = extract_variable(cleaned_line)
    if not line_info["defined_label"] or line_info["defined_label"]:
        line_info["machine_code"] = machine_code_from_line(cleaned_line)
        if line_info["machine_code"]:
            labels, variables, numbers = extract_constants(
                line_info["machine_code"]
            )
            line_info["used_labels"] = labels
            line_info["used_varibles"] = variables
            line_info["used_numbers"] = numbers
    return line_info


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


def extract_label(test_string):
    """
    Extract a valid label.

    If the string is a valid label, return it. If it's marked as a label
    (starts with an @) but is then incorrectly named, an exception is
    raised. If it's not marked as a label, an empty string is returned.

    Args:
        test_string (str): The string to try extracting a label from.
    Returns:
        str: The string that was passed in if it's valid, an empty
        string if it's not marked as a label.
    Raises:
        LineProcessingError: The string was marked as a label, but it
        was incorrectly named.
    """
    pass


def extract_variable(test_string):
    """
    Extract a valid variable.

    If the string is a valid variable, return it. If it's marked as a
    variable (starts with an $) but is then incorrectly named, an
    exception is raised. If it's not marked as a variable, an empty
    string is returned.

    Args:
        test_string (str): The string to try extracting a variable from.
    Returns:
        str: The string that was passed in if it's valid, an empty
        string if it's not marked as a variable.
    Raises:
        LineProcessingError: The string was marked as a variable, but it
        was incorrectly named.
    """
    pass


def machine_code_from_line(line):
    """
    Get the machine code that this assembly line is equivalent to.

    Uses all the defined instructions and defers the work of parsing to
    them. See XXX for information on machine code dictionaries from
    instructions.

    Args:
        line (str): Line to parse
    Returns:
        list(dict): Machine code byte information dictionaries or an
        empty list if no machine code should be generated from this
        line.
    Raises:
        LineProcessingError: Failure to extract machine code.
    """
    if not line:
        return []
    machine_code = None
    for instruction in instructions:
        try:
            machine_code = instruction.parse_line(line)
        except InstructionParsingError as e:
            raise LineProcessingError(e)
    if machine_code is None:
        raise LineProcessingError("Unable to match line")
    return machine_code


def extract_constants(machine_code):
    """
    Extract and identify constants from instruction machine code dictionaries.

    Assumed constants are returned from the instruction parsers. This
    function then validates them to make sure they are correct.

    See XXX for information on machine code dictionaries from
    instructions.

    Args:
        machine_code (list(dict)): The machine code bytes as returned by
            an instruction line parser.
    Returns:
        tuple(list(str), list(str), list(str)): Lists of the labels,
        variables, and numbers used in this instruction.
    Raises:
        LineProcessingError: Invalid constants were specified.
    """
    labels = []
    variables = []
    numbers = []

    if not machine_code:
        return labels, variables, numbers

    for instruction_byte in machine_code:
        constant = instruction_byte["constant"]
        if constant:
            label = extract_label(constant)
            variable = extract_variable(constant)
            number = extract_number(constant)

            if not any(label, variable, number):
                raise LineProcessingError()

            if label:
                labels.append(label)
            if variable:
                variables.append(variable)
            if number:
                numbers.append(number)

    return labels, variables, numbers


def extract_number(test_string):
    """
    Extract a valid number.

    If the string is a valid number, return it. If it's marked as a
    number (starts with an #) but is then incorrectly specified, an
    exception is raised. If it's not marked as a number, an empty string
    is returned.

    Numbers must be between -127 and 255.

    Args:
        test_string (str): The string to try extracting a number from.
    Returns:
        str: The string that was passed in if it's valid, an empty
        string if it's not marked as a number.
    Raises:
        LineProcessingError: The string was marked as a number, but it
        was incorrectly specified.
    """
    pass


def check_structure_validity(assembly_lines):
    """
    Check the processed assembly lines for consistency/correctness.

    Args:
        assembly_lines (list(dict)): List of dictionaries (that conform
            to the :data:`~LINE_INFO_TEMPLATE` dictionary) with
            information about all the lines in the assembly file.
    """
    check_multiple_label_defs(assembly_lines)
    check_multiple_label_assignment(assembly_lines)
    check_undefined_label_ref(assembly_lines)
    check_multiple_variable_def(assembly_lines)
    check_num_variables(assembly_lines)
    check_num_instruction_bytes(assembly_lines)


def check_multiple_label_defs(assembly_lines):
    """

    Args:
        assembly_lines (list(dict)): List of dictionaries (that conform
            to the :data:`~LINE_INFO_TEMPLATE` dictionary) with
            information about all the lines in the assembly file.
    Raises:
        AssemblyError: If
    """
    pass


def check_multiple_label_assignment(assembly_lines):
    """


    Args:
        assembly_lines (list(dict)): List of dictionaries (that conform
            to the :data:`~LINE_INFO_TEMPLATE` dictionary) with
            information about all the lines in the assembly file.
    Raises:
        AssemblyError: If
    """
    pass


def check_undefined_label_ref(assembly_lines):
    """


    Args:
        assembly_lines (list(dict)): List of dictionaries (that conform
            to the :data:`~LINE_INFO_TEMPLATE` dictionary) with
            information about all the lines in the assembly file.
    Raises:
        AssemblyError: If
    """
    pass


def check_multiple_variable_def(assembly_lines):
    """


    Args:
        assembly_lines (list(dict)): List of dictionaries (that conform
            to the :data:`~LINE_INFO_TEMPLATE` dictionary) with
            information about all the lines in the assembly file.
    Raises:
        AssemblyError: If
    """
    pass


def check_num_variables(assembly_lines):
    """


    Args:
        assembly_lines (list(dict)): List of dictionaries (that conform
            to the :data:`~LINE_INFO_TEMPLATE` dictionary) with
            information about all the lines in the assembly file.
    Raises:
        AssemblyError: If
    """
    pass


def check_num_instruction_bytes(assembly_lines):
    """


    Args:
        assembly_lines (list(dict)): List of dictionaries (that conform
            to the :data:`~LINE_INFO_TEMPLATE` dictionary) with
            information about all the lines in the assembly file.
    Raises:
        AssemblyError: If
    """
    pass


def create_label_mapping(assembly_lines):
    """
    Create a mapping from labels to machine code byte indexes.

    Args:
        assembly_lines (list(dict)): List of dictionaries (that conform
            to the :data:`~LINE_INFO_TEMPLATE` dictionary) with
            information about all the lines in the assembly file.
    Returns:
        dict(str:str): Labels to program memory indexes in byte
        bitstring format.
    """


def create_variable_mapping(assembly_lines, variable_start_offset=0):
    """
    Create a mapping from variables to data byte indexes.

    Args:
        assembly_lines (list(dict)): List of dictionaries (that conform
            to the :data:`~LINE_INFO_TEMPLATE` dictionary) with
            information about all the lines in the assembly file.
        variable_start_offset (int) (optional): How far to offset the
            first variable in data memory from 0.
    Returns:
        dict(str:str): Variables to data memory indexes in byte
        bitstring format.
    """
    pass


def assembly_lines_to_machine_code(
        assembly_lines, label_mapping, variable_mapping):
    """

    """
    pass
