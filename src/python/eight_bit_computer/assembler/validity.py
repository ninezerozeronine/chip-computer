"""
Validity checks on the processed assembly lines
"""


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
    Has the same label been defines more than once
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
    Has a single line been assigned more than one label

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
    Is a jump tyring to jump tp a label that hasn't been defined

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
    Has the same variable been defined mutiple times (?)

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
    Check there aren't more variables defined than will fit in data mem

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
    Check there aren't more instruction bytes that will fit in prog mem

    Args:
        assembly_lines (list(dict)): List of dictionaries (that conform
            to the :data:`~LINE_INFO_TEMPLATE` dictionary) with
            information about all the lines in the assembly file.
    Raises:
        AssemblyError: If
    """
    pass
