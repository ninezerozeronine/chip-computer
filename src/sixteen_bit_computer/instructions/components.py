from enum import Enum, auto


class OpCode(Enum):
    NOOP = auto()
    LOAD = auto()
    STORE = auto()
    ADD = auto()


NOOP = OpCode.NOOP
LOAD = OpCode.LOAD
STORE = OpCode.STORE
ADD = OpCode.ADD


class Module(Enum):
    A = auto()
    B = auto()
    C = auto()


A = Module.A
B = Module.B
C = Module.C


class Constant(Enum):
    CONST = auto()


CONST = Constant.CONST


class MemoryReference(Enum):
    M_A = auto()
    M_B = auto()
    M_CONST = auto()


M_A = MemoryReference.M_A
M_B = MemoryReference.M_B
M_CONST = MemoryReference.M_CONST
