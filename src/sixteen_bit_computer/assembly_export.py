def assembly_to_arduino():
    generate_arduino_header()
    generate_arduino_cpp()

def generate_arduino_header(progname):
    """

    Create arduino header file for the given assembly.

    The header file looks approximately like this::

        #ifndef PROG_PROGNAME_H
        #define PROG_PROGNAME_H

        #include "Arduino.h"

        extern const unsigned int num_progname_words;
        extern const unsigned int progname_addresses[];
        extern const unsigned int progname_words[];

        extern const char fibonacci_program_name[];

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
    h_lines.append("extern const unsigned int {progname}_words;".format(
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

    The cpp file looks like this::

        #include "prog_fibonacci.h"

        extern const byte num_fibonacci_program_bytes = 13;
        extern const byte fibonacci_program_bytes[] PROGMEM = {
            0x39, // 000 SET A #1 (@set_initial)
            0x01, // 001 (1)
            0x3A, // 002 SET B #1
            0x01, // 003 (1)
            0x08, // 004 COPY A ACC (@fib_loop)
            0xCE, // 005 ADD B
            0x24, // 006 JUMP_IF_OVERFLOW_FLAG @set_initial
            0x00, // 007 (0)
            0x03, // 008 COPY ACC C (to display)
            0x11, // 009 COPY B A
            0x02, // 010 COPY ACC B
            0x3D, // 011 JUMP @fib_loop
            0x04  // 012 (4)
        };

        extern const byte num_fibonacci_data_bytes = 0;

        // Needs to be at least 1 byte in this array
        extern const byte fibonacci_data_bytes[] PROGMEM = {
            0x00 // Placeholder.
        };

        // Max of seven characters
        extern const char fibonacci_program_name[] = "Fbnacci";
    """
    pass


def assembly_to_logisim():
    pass