"""
Validity checks on the processed assembly lines
"""

ERROR_TEMPLATE = "Error on line {line_no}:\n\n{details}"


def check_structure_validity(asm_line_infos, variable_start_offset):
    """
    Check the processed assembly lines for consistency/correctness.

    Args:
        asm_line_infos (list(dict)): List of dictionaries (conforming to
            :func:~`get_line_info_template`) with information about all
            the lines in the assembly file.
    """
    check_multiple_label_defs(assembly_lines)
    check_multiple_label_assignment(assembly_lines)
    check_undefined_label_ref(assembly_lines)
    check_multiple_variable_def(assembly_lines)
    check_num_variables(assembly_lines, variable_start_offset)
    check_num_instruction_bytes(assembly_lines)


def check_multiple_label_defs(asm_line_infos):
    """
    Check if the same label been defined more than once.

    Args:
        asm_line_infos (list(dict)): List of dictionaries (conforming to
            :func:~`get_line_info_template`) with information about all
            the lines in the assembly file.
    Raises:
        AssemblyError: If
    """

    labels = set()
    label_lines = {}
    for asm_line_info in asm_line_infos:
        if asm_line_info["defines_label"]:
            label = asm_line_info["defined_label"]
            if label in labels:
                details = (
                    "The label: \"{label}\" has already been defined on "
                    "line {prev_line}.".format(
                        line_no=asm_line_info["line_no"],
                        label=label,
                        prev_line=label_lines[label],
                    )
                )
                msg = ERROR_TEMPLATE.format(
                    line_no=asm_line_info["line_no"],
                    details=details,
                )
                Raise AssemblyError(msg)
            else:
                labels.add(label)
                label_lines[label] = asm_line_info["line_no"]


def check_multiple_label_assignment(assembly_lines):
    """
    Has a single line been assigned more than one label

    Args:
        asm_line_infos (list(dict)): List of dictionaries (conforming to
            :func:~`get_line_info_template`) with information about all
            the lines in the assembly file.
    Raises:
        AssemblyError: If
    """

    label_queued = False
    last_label = ""
    for asm_line_info in asm_line_infos:
        if label_queued and asm_line_info["defines_label"]:
            details = (
                "There is already a label ({label}) queued for "
                "assignment to the next instruction.".format(
                    label=last_label
                )
            )
            msg = ERROR_TEMPLATE.format(
                line_no=asm_line_info["line_no"],
                details=details,
            )
            Raise AssemblyError(msg)

        if asm_line_info["defines_label"]:
            label_queued = True
            last_label = asm_line_info["label"]

        if assembly_line["has_machine_code"] and label_queued:
            label_queued = False


def check_undefined_label_ref(assembly_lines):
    """
    Is a jump tyring to jump tp a label that hasn't been defined

    Args:
        asm_line_infos (list(dict)): List of dictionaries (conforming to
            :func:~`get_line_info_template`) with information about all
            the lines in the assembly file.
    Raises:
        AssemblyError: If
    """
    # Gather labels
    labels = []
    for asm_line_info in asm_line_infos:
        if asm_line_info["defines_label"]:
            labels.append(asm_line_info["defined_label"])

    for asm_line_info in asm_line_infos:
        if assembly_line["has_machine_code"]:
            for mc_byte_info in assembly_line["mc_byte_infos"]:
                if (mc_byte_info["byte_type"] == "constant"
                        and mc_byte_info["constant_type"] == "label"
                        and mc_byte_info["constant"] not in labels):
                    details = (
                        "This line is referencing a label ({label}) "
                        "that has not been defined."
                    )
                    msg = ERROR_TEMPLATE.format(
                        line_no=asm_line_info["line_no"],
                        details=details,
                    )
                    Raise AssemblyError(msg)


def check_multiple_variable_def(assembly_lines):
    """
    Has the same variable been defined mutiple times (?)

    Args:
        asm_line_infos (list(dict)): List of dictionaries (conforming to
            :func:~`get_line_info_template`) with information about all
            the lines in the assembly file.
    Raises:
        AssemblyError: If
    """
    variables = set()
    variable_lines = {}
    for asm_line_info in asm_line_infos:
        if asm_line_info["defines_variable"]:
            variable = asm_line_info["defined_variable"]
            if variable in variables:
                details = (
                    "The variable: \"{variable}\" has already been defined on "
                    "line {prev_line}.".format(
                        line_no=asm_line_info["line_no"],
                        variable=variable,
                        prev_line=variable_lines[variable],
                    )
                )
                msg = ERROR_TEMPLATE.format(
                    line_no=asm_line_info["line_no"],
                    details=details,
                )
                Raise AssemblyError(msg)
            else:
                variables.add(variable)
                variable_lines[variable] = asm_line_info["line_no"]


def check_num_variables(assembly_lines, variable_start_offset):
    """
    Check there aren't more variables defined than will fit in data mem

    Args:
        asm_line_infos (list(dict)): List of dictionaries (conforming to
            :func:~`get_line_info_template`) with information about all
            the lines in the assembly file.
    Raises:
        AssemblyError: If
    """
    pass


def check_num_instruction_bytes(assembly_lines):
    """
    Check there aren't more instruction bytes that will fit in prog mem

    Args:
        asm_line_infos (list(dict)): List of dictionaries (conforming to
            :func:~`get_line_info_template`) with information about all
            the lines in the assembly file.
    Raises:
        AssemblyError: If
    """
    pass
