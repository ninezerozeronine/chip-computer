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
