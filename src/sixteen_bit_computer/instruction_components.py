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

    #Arithmetic
    ADD = auto()
    ADDC = auto()
    SUB = auto()
    SUBB = auto()
    INCR = auto()
    DECR= auto()

    # Data
    COPY = auto()
    LOAD = auto()
    STORE = auto()
    PUSH = auto()
    POP = auto()
    SET = auto()
    SET_ZERO = auto()

    # Program Control
    NOOP = auto()
    JUMP = auto()
    JUMP_IF_ACC_LT = auto()
    JUMP_IF_ACC_LTE = auto()
    JUMP_IF_ACC_EQ = auto()
    JUMP_IF_ACC_NEQ = auto()
    JUMP_IF_ACC_GTE = auto()
    JUMP_IF_ACC_GT = auto()
    JUMP_IF_EQ_ZERO = auto()
    JUMP_IF_NEQ_ZERO = auto()
    JUMP_IF_CARRY = auto()
    JUMP_IF_NOT_CARRY = auto()
    JUMP_IF_BORROW = auto()
    JUMP_IF_NOT_BORROW = auto()
    JUMP_IF_NEGATIVE_FLAG = auto()
    JUMP_IF_NOT_NEGATIVE_FLAG = auto()
    JUMP_IF_EQUAL_FLAG = auto()
    JUMP_IF_NOT_EQUAL_FLAG = auto()
    JUMP_IF_ZERO_FLAG = auto()
    JUMP_IF_NOT_ZERO_FLAG = auto()
    CALL = auto()
    RETURN = auto()
    HALT = auto()

    # Logic
    NOT = auto()
    AND = auto()
    NAND = auto()
    OR = auto()
    NOR = auto()
    XOR = auto()
    NXOR = auto()

    # Misc
    ROT_LEFT = auto()
    SHIFT_LEFT = auto()
    ROT_RIGHT = auto()
    SHIFT_RIGHT = auto()
    STORE_DECR = auto()
    STORE_INCR = auto()


ADD = OpCode.ADD
ADDC = OpCode.ADDC
SUB = OpCode.SUB
SUBB = OpCode.SUBB
INCR = OpCode.INCR
DECR = OpCode.DECR

COPY = OpCode.COPY
LOAD = OpCode.LOAD
STORE = OpCode.STORE
PUSH = OpCode.PUSH
POP = OpCode.POP
SET = OpCode.SET
SET_ZERO = OpCode.SET_ZERO

NOOP = OpCode.NOOP
JUMP = OpCode.JUMP
JUMP_IF_ACC_LT = OpCode.JUMP_IF_ACC_LT
JUMP_IF_ACC_LTE = OpCode.JUMP_IF_ACC_LTE
JUMP_IF_ACC_EQ = OpCode.JUMP_IF_ACC_EQ
JUMP_IF_ACC_NEQ = OpCode.JUMP_IF_ACC_NEQ
JUMP_IF_ACC_GTE = OpCode.JUMP_IF_ACC_GTE
JUMP_IF_ACC_GT = OpCode.JUMP_IF_ACC_GT
JUMP_IF_EQ_ZERO = OpCode.JUMP_IF_EQ_ZERO
JUMP_IF_NEQ_ZERO = OpCode.JUMP_IF_NEQ_ZERO
JUMP_IF_CARRY = OpCode.JUMP_IF_CARRY
JUMP_IF_NOT_CARRY = OpCode.JUMP_IF_NOT_CARRY
JUMP_IF_BORROW = OpCode.JUMP_IF_BORROW
JUMP_IF_NOT_BORROW = OpCode.JUMP_IF_NOT_BORROW
JUMP_IF_NEGATIVE_FLAG = OpCode.JUMP_IF_NEGATIVE_FLAG
JUMP_IF_NOT_NEGATIVE_FLAG = OpCode.JUMP_IF_NOT_NEGATIVE_FLAG
JUMP_IF_EQUAL_FLAG = OpCode.JUMP_IF_EQUAL_FLAG
JUMP_IF_NOT_EQUAL_FLAG = OpCode.JUMP_IF_NOT_EQUAL_FLAG
JUMP_IF_ZERO_FLAG = OpCode.JUMP_IF_ZERO_FLAG
JUMP_IF_NOT_ZERO_FLAG = OpCode.JUMP_IF_NOT_ZERO_FLAG
CALL = OpCode.CALL
RETURN = OpCode.RETURN
HALT = OpCode.HALT

NOT = OpCode.NOT
AND = OpCode.AND
NAND = OpCode.NAND
OR = OpCode.OR
NOR = OpCode.NOR
XOR = OpCode.XOR
NXOR = OpCode.NXOR

ROT_LEFT = OpCode.ROT_LEFT
ROT_RIGHT = OpCode.ROT_RIGHT
SHIFT_LEFT = OpCode.SHIFT_LEFT
SHIFT_RIGHT = OpCode.SHIFT_RIGHT
STORE_DECR = OpCode.STORE_DECR
STORE_INCR = OpCode.STORE_INCR

