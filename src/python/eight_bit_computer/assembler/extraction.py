"""
Extract information from a list of assembly line info dictionaries.
"""

from ..numbers import number_to_bitstring

"""

"""


def get_assembly_summary_data(asm_line_infos):
    """
    Get print friendly lists of the data in assembly line info dicts.

    Args:
        asm_line_infos (list(dict)): List of line info dictionaries as
            returned by :func:`~assembler.lines_to_machine_code`.
    Returns:
        list: List of entries for the assembly summary print out
    """

    assembly_summary = []

    for asm_line_info in asm_line_infos:
        if asm_line_info["machine_code_templates"]:
            dual_entry = {}
            dual_entry["assembly"] = {}
            dual_entry["assembly"]["info"] = asm_line_info
            dual_entry["machine_code_byte"] = {}
            dual_entry["machine_code_byte"]["info"] = asm_line_info["machine_code_templates"][0]
            if asm_line_info["assigned_label"]:
                dual_entry["machine_code_byte"]["has_label"] = True
                dual_entry["machine_code_byte"]["label"] = asm_line_info["assigned_label"]
            else:
                dual_entry["machine_code_byte"]["has_label"] = False
            assembly_summary.append(dual_entry)

            for mc_byte_info in asm_line_info["machine_code_templates"][1:]:
                byte_only_entry = {}
                byte_only_entry["assembly"] = None
                byte_only_entry["machine_code_byte"] = {}
                byte_only_entry["machine_code_byte"]["info"] = mc_byte_info
                assembly_summary.append(byte_only_entry)

        else:
            assembly_only_entry = {}
            assembly_only_entry["machine_code_byte"] = None
            assembly_only_entry["assembly"] = {}
            assembly_only_entry["assembly"]["info"] = asm_line_info
            assembly_summary.append(assembly_only_entry)

    return assembly_summary


def generate_assembly_summary(asm_line_infos):
    """

    The end result is a print out like this::

        010 @label1            |
        011     LOAD [$var] 11 | 15 0F 00001111 - @label1 01010101 55
                               | 16 10 00010000 -         11001001 C9 $var
        012     // comment     |
        013     SET A #123     | 17 11 00010001 -         00101010 2A
                               | 18 12 00010010 -         01111011 7B #123
        015                    |
        016 @label2            |
        017     JUMP @label1   | 19 13 00010011 - @label2 01111100 7C
                               | 20 14 00010100 -         00001111 0F @label1
        018     // comment     |
    """

    summary_data = get_assembly_summary_data(asm_line_infos)
    widest_values = get_widest_column_values(summary_data)
    summary_line_template = (
        "{asm_line_no: <{widest_asm_line_no}} "
        "{raw_assembly_line: <{widest_asm_line}} "
        "| "
        "{mc_index_decimal: {widest_mc_index_decimal}} "
        "{mc_index_hex: {widest_mc_index_hex}} "
        "{mc_index_bitstring} "
        "{mc_byte_sep} "
        "{mc_label: {widest_mc_label}} "
        "{mc_byte_bitstring} "
        "{mc_byte_hex: {widest_mc_byte_hex}} "
        "{mc_byte_constant}"
    )
    formatted_summary_lines = []
    for summary_line in summary_data:
        if summary_line["assembly"]:
            asm_line_info = summary_line["assembly"]["info"]
            asm_line_no = asm_line_info["line_no"]
            raw_assembly_line = asm_line_info["raw"]
        else:
            asm_line_no = ""
            raw_assembly_line = ""

        if summary_line["machine_code_byte"]:
            mc_byte_info = summary_line["machine_code_byte"]["info"]
            mc_index_decimal = mc_byte_info["index"]
            mc_index_hex = "{index:0{width}X}".format(
                index=mc_byte_info["index"],
                width=widest_values["mc_index_hex"],
                )
            mc_index_bitstring = number_to_bitstring((mc_byte_info["index"]))
            mc_byte_sep = "-"
            if summary_line["machine_code_byte"]["has_label"]:
                mc_label = summary_line["machine_code_byte"]["label"]
            else:
                mc_label = ""
            mc_byte_bitstring = mc_byte_info["machine_code"]
            mc_byte_hex = "{mc_byte:0{width}X}".format(
                mc_byte=int(mc_byte_info["machine_code"], 2),
                width=widest_values["mc_byte_hex"],
            )
            if mc_byte_info["byte_type"] == "constant":
                mc_byte_constant = mc_byte_info["constant"]
            else:
                mc_byte_constant = ""
        else:
            mc_index_decimal = ""
            mc_index_hex = ""
            mc_index_bitstring = ""
            mc_byte_sep = ""
            mc_label = ""
            mc_byte_bitstring = ""
            mc_byte_hex = ""
            mc_byte_constant = ""

        formatted_line = summary_line_template.format(
            asm_line_no=asm_line_no,
            widest_asm_line_no=widest_values["asm_line_no"]
            raw_assembly_line=raw_assembly_line,
            widest_asm_line=widest_values["asm_line"]
            mc_index_decimal=mc_index_decimal,
            widest_mc_index_decimal=widest_values["mc_index_decimal"]
            mc_index_hex=mc_index_hex,
            widest_mc_index_hex=widest_values["mc_index_hex"]
            mc_index_bitstring=mc_index_bitstring,
            mc_byte_sep=mc_byte_sep,
            mc_label=mc_label,
            widest_mc_label=widest_values["mc_label"]
            mc_byte_bitstring=mc_byte_bitstring,
            mc_byte_hex=mc_byte_hex,
            widest_mc_byte_hex=widest_values["mc_byte_hex"]
            mc_byte_constant=mc_byte_constant,
        )
    formatted_summary_lines.append(formatted_line)

    return "\n".join(formatted_summary_lines)


