from enum import Enum, auto


class OpCode(Enum):
    NOOP = auto()
    SET_ZERO = auto()
    LOAD = auto()
    STORE = auto()
    ADD = auto()


NOOP = OpCode.NOOP
SET_ZERO = OpCode.SET_ZERO
LOAD = OpCode.LOAD
STORE = OpCode.STORE
ADD = OpCode.ADD


class Module(Enum):
    ACC = auto()
    A = auto()
    B = auto()
    C = auto()
    SP = auto()


ACC = Module.ACC
A = Module.A
B = Module.B
C = Module.C
SP = Module.SP


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
