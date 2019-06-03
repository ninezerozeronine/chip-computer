.. _sw_assembler:

Assembler
=========

The :mod:`~eight_bit_computer.assembler` module is responsible for taking lines
of assembly code and processing it to generate equivalent machine code.

It is passed a list of strings which are the lines of the assembly file. Each
line is then processed and the information about the line stored in :func:`a
dictionary<.get_assembly_line_template>`.

During processing each line is checked to see if it's a constant definition, if
not, it's treated as an assembly line and
:func:`parsed into machine code bytes<.machine_code_bytes_from_line>`.

The line is passed to :func:`each operation<.get_all_operations>` to attempt to
generate the machine code bytes. The operations can expect certain tokens on the
line to be constants and are identified as such and returned to the assembler.
The constants are then :func:`validated and identified
<.validate_and_identify_constants>` and the machine code bytes added to the
dictionary of information about the line of assembly.

With all the lines processed, machine code bytes generated and constants
identified, the assembler :func:`checks for overall validity and structure
<.check_structure_validity>` The assembler then performs global operations that
need to take the entire assembly code into account:

- :func:`Assigning indexes to the machine code bytes<.assign_machine_code_byte_indexes>`
- :func:`Assigning labels to machine code bytes<.assign_labels>`
- :func:`Resolving labels to indexes in program memory<.resolve_labels>`
- :func:`Resolving number constants to bytes<.resolve_numbers>`
- :func:`Resolving variable constants to indexes in data memory<.resolve_variables>`
  
With these checks, assignments and resolutions complete, the final assembly
line dictionaries are returned.