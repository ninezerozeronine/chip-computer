"""
Generate a summary of the assembly lines and machine code.
"""

from . import number_utils
from .data_structures import get_summary_entry_template


"""
// A comment
!alias #255

@ #10
$var #1 #2
    NOOP
    ADD A

@ #20
&label
    NOOP
    AND #0b101
    ADD [!alias]



 1 // A comment     |
 2 !alias #255      |
 3                  |
 4 @ #5             |
 5 $var1 #1 #2      |  5 0x000A -          1 0x0001 #1
                    |  6 0x000B -          2 0x0002 #2
 6     NOOP         |  7 0x000C -          0 0x0000
 7     ADD A        |  8 0x000D -         32 0x0020
 8                  |
 9 @ #20            |
10 &label           |
11     NOOP         | 20 0x0014 - &label   0 0x0000
12     AND #0b111   | 21 0x0015 -         64 0x0040 
                    | 22 0x0016 -          7 0x0007 #0b111
13     ADD [!alias] | 23 0x0017 -         65 0x0041
                    | 24 0x0018 -        255 0x0005 !alias
14     AND $var     | 25 0x0019 -         64 0x0040
                    | 26 0x001A -          5 0x0005 $var

"""



def generate_assembly_summary(assembly_lines):
    """
    Produce a summary that combines assembly and machine code.

    The summary will be like this::

         1 $variable0              |
         2 @label1                 |
         3     LOAD [$variable1] A |  0 00 00000000 - @label1 255 FF 11111111
                                   |  1 01 00000001 -           1 01 00000001 $variable1
         4                         |
         5 @label2                 |
         6     LOAD [$variable2] A |  2 02 00000010 - @label2 255 FF 11111111
                                   |  3 03 00000011 -           2 02 00000010 $variable2
         7     JUMP @label1        |  4 04 00000100 -         255 FF 11111111
                                   |  5 05 00000101 -           0 00 00000000 @label1
         8                         |
         9     STORE A [#123]      |  6 06 00000110 -         255 FF 11111111
                                   |  7 07 00000111 -         123 7B 01111011 #123
        10 @label3                 |
        11     LOAD [$variable3] B |  8 08 00001000 - @label3 255 FF 11111111
                                   |  9 09 00001001 -           3 03 00000011 $variable3
        12     LOAD [$variable0] C | 10 0A 00001010 -         255 FF 11111111
                                   | 11 0B 00001011 -           0 00 00000000 $variable0
        13 $variable4              |
        14 // comment

    Args:
        assembly_lines (list(dict)): List of dictionaries of information
            about the parsed assembly.
    Returns:
        str: Printable summary.
    """
    label_map = assembler.create_label_map(assembly_lines)
    summary_data = get_assembly_summary_data(assembly_lines, label_map)
    lines = generate_assembly_summary_lines(summary_data)
    return "\n".join(lines)


def get_assembly_summary_data(assembly_lines, label_map):
    """
    Process assembly data to make formatting easier for the summary.

    Args:
        asm_line_infos (list(AssemblyLine)): List of processed assembly
            line objects.
    Returns:
        list: List of entries for the assembly summary print out
    """

    index_to_label = {}
    for label, index in label_map.items():
        index_to_label[index] = label

    assembly_summary = []
    for line in assembly_lines:
        if line.pattern.machinecode:
            line_info = {}

            # This summary line has both assembly and machinecode
            assembly_info = {}

            assembly_info["raw"] = line.raw_line
            assembly_info["line_no"] = str(line.line_no)
            line_info["assembly"] = assembly_info

            word_info = {}

            index = line.pattern.machinecode[0].index
            word_info["index_decimal"] = str(index)
            word_info["index_hex"] = "0x{index:04X}".format(index=index)
            label = index_to_label.get(index)
            if label is not None:
                # Don't like hard coding this label identifier here...
                word_info["label"] = "&{label}".format(label=label)

            value = line.pattern.machinecode[0].value
            word_info["value_decimal"] = str(value)
            word_info["value_hex"] = "0x{value:04X}".format(value=value)

            if const_token := line.pattern.machinecode[0].const_token:
                word_info["const"] = const_token.raw

            line_info["word"] = word_info

            assembly_summary.append(line_info)

            # These summary lines only have machinecode
            for word in line.pattern.machinecode[1:]:
                word_info = {}

                index = word.index
                word_info["index_decimal"] = str(index)
                word_info["index_hex"] = "0x{index:04X}".format(index=index)
                value = word.value
                word_info["value_decimal"] = str(value)
                word_info["value_hex"] = "0x{value:04X}".format(value=value)
                const_token = word.const_token
                if const_token:
                    word_info["const"] = const_token.raw
                else:
                    word_info["const"] = ""

                assembly_summary.append({"word":word_info})
        else:
            # This summary line only has assembly and machinecode
            assembly_info = {}

            assembly_info["raw"] = line.raw_line
            assembly_info["line_no"] = str(line.line_no)

            assembly_summary.append({"assembly":assembly_info})

    return assembly_summary