def get_widest_column_values(assembly_summary_data):
    """

    """

    widest_values = {
        "asm_line_no": 0,
        "asm_line": 0
        "mc_index_decimal": 0,
        "mc_index_hex": 0,
        "mc_label": 0,
        "mc_byte_hex": 0,
    }

    for entry in assembly_summary_data:
        if entry["assembly"] is not None:
            # Assembly line number width
            line_no_width = len(str(entry["assembly"]["info"]["line_no"]))
            if line_no_width > widest_values["asm_line_no"]:
                widest_values["asm_line_no"] = line_no_width

            # Assembly line width
            asm_line_width = len(str(entry["assembly"]["info"]["raw"]))
            if asm_line_width > widest_values["asm_line"]:
                widest_values["asm_line"] = asm_line_width

        if entry["machine_code_byte"] is not None:
            # Decimal byte index width
            mc_index_decimal_width = len(
                entry["machine_code_byte"]["info"]["index"]
            )
            if mc_index_decimal_width > widest_values["mc_index_decimal"]:
                widest_values["mc_index_decimal"] = mc_index_decimal_width

            # Hex byte index width
            mc_index_hex_width = len(
                "{index:X}".format(
                    index=entry["machine_code_byte"]["info"]["index"]
                )
            )
            if mc_index_hex_width > widest_values["mc_index_hex"]:
                widest_values["mc_index_hex"] = mc_index_hex_width

            # Label width
            if entry["machine_code_byte"]["has_label"]:
                mc_label_width = len(entry["machine_code_byte"]["label"])
                if mc_label_width > widest_values["mc_label"]:
                    widest_values["mc_label"] = mc_label_width

            # Hex byte width
            if entry["machine_code_byte"]["info"]["byte_type"] == "constant":
                mc_constant_width = len(
                    entry["machine_code_byte"]["info"]["constant"]
                )
                if mc_constant_width > widest_values["mc_constant"]:
                    widest_values["mc_constant"] = mc_constant_width

    return widest_values
