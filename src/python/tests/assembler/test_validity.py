import pytest

from eight_bit_computer.assembler import validity
from eight_bit_computer.assembler.assembler import get_assembly_line_template
from eight_bit_computer.exceptions import AssemblyError
from eight_bit_computer.language.utils import get_machine_code_byte_template


def test_check_multiple_label_defs_raises():
    lines = []

    # "$variable0"
    line = get_assembly_line_template()
    line["line_no"] = 1
    line["raw"] = "$variable0"
    line["clean"] = "$variable0"
    line["defines_variable"] = True
    line["defined_variable"] = "$variable0"
    lines.append(line)

    # "@label1"
    line = get_assembly_line_template()
    line["line_no"] = 2
    line["raw"] = "@label1"
    line["clean"] = "@label1"
    line["defines_label"] = True
    line["defined_label"] = "@label1"
    lines.append(line)

    # "@label1"
    line = get_assembly_line_template()
    line["line_no"] = 3
    line["raw"] = "@label1"
    line["clean"] = "@label1"
    line["defines_label"] = True
    line["defined_label"] = "@label1"
    lines.append(line)

    with pytest.raises(AssemblyError):
        validity.check_multiple_label_defs(lines)


def test_check_multiple_label_defs_does_not_raise(processed_assembly_lines):
    validity.check_multiple_label_defs(processed_assembly_lines)
    assert True


def test_check_multiple_label_assignment_raises():
    lines = []

    # "$variable0"
    line = get_assembly_line_template()
    line["line_no"] = 1
    line["raw"] = "$variable0"
    line["clean"] = "$variable0"
    line["defines_variable"] = True
    line["defined_variable"] = "$variable0"
    lines.append(line)

    # "@label1"
    line = get_assembly_line_template()
    line["line_no"] = 2
    line["raw"] = "@label1"
    line["clean"] = "@label1"
    line["defines_label"] = True
    line["defined_label"] = "@label1"
    lines.append(line)

    # "@label2"
    line = get_assembly_line_template()
    line["line_no"] = 3
    line["raw"] = "@label2"
    line["clean"] = "@label2"
    line["defines_label"] = True
    line["defined_label"] = "@label2"
    lines.append(line)

    # "    LOAD [$variable1] A"
    line = get_assembly_line_template()
    line["line_no"] = 4
    line["raw"] = "    LOAD [$variable1] A"
    line["clean"] = "LOAD [$variable1] A"
    line_mc_0 = get_machine_code_byte_template()
    line_mc_0["byte_type"] = "instruction"
    line_mc_0["bitstring"] = "11111111"
    line_mc_1 = get_machine_code_byte_template()
    line_mc_1["byte_type"] = "constant"
    line_mc_1["constant"] = "$variable1"
    line_mc_1["constant_type"] = "variable"
    line["mc_bytes"] = [line_mc_0, line_mc_1]
    line["has_machine_code"] = True
    lines.append(line)

    with pytest.raises(AssemblyError):
        validity.check_multiple_label_assignment(lines)


def test_check_multiple_label_assignment_does_not_raise(processed_assembly_lines):
    validity.check_multiple_label_assignment(processed_assembly_lines)
    assert True


def test_check_undefined_label_ref_raises():
    lines = []

    # "$variable0"
    line = get_assembly_line_template()
    line["line_no"] = 1
    line["raw"] = "$variable0"
    line["clean"] = "$variable0"
    line["defines_variable"] = True
    line["defined_variable"] = "$variable0"
    lines.append(line)

    # "@label1"
    line = get_assembly_line_template()
    line["line_no"] = 2
    line["raw"] = "@label1"
    line["clean"] = "@label1"
    line["defines_label"] = True
    line["defined_label"] = "@label1"
    lines.append(line)

    # "    JUMP @newlabel"
    line = get_assembly_line_template()
    line["line_no"] = 3
    line["raw"] = "    JUMP @newlabel"
    line["clean"] = "JUMP @newlabel"
    line_mc_0 = get_machine_code_byte_template()
    line_mc_0["byte_type"] = "instruction"
    line_mc_0["bitstring"] = "11111111"
    line_mc_1 = get_machine_code_byte_template()
    line_mc_1["byte_type"] = "constant"
    line_mc_1["constant"] = "@newlabel"
    line_mc_1["constant_type"] = "label"
    line["mc_bytes"] = [line_mc_0, line_mc_1]
    line["has_machine_code"] = True
    lines.append(line)

    with pytest.raises(AssemblyError):
        validity.check_undefined_label_ref(lines)


