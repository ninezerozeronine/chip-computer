"""
Top level interface for the module
"""

import os

from .assembler import process_assembly_lines
from .assembly_summary import generate_assembly_summary
from .exceptions import AssemblyError
from .number_utils import number_to_bitstring
from . import export
from . import rom


def assemble(
        input_filepath,
        output_filepath=None
        ):
    """
    Read an assembly file and write out equivalent machine code.

    Args:
        input_filepath (str): The location of the assembly file.
        output_filepath (str) (optional): The location to write out the
            machine code. If nothing is passed, the output path will be
            the input path with the extension changed to mc.
    """

    # Does input file exist
    if not os.path.isfile(input_filepath):
        print "Input file: {input_filepath} does not exist.".format(
            input_filepath=input_filepath)
        return

    # Does input file have the correct extension
    if not input_filepath.endswith(".asm"):
        print "Input file must have a .asm extension."
        return

    # Validate/generate output filepath
    if output_filepath is None:
        output_filepath = get_mc_filepath(input_filepath)
    output_dir = os.path.dirname(output_filepath)
    if output_dir == "":
        output_filepath = "./{output_filepath}".format(
            output_filepath=output_filepath
        )
    elif not os.path.isdir(output_dir):
        print "Output directory: {output_dir} does not exist.".format(
            output_dir=output_dir
        )
        return

    # Do assembly
    lines = filepath_to_lines(input_filepath)
    try:
        assembly_line_infos = process_assembly_lines(lines)
    except AssemblyError as inst:
        print inst.args[0]
        return

    # Success message and summary
    completion_msg = (
        "Assembly complete. Assembly file written to: {output_filepath}."
        "\n\nAssembly summary:\n".format(output_filepath=output_filepath)
    )
    print completion_msg
    print generate_assembly_summary(assembly_line_infos)

    # Convert to correct format
    mc_byte_bitstrings = extract_machine_code(assembly_line_infos)
    variable_bitstrings = extract_variables(assembly_line_infos)
    combined_bitstrings = combine_mc_and_variable_bitstrings(mc_byte_bitstrings, variable_bitstrings)
    output = export.bitstrings_to_logisim(combined_bitstrings)

    # Write file.
    with open(output_filepath, "w") as file:
        file.write(output)


def filepath_to_lines(input_filepath):
    """
    Take a filepath and get all the lines of the file.

    The lines returned have the newline stripped.

    Args:
        input_filepath (str): Path to the file of disk to read.
    Returns:
        list(str): Lines of the file.
    """
    with open(input_filepath) as file:
        lines = file.read().splitlines()
    return lines


def get_mc_filepath(asm_path):
    """
    Get the filepath for the machine code.

    This is the assembly filepath with .asm replaced with .mc

    Args:
        asm_path (str): Path to the assembly file.
    Returns:
        str: Path to the machine code file.
    """

    return "{basepath}.mc".format(basepath=asm_path[:-4])


def extract_machine_code(assembly_lines):
    """
    Extract machine code from assembly line dictionaries.

    Args:
        assembly_lines (list(dict)): List of assembly line info
            dictionaries to extract machine code from. See
            :func:`~.get_assembly_line_template` for details on what
            those dictionaries contain.
    Returns:
        list(str): List of bit strings for the machine code.
    """
    machine_code = []
    for assembly_line in assembly_lines:
        if assembly_line["has_machine_code"]:
            for mc_byte in assembly_line["mc_bytes"]:
                machine_code.append(mc_byte["bitstring"])
    return machine_code


