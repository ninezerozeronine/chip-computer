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

ALU Arguments
-------------

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
