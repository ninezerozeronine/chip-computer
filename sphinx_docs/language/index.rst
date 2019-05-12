.. _language:

Language
========

The language of the computer is broadly defined with the following terms:

+--------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Name                     | Description                                                                                                                                                                                |
+==========================+============================================================================================================================================================================================+
| Assembly / Assembly code | Collective name for operations in sequence to form a program. The input to the assembler.                                                                                                  |
+--------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Operation                | A specific, simple step that the computer can perform. E.g. add that value in a given register to the accumulator, or copy a value in one register to another.                             |
+--------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Operation code / Op code | A unique code used to identify an operation, e.g. ``AND``, ``JUMP``, or ``ADD``.                                                                                                           |
+--------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Operation Argument       | A value passed to an operation to specify it's behaviour. E.g. passing ``B`` to the ``ADD`` operation to specify that the value in register B should be added to the accumulator register. |
+--------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Instruction              | A fully specified operation, e.g. a copy from B to C. or setting the A register to a value. Effectively a line of assembly.                                                                |
+--------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Instruction byte         | A byte that uniquely identifies an instruction.                                                                                                                                            |
+--------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Machine code             | Collective name for the bytes in program memory that form the instructions and constants of a program. The assembler generates machine code.                                               |
+--------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Machine code byte        | A byte that makes up machine code. Could be an instruction or a constant.                                                                                                                  |
+--------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Microcode                | The pattern of bits that determine the control signals to operate the computer to complete an instruction. The Control Unit contains microcode.                                            |
+--------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Microcode Step           | A single transfer of data via the bus or action of a module ocurring on a rising clock edge. The smallest, most specific level of control.                                                 |
+--------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

.. toctree::
   :maxdepth: 2
   :caption: Language Elements:

   assembly
   machine_code
   micro_code