from .instruction_components import (
    NOOP,
    SET_ZERO,
    ACC,
    A,
    B,
    C,
)
from . import operations


_INSTRUCTION_SIGNATURES = frozenset([
    (NOOP,),
    (SET_ZERO, ACC),
    (SET_ZERO, A),
    (SET_ZERO, B),
    (SET_ZERO, C),
])


_INSTRUCTION_INDECIES = {
    (NOOP,): 0,
    (SET_ZERO, ACC): 1,
    (SET_ZERO, A): 2,
    (SET_ZERO, B): 3,
    (SET_ZERO, C): 4,
}


def get_instruction_index(signature):
    return _INSTRUCTION_INDECIES[signature]


def all_signatures():
    return _INSTRUCTION_SIGNATURES


def is_supported_signature(signature):
    return signature in _INSTRUCTION_SIGNATURES


_FUNC_MAPPING = None


def generate_signature_to_machinecode_function_map():
    mapping = {}
    for signature in _INSTRUCTION_SIGNATURES:
        for operation in operations.all_operations():
            if operation.supports(signature):
                mapping[signature] = operation.generate_machinecode
    return mapping


def get_machinecode_function(signature):
    global _FUNC_MAPPING
    if _FUNC_MAPPING is None:
        _FUNC_MAPPING = generate_signature_to_machinecode_function_map()

    return _FUNC_MAPPING[signature]
