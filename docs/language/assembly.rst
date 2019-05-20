Assembly
========

Assembly code provides a way to specify instructions for the computer to
perform in a more human readable from than machine code

Assembly operations and arguments to specify thier behaviour can be saved in an
assembly file and passed to an assembler to convert them to machine code that
the computer can then execute.

These are the operations and other assembly constructs that can be used to
create a valid assembly file.

Arithmetic Operations
---------------------

ADD
^^^

ADDC
^^^^

SUB
^^^

SUBB
^^^^

LSHIFT
^^^^^^

LSHIFTC
^^^^^^^

INCR
^^^^

DECR
^^^^

Data Operations
---------------

COPY
^^^^

The ``COPY`` operation copies the value from a source module to a destination
module. This overwrites the current value of the destination register. It
requires a single machine code byte in program memory.

It is used by specifying the source module as the first argument and the
destination module as the second.

The possible usages are:

 - ``COPY ACC A``
 - ``COPY ACC B``
 - ``COPY ACC C``
 - ``COPY ACC SP``
 - ``COPY A ACC``
 - ``COPY A B``
 - ``COPY A C``
 - ``COPY A SP``
 - ``COPY B ACC``
 - ``COPY B A``
 - ``COPY B C``
 - ``COPY B SP``
 - ``COPY C ACC``
 - ``COPY C A``
 - ``COPY C B``
 - ``COPY C SP``
 - ``COPY PC ACC``
 - ``COPY PC A``
 - ``COPY PC B``
 - ``COPY PC C``
 - ``COPY PC SP``
 - ``COPY SP ACC``
 - ``COPY SP A``
 - ``COPY SP B``
 - ``COPY SP C``

LOAD
^^^^

The ``LOAD`` operation loads a value from data memory into a module.

It is used by specifying the position in memory as the first argument and the
destination module as the second. The position in memory can be a module or a
constant and is encased in square parentheses.

The possible usages are:

 - ``LOAD [ACC] ACC``
 - ``LOAD [ACC] A``
 - ``LOAD [ACC] B``
 - ``LOAD [ACC] C``
 - ``LOAD [A] ACC``
 - ``LOAD [A] A``
 - ``LOAD [A] B``
 - ``LOAD [A] C``
 - ``LOAD [B] ACC``
 - ``LOAD [B] A``
 - ``LOAD [B] B``
 - ``LOAD [B] C``
 - ``LOAD [C] ACC``
 - ``LOAD [C] A``
 - ``LOAD [C] B``
 - ``LOAD [C] C``
 - ``LOAD [PC] ACC``
 - ``LOAD [PC] A``
 - ``LOAD [PC] B``
 - ``LOAD [PC] C``
 - ``LOAD [SP] ACC``
 - ``LOAD [SP] A``
 - ``LOAD [SP] B``
 - ``LOAD [SP] C``
 - ``LOAD [CONST] ACC``
 - ``LOAD [CONST] A``
 - ``LOAD [CONST] B``
 - ``LOAD [CONST] C``


STORE
^^^^^

PROGLOAD
^^^^^^^^

PROGSTORE
^^^^^^^^^

PUSH
^^^^

POP
^^^

SET
^^^

The ``SET`` operation will set a module in the computer to a given
constant value.

It is used by specifying a module as the first argument, then the value to set
it to as a constant.

It requires two machine code bytes in program memory. Consider the
:ref:`setzero` operation if the constant is zero.

The possible usages are:

 - ``SET ACC CONST``
 - ``SET A CONST``
 - ``SET B CONST``
 - ``SET C CONST``
 - ``SET SP CONST``


.. _setzero:

SETZERO
^^^^^^^

Program Control Operations
--------------------------

NOOP
^^^^

JUMP
^^^^

JUMP_IF_LT_ACC
^^^^^^^^^^^^^^

JUMP_IF_LTE_ACC
^^^^^^^^^^^^^^^

JUMP_IF_EQ_ACC
^^^^^^^^^^^^^^

JUMP_IF_GTEQ_ACC
^^^^^^^^^^^^^^^^

JUMP_IF_GT_ACC
^^^^^^^^^^^^^^

JUMP_IF_EQ_ZERO
^^^^^^^^^^^^^^^

JUMP_IF_POSITIVE_FLAG
^^^^^^^^^^^^^^^^^^^^^

JUMP_IF_NEGATIVE_FLAG
^^^^^^^^^^^^^^^^^^^^^

JUMP_IF_OVERFLOW_FLAG
^^^^^^^^^^^^^^^^^^^^^

JUMP_IF_NOT_OVERFLOW_FLAG
^^^^^^^^^^^^^^^^^^^^^^^^^

JUMP_IF_UNDERFLOW_FLAG
^^^^^^^^^^^^^^^^^^^^^^

JUMP_IF_NOT_UNDERFLOW_FLAG
^^^^^^^^^^^^^^^^^^^^^^^^^^

JUMP_IF_ZERO_FLAG
^^^^^^^^^^^^^^^^^

JUMP_IF_NOT_ZERO_FLAG
^^^^^^^^^^^^^^^^^^^^^

CALL
^^^^

RETURN
^^^^^^

HALT
^^^^

Logical Operations
------------------

NOT
^^^

AND
^^^

NAND
^^^^

OR
^^

NOR
^^^

XOR
^^^

NXOR
^^^^

Constants
---------

Constants are values that the assembler will convert to machine code bytes for
operations that require data in the machine code. For example, a jump to an
explicit index in program memory, or setting a register to an explicit value.

Labels
^^^^^^

A label binds to the line of assembly that follows it. Once assembly is complete
the label's value is the index in program memory of the instruction byte that
followed the label definition. E.g. If an assembly file looked like this:

.. code-block:: text

        LOAD [#123] A
        ADD A

    @label
        SET B #42

The value of ``@label`` would be 3. The instruction byte corresponding to ``SET
B #42`` is at program memory index 3. ``LOAD [#123] A`` takes 2 bytes, ``ADD A``
one, and ``SET B #42`` is the byte after that.

Labels are typically used by jump operations.

A label is a token that starts with the ``@`` character followed by any letter or
an underscore, then any alphanumeric or an underscore. E.g.:

 - ``@label``
 - ``@label_1``
 - ``@_other_label``
   
Labels must be unique.

A label is defined by putting it on a line by itself.

Variables
^^^^^^^^^

Variables are named aliases for indexes into data memory. They can be
predeclared by putting them by themselves on a line or declared as they are
used by using them as an argument.

The index for a given variable is determined by the assembler. As it parses
assembly lines from the start of the file to the end, addresses are assigned to
variables as they are encountered in the file. E.g. for the following assembly:

.. code-block:: text

        $variable1
        LOAD [$variable2] A

variable1 is predclared, variable2 is declared as it's used. Variable1 is an
alias for 0, variable2 is an alias for 1.

A variable is a token that starts with the ``$`` character followed by any letter or
an underscore, then any alphanumeric or an underscore. E.g.:

 - ``$variable``
 - ``$variable1``
 - ``$_other_variable``

Numbers
^^^^^^^

Numbers are integer values. In most cases they within the range -127 to 255
(inclusive). This range comes from the minimum and maximum values that 8 bits,
or 8 bits with 2's compliment encoding can hold.

A number is a token that starts with the ``#`` character and is followed by any
valid Python integer definition. E.g. 

 - ``#123`` (decimal)
 - ``#-5`` (decimal)
 - ``#0b00010010`` (binary)
 - ``#-0b0101`` (binary)
 - ``#0xA2`` (hex)
 - ``#0o107`` (octal)

Comments
--------

Comments are parts of the assembly file ignored by the assembler.

A comment is anything after and including ``//`` on a line until the end of the
line.















