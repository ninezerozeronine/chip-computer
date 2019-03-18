"""
Process assembly code and output machine code.
"""

LINE_INFO_TEMPLATE = {
    "line_no": 0,
    "raw": "",
    "clean": "",

    "is_label_def": False,
    "defined_label": "",
    "assigned_label": ""
    "used_labels": [],

    "is_variable_def": False
    "defined_variable" "",
    "used_variables": [],

    "used_numbers": [],
    "constants": [],
    "machine_code": [],
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
    pass


try:
    machine_code = assemble(filepath)
except AssemblyError:
    print AssemblyError


def assemble(file):
    lines = [line for line in file]

    assembly_lines = []
    for line_no, line in enumerate(lines):
        assembly_lines.append(process_line(line, line_no))

    check_multiple_label_defs(assembly_lines)
    check_multiple_label_assignment(assembly_lines)
    check_undefined_label_ref(assembly_lines)
    check_multiple_variable_def(assembly_lines)
    check_num_variables(assembly_lines)
    check_num_instruction_bytes(assembly_lines)

    label = None
    for assembly_line in assembly_lines:
        if label is None:
            label = assembly_line["defined_label"] or None
        if assembly_line["machine_code"] and label is not None:
            assembly_line["assigned_label"] = label
            label = None
        else:
            assembly_line["assigned_label"] = []


def label_basneame(label):
    pass


def variable_basename(variable):
    pass


def process_line(line, line_no):
    line_info = {}
    line_info["line_no"] = line_no
    line_info["raw"] = line
    cleaned_line = clean_line(line)
    line_info["clean"] = cleaned_line
    defined_label = get_defined_label(cleaned_line)
    defined_variable = get_defined_variable(cleaned_line)



    line_info["used_labels"] = get_used_labels(cleaned_line)
    line_info["used_variables"] = get_used_variables(cleaned_line)
    line_info["used_numbers"] = get_used_numbers(cleaned_line)
    line_info["constants"] = get_constants(line_info)
    return line_info


def machine_code_from_line(line):
    if not line:
        return []
    machine_code = None
    for instruction in instructions:
        try:
            machine_code = instruction.parse_line(line)
        except InstructionParsingError as e:
            raise ParsingError(e)
    if machine_code is None:
        raise UnmatchedInstructionError()
    return machine_code


def assembly_lines_to_machine_code(assembly_lines):
    variables = index_variables(assembly_lines)
    labels = index_labels(assembly_lines)


def get_constants(line_info):
    constants = []
    constants.append(line_info["used_labels"])
    constants.append(line_info["variables"])
    constants.append(line_info["numbers"].keys())
    return constants
