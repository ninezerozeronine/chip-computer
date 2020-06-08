"""
Functionality to convert data other package friendly formats.
"""

import os

from . import number_utils


def bitstrings_to_arduino_cpp(
        bitstrings, rom_index, header_filename, rom_var_name
    ):
    """
    Convert rom bitstrings to arduino header cpp file.

    The format of the file is::

        #include "mc_rom_0.h"

        extern const byte MC_ROM_0[] __attribute__ (( __section__(".fini1") )) = {
            0x00, 0x01, 0x02, 0x03,  0x04, 0x05, 0x06, 0x07,  0x08, 0x09, 0x0A, 0x0B,  0x0C, 0x0D, 0x0E, 0x0F, // 00000
            0x10, 0x11, 0x12, 0x13,  0x14, 0x15, 0x16, 0x17,  0x18, 0x19, 0x1A, 0x1B,  0x1C, 0x1D, 0x1E, 0x1F, // 00016
            ...
            ...
            0xE0, 0xE1, 0xE2, 0xE3,  0xE4, 0xE5, 0xE6, 0xE7,  0xE8, 0xE9, 0xEA, 0xEB,  0xEC, 0xED, 0xEE, 0xEF, // 32736
            0xF0, 0xF1, 0xF2, 0xF3,  0xF4, 0xF5, 0xF6, 0xF7,  0xF8, 0xF9, 0xFA, 0xFB,  0xFC, 0xFD, 0xFE        // 32752
        };
        extern const byte MC_ROM_0_LAST_BYTE = 0xFF;

    Where the rom index +1 is used for the index of the fini part.

    Args:
        bitstrings (list(str)): This of bitstrings that make up the rom.
        rom_index (int): Index of the rom beind written (index in the
            list of all the roms being written to the arduino).
        header_filename (str): Name of the header file, e.g.
            "mc_rom_0.h".
        rom_var_name(str): The variable name used for the rom data in
            the arduino code.
    Returns:
        str: String ready to be written to cpp file
    """
    cpp_lines = []
    cpp_lines.append("#include \"{header_filename}\"".format(
        header_filename=header_filename
    ))
    cpp_lines.append("")
    cpp_lines.append(
        "extern const byte {rom_var_name}[] __attribute__ (( __section__(\".fini{fini_index}\") )) = {{".format(
            rom_var_name=rom_var_name, fini_index=rom_index + 1
        )
    )
    data_lines = []
    for line_index, line_bytes in enumerate(chunker(bitstrings[:-1], 16)):
        line_parts = []
        for line_chunk in chunker(line_bytes, 4):
            chunk_bytes = [
                "0x{hex}".format(hex=number_utils.bitstring_to_hex_string(
                    chunk_byte
                ))
                for chunk_byte
                in line_chunk
            ]
            four_hex_bytes = ", ".join(chunk_bytes)
            line_parts.append(four_hex_bytes)
        data_line = ",  ".join(line_parts)

        # Add extra spacing if it's the last row
        if len(line_bytes) == 16:
            data_line = "    {data_line}, // {byte_index:05}".format(
                data_line=data_line, byte_index=line_index*16)
        else:
            data_line = "    {data_line}        // {byte_index:05}".format(
                data_line=data_line, byte_index=line_index*16)

        data_lines.append(data_line)
    cpp_lines.extend(data_lines)
    cpp_lines.append("};")
    cpp_lines.append(
        "extern const byte {rom_var_name}_LAST_BYTE = 0x{byte};".format(
            rom_var_name=rom_var_name,
            byte=number_utils.bitstring_to_hex_string(bitstrings[-1])
        )
    )
    cpp_string = "\n".join(cpp_lines)
    cpp_string += "\n"
    return cpp_string


def create_arduino_header(header_file_basename, rom_var_name):
    """
    Create arduino header file

    The header file looks like this::

        #ifndef MC_ROM_0_H
        #define MC_ROM_0_H

        #include <Arduino.h>

        extern const byte MC_ROM_0[];
        extern const byte MC_ROM_0_LAST_BYTE;

        #endif

    Args:
        header_file_basename (str): The basename of the header file.
            E.g. if the header file is named mc_rom_0.h, the basename is
            mc_rom_0.
        rom_var_name(str): The variable name used for the rom data in
            the arduino code.
    Returns:
        str: String ready to be written to a file.
    """

    h_lines = []
    h_lines.append("#ifndef {header_file_basename}_H".format(
        header_file_basename=header_file_basename.upper()
    ))
    h_lines.append("#define {header_file_basename}_H".format(
        header_file_basename=header_file_basename.upper()
    ))
    h_lines.append("")
    h_lines.append("#include <Arduino.h>")
    h_lines.append("")
    h_lines.append("extern const byte {rom_var_name}[];".format(
        rom_var_name=rom_var_name
    ))
    h_lines.append(
        "extern const byte {rom_var_name}_LAST_BYTE;".format(
            rom_var_name=rom_var_name
        )
    )
    h_lines.append("")
    h_lines.append("#endif")
    h_lines.append("")
    return "\n".join(h_lines)