def generate_assembly_summary_lines(summary_data):
    """
    Generate list of lines for an assembly summary

    Args:
        summary_data
    Returns:
        list(str): List of lines for the summary.
    """

    widest_values = get_widest_column_values(summary_data)

    summary_lines = []
    for entry in summary_data:
        line_parts = []

        # Assembly line number
        line_no = entry.get("assembly", {}).get("line_no", "")
        line_parts.append("{line_no: >{widest_asm_line_no}}".format(
            line_no=line_no,
            widest_asm_line_no=widest_values["asm_line_no"]
        ))

        # Assembly line
        raw = entry.get("assembly", {}).get("raw", "")
        line_parts.append("{raw_assembly_line: <{widest_asm_line}}".format(
            raw_assembly_line=raw,
            widest_asm_line=widest_values["asm_line"]
        ))

        # Assembly/machinecode separator
        line_parts.append("|")

        if word := entry.get("word"):

            # Decimal word index
            line_parts.append(
                "{word_index_decimal: >{widest}}".format(
                    word_index_decimal=word["index_decimal"],
                    widest=widest_values["word_index_decimal"]
            ))

            # Hex word index
            line_parts.append(word["index_hex"])

            # Index/value seperator
            line_parts.append("-")

            # Label
            if widest_values["word_label"] > 0:
                label = word.get("label", "")
                line_parts.append(
                    "{label: <{widest}}".format(
                        label=label,
                        widest=widest_values["word_label"]
                ))

            # Decimal word value
            line_parts.append(
                "{word_value_decimal: >{widest}}".format(
                    word_value_decimal=word["value_decimal"],
                    widest=widest_values["word_value_decimal"]
            ))

            # Hex word value
            line_parts.append(word["value_hex"])

            # Constant
            if const := word.get("const"):
                line_parts.append(const)

        summary_lines.append(" ".join(line_parts).rstrip())

    return summary_lines


    # summary_line_template = (
    #     "{asm_line_no: >{widest_asm_line_no}} "
    #     "{raw_assembly_line: <{widest_asm_line}} "
    #     "| "
    #     "{word_index_decimal: >{widest_word_index_decimal}} "
    #     "{word_index_hex} "
    #     "{word_sep} "
    #     "{word_label: <{widest_word_label}}"
    #     "{word_value_decimal: >{widest_word_value_decimal}} "
    #     "{word_value_hex} "
    #     "{word_value_constant}"
    # )
    # formatted_summary_lines = []
    # for entry in summary_data:
    #     if assembly := entry.get("assembly"):
    #         asm_line_no = assembly["line_no"]
    #         raw_assembly_line = assembly["raw"]
    #     else:
    #         asm_line_no = ""
    #         raw_assembly_line = ""

    #     if word := entry.get("word"):
    #         word_index_decimal = word["index_decimal"]
    #         word_index_hex = word["index_hex"]
    #         word_sep = "-"

    #         word_value_decimal = word["value_decimal"]
    #         word_value_hex = word["value_hex"]

    #         if label := word.get("label"):
    #             word_label = label
    #         else:
    #             word_label = ""

    #         if const := word.get("const"):
    #             word_value_constant = const
    #         else:
    #             word_value_constant = ""
    #     else:
    #         word_index_decimal = ""
    #         word_index_hex = ""
    #         word_index_bitstring = ""
    #         word_sep = ""
    #         word_label = ""
    #         word_value_decimal = ""
    #         word_value_bitstring = ""
    #         word_value_hex = ""
    #         word_value_constant = ""

    #     formatted_line = summary_line_template.format(
    #         asm_line_no=asm_line_no,
    #         widest_asm_line_no=widest_values["asm_line_no"],
    #         raw_assembly_line=raw_assembly_line,
    #         widest_asm_line=widest_values["asm_line"],
    #         word_index_decimal=word_index_decimal,
    #         widest_word_index_decimal=widest_values["word_index_decimal"],
    #         word_index_hex=word_index_hex,
    #         word_sep=word_sep,
    #         word_label=word_label,
    #         widest_word_label=widest_values["word_label"],
    #         word_value_decimal=word_value_decimal,
    #         widest_word_value_decimal=widest_values["word_value_decimal"],
    #         word_value_hex=word_value_hex,
    #         word_value_constant=word_value_constant,
    #     ).rstrip()
    #     formatted_summary_lines.append(formatted_line)

    # return formatted_summary_lines





    # assembly_summary = []

    # for asm_line_info in asm_line_infos:
    #     if asm_line_info["has_machine_code"]:
    #         dual_entry = get_summary_entry_template()
    #         dual_entry["has_assembly"] = True
    #         dual_entry["assembly"]["info"] = deepcopy(asm_line_info)

    #         dual_entry["has_mc_byte"] = True
    #         dual_entry["mc_byte"]["info"] = deepcopy(
    #             asm_line_info["mc_bytes"][0]
    #         )
    #         if asm_line_info["has_label_assigned"]:
    #             dual_entry["mc_byte"]["has_label"] = True
    #             dual_entry["mc_byte"]["label"] = asm_line_info["assigned_label"]
    #         assembly_summary.append(dual_entry)

    #         for mc_byte_info in asm_line_info["mc_bytes"][1:]:
    #             byte_only_entry = get_summary_entry_template()
    #             byte_only_entry["has_mc_byte"] = True
    #             byte_only_entry["mc_byte"]["info"] = deepcopy(mc_byte_info)
    #             assembly_summary.append(byte_only_entry)

    #     else:
    #         assembly_only_entry = get_summary_entry_template()
    #         assembly_only_entry["has_assembly"] = True
    #         assembly_only_entry["assembly"]["info"] = deepcopy(asm_line_info)
    #         assembly_summary.append(assembly_only_entry)

    # return assembly_summary