class Module(Enum):
    """
    All the possible modules.
    """
    ACC = auto()
    A = auto()
    B = auto()
    C = auto()
    X = auto()
    Y = auto()
    Z = auto()
    SP = auto()
    PC = auto()


ACC = Module.ACC
A = Module.A
B = Module.B
C = Module.C
X = Module.X
Y = Module.Y
Z = Module.Z
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
    M_SP = auto()
    M_PC = auto()
    M_CONST = auto()


M_ACC = MemoryReference.M_ACC
M_A = MemoryReference.M_A
M_B = MemoryReference.M_B
M_C = MemoryReference.M_C
M_SP = MemoryReference.M_SP
M_PC = MemoryReference.M_PC
M_CONST = MemoryReference.M_CONST


_MEMORY_REF_TO_COMPONENT = {
    M_ACC: ACC,
    M_A: A,
    M_B: B,
    M_C: C,
    M_SP: SP,
    M_PC: PC,
    M_CONST: CONST,
}


def memory_ref_to_component(memory_ref):
    """
    Given a memory reference, get the component it's referencing.

    Args:
        memory_ref (MemoryReference): The mrmory ref to convert.
    """

    return _MEMORY_REF_TO_COMPONENT[memory_ref]

_COMPONENT_TO_ASSEMBLY = {
    ADD: "ADD",
    ADDC: "ADDC",
    SUB: "SUB",
    SUBB: "SUBB",
    INCR: "INCR",
    DECR: "DECR",

    COPY: "COPY",
    LOAD: "LOAD",
    STORE: "STORE",
    PUSH: "PUSH",
    POP: "POP",
    SET: "SET",
    SET_ZERO: "SET_ZERO",

    NOOP: "NOOP",
    JUMP: "JUMP",
    JUMP_IF_ACC_LT: "JUMP_IF_ACC_LT",
    JUMP_IF_ACC_LTE: "JUMP_IF_ACC_LTE",
    JUMP_IF_ACC_EQ: "JUMP_IF_ACC_EQ",
    JUMP_IF_ACC_NEQ: "JUMP_IF_ACC_NEQ",
    JUMP_IF_ACC_GTE: "JUMP_IF_ACC_GTE",
    JUMP_IF_ACC_GT: "JUMP_IF_ACC_GT",
    JUMP_IF_EQ_ZERO: "JUMP_IF_EQ_ZERO",
    JUMP_IF_NEQ_ZERO: "JUMP_IF_NEQ_ZERO",
    JUMP_IF_CARRY: "JUMP_IF_CARRY",
    JUMP_IF_NOT_CARRY: "JUMP_IF_NOT_CARRY",
    JUMP_IF_BORROW: "JUMP_IF_BORROW",
    JUMP_IF_NOT_BORROW: "JUMP_IF_NOT_BORROW",
    JUMP_IF_NEGATIVE_FLAG: "JUMP_IF_NEGATIVE_FLAG",
    JUMP_IF_NOT_NEGATIVE_FLAG: "JUMP_IF_NOT_NEGATIVE_FLAG",
    JUMP_IF_EQUAL_FLAG: "JUMP_IF_EQUAL_FLAG",
    JUMP_IF_NOT_EQUAL_FLAG: "JUMP_IF_NOT_EQUAL_FLAG",
    JUMP_IF_ZERO_FLAG: "JUMP_IF_ZERO_FLAG",
    JUMP_IF_NOT_ZERO_FLAG: "JUMP_IF_NOT_ZERO_FLAG",
    CALL: "CALL",
    RETURN: "RETURN",
    HALT: "HALT",

    NOT: "NOT",
    AND: "AND",
    NAND: "NAND",
    OR: "OR",
    NOR: "NOR",
    XOR: "XOR",
    NXOR: "NXOR",

    ROT_LEFT: "ROT_LEFT",
    ROT_RIGHT: "ROT_RIGHT",
    SHIFT_LEFT: "SHIFT_LEFT",
    SHIFT_RIGHT: "SHIFT_RIGHT",
    
    STORE_DECR: "STORE_DECR",
    STORE_INCR: "STORE_INCR",

    ACC: "ACC",
    A: "A",
    B: "B",
    C: "C",
    X: "X",
    Y: "Y",
    Z: "Z",
    SP: "SP",
    PC: "PC",

    CONST: "#123",

    M_ACC: "[ACC]",
    M_A: "[A]",
    M_B: "[B]",
    M_C: "[C]",
    M_SP: "[SP]",
    M_PC: "[PC]",
    M_CONST: "[#456]",
}

def component_to_assembly(component):
    """
    Given an instruction component, get the equivalent assembly.

    Args:
        component (Any): The component to convert.
    """
    return _COMPONENT_TO_ASSEMBLY[component]