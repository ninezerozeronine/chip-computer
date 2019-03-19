"""
Process assembly code and output machine code.

Attributes:
    LINE_INFO_TEMPLATE (dict): Template for assembly line information.
        the meaning of the keys is as follows:

        - line_no: The line in the assembly file that this line was on.
        - raw: The line as it was in the assembly file.
        - clean: The cleaned up line, ready for parsing.
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


def assemble(input_path, output_path=None):
    """
    Read an assembly file and write out equivalent machine code.

    Args:
        input_path (str): The location of the assembly file.
        output_path (str) (optional): The location to write out the
            machine code. If nothing is passed, the output path will be
            the input path with the extension changed to mc or have mc
            added if no extension was present.
    """

    lines = filepath_to_lines(input_path)

    try:
        machine_code = lines_to_machine_code(lines)
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
    pass


def write_machine_code(machine_code, output_path):
    """
    Write machine code to a file

    Args:
        machine_code (list(str)): List of the machine code values.
        output_path (str): Path of the file to write to.
    """
    pass


def lines_to_machine_code(lines):
    """
    Convert assembly lines to machine code lines.

    Args:
        lines (list(str)): The lines that made up the assembly file to
            be assembled.
    Returns:
        list(str): The assembly file converted to an equivalent list of
        machine code bytes as 8 bit binary strings.
    Raises:
        AssemblyError: If there was an error assembling the machine
            code.
    """

    assembly_lines = []
    for line_no, line in enumerate(lines):
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
    variable_mapping = create_variable_mapping(assembly_lines)

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
        LINE_INFO_TEMPLATE documentation for more information about what
        is in the dictionary.
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
    pass


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
    check_multiple_label_defs(assembly_lines)
    check_multiple_label_assignment(assembly_lines)
    check_undefined_label_ref(assembly_lines)
    check_multiple_variable_def(assembly_lines)
    check_num_variables(assembly_lines)
    check_num_instruction_bytes(assembly_lines)


def create_label_mapping(assembly_lines):
    pass


def create_variable_mapping(assembly_lines):
    pass


def assembly_lines_to_machine_code(
        assembly_lines, label_mapping, variable_mapping):

    variables = index_variables(assembly_lines)
    labels = index_labels(assembly_lines)