def chunker(seq, chunk_size):
    """
    Take a larger sequence and split it into smaller chunks.

    E.g.::

        chunker([0,1,2,3,4,5], 4) -> [0,1,2,3], [4,5]

    Args:
        seq (list): List of things to chunk up
        chunk_size (int): How big each chunk should be.
    Returns:
        generator: Generator that yields each chunk.
    """
    return (
        seq[pos:pos + chunk_size] for pos in xrange(0, len(seq), chunk_size)
    )


def write_arduino_pair(
        bitstrings, output_dir, file_basename, rom_var_name, rom_index
    ):
    """
    Write the header and cpp files for the arduino roms.

    Args:
        bitstrings (list(str)): List of bitstrings that will make up the
            rom.
        output_dir (str): Directory (relative or absolute) to output the
            pair of files into.
        file_basename (str): Basename of the h and cpp files. The
            basename is the part of the file without the extention or
            the period.
        rom_var_name(str): The variable name used for the rom data in
            the arduino code.
        rom_index (int): Index of the rom to be written. This index is
            the index in the sequence of all roms to be written to the
            arduino.
    """

    # Write h
    h_output = create_arduino_header(file_basename, rom_var_name)
    h_filename = "{file_basename}.h".format(file_basename=file_basename)
    h_filepath = os.path.join(output_dir, h_filename)
    with open(h_filepath, "w") as h_file:
        h_file.write(h_output)

    # Write cpp
    cpp_output = bitstrings_to_arduino_cpp(
        bitstrings, rom_index, h_filename, rom_var_name
    )
    cpp_filename = "{file_basename}.cpp".format(file_basename=file_basename)
    cpp_filepath = os.path.join(output_dir, cpp_filename)
    with open(cpp_filepath, "w") as cpp_file:
        cpp_file.write(cpp_output)


def gen_logisim_program_file(mc_byte_bitstrings, variable_bitstrings):
    """
    Generate contents for logisim files holding a program.

    Args:
        assembly_line_infos (list(dict)): List of dictionaries of information
            about the parsed assembly.
    Returns:
        str: Content of the logisim file.
    """

    mc_byte_bitstrings = extract_machine_code(assembly_line_infos)
    variable_bitstrings = extract_variables(assembly_line_infos)
    combined_bitstrings = combine_mc_and_variable_bitstrings(
        mc_byte_bitstrings, variable_bitstrings
    )
    return bitstrings_to_logisim(combined_bitstrings)


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


def bitstrings_to_logisim(bitstrings):
    """
    Convert bitstrigs to a logisim RAM/ROM file format.

    Used to convert ROMs and machine code.

    Args:
        bitstrings (list(str)): List of bitstrings to convert to a
            logisim friendly format.
    Returns:
        str: String ready to be written to a file.

    """
    logisim_lines = ["v2.0 raw"]
    for line_bytes in chunker(bitstrings, 16):
        line_parts = []
        for line_chunk_bytes in chunker(line_bytes, 4):
            hex_strings = [
                number_utils.bitstring_to_hex_string(bit_string)
                for bit_string
                in line_chunk_bytes
            ]
            four_hex_bytes = " ".join(hex_strings)
            line_parts.append(four_hex_bytes)
        line = "  ".join(line_parts)
        logisim_lines.append(line)
    logisim_string = "\n".join(logisim_lines)
    logisim_string += "\n"
    return logisim_string


def gen_arduino_program_h_file(assembly_line_infos, h_basename):
    """
    Generate header file for program for Arduino.

    The header file looks like this::

        #ifndef PROG_FIBONACCI_H
        #define PROG_FIBONACCI_H

        #include "Arduino.h"

        extern const byte num_fibonacci_program_bytes;
        extern const byte fibonacci_program_bytes[];

        extern const byte num_fibonacci_data_bytes;
        extern const byte fibonacci_data_bytes[];

        extern const char fibonacci_program_name[];

        #endif

    Args:
        assembly_line_infos (list(dict)): List of assembly line info
            dictionaries to extract variables from. See
            :func:`~.get_assembly_line_template` for details on what
            those dictionaries contain.
        h_basename (str): The filename (with no extension) for the file.

    Returns:
        str: String ready to be written to a file.
    """

    h_lines = []
    h_lines.append("#ifndef PROG_{h_basename}_H".format(
        h_basename=h_basename.upper()
    ))
    h_lines.append("#define {h_basename}_H".format(
        h_basename=h_basename.upper()
    ))
    h_lines.append("")
    h_lines.append("#include <Arduino.h>")
    h_lines.append("")
    h_lines.append("extern const byte num_{h_basename}_program_bytes;".format(
        h_basename=h_basename
    ))
    h_lines.append("extern const byte {h_basename}_program_bytes[];".format(
        h_basename=h_basename
    ))
    h_lines.append("")
    h_lines.append("extern const byte num_{h_basename}_data_bytes;".format(
        h_basename=h_basename
    ))
    h_lines.append("extern const byte {h_basename}_data_bytes[];".format(
        h_basename=h_basename
    ))
    h_lines.append("")
    h_lines.append("extern const char {h_basename}_program_name[];".format(
        h_basename=h_basename
    ))
    h_lines.append("")
    h_lines.append("#endif")
    h_lines.append("")

    return "\n".join(h_lines)


