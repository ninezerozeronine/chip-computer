"""
Export processed assembly to various fileformats.

Note that during this process negative numbers are converted to thier
unsigned equivalents.
"""

from . import number_utils
from .utils import chunker

def generate_arduino_header(progname):
    """

    Create arduino header file for the given assembly.

    The header file looks approximately like this:

    .. code-block:: none

        #ifndef PROG_PROGNAME_H
        #define PROG_PROGNAME_H

        #include "Arduino.h"

        extern const unsigned int num_progname_words;
        extern const unsigned int progname_addresses[];
        extern const unsigned int progname_words[];

        extern const char progname_program_name[];

        #endif
    
    Args:
        progname (str): The name of the program, used to refer to it in
            the header and cpp files.

    Returns:
        str: String ready to be written to a file.
    """

    h_lines = []
    h_lines.append("#ifndef PROG_{progname}_H".format(
        progname=progname.upper()
    ))
    h_lines.append("#define PROG_{progname}_H".format(
        progname=progname.upper()
    ))
    h_lines.append("")
    h_lines.append("#include <Arduino.h>")
    h_lines.append("")
    h_lines.append("extern const unsigned int num_{progname}_words;".format(
        progname=progname
    ))
    h_lines.append("extern const unsigned int {progname}_addresses[];".format(
        progname=progname
    ))
    h_lines.append("extern const unsigned int {progname}_words[];".format(
        progname=progname
    ))

    h_lines.append("")
    h_lines.append("extern const char {progname}_program_name[];".format(
        progname=progname
    ))
    h_lines.append("")
    h_lines.append("#endif")
    h_lines.append("")

    return "\n".join(h_lines)


def generate_arduino_cpp(assembly, progname, h_filename):
    """
    Generate cpp file for program for Arduino.

    The cpp file looks like this:

    .. code-block:: none

        #include "prog_progname.h"

        // Number of words in the program
        extern const unsigned int num_progname_words = 13;

        // Address of each word in the list of machinecode words
        extern const unsigned int progname_addresses[] PROGMEM = {
            0xFF00, // 0x003D - 0001 SET A #0xC
            0xFF01, // 0x000C - 0001 
            0xFF02, // 0x002F - 0002 SET B #1
            0x00A1, // 0x0001 - 0002 
            0x00A2, // 0x0000 - 0003 NOOP
            0x00A3  // 0xFFFF - 0004 HALT
        };

        // Value for each machinecode word
        extern const unsigned int progname_words[] PROGMEM = {
            0x003D, // 0xFF00 - 0001 SET A #0x000C
            0x000C, // 0xFF01 - 0001 
            0x002F, // 0xFF02 - 0002 SET B #1
            0x0001, // 0x00A1 - 0002 
            0x0000, // 0x00A2 - 0003 NOOP
            0xFFFF  // 0x00A3 - 0004 HALT
        };

        // Max of seven characters
        extern const char progname_program_name[] = "Prgname";

    The values of the machinecode words are converted to thier unsigned
    equivalents during this process.

    Args:
        assembly (list(AssemblyLine)): Assembly lines to generate the
            cpp file for.
        progname (str): Identifier for this program in the cpp code.
            Used for variable names in the code.
        h_filename (str): Name of the headerfile including extension.
    Returns:
        str: String ready to be written to a file.
    """

    address_lines, word_lines = get_address_and_word_lines(assembly)
    num_words = len(address_lines)

    cpp_lines = []
    cpp_lines.append("#include \"{h_filename}\"".format(h_filename=h_filename))
    cpp_lines.append("")


    cpp_lines.append("// Number of words in the program")
    cpp_lines.append(
        "extern const unsigned int num_{progname}_words "
        "= {num_words};".format(
            progname=progname, num_words=num_words
        )
    )
    cpp_lines.append("")


    cpp_lines.append(
        "// Address of each word in the list of machinecode words"
    )
    cpp_lines.append(
        "extern const unsigned int {progname}_addresses[] "
        "PROGMEM = {{".format(progname=progname)
    )
    for line in address_lines:
        cpp_lines.append(line)
    cpp_lines.append("};")
    cpp_lines.append("")


    cpp_lines.append("// Value for each machinecode word")
    cpp_lines.append(
        "extern const unsigned int {progname}_words[] "
        "PROGMEM = {{".format(progname=progname)
    )
    for line in word_lines:
        cpp_lines.append(line)
    cpp_lines.append("};")
    cpp_lines.append("")


    cpp_lines.append("// Max of seven characters")
    cpp_lines.append(
        "extern const char {progname}_program_name[] = \"DEFAULT\";".format(
        progname=progname,
    ))
    cpp_lines.append("")

    return "\n".join(cpp_lines)


