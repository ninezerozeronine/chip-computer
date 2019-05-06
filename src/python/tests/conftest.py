import textwrap
from copy import deepcopy

import pytest

from eight_bit_computer.data_structures import (
    get_machine_code_byte_template,
    get_summary_entry_template,
    get_assembly_line_template,
)


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
        // comment
        """
    ).splitlines()


@pytest.fixture
def processed_assembly_lines():
    return gen_processed_assembly_lines_data()


def gen_processed_assembly_lines_data():
    """
    The result of processing each line returned by assembly_lines above.
    """

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

    # "    LOAD [$variable1] A"
    line = get_assembly_line_template()
    line["line_no"] = 3
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

    # ""
    line = get_assembly_line_template()
    line["line_no"] = 4
    lines.append(line)

    # @label2
    line = get_assembly_line_template()
    line["line_no"] = 5
    line["raw"] = "@label2"
    line["clean"] = "@label2"
    line["defines_label"] = True
    line["defined_label"] = "@label2"
    lines.append(line)

    # "    LOAD [$variable2] A"
    line = get_assembly_line_template()
    line["line_no"] = 6
    line["raw"] = "    LOAD [$variable2] A"
    line["clean"] = "LOAD [$variable2] A"
    line_mc_0 = get_machine_code_byte_template()
    line_mc_0["byte_type"] = "instruction"
    line_mc_0["bitstring"] = "11111111"
    line_mc_1 = get_machine_code_byte_template()
    line_mc_1["byte_type"] = "constant"
    line_mc_1["constant"] = "$variable2"
    line_mc_1["constant_type"] = "variable"
    line["mc_bytes"] = [line_mc_0, line_mc_1]
    line["has_machine_code"] = True
    lines.append(line)

    # "    JUMP @label1"
    line = get_assembly_line_template()
    line["line_no"] = 7
    line["raw"] = "    JUMP @label1"
    line["clean"] = "JUMP @label1"
    line_mc_0 = get_machine_code_byte_template()
    line_mc_0["byte_type"] = "instruction"
    line_mc_0["bitstring"] = "11111111"
    line_mc_1 = get_machine_code_byte_template()
    line_mc_1["byte_type"] = "constant"
    line_mc_1["constant"] = "@label1"
    line_mc_1["constant_type"] = "label"
    line["mc_bytes"] = [line_mc_0, line_mc_1]
    line["has_machine_code"] = True
    lines.append(line)

    # ""
    line = get_assembly_line_template()
    line["line_no"] = 8
    lines.append(line)

    # "    STORE A [#123]""
    line = get_assembly_line_template()
    line["line_no"] = 9
    line["raw"] = "    STORE A [#123]"
    line["clean"] = "STORE A [#123]"
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

    # "@label3"
    line = get_assembly_line_template()
    line["line_no"] = 10
    line["raw"] = "@label3"
    line["clean"] = "@label3"
    line["defines_label"] = True
    line["defined_label"] = "@label3"
    lines.append(line)

    # "    LOAD [$variable3] B"
    line = get_assembly_line_template()
    line["line_no"] = 11
    line["raw"] = "    LOAD [$variable3] B"
    line["clean"] = "LOAD [$variable3] B"
    line_mc_0 = get_machine_code_byte_template()
    line_mc_0["byte_type"] = "instruction"
    line_mc_0["bitstring"] = "11111111"
    line_mc_1 = get_machine_code_byte_template()
    line_mc_1["byte_type"] = "constant"
    line_mc_1["constant"] = "$variable3"
    line_mc_1["constant_type"] = "variable"
    line["mc_bytes"] = [line_mc_0, line_mc_1]
    line["has_machine_code"] = True
    lines.append(line)

    # "    LOAD [$variable0] C"
    line = get_assembly_line_template()
    line["line_no"] = 12
    line["raw"] = "    LOAD [$variable0] C"
    line["clean"] = "LOAD [$variable0] C"
    line_mc_0 = get_machine_code_byte_template()
    line_mc_0["byte_type"] = "instruction"
    line_mc_0["bitstring"] = "11111111"
    line_mc_1 = get_machine_code_byte_template()
    line_mc_1["byte_type"] = "constant"
    line_mc_1["constant"] = "$variable0"
    line_mc_1["constant_type"] = "variable"
    line["mc_bytes"] = [line_mc_0, line_mc_1]
    line["has_machine_code"] = True
    lines.append(line)

    # "$variable4"
    line = get_assembly_line_template()
    line["line_no"] = 13
    line["raw"] = "$variable4"
    line["clean"] = "$variable4"
    line["defined_variable"] = "$variable4"
    line["defines_variable"] = True
    lines.append(line)

    # "// comment"
    line = get_assembly_line_template()
    line["line_no"] = 14
    line["raw"] = "// comment"
    line["clean"] = ""
    lines.append(line)

    return lines


@pytest.fixture
def assembly_line_infos():
    return gen_assembly_line_infos_data()


def gen_assembly_line_infos_data():
    """
    The result of fully parsing and evaulating the lines returned by
    assembly_lines above.
    """

    full_line_info = gen_processed_assembly_lines_data()

    # LOAD [$variable1] A
    full_line_info[2]["has_label_assigned"] = True
    full_line_info[2]["assigned_label"] = "@label1"
    full_line_info[2]["mc_bytes"][0]["index"] = 0
    full_line_info[2]["mc_bytes"][1]["bitstring"] = "00000001"
    full_line_info[2]["mc_bytes"][1]["index"] = 1

    # LOAD [$variable2] A
    full_line_info[5]["has_label_assigned"] = True
    full_line_info[5]["assigned_label"] = "@label2"
    full_line_info[5]["mc_bytes"][0]["index"] = 2
    full_line_info[5]["mc_bytes"][1]["bitstring"] = "00000010"
    full_line_info[5]["mc_bytes"][1]["index"] = 3

    # JUMP @label1
    full_line_info[6]["mc_bytes"][0]["index"] = 4
    full_line_info[6]["mc_bytes"][1]["bitstring"] = "00000000"
    full_line_info[6]["mc_bytes"][1]["index"] = 5

    # STORE A [#123]
    full_line_info[8]["mc_bytes"][0]["index"] = 6
    full_line_info[8]["mc_bytes"][1]["bitstring"] = "01111011"
    full_line_info[8]["mc_bytes"][1]["index"] = 7

    # LOAD [$variable3] B
    full_line_info[10]["has_label_assigned"] = True
    full_line_info[10]["assigned_label"] = "@label3"
    full_line_info[10]["mc_bytes"][0]["index"] = 8
    full_line_info[10]["mc_bytes"][1]["bitstring"] = "00000011"
    full_line_info[10]["mc_bytes"][1]["index"] = 9

    # LOAD [$variable0] C
    full_line_info[11]["mc_bytes"][0]["index"] = 10
    full_line_info[11]["mc_bytes"][1]["bitstring"] = "00000000"
    full_line_info[11]["mc_bytes"][1]["index"] = 11

    return full_line_info


@pytest.fixture
def assembly_summary_data():

    asm_line_infos = gen_assembly_line_infos_data()

    summary_lines = []

    # $variable0
    summary_line = get_summary_entry_template()
    summary_line["has_assembly"] = True
    summary_line["assembly"]["info"] = deepcopy(asm_line_infos[0])
    summary_lines.append(summary_line)

    # @label1
    summary_line = get_summary_entry_template()
    summary_line["has_assembly"] = True
    summary_line["assembly"]["info"] = deepcopy(asm_line_infos[1])
    summary_lines.append(summary_line)

    # LOAD [$variable1] A
    # byte0
    summary_line = get_summary_entry_template()
    summary_line["has_machine_code_byte"] = True
    summary_line["machine_code_byte"]["info"] = deepcopy(asm_line_infos[2]["mc_bytes"][0])
    summary_line["machine_code_byte"]["has_label"] = True
    summary_line["machine_code_byte"]["label"] = "@label1"

    summary_line["has_assembly"] = True
    summary_line["assembly"]["info"] = deepcopy(asm_line_infos[2])
    summary_lines.append(summary_line)
    # byte1
    summary_line = get_summary_entry_template()
    summary_line["has_machine_code_byte"] = True
    summary_line["machine_code_byte"]["info"] = deepcopy(asm_line_infos[2]["mc_bytes"][1])
    summary_lines.append(summary_line)

    #
    summary_line = get_summary_entry_template()
    summary_line["has_assembly"] = True
    summary_line["assembly"]["info"] = deepcopy(asm_line_infos[3])
    summary_lines.append(summary_line)

    # @label2
    summary_line = get_summary_entry_template()
    summary_line["has_assembly"] = True
    summary_line["assembly"]["info"] = deepcopy(asm_line_infos[4])
    summary_lines.append(summary_line)

    # LOAD [$variable2] A
    # byte0
    summary_line = get_summary_entry_template()
    summary_line["has_machine_code_byte"] = True
    summary_line["machine_code_byte"]["info"] = deepcopy(asm_line_infos[5]["mc_bytes"][0])
    summary_line["machine_code_byte"]["has_label"] = True
    summary_line["machine_code_byte"]["label"] = "@label2"

    summary_line["has_assembly"] = True
    summary_line["assembly"]["info"] = deepcopy(asm_line_infos[5])
    summary_lines.append(summary_line)
    # byte1
    summary_line = get_summary_entry_template()
    summary_line["has_machine_code_byte"] = True
    summary_line["machine_code_byte"]["info"] = deepcopy(asm_line_infos[5]["mc_bytes"][1])
    summary_lines.append(summary_line)

    # JUMP @label1
    # byte0
    summary_line = get_summary_entry_template()
    summary_line["has_machine_code_byte"] = True
    summary_line["machine_code_byte"]["info"] = deepcopy(asm_line_infos[6]["mc_bytes"][0])

    summary_line["has_assembly"] = True
    summary_line["assembly"]["info"] = deepcopy(asm_line_infos[6])
    summary_lines.append(summary_line)
    # byte1
    summary_line = get_summary_entry_template()
    summary_line["has_machine_code_byte"] = True
    summary_line["machine_code_byte"]["info"] = deepcopy(asm_line_infos[6]["mc_bytes"][1])
    summary_lines.append(summary_line)

    #
    summary_line = get_summary_entry_template()
    summary_line["has_assembly"] = True
    summary_line["assembly"]["info"] = deepcopy(asm_line_infos[7])
    summary_lines.append(summary_line)

    # STORE A [#123]
    # byte0
    summary_line = get_summary_entry_template()
    summary_line["has_machine_code_byte"] = True
    summary_line["machine_code_byte"]["info"] = deepcopy(asm_line_infos[8]["mc_bytes"][0])

    summary_line["has_assembly"] = True
    summary_line["assembly"]["info"] = deepcopy(asm_line_infos[8])
    summary_lines.append(summary_line)
    # byte1
    summary_line = get_summary_entry_template()
    summary_line["has_machine_code_byte"] = True
    summary_line["machine_code_byte"]["info"] = deepcopy(asm_line_infos[8]["mc_bytes"][1])
    summary_lines.append(summary_line)

    # @label3
    summary_line = get_summary_entry_template()
    summary_line["has_assembly"] = True
    summary_line["assembly"]["info"] = deepcopy(asm_line_infos[9])
    summary_lines.append(summary_line)

    # LOAD [$variable3] B
    # byte0
    summary_line = get_summary_entry_template()
    summary_line["has_machine_code_byte"] = True
    summary_line["machine_code_byte"]["info"] = deepcopy(asm_line_infos[10]["mc_bytes"][0])
    summary_line["machine_code_byte"]["has_label"] = True
    summary_line["machine_code_byte"]["label"] = "@label3"

    summary_line["has_assembly"] = True
    summary_line["assembly"]["info"] = deepcopy(asm_line_infos[10])
    summary_lines.append(summary_line)
    # byte1
    summary_line = get_summary_entry_template()
    summary_line["has_machine_code_byte"] = True
    summary_line["machine_code_byte"]["info"] = deepcopy(asm_line_infos[10]["mc_bytes"][1])
    summary_lines.append(summary_line)

    # LOAD [$variable0] C
    # byte0
    summary_line = get_summary_entry_template()
    summary_line["has_machine_code_byte"] = True
    summary_line["machine_code_byte"]["info"] = deepcopy(asm_line_infos[11]["mc_bytes"][0])

    summary_line["has_assembly"] = True
    summary_line["assembly"]["info"] = deepcopy(asm_line_infos[11])
    summary_lines.append(summary_line)
    # byte1
    summary_line = get_summary_entry_template()
    summary_line["has_machine_code_byte"] = True
    summary_line["machine_code_byte"]["info"] = deepcopy(asm_line_infos[11]["mc_bytes"][1])
    summary_lines.append(summary_line)

    # $variable4
    summary_line = get_summary_entry_template()
    summary_line["has_assembly"] = True
    summary_line["assembly"]["info"] = deepcopy(asm_line_infos[12])
    summary_lines.append(summary_line)

    # // comment
    summary_line = get_summary_entry_template()
    summary_line["has_assembly"] = True
    summary_line["assembly"]["info"] = deepcopy(asm_line_infos[13])
    summary_lines.append(summary_line)

    return summary_lines