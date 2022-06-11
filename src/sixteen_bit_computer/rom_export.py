from . import number_utils
from .utils import chunker


def generate_arduino_cpp(
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


def generate_arduino_header(header_file_basename, rom_var_name):
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


def generate_logisim(bitstrings):
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
