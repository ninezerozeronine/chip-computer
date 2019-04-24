"""
Extract information from a list of assembly line info dictionaries.
"""

"""
15 0F 00001111 - @label1 01010101 55
16 10 00010000 -         11001001 C9
17 11 00010001 -         00101010 2A

18 12 00010010 -         01111011 7B <- #123
19 13 00010011 - @label2 01111100 7C
20 14 00010100 -         00001111 0F <- @label1
"""


def get_spaced_assembly_and_machine_code(asm_line_infos):
    """
    Get print friendly lists of the data in assembly line info dicts.

    Args:
        asm_line_infos (list(dict)): List of line info dictionaries as
            returned by :func:`~assembler.lines_to_machine_code`.
    Returns:
        (list, list)
    """

    spaced_assembly = []
    spaced_machine_code = []
    for asm_line_info in asm_line_infos:

        spaced_assembly_entry = gen_spaced_assembly_entry(asm_line_info)
        spaced_assembly.append(spaced_assembly_entry)

        if asm_line_info["machine_code_templates"]:

            for mc_byte_info in asm_line_info["machine_code_templates"][0]:
                spaced_mc_entry = gen_spaced_machine_code_entry(mc_byte_info)
                if asm_line_info["assigned_label"]:
                    spaced_mc_entry["has_label"] = True
                    spaced_mc_entry["label"] = asm_line_info["assigned_label"]
                spaced_machine_code.append(spaced_mc_entry)

            for mc_byte_info in asm_line_info["machine_code_templates"][1:]:
                empty_assembly = gen_empty_assembly_entry()
                spaced_assembly.append(empty_assembly)
                spaced_mc_entry = gen_spaced_machine_code_entry(mc_byte_info)
                spaced_machine_code.append(spaced_mc_entry)
        else:
            empty_machine_code = gen_empty_machine_code_entry()
            spaced_machine_code.append(empty_machine_code)

    return spaced_assembly, spaced_machine_code


def get_spaced_assembly_template():
    """

    """

    return {
        "has_content": False,
        "line_no": -1,
        "raw": "",
    }


def get_spaced_machine_code_template():
    """

    """
    return {
        "has_content": False,
        "prog_mem_index": -1,
        "is_constant": False,
        "constant": "",
        "has_label": False,
        "label": "",
        "bitstring": "",
    }


def gen_empty_assembly_entry():
    """

    """
    entry = get_spaced_assembly_template()
    entry["has_content"] = False
    return entry


def gen_empty_machine_code_entry():
    """

    """
    entry = get_spaced_machine_code_template()
    entry["has_content"] = False
    return entry


def gen_spaced_assembly_entry(asm_line_info):
    """

    """

    entry = get_spaced_assembly_template()
    entry["has_content"] = True
    entry["line_no"] = asm_line_info["line_no"]
    entry["raw"] = asm_line_info["raw"]
    return entry


def gen_spaced_machine_code_entry(mc_byte_info):
    """

    """

    entry = get_spaced_machine_code_template()
    entry["has_content"] = True
    entry["prog_mem_index"] = mc_byte_info["index"]
    entry["bitstring"] = mc_byte_info["machine_code"]
    if mc_byte_info["byte_type"] == "constant":
        entry["is_constant"] = True
        entry["constant"] = mc_byte_info["constant"]
    return entry
