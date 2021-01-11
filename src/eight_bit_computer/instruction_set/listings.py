from .instruction_components import (
    NOOP,
    LOAD,
    STORE,
    A,
    M_A,
    M_CONST
)

all_instructions = set(
    (NOOP,),
    (LOAD, M_CONST, A),
    (STORE, A, M_CONST),
    (ADD, M_A),
    (ADD, A)
)


def get_instruction_byte_val(instruction):
    pass

