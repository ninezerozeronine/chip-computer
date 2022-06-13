"""
Generate a summary of the assembly lines and machine code.
"""

from . import number_utils
from . import assembler


def generate_assembly_summary(assembly_lines):
    """
    Produce a summary that combines assembly and machine code.

    For the following assembly:

    .. code-block:: none

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

    The summary will be as follows (The values for the instruction
    words may differ):

    .. code-block:: none

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

    In an example line:

    .. code-block:: none

        11     NOOP      | 20 0x0014 - &label   0 0x0000 !alias

    The elements are:

     - ``11`` - The line of the assembly file.
     - ``NOOP`` - The assembly line.
     - ``|`` - Assembly/machinecode seperator.
     - ``20`` - Machinecode word index in decimal.
     - ``0x0014`` - Machinecode word index in hex.
     - ``-`` - Index and value seperator.
     - ``&label`` - A label (if any) assigned to this machinecode index.
     - ``0`` - Machinecode word value in decimal.
     - ``0x0000`` - Machinecode word value in hex.
     - ``!alias`` - The constant used to define this word (if any).

    Args:
        assembly_lines (list(AssemblyLine)): List of Assembly line
            ojbects representing the parsed assembly.
    Returns:
        str: Printable summary.
    """
    label_map = assembler.build_label_map(assembly_lines)
    summary_data = get_assembly_summary_data(assembly_lines, label_map)
    lines = generate_assembly_summary_lines(summary_data)
    return "\n".join(lines)


def get_assembly_summary_data(assembly_lines, label_map):
    """
    Process assembly data to make formatting easier for the summary.

    Generate a list of dictionaries of the form:

    .. code-block:: none

        {
            "assembly" : {
                "raw": "NOOP",
                "line_no": "23",
            },
            "word" : {
                "index_decimal": "13",
                "index_hex": "0x000D",
                "label": "&my_label",
                "value_decimal": "0",
                "value_hex": "0x0000",
                "const": "!alias"
            }
        }

    Note that the values of the keys are only representative examples.
    Not all keys will necessarily be present.


    Args:
        assembly_lines (list(AssemblyLine)): List of Assembly line
            ojbects representing the parsed assembly.
        label_map (dict()): Label map as returned from
            :func:`~sixteen_bit_computer.assembler.build_label_map`.
    Returns:
        list(dict): Relevant data pulled from the assembly lines to
        build the summary with.
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
        summary_data (list(dict)): As returned by
            :func:`~.get_assembly_summary_data`.
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


def get_widest_column_values(assembly_summary_data):
    """
    Find widest values in the columns of the output.

    Required for the eventual printed table to line up correctly.

    Args:
        assembly_summary_data (list(dict)): List of dictionaries (as
            returned by :func:`~.get_assembly_summary_data`) with all the
            summary information data.
    Returns:
        dict(): Mapping of string columns to int widest values.
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