def extract_variables(assembly_lines):
    """
    Extract variables from assembly line dictionaries.

    Args:
        assembly_lines (list(dict)): List of assembly line info
            dictionaries to extract variables from. See
            :func:`~.get_assembly_line_template` for details on what
            those dictionaries contain.
    Returns:
        list(str): List of bit strings for the machine code. Empty
        list if there's no variables
    """

    # Extract all the variables and their positions
    pos_to_value_map = {}
    for assembly_line in assembly_lines:
        if assembly_line["defines_variable"]:
            bitstring = number_to_bitstring(assembly_line["defined_variable_value"])
            pos_to_value_map[assembly_line["defined_variable_location"]] = bitstring

    # Put the variables into a list, filling empty positions with zeroes.
    ret = []
    if pos_to_value_map:
        biggest = max(pos_to_value_map)
        for position in range(biggest + 1):
            if position in pos_to_value_map:
                ret.append(pos_to_value_map[position])
            else:
                ret.append(number_to_bitstring(0))

    return ret


def combine_mc_and_variable_bitstrings(mc_byte_bitstrings, variable_bitstrings):
    """
    Combine machine code and variables into a single appropriately padded list.

    Args:
        mc_byte_bitstrings (list(str)): List of bitstrings that make
            up the machine code.
        variable_bitstrings (list(str)): List of bitstrings that
            represent the variables.
    Returns:
        list(str): List of the machine code and variable bitstrings,
        padded to that the variables begin at byte 257.
    """
    
    if not variable_bitstrings:
        return mc_byte_bitstrings

    # Pad the machine code bytes up to 256 bytes
    num_mc_bytes = len(mc_byte_bitstrings)
    padded_mc_bytes = mc_byte_bitstrings + [number_to_bitstring(0)] * (256 - num_mc_bytes)

    return padded_mc_bytes + variable_bitstrings


def gen_roms(output_dir=".", file_prefix=None, output_format="logisim"):
    """
    Write files containing microcode for drive the roms.

    Args:
        output_dir (str) (optional): The directory to write the roms
            into.
        file_prefix (str) (optional): The prefix for the rom files.
        output_format (str) (optional): How to format the output.
            ``logisim`` or ``arduino``.
    """

    if not os.path.isdir(output_dir):
        print "Output directory: {output_dir} does not exist.".format(
            output_dir=output_dir
        )
        return

    if file_prefix is None:
        file_prefix = ""

    rom_data = rom.get_rom()
    rom_slices = rom.slice_rom(rom_data)
    for rom_index, rom_slice in rom_slices.iteritems():
        slice_bitstrings = [romdata.data for romdata in rom_slice]
        file_basename = "{file_prefix}mc_rom_{rom_index}".format(
            file_prefix=file_prefix, rom_index=rom_index
        )
        if output_format == "logisim":
            output = export.bitstrings_to_logisim(slice_bitstrings)
            filepath = os.path.join(output_dir, file_basename)
            with open(filepath, "w") as romfile:
                romfile.write(output)

        elif output_format == "arduino":
            rom_var_name = "MC_ROM_{rom_index}".format(rom_index=rom_index)
            export.write_arduino_pair(
                slice_bitstrings,
                output_dir,
                file_basename,
                rom_var_name,
                rom_index,
            )

    decimal_rom_index = len(rom_slices)
    decimal_rom = rom.get_decimal_rom()
    decimal_file_basename = "{file_prefix}decimal_rom".format(
        file_prefix=file_prefix,
    )
    decimal_bitstrings = [
        decimal_rom_entry.data for decimal_rom_entry in decimal_rom
    ]
    if output_format == "logisim":
        output = export.bitstrings_to_logisim(decimal_bitstrings)
        filepath = os.path.join(output_dir, decimal_file_basename)
        with open(filepath, "w") as decimal_rom_file:
            decimal_rom_file.write(output)

    elif output_format == "arduino":
        rom_var_name = "DECIMAL_ROM"
        export.write_arduino_pair(
            decimal_bitstrings,
            output_dir,
            decimal_file_basename,
            rom_var_name,
            decimal_rom_index,
        )

    msg = "ROM writing complete. ROMs written to {output_dir}".format(
        output_dir=output_dir
    )
    print msg