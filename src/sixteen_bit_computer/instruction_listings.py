"""
Listings of all the defined instructions.
"""

from .instruction_components import (
    NOOP,
    HALT,
    SET_ZERO,
    ADD,
    AND,
    ACC,
    A,
    B,
    C,
    CONST,
    M_CONST,
)
from . import operations


_INSTRUCTION_SIGNATURES = frozenset([
    (NOOP,),
    (SET_ZERO, ACC),
    (SET_ZERO, A),
    (SET_ZERO, B),
    (SET_ZERO, C),
    (ADD, A),
    (ADD, B),
    (ADD, C),
    (ADD, CONST),
    (ADD, M_CONST),
    (AND, A),
    (AND, B),
    (AND, C),
    (AND, CONST),
    (AND, M_CONST),
    (HALT,)
])
"""
All possible instruction signatures.

An instruction signature is a tuple of the :mod:`Instruction component
<.instruction_components>` s it's made up of.
"""


_INSTRUCTION_INDECIES = {
    (NOOP,): 0,
    (SET_ZERO, ACC): 1,
    (SET_ZERO, A): 2,
    (SET_ZERO, B): 3,
    (SET_ZERO, C): 4,
    (ADD, A): 5,
    (ADD, B): 6,
    (ADD, C): 7,
    (ADD, CONST): 8,
    (ADD, M_CONST): 9,
    (AND, A): 10,
    (AND, B): 11,
    (AND, C): 12,
    (AND, CONST): 13,
    (AND, M_CONST): 14,
    (HALT,): 15
}
"""
The index of all instructions.

All the instructions need a unique index that eventually become the
8 bits that uniquely identify it at the machinecode level.
"""


def get_instruction_index(signature):
    """
    Get the index of the given signature.

    Args:
        signature (Tuple(:mod:`Instruction component<.instruction_components>`)):
            The signature to find the index of.

    Returns:
        int: Index of the signature.
    """
    return _INSTRUCTION_INDECIES[signature]


def all_signatures():
    """
    Get the set of all the possible signatures.

    Returns:
        frozenset(Tuple(:mod:`Instruction component<.instruction_components>`)):
        All the signatures.
    """
    return _INSTRUCTION_SIGNATURES


def is_supported_signature(signature):
    """
    Whether or not the signature is supported.

    Args:
        signature (Tuple(:mod:`Instruction component<.instruction_components>`)):
            The signature to check.

    Returns:
        bool: True if the signature is supported, false if not.
    """
    return signature in _INSTRUCTION_SIGNATURES


_FUNC_MAPPING = None
"""
A mapping of instruction signatures to the functions that generate
machinecode for them.

This is generated at runtime to save hardcoding, and reduce lookup
costs while assembling.
"""


def _generate_signature_to_machinecode_function_map():
    """
    Generate a mapping of instruction signatures to the functions that
    generate machinecode for them.

    Returns:
        dict(Tuple(:mod:`Instruction component<.instruction_components>`), function):
        Dictionary of signature keys to functions that generate
        machinecode for them.
    """
    mapping = {}
    for signature in _INSTRUCTION_SIGNATURES:
        for operation in operations.get_all_operations():
            if operation.supports(signature):
                mapping[signature] = operation.generate_machinecode
    return mapping


def get_machinecode_function(signature):
    """
    Get machinecode generating function for given signature.

    See :meth:`~set_zero_op.generate_machinecode` for an example of a
    machinecode generating function and
    :meth:`~Instruction._generate_machinecode` for an example of how
    it's called.

    Args:
        signature (Tuple(:mod:`Instruction component <.instruction_components>`)):
            The signature to get machinecode for.

    Returns:
        func: The function that generates machinecode for the given
        signature.
    """
    global _FUNC_MAPPING
    if _FUNC_MAPPING is None:
        _FUNC_MAPPING = _generate_signature_to_machinecode_function_map()

    return _FUNC_MAPPING[signature]
