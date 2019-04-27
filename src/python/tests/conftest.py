import textwrap

import pytest

from eight_bit_computer.assembler import assembler
from eight_bit_computer.language.utils import get_machine_code_byte_template


@pytest.fixture
def assembly_lines():
    return textwrap.dedent(
        """\
        $variable0
        @label1
            LOAD [$variable1] A

        @label2
            LOAD [$variable2] A
            JUMP @label1

            STORE A [#123]
        @label3
            LOAD [$variable3] B
            LOAD [$variable0] C
        $variable4
        """
    ).splitlines()


@pytest.fixture
def processed_assembly_lines():
    """
    The result of processing each line of assembly_lines above:
    """

    lines = []

    line = assembler.get_line_info_template()
    line["line_no"] = 1
    line["raw"] = "$variable0"
    line["clean"] = "$variable0"
    line["defined_variable"] = "$variable0"
    lines.append(line)

    line = assembler.get_line_info_template()
    line["line_no"] = 2
    line["raw"] = "@label1"
    line["clean"] = "@label1"
    line["defined_label"] = "@label1"
    lines.append(line)

    line = assembler.get_line_info_template()
    line["line_no"] = 3
    line["raw"] = "LOAD [$variable1] A"
    line["clean"] = "LOAD [$variable1] A"
    line_mc_0 = get_machine_code_byte_template()
    line_mc_0["byte_type"] = "instruction"
    line_mc_0["machine_code"] = "99999999"
    line_mc_1 = get_machine_code_byte_template()
    line_mc_1["byte_type"] = "constant"
    line_mc_1["constant"] = "$variable1"
    line_mc_1["constant_type"] = "variable"
    line["machine_code_templates"] = [line_mc_0, line_mc_1]
    lines.append(line)

    line = assembler.get_line_info_template()
    line["line_no"] = 4
    lines.append(line)

    line = assembler.get_line_info_template()
    line["line_no"] = 5
    line["raw"] = "@label2"
    line["clean"] = "@label2"
    line["defined_label"] = "@label2"
    lines.append(line)

    line = assembler.get_line_info_template()
    line["line_no"] = 6
    line["raw"] = "LOAD [$variable2] A"
    line["clean"] = "LOAD [$variable2] A"
    line_mc_0 = get_machine_code_byte_template()
    line_mc_0["byte_type"] = "instruction"
    line_mc_0["machine_code"] = "99999999"
    line_mc_1 = get_machine_code_byte_template()
    line_mc_1["byte_type"] = "constant"
    line_mc_1["constant"] = "$variable2"
    line_mc_1["constant_type"] = "variable"
    line["machine_code_templates"] = [line_mc_0, line_mc_1]
    lines.append(line)

    line = assembler.get_line_info_template()
    line["line_no"] = 7
    line["raw"] = "JUMP @label1"
    line["clean"] = "JUMP @label1"
    line_mc_0 = get_machine_code_byte_template()
    line_mc_0["byte_type"] = "instruction"
    line_mc_0["machine_code"] = "99999999"
    line_mc_1 = get_machine_code_byte_template()
    line_mc_1["byte_type"] = "constant"
    line_mc_1["constant"] = "@label1"
    line_mc_1["constant_type"] = "label"
    line["machine_code_templates"] = [line_mc_0, line_mc_1]
    lines.append(line)

    line = assembler.get_line_info_template()
    line["line_no"] = 8
    lines.append(line)

    line = assembler.get_line_info_template()
    line["line_no"] = 9
    line["raw"] = "STORE A [#123]"
    line["clean"] = "STORE A [#123]"
    line_mc_0 = get_machine_code_byte_template()
    line_mc_0["byte_type"] = "instruction"
    line_mc_0["machine_code"] = "99999999"
    line_mc_1 = get_machine_code_byte_template()
    line_mc_1["byte_type"] = "constant"
    line_mc_1["constant"] = "#123"
    line_mc_1["constant_type"] = "number"
    line_mc_1["number_value"] = 123
    line["machine_code_templates"] = [line_mc_0, line_mc_1]
    lines.append(line)

    line = assembler.get_line_info_template()
    line["line_no"] = 10
    line["raw"] = "@label3"
    line["clean"] = "@label3"
    line["defined_label"] = "@label3"
    lines.append(line)

    line = assembler.get_line_info_template()
    line["line_no"] = 11
    line["raw"] = "LOAD [$variable3] B"
    line["clean"] = "LOAD [$variable3] A"
    line_mc_0 = get_machine_code_byte_template()
    line_mc_0["byte_type"] = "instruction"
    line_mc_0["machine_code"] = "99999999"
    line_mc_1 = get_machine_code_byte_template()
    line_mc_1["byte_type"] = "constant"
    line_mc_1["constant"] = "$variable3"
    line_mc_1["constant_type"] = "variable"
    line["machine_code_templates"] = [line_mc_0, line_mc_1]
    lines.append(line)

    line = assembler.get_line_info_template()
    line["line_no"] = 12
    line["raw"] = "LOAD [$variable0] C"
    line["clean"] = "LOAD [$variable0] A"
    line_mc_0 = get_machine_code_byte_template()
    line_mc_0["byte_type"] = "instruction"
    line_mc_0["machine_code"] = "99999999"
    line_mc_1 = get_machine_code_byte_template()
    line_mc_1["byte_type"] = "constant"
    line_mc_1["constant"] = "$variable0"
    line_mc_1["constant_type"] = "variable"
    line["machine_code_templates"] = [line_mc_0, line_mc_1]
    lines.append(line)

    line = assembler.get_line_info_template()
    line["line_no"] = 13
    line["raw"] = "$variable4"
    line["clean"] = "$variable4"
    line["defined_variable"] = "$variable4"
    lines.append(line)

    return lines