def get_widest_column_values(assembly_summary_data):
    """
    Find widest values in the columns of the output.

    Required for the eventual printed table to line up correctly.

    Args:
        assembly_summary_data (list(dict)): List of dictionaries (as
            returned by :func:`~.get_assembly_summary_data`) with all the
            summary information data.
    Returns:
        dict: Mapping of columns for widest values.
    """

    widest_values = {
        "asm_line_no": 0,
        "asm_line": 0,
        "word_index_decimal": 0,
        "word_value_decimal": 0,
        "word_label": 0,
    }

    for entry in assembly_summary_data:
        if assembly := entry.get("assembly"):
            # Assembly line number width
            line_no_width = len(assembly["line_no"])
            if line_no_width > widest_values["asm_line_no"]:
                widest_values["asm_line_no"] = line_no_width

            # Assembly line width
            asm_line_width = len(assembly["raw"])
            if asm_line_width > widest_values["asm_line"]:
                widest_values["asm_line"] = asm_line_width

        if word := entry.get("word"):
            # Decimal word index width
            word_index_decimal_width = len(word["index_decimal"])
            if word_index_decimal_width > widest_values["word_index_decimal"]:
                widest_values["word_index_decimal"] = word_index_decimal_width

            # Decimal word value width
            word_value_decimal_width = len(word["value_decimal"])
            if word_value_decimal_width > widest_values["word_value_decimal"]:
                widest_values["word_value_decimal"] = word_value_decimal_width

            # Label width
            if label := word.get("label"):
                word_label_width = len(label)
                if word_label_width > widest_values["word_label"]:
                    widest_values["word_label"] = word_label_width

    return widest_values