def gen_arduino_program_cpp_file(assembly_line_infos, filename_base, h_filename):
    """
    Generate cpp file for program for Arduino.

    The cpp file looks like this::

        #include "prog_fibonacci.h"

        extern const byte num_fibonacci_program_bytes = 13;
        extern const byte fibonacci_program_bytes[] PROGMEM = {
            0x39, // SET A #1 (@set_initial)
            0x01, // (1)
            0x3A, // SET B #1
            0x01, // (1)
            0x08, // COPY A ACC (@fib_loop)
            0xCE, // ADD B
            0x24, // JUMP_IF_OVERFLOW_FLAG @set_initial
            0x00, // (0)
            0x03, // COPY ACC C (to display)
            0x11, // COPY B A
            0x02, // COPY ACC B
            0x3D, // JUMP @fib_loop
            0x04  // (4)
        };

        extern const byte num_fibonacci_data_bytes = 0;

        // Needs to be at least 1 byte in this array
        extern const byte fibonacci_data_bytes[] PROGMEM = {
            0x00 // Placeholder.
        };

        // Max of seven characters
        extern const char fibonacci_program_name[] = "Fbnacci";

    Args:
        assembly_line_infos (list(dict)): List of assembly line info
            dictionaries to extract variables from. See
            :func:`~.get_assembly_line_template` for details on what
            those dictionaries contain.
        filename_base (str): The basename (no extension) for the file.
            Also used as a general identifier.
        h_filename (str): The filename of the headerfile (including extension).

    Returns:
        str: String ready to be written to a file.
    """

    machinecode_info = extract_program_file_machinecode_info(assembly_line_infos)
    num_prog_bytes = len(machinecode_info)

    cpp_lines = []
    cpp_lines.append("#include \"{h_filename}\"".format(h_filename=h_filename))
    cpp_lines.append("")

    cpp_lines.append(
        "extern const byte num_{filename_base}_program_bytes "
        "= {num_prog_bytes};".format(
            filename_base=filename_base, num_prog_bytes=num_prog_bytes
        )
    )
    cpp_lines.append(
        "extern const byte {filename_base}_program_bytes[] "
        "PROGMEM = {".format(filename_base=filename_base)
    )

    # Generate machine code bytes
    for byte_index, byte_info in enumerate(machinecode_info):
        line = "    0x{hex_byte}".format(
            number_utils.bitstring_to_hex_string(byte_info["bitstring"])
        )
        if byte_index != (num_prog_bytes - 1):
            line += ', '
        else:
            line += '  '
        line += byte_info["comment"]
        cpp_lines.append(line)
    cpp_lines.append("};")

    databyte_info = extract_program_file_databyte_info(assembly_line_infos)
    num_data_bytes = len(databyte_info)

    cpp_lines.append(
        "extern const byte num_{filename_base}_data_bytes "
        "= {num_data_bytes};".format(
            filename_base=filename_base, num_data_bytes=num_data_bytes
        )
    )
    cpp_lines.append("")
    cpp_lines.append("// Needs to be at least 1 byte in this array")
    cpp_lines.append(
        "extern const byte {filename_base}_data_bytes[] PROGMEM = {".format(
            filename_base=filename_base)
        )

    # Generate data (variable) bytes
    if num_data_bytes == 0:
        cpp_lines.append("    0x00 // Placeholder.")
    else:
        
    cpp_lines.append("};")


def extract_program_file_machinecode_info(assembly_line_infos):
    """
    Get necessary machine code info for arduino cpp file.

    Args:
        assembly_line_infos (list(dict)): List of assembly line info
            dictionaries to extract variables from. See
            :func:`~.get_assembly_line_template` for details on what
            those dictionaries contain.
    Returns:
        list(dict(str:str)): Bitstring and relevant comment for each
        machinecode byte.
    """

    mc_byte_infos = []
    byte_index = 0
    for assembly_line in assembly_lines:
        if assembly_line["has_machine_code"]:
            for mc_byte in assembly_line["mc_bytes"]:
                byte_data = {}
                byte_data["bitstring"] = mc_byte["bitstring"]
                comment = "// {byte_index:03d}".format(byte_index=byte_index)

                if mc_byte["byte_type"] == "instruction":
                    comment = "{comment} {raw_line}".format(
                        raw_line=assembly_line["raw"]
                    )
                    if assembly_line["has_label_assigned"]:
                        comment = "{comment} ({label})".format(
                            assembly_line["assigned_label"]
                        )

                elif mc_byte["byte_type"] == "constant":
                    comment = "{comment} ({constant})".format(
                        constant=number_utils.bitstring_to_number(mc_byte["bitstring"])
                    )
                    pass

                byte_data["comment"] = comment
                mc_byte_infos.append(byte_data)
                byte_index += 1

    return mc_byte_infos


def extract_program_file_variable_info(assembly_line_infos):
    """

    """
    pass