def get_address_and_word_lines(assembly):
    """
    Generate the lines that actually specify address and word data.

    Taking the address defition as an example:

    .. code-block:: none

        // Address of each word in the list of machinecode words
        extern const unsigned int progname_addresses[] PROGMEM = {
            0xFF00, // 0x003D - 0001 SET A #0xC
            0xFF01, // 0x000C - 0001 
            0xFF02, // 0x002F - 0002 SET B #1
            0x00A1, // 0x0001 - 0002 
            0x00A2, // 0x0000 - 0003 NOOP
            0x00A3  // 0xFFFF - 0004 HALT
        };

    These would be the lines generated:

    .. code-block:: none

            0xFF00, // 0x003D - 0001 SET A #0xC
            0xFF01, // 0x000C - 0001 
            0xFF02, // 0x002F - 0002 SET B #1
            0x00A1, // 0x0001 - 0002 
            0x00A2, // 0x0000 - 0003 NOOP
            0x00A3  // 0xFFFF - 0004 HALT

    Args:
        assembly (list(AssemblyLine)): The assembly to get address and
            word lines for.

    Returns:
        tuple(list(str), list(str)): Lists of the address and word
        lines.
    """    
    address_lines = []
    word_lines = []

    for line in assembly:
        for index, word in enumerate(line.pattern.machinecode):
            # Add line if it's the first machincode word generated by
            # this line
            if index == 0:
                line_part = " {line}".format(line=line.raw_line)
            else:
                line_part = ""

            # Generate string for address
            address_line = (
                "    0x{address:04X}, // 0x{word:04X} - {line_no:04}"
                "{line_part}"
            )
            address_line = address_line.format(
                address=word.index,
                word=number_utils.get_positive_equivalent(
                    word.value, bitwidth=16
                ),
                line_no=line.line_no,
                line_part=line_part
            )
            address_lines.append(address_line)

            # Generate string for word
            word_line = (
                "    0x{word:04X}, // 0x{address:04X} - {line_no:04}"
                "{line_part}"
            )
            word_line = word_line.format(
                word=number_utils.get_positive_equivalent(
                    word.value, bitwidth=16
                ),
                address=word.index,
                line_no=line.line_no,
                line_part=line_part
            )
            word_lines.append(word_line)

    # Remove commas from last lines
    address_lines[-1] = address_lines[-1].replace(",", " ", 1)
    word_lines[-1] = word_lines[-1].replace(",", " ", 1)

    return address_lines, word_lines


def assembly_to_logisim(assembly, default_value=0):
    """
    Take assembly and convert to Logisim ram format

    Args:
        assembly (list(AssemblyLine)): The assembly to convert.
        default_value (int, optional): The value to use for addresses
            that are less than the maximum specified address but not
            specified.

    Returns:
        (str): String representing contects on the logisim file.
    """
    machinecode = assembly_lines_to_dictionary(assembly)
    highest = max(machinecode)
    words = []
    for index in range(highest + 1):
        value = machinecode.get(index, default_value)
        words.append(value)

    logisim_lines = ["v2.0 raw"]

    for line_words in chunker(words, 16):
        line_parts = []
        for line_chunk_words in chunker(line_words, 4):
            hex_strings = [
                "{value:04X}".format(value=word)
                for word
                in line_chunk_words
            ]
            four_words_chunk = " ".join(hex_strings)
            line_parts.append(four_words_chunk)
        line = "  ".join(line_parts)
        logisim_lines.append(line)

    logisim_string = "\n".join(logisim_lines)
    logisim_string += "\n"

    return logisim_string


def assembly_lines_to_dictionary(assembly_lines):
    """
    Convert the assembly lines to a dictionary of indexes and values.

    The keys in the dictionary are the indexes of the machinecode words
    to write, the values are the values of the machinecode words. The
    values are converted to the unsighed equivalent if the number is
    negative.

    Args:
        assembly_lines (List(AssemblyLine)): Fully processed assembly
            lines to convert to a raw dictionary.

    Returns:
        Dict(int,int)
    """

    assembly = {}
    for line in assembly_lines:
        for word in line.pattern.machinecode:
            assembly[word.index] = number_utils.get_positive_equivalent(
                word.value, bitwidth=16
            )
    return assembly


