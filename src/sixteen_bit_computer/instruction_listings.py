"""
Listings of all the defined instructions.
"""

from .instruction_components import (
    NOOP,
    HALT,
    SET_ZERO,
    JUMP_IF_EQ_ZERO,
    JUMP_IF_NEQ_ZERO,
    JUMP_IF_ACC_EQ,
    JUMP_IF_ACC_NEQ,
    JUMP,
    COPY,
    ADD,
    SUB,
    AND,
    OR,
    XOR,
    NAND,
    NOR,
    NXOR,
    ACC,
    A,
    B,
    C,
    SP,
    PC,
    CONST,
    M_CONST,
)
from . import operations


_INSTRUCTION_SIGNATURES = (
    (NOOP,),
    (SET_ZERO, ACC),
    (SET_ZERO, A),
    (SET_ZERO, B),
    (SET_ZERO, C),
    (JUMP_IF_EQ_ZERO, ACC, CONST),
    (JUMP_IF_EQ_ZERO, A, CONST),
    (JUMP_IF_EQ_ZERO, B, CONST),
    (JUMP_IF_EQ_ZERO, C, CONST),
    (JUMP_IF_EQ_ZERO, PC, CONST),
    (JUMP_IF_EQ_ZERO, SP, CONST),
    (JUMP_IF_NEQ_ZERO, ACC, CONST),
    (JUMP_IF_NEQ_ZERO, A, CONST),
    (JUMP_IF_NEQ_ZERO, B, CONST),
    (JUMP_IF_NEQ_ZERO, C, CONST),
    (JUMP_IF_NEQ_ZERO, PC, CONST),
    (JUMP_IF_NEQ_ZERO, SP, CONST),
    (JUMP_IF_ACC_EQ, A, CONST),
    (JUMP_IF_ACC_EQ, B, CONST),
    (JUMP_IF_ACC_EQ, C, CONST),
    (JUMP_IF_ACC_EQ, PC, CONST),
    (JUMP_IF_ACC_EQ, SP, CONST),
    (JUMP_IF_ACC_EQ, CONST, CONST),
    (JUMP_IF_ACC_NEQ, A, CONST),
    (JUMP_IF_ACC_NEQ, B, CONST),
    (JUMP_IF_ACC_NEQ, C, CONST),
    (JUMP_IF_ACC_NEQ, PC, CONST),
    (JUMP_IF_ACC_NEQ, SP, CONST),
    (JUMP_IF_ACC_NEQ, CONST, CONST),
    (JUMP, CONST),
    (COPY, ACC, A),
    (COPY, ACC, B),
    (COPY, ACC, C),
    (COPY, ACC, SP),
    (COPY, A, ACC),
    (COPY, A, B),
    (COPY, A, C),
    (COPY, A, SP),
    (COPY, B, ACC),
    (COPY, B, A),
    (COPY, B, C),
    (COPY, B, SP),
    (COPY, C, ACC),
    (COPY, C, A),
    (COPY, C, B),
    (COPY, C, SP),
    (COPY, PC, ACC),
    (COPY, PC, A),
    (COPY, PC, B),
    (COPY, PC, C),
    (COPY, PC, SP),
    (COPY, SP, ACC),
    (COPY, SP, A),
    (COPY, SP, B),
    (COPY, SP, C),
    (ADD, A),
    (ADD, B),
    (ADD, C),
    (ADD, CONST),
    (ADD, M_CONST),
    (SUB, A),
    (SUB, B),
    (SUB, C),
    (SUB, CONST),
    (SUB, M_CONST),
    (AND, A),
    (AND, B),
    (AND, C),
    (AND, CONST),
    (AND, M_CONST),
    (OR, A),
    (OR, B),
    (OR, C),
    (OR, CONST),
    (OR, M_CONST),
    (XOR, A),
    (XOR, B),
    (XOR, C),
    (XOR, CONST),
    (XOR, M_CONST),
    (NAND, A),
    (NAND, B),
    (NAND, C),
    (NAND, CONST),
    (NAND, M_CONST),
    (NOR, A),
    (NOR, B),
    (NOR, C),
    (NOR, CONST),
    (NOR, M_CONST),
    (NXOR, A),
    (NXOR, B),
    (NXOR, C),
    (NXOR, CONST),
    (NXOR, M_CONST),
    (HALT,)
)
"""
All possible instruction signatures.

An instruction signature is a tuple of the :mod:`Instruction component
<.instruction_components>` s it's made up of.
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
    return _INSTRUCTION_SIGNATURES.index(signature)


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
