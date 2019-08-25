Machine Code
============

The computer is directly controlled by machine code. It is stored in program
memory. The machine code is stored as 8 bit bytes.

Machine code consists of instruction bytes and constant bytes. Instruction bytes
encode a particular instruction (e.g. copying the value in register A to
register B), constant bytes encode a value that an operation may require (e.g.
setting the A register to 42).

There are 256 possible instruction bytes, most of these are occupied by the
instruction set. They are organised using the grouping described below. This
is very much inspired by how :ref:`james_bates` organised his machine code.

See the `language table <../_static/language_table.html>`_ (or
:download:`download it <../_static/language_table.csv>`) for a complete listing
of all the machine code and operations with their arguments. The table is
sortable by clicking on the headers (but it's a little slow).

Instruction Groups
------------------

The first two bytes of an instruction byte always represent the instruction
group. There are 4 groups:

+--------------+------------+
| Bit value    | Group Name |
+==============+============+
| ``00......`` | Copy       |
+--------------+------------+
| ``01......`` | Load       |
+--------------+------------+
| ``10......`` | Store      |
+--------------+------------+
| ``11......`` | ALU        |
+--------------+------------+

Sources and destinations
------------------------

For copy, load and store instructions, the third to fifth, and sixth to eighth
bytes are the source and destination respectively.

The table below only shows the source codes for brevity. The destination bits
are the last 3 bits, e.g.: ``.....000`` and have the same name and meaning.

+--------------+-------+-----------------------------------------------------------------------------+
| Bit value    | Name  | Meaning                                                                     |
+==============+=======+=============================================================================+
| ``..000...`` | ACC   | The accumulator register.                                                   |
+--------------+-------+-----------------------------------------------------------------------------+
| ``..001...`` | A     | The A register.                                                             |
+--------------+-------+-----------------------------------------------------------------------------+
| ``..010...`` | B     | The B register.                                                             |
+--------------+-------+-----------------------------------------------------------------------------+
| ``..011...`` | C     | The C register.                                                             |
+--------------+-------+-----------------------------------------------------------------------------+
| ``..100...`` | SP    | The stack pointer.                                                          |
+--------------+-------+-----------------------------------------------------------------------------+
| ``..101...`` | PC    | The program counter                                                         |
+--------------+-------+-----------------------------------------------------------------------------+
| ``..110...`` | SP+/- | The stack pointer, preceded or followed by incrementing or decrementing it. |
+--------------+-------+-----------------------------------------------------------------------------+
| ``..111...`` | CONST | A constant value.                                                           |
+--------------+-------+-----------------------------------------------------------------------------+

ALU Operations
--------------

There are 16 ALU operations and they are identified with bits 3-6 of the
instruction byte when the operation group is ALU. The operations and codes are:

+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Bit value    | Name    | Meaning                                                                                                                                                                           |
+==============+=========+===================================================================================================================================================================================+
| ``110000..`` | ZERO    | The argument will be set to zero.                                                                                                                                                 |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``110001..`` | INCR    | The argument supplied will be incremented by 1.                                                                                                                                   |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``110010..`` | DECR    | The argument supplied will be decremented by 1.                                                                                                                                   |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``110011..`` | ADD     | The argument will be added to the accumulator.                                                                                                                                    |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``110100..`` | ADDC    | The argument will be added to the accumulator and one will be added if the last add resulted in a carry.                                                                          |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``110101..`` | SUB     | The argument will be subtracted from the accumulator.                                                                                                                             |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``110110..`` | SUBB    | The argument will be subtracted from the accumulator and one will be subtracted if the last subtraction resulted in a borrow.                                                     |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``110111..`` | AND     | The argument will be ANDed with the accumulator.                                                                                                                                  |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``111000..`` | NAND    | The argument will be NANDed with the accumulator.                                                                                                                                 |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``111001..`` | OR      | The argument will be ORed with the accumulator.                                                                                                                                   |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``111010..`` | NOR     | The argument will be NORed with the accumulator.                                                                                                                                  |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``111011..`` | XOR     | The argument will be XORed with the accumulator.                                                                                                                                  |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``111100..`` | NXOR    | The argument will be NXORed with the accumulator.                                                                                                                                 |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``111101..`` | NOT     | The argument will have all it's bits inverted                                                                                                                                     |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``111110..`` | LSHIFT  | All the bits in the argument will move one place to the left (toward the most significant bit)                                                                                    |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``111111..`` | LSHIFTC | All the bits in the argument will move one place to the left (toward the most significant bit). If the last shift resulted in a carry then the least significant bit is set to 1. |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

ALU Arguments
-------------

ALU operations work on an argument. This is specified with bits 7 and 8 of the
instruction byte when the operation group is ALU. The arguments and codes are:

+--------------+-----------+
| Bit value    | Argument  |
+==============+===========+
| ``11....00`` | ACC/CONST |
+--------------+-----------+
| ``11....01`` | A         |
+--------------+-----------+
| ``11....10`` | B         |
+--------------+-----------+
| ``11....11`` | C         |
+--------------+-----------+

Instruction byte gaps
---------------------

Not all source and destination combinations are valid or make sense. For
example, copying the value in Register A to Register A has no purpose. In these
cases, those instructions are re purposed for other instructions.

These "instruction byte gaps" are:

+---------------------+---------------------------------------------------------------------------------------+------------------+
| Instruction byte(s) | Explanation                                                                           | Used by          |
+=====================+=======================================================================================+==================+
| - ``00000000``      | Copying a register to itself.                                                         | JUMP_IF_XXX_FLAG |
| - ``00001001``      |                                                                                       |                  |
| - ``00010010``      |                                                                                       |                  |
| - ``00011011``      |                                                                                       |                  |
| - ``00100100``      |                                                                                       |                  |
| - ``00101101``      |                                                                                       |                  |
| - ``00110110``      |                                                                                       |                  |
| - ``00111111``      |                                                                                       |                  |
+---------------------+---------------------------------------------------------------------------------------+------------------+
| ``00110...``        | Copy from SP+/-. Ambiguous.                                                           | JUMP_IF_LT_ACC   |
+---------------------+---------------------------------------------------------------------------------------+------------------+
| ``00...110``        | Copy to SP+/-. Ambiguous.                                                             | JUMP_IF_LTE_ACC  |
+---------------------+---------------------------------------------------------------------------------------+------------------+
| ``00...111``        | Copy to a constant. Constants cannot be written to.                                   | JUMP_IF_EQ_ACC   |
+---------------------+---------------------------------------------------------------------------------------+------------------+
| ``01...100``        | Loading into SP. SP has a dedicated register, instead a load to a register then copy. | JUMP_IF_GTE_ACC  |
+---------------------+---------------------------------------------------------------------------------------+------------------+
| ``01...110``        | Loading into SP+/-. SP+/- cannot be written to.                                       | CALL             |
+---------------------+---------------------------------------------------------------------------------------+------------------+
| ``01...111``        | Loading into a constant. Constants cannot be written to.                              | PROGRAM_LOAD     |
+---------------------+---------------------------------------------------------------------------------------+------------------+
| ``10110...``        | Storing SP+/-. Ambiguous.                                                             | JUMP_IF_GT_ACC   |
+---------------------+---------------------------------------------------------------------------------------+------------------+
| ``10100...``        | Storing SP. SP has a dedicated register, instead copy to a register and store.        | JUMP_IF_EQ_ZERO  |
+---------------------+---------------------------------------------------------------------------------------+------------------+
| ``10111...``        | Storing a constant value. Instead Set a register and store.                           | PROGRAM_STORE    |
+---------------------+---------------------------------------------------------------------------------------+------------------+

Fetch
-----

To execute an instruction, the instruction byte must be loaded from program
memory into the instruction register.

This is handled by the first two steps of every instruction which:

- Load the program counter into the memory address register.
- Load the instruction register with the data from program memory at increment
  the program counter ready for the next instruction.