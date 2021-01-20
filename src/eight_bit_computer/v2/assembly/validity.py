"""
Validity checks on the processed assembly lines
"""

from .exceptions import AssemblyError

ERROR_TEMPLATE = "Error processing line {line_no} ({line}): {details}"

def check_structure_validity(assembly_lines):
    """
    Check the processed assembly lines for consistency/correctness.

    Args:
        assembly_lines (list(:class:`~.AssemblyLine`)): List of processed
            lines of assembly.
    """
    check_multiple_label_defs(assembly_lines)
    check_multiple_label_assignment(assembly_lines)
    check_undefined_label_ref(assembly_lines)
    check_multiple_variable_def(assembly_lines)
    check_overlapping_variables(assembly_lines)
    check_undefined_variable_ref(assembly_lines)
    check_num_instruction_bytes(assembly_lines)

def check_multiple_label_defs(assembly_lines):
    """
    Check if a label been defined more than once.

    E.g. This is allowed::

        &label_1
            NOOP
        &label_2
            SET_ZERO A

    But this is not::

        &label_1
            NOOP
        &label_1
            SET_ZERO A

    As ``&label_1`` is already assigned to the index holding the
    ``NOOP`` instruction.

    Args:
        assembly_lines (list(:class:`~.AssemblyLine`)): List of
            processed lines of assembly.
    Raises:
        AssemblyError: If the same label been defined more than once.
    """

    labels = set()
    label_lines = {}
    for assembly_line in assembly_lines:
        if isinstance(assembly_line.pattern, Label):
            label = assembly_line.pattern.label
            if label in labels:
                details = (
                    "The label: \"{label}\" has already been defined on "
                    "line {prev_line}.".format(
                        label=label,
                        prev_line=label_lines[label],
                    )
                )
                msg = ERROR_TEMPLATE.format(
                    line_no=assembly_line.line_no,
                    line=assembly_line.raw_line,
                    details=details,
                )
                raise AssemblyError(msg)
            else:
                labels.add(label)
                label_lines[label] = assembly_line.line_no


def check_multiple_label_assignment(asm_line_infos):
    """
    Check if a line would be assigned more than one label.

    E.g. This is allowed::

        &label_1
            NOOP
        &label_2
            SET_ZERO A

    But this is not::

        &label_1
        &label_2
            SET_ZERO A

    As the ``SET_ZERO A`` instruction would have both ``&label_1`` and 
    ``&label_1`` assgned to it.

    Args:
        assembly_lines (list(:class:`~.AssemblyLine`)): List of
            processed lines of assembly.
    Raises:
        AssemblyError: If a line been assigned more than one label.
    """

    label_queued = False
    last_label = ""
    for assembly_line in assembly_lines:
        if label_queued and isinstance(assembly_line.pattern, Label):
            details = (
                "There is already a label ({label}) queued for "
                "assignment to the next machinecode word.".format(
                    label=last_label
                )
            )
            msg = ERROR_TEMPLATE.format(
                line_no=assembly_line.line_no,
                line=assembly_line.raw_line,
                details=details,
            )
            raise AssemblyError(msg)

        if isinstance(assembly_line.pattern, Label):
            label_queued = True
            last_label = assembly_line.pattern.label

        if assembly_line.has_machine_code() and label_queued:
            label_queued = False