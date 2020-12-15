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
        output_filename_base=None, 
        output_dir=None, 
        output_format="logisim"
    ):
    """
    Read an assembly file and write out equivalent machine code.

    Args:
        input_filepath (str): The location of the assembly file.
        output_filename_base (str) (optional): The location to write out the
            machine code (without extension). If nothing is passed,
            the output path will be the input filename with the
            extension changed to mc.
        output_dir (str) (optional): The directory to write the
            assembled code into.
        output_format (str) (optional): How to format the output.
            ``logisim`` or ``arduino``.
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

    # Is output format correct
    output_formats = ["logisim", "arduino"]
    if output_format not in output_formats:
        formats_str = " ".join(["'{name}'".format(name=name) for name in output_formats])
        print "Output format must be one of: {output_formats}.".format(
            output_formats=formats_str
        )
        return

    # Generate output filename
    if output_filename_base is None:
        output_filename_base = os.path.splitext(os.path.basename(input_filepath))[0]

    # Generate output dir
    if output_dir is None:
        output_dir = "./"
    else:
        if not os.path.isdir(output_dir):
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

    if output_format == "logisim":
        write_bitstrings_to_logisim(assembly_line_infos, output_dir, output_filename_base)
    if output_format == "arduino":
        write_bitstrings_to_arduino(assembly_line_infos, output_dir, output_filename_base)

    print "\n\nAssembly summary:\n"
    print generate_assembly_summary(assembly_line_infos)


def write_bitstrings_to_logisim(assembly_line_infos, output_dir, output_filename_base):
    """
    Write machine code and variable bitstrings to logisim format.

    Args:
        assembly_line_infos (list(dict)): List of dictionaries of information
            about the parsed assembly.
        output_dir (str): The directory to write the assembled code into.
        output_filename_base (str): the basename (no extension) for the logisim
            file.
    """

    file_contents = export.gen_logisim_program_file(assembly_line_infos)
    file_name = output_filename_base + ".mc"
    file_path = os.path.join(output_dir, file_name)

    with open(file_path, "w") as file:
        file.write(file_contents)

    completion_msg = (
        "Assembly complete. Assembly file written to: {output_filepath}.".format(
            output_filepath=file_path
        )
    )
    print completion_msg


def write_bitstrings_to_arduino(assembly_line_infos, output_dir, output_filename_base):
    
    """
    Write machine code and variable bitstrings to arduino format.

    Args:
        assembly_line_infos (list(dict)): List of dictionaries of information
            about the parsed assembly.
        output_dir (str): The directory to write the assembled code into.
        output_filename_base (str): The filename (with no extension) for the file.
    """
    
    h_filename = "prog_{}.h".format(output_filename_base)
    cpp_filename = "prog_{}.cpp".format(output_filename_base)

    h_file_contents = export.gen_arduino_program_h_file(output_filename_base)
    cpp_file_contents = export.gen_arduino_program_cpp_file(assembly_line_infos, output_filename_base, h_filename)

    h_filepath = os.path.join(output_dir, h_filename)
    cpp_filepath = os.path.join(output_dir, cpp_filename)

    with open(h_filepath, "w") as h_file:
        h_file.write(h_file_contents)
    with open(cpp_filepath, "w") as cpp_file:
        cpp_file.write(cpp_file_contents)

    completion_msg = (
        "Assembly complete. Assembly files written to: {h_filepath} and ."
        "{cpp_filepath}".format(h_filepath=h_filepath, cpp_filepath=cpp_filepath)
        )
    print completion_msg


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


def get_mc_filename(asm_path):
    """
    Get the filename for the machine code.

    This is the assembly filename with .asm replaced with .mc

    Args:
        asm_path (str): Path to the assembly file.
    Returns:
        str: Path to the machine code file.
    """
    filename = os.path.basename(asm_path)
    return "{basename}.mc".format(basename=filename[:-4])


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