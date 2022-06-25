"""
Pieces that make up an instruction.

E.g. In the instruction::

    LOAD [#123] A

There are 3 components:

 - ``LOAD`` - The opcode.
 - ``[#123]`` - A memory reference to a constant.
 - ``A`` - The A module.
"""

from enum import Enum, auto


class OpCode(Enum):
    """
    All the possible opcodes.
    """
    NOOP = auto()
    HALT = auto()
    SET_ZERO = auto()
    JUMP_IF_EQ_ZERO = auto()
    JUMP_IF_NEQ_ZERO = auto()
    COPY = auto()
    LOAD = auto()
    STORE = auto()
    ADD = auto()
    SUB = auto()
    AND = auto()
    OR = auto()
    XOR = auto()
    NAND = auto()
    NOR = auto()
    NXOR = auto()


NOOP = OpCode.NOOP
HALT = OpCode.HALT
SET_ZERO = OpCode.SET_ZERO
JUMP_IF_EQ_ZERO = OpCode.JUMP_IF_EQ_ZERO
JUMP_IF_NEQ_ZERO = OpCode.JUMP_IF_NEQ_ZERO
COPY = OpCode.COPY
LOAD = OpCode.LOAD
STORE = OpCode.STORE
ADD = OpCode.ADD
SUB = OpCode.SUB
AND = OpCode.AND
OR = OpCode.OR
XOR = OpCode.XOR
NAND = OpCode.NAND
NOR = OpCode.NOR
NXOR = OpCode.NXOR


class Module(Enum):
    """
    All the possible modules.
    """
    ACC = auto()
    A = auto()
    B = auto()
    C = auto()
    SP = auto()
    PC = auto()


ACC = Module.ACC
A = Module.A
B = Module.B
C = Module.C
SP = Module.SP
PC = Module.PC


class Constant(Enum):
    """
    A constant value.

    This is constant in the sense that it ends up as raw data in the
    machinecode, as opposed the instructions.

    Constants can either be part of an instruction, e.g. the ``#34``
    in::

        SET A #34

    Or raw data::

        DATA "Hello, world!"
    """
    CONST = auto()


CONST = Constant.CONST


class MemoryReference(Enum):
    """
    A memory reference.

    Rather than using the value in a module, or a constant value in the
    operation, use the value currently in memory at the location
    specified by the item in the square braces.
    """
    M_ACC = auto()
    M_A = auto()
    M_B = auto()
    M_C = auto()
    M_CONST = auto()


M_ACC = MemoryReference.M_ACC
M_A = MemoryReference.M_A
M_B = MemoryReference.M_B
M_C = MemoryReference.M_C
M_CONST = MemoryReference.M_CONST