def test_check_undefined_label_ref_does_not_raise(processed_assembly_lines):
    validity.check_undefined_label_ref(processed_assembly_lines)
    assert True


def test_check_multiple_variable_def_raises():
    lines = []

    # "$variable0"
    line = get_assembly_line_template()
    line["line_no"] = 1
    line["raw"] = "$variable0"
    line["clean"] = "$variable0"
    line["defines_variable"] = True
    line["defined_variable"] = "$variable0"
    lines.append(line)

    # "@label1"
    line = get_assembly_line_template()
    line["line_no"] = 2
    line["raw"] = "@label1"
    line["clean"] = "@label1"
    line["defines_label"] = True
    line["defined_label"] = "@label1"
    lines.append(line)

    # "$variable0"
    line = get_assembly_line_template()
    line["line_no"] = 3
    line["raw"] = "$variable0"
    line["clean"] = "$variable0"
    line["defines_variable"] = True
    line["defined_variable"] = "$variable0"
    lines.append(line)

    with pytest.raises(AssemblyError):
        validity.check_multiple_variable_def(lines)


def test_check_multiple_variable_def_does_not_raise(processed_assembly_lines):
    validity.check_multiple_variable_def(processed_assembly_lines)
    assert True


def test_check_num_variables_raises():
    lines = []
    for num in range(1, 301):
        var = "$variable{num}".format(num=num)
        line = get_assembly_line_template()
        line["line_no"] = num
        line["raw"] = var
        line["clean"] = var
        line["defines_variable"] = True
        line["defined_variable"] = var
        lines.append(line)

    with pytest.raises(AssemblyError):
        validity.check_num_variables(lines, 0)


def test_check_num_variables_offset_raises():
    lines = []
    for num in range(1, 11):
        var = "$variable{num}".format(num=num)
        line = get_assembly_line_template()
        line["line_no"] = num
        line["raw"] = var
        line["clean"] = var
        line["defines_variable"] = True
        line["defined_variable"] = var
        lines.append(line)

    with pytest.raises(AssemblyError):
        validity.check_num_variables(lines, 250)


def test_check_num_variables_does_not_raise(processed_assembly_lines):
    validity.check_num_variables(processed_assembly_lines, 0)
    assert True


def test_check_num_instruction_bytes_raises():
    lines = []

    # "@label1"
    line = get_assembly_line_template()
    line["line_no"] = 1
    line["raw"] = "@label1"
    line["clean"] = "@label1"
    line["defines_label"] = True
    line["defined_label"] = "@label1"
    lines.append(line)

    for num in range(2, 200):
        # "    LOAD [#123] A"
        line = get_assembly_line_template()
        line["line_no"] = 3
        line["raw"] = "    LOAD [#123] A"
        line["clean"] = "LOAD [#123] A"
        line_mc_0 = get_machine_code_byte_template()
        line_mc_0["byte_type"] = "instruction"
        line_mc_0["bitstring"] = "11111111"
        line_mc_1 = get_machine_code_byte_template()
        line_mc_1["byte_type"] = "constant"
        line_mc_1["constant"] = "#123"
        line_mc_1["constant_type"] = "number"
        line_mc_1["number_value"] = 123
        line["mc_bytes"] = [line_mc_0, line_mc_1]
        line["has_machine_code"] = True
        lines.append(line)

    with pytest.raises(AssemblyError):
        validity.check_num_instruction_bytes(lines)


def test_check_num_instruction_bytes_does_not_raise(processed_assembly_lines):
    validity.check_num_instruction_bytes(processed_assembly_lines)
    assert True
