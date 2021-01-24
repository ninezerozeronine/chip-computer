from enum import Enum

class OpCode(Enum):
    NOOP = 1
    LOAD = 2
    STORE = 3
    ADD = 4

NOOP = OpCode.NOOP
LOAD = OpCode.LOAD
STORE = OpCode.STORE
ADD = OpCode.ADD


class Module(Enum):
    A = 1
    B = 2
    C = 3

A = Module.A
B = Module.B
C = Module.C


class Constant(Enum):
    CONST = 1

CONST = Constant.CONST


class MemoryReference(Enum):
    M_A = 1
    M_B = 2
    M_CONST = 3

M_A = MemoryReference.M_A
M_B = MemoryReference.M_B
M_CONST = MemoryReference.M_CONST
