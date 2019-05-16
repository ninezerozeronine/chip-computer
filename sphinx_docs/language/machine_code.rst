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

See the full :download:`language table <language_table.html>` for a complete
listing of all the machine code and operations and their arguments. The table is
sortable by clicking on the headers (but it's a little slow).

Instruction Groups
------------------

The first two bytes of an instruction byte always represent the instruction
group. There are 4 groups:

+--------------+------------+
| Bit value    | Group Name |
+==============+============+
| ``00xxxxxx`` | Copy       |
+--------------+------------+
| ``01xxxxxx`` | Load       |
+--------------+------------+
| ``10xxxxxx`` | Store      |
+--------------+------------+
| ``11xxxxxx`` | ALU        |
+--------------+------------+

Sources and destinations
------------------------

For copy, load and store instructions, the third to fifth, and sixth to eighth
bytes are the source and destination respectively.

The table below only shows the source codes for brevity. The destination bits
are the last 3 bits, e.g.: ``xxxxx000`` and have the same name and meaning.

+--------------+-------+-----------------------------------------------------------------------------+
| Bit value    | Name  | Meaning                                                                     |
+==============+=======+=============================================================================+
| ``xx000xxx`` | ACC   | The accumulator register.                                                   |
+--------------+-------+-----------------------------------------------------------------------------+
| ``xx001xxx`` | A     | The A register.                                                             |
+--------------+-------+-----------------------------------------------------------------------------+
| ``xx010xxx`` | B     | The B register.                                                             |
+--------------+-------+-----------------------------------------------------------------------------+
| ``xx011xxx`` | C     | The C register.                                                             |
+--------------+-------+-----------------------------------------------------------------------------+
| ``xx100xxx`` | SP    | The stack pointer.                                                          |
+--------------+-------+-----------------------------------------------------------------------------+
| ``xx101xxx`` | PC    | The program counter                                                         |
+--------------+-------+-----------------------------------------------------------------------------+
| ``xx110xxx`` | SP+/- | The stack pointer, preceded or followed by incrementing or decrementing it. |
+--------------+-------+-----------------------------------------------------------------------------+
| ``xx111xxx`` | CONST | A constant value.                                                           |
+--------------+-------+-----------------------------------------------------------------------------+

ALU Operations
--------------

There are 16 ALU operations and they are identified with bits 3-6 of the
instruction byte when the operation group is ALU. The operations and codes are:

+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Bit value    | Name    | Meaning                                                                                                                                                                           |
+==============+=========+===================================================================================================================================================================================+
| ``110000xx`` | ZERO    | The ALU will output zero.                                                                                                                                                         |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``110001xx`` | INCR    | The argument supplied will be incremented by 1.                                                                                                                                   |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``110010xx`` | DECR    | The argument supplied will be decremented by 1.                                                                                                                                   |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``110011xx`` | ADD     | The argument will be added to the accumulator.                                                                                                                                    |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``110100xx`` | ADDC    | The argument will be added to the accumulator and one will be added if the last add resulted in a carry.                                                                          |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``110101xx`` | SUB     | The argument will be subtracted from the accumulator.                                                                                                                             |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``110110xx`` | SUBB    | The argument will be subtracted from the accumulator and one will be subtracted if the last subtraction resulted in a borrow.                                                     |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``110111xx`` | AND     | The argument will be ANDed with the accumulator.                                                                                                                                  |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``111000xx`` | NAND    | The argument will be NANDed with the accumulator.                                                                                                                                 |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``111001xx`` | OR      | The argument will be ORed with the accumulator.                                                                                                                                   |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``111010xx`` | NOR     | The argument will be NORed with the accumulator.                                                                                                                                  |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``111011xx`` | XOR     | The argument will be XORed with the accumulator.                                                                                                                                  |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``111100xx`` | NXOR    | The argument will be NXORed with the accumulator.                                                                                                                                 |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``111101xx`` | NOT     | The argument will have all it's bits inverted                                                                                                                                     |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``111110xx`` | LSHIFT  | All the bits in the argument will move one place to the left (toward the most significant bit)                                                                                    |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``111111xx`` | LSHIFTC | All the bits in the argument will move one place to the left (toward the most significant bit). If the last shift resulted in a carry then the least significant bit is set to 1. |
+--------------+---------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

ALU Arguments
-------------

ALU operations work on an argument. This is specified with bits 7 and 8 of the
instruction byte when the operation group is ALU. The arguments and codes are:

+--------------+----------+
| Bit value    | Argument |
+==============+==========+
| ``11xxxx00`` | ACC      |
+--------------+----------+
| ``11xxxx01`` | A        |
+--------------+----------+
| ``11xxxx10`` | B        |
+--------------+----------+
| ``11xxxx11`` | C        |
+--------------+----------+

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
| ``00110XXX``        | Copy from SP+/-. Ambiguous.                                                           | JUMP_IF_LT_ACC   |
+---------------------+---------------------------------------------------------------------------------------+------------------+
| ``00XXX110``        | Copy to SP+/-. Ambiguous.                                                             | JUMP_IF_LTE_ACC  |
+---------------------+---------------------------------------------------------------------------------------+------------------+
| ``00XXX111``        | Copy to a constant. Constants cannot be written to.                                   | JUMP_IF_EQ_ACC   |
+---------------------+---------------------------------------------------------------------------------------+------------------+
| ``01XXX100``        | Loading into SP. SP has a dedicated register, instead a load to a register then copy. | JUMP_IF_GTE_ACC  |
+---------------------+---------------------------------------------------------------------------------------+------------------+
| ``01XXX110``        | Loading into SP+/-. SP+/- cannot be written to.                                       | CALL             |
+---------------------+---------------------------------------------------------------------------------------+------------------+
| ``01XXX111``        | Loading into a constant. Constants cannot be written to.                              | PROGRAM_LOAD     |
+---------------------+---------------------------------------------------------------------------------------+------------------+
| ``10110XXX``        | Storing SP+/-. Ambiguous.                                                             | JUMP_IF_GT_ACC   |
+---------------------+---------------------------------------------------------------------------------------+------------------+
| ``10100XXX``        | Storing SP. SP has a dedicated register, instead copy to a register and store.        | JUMP_IF_EQ_ZERO  |
+---------------------+---------------------------------------------------------------------------------------+------------------+
| ``10111XXX``        | Storing a constant value. Instead Set a register and store.                           | PROGRAM_STORE    |
+---------------------+---------------------------------------------------------------------------------------+------------------+
