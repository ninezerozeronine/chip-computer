"""
Listings of all the defined instructions.
"""

from .instruction_components import (
    ADD,
    ADDC,
    SUB,
    SUBB,
    LSHIFT,
    LSHIFTC,
    INCR,
    DECR,
    COPY,
    LOAD,
    STORE,
    PUSH,
    POP,
    SET,
    SET_ZERO,
    NOOP,
    JUMP,
    JUMP_IF_ACC_LT,
    JUMP_IF_ACC_LTE,
    JUMP_IF_ACC_EQ,
    JUMP_IF_ACC_NEQ,
    JUMP_IF_ACC_GTE,
    JUMP_IF_ACC_GT,
    JUMP_IF_EQ_ZERO,
    JUMP_IF_NEQ_ZERO,
    JUMP_IF_NEGATIVE_FLAG,
    JUMP_IF_NOT_NEGATIVE_FLAG,
    JUMP_IF_CARRY_FLAG,
    JUMP_IF_NOT_CARRY_FLAG,
    JUMP_IF_BORROW_FLAG,
    JUMP_IF_NOT_BORROW_FLAG,
    JUMP_IF_ZERO_FLAG,
    JUMP_IF_NOT_ZERO_FLAG,
    CALL,
    RETURN,
    HALT,
    NOT,
    AND,
    NAND,
    OR,
    NOR,
    XOR,
    NXOR,
    ROT_LEFT,
    ACC,
    A,
    B,
    C,
    SP,
    PC,
    CONST,
    M_ACC,
    M_A,
    M_B,
    M_C,
    M_SP,
    M_CONST,
)
from . import operations


_INSTRUCTION_SIGNATURES = (
    (ADD, A),
    (ADD, B),
    (ADD, C),
    (ADD, CONST),
    (ADD, M_CONST),
    # (ADDC, A),
    # (ADDC, B),
    # (ADDC, C),
    # (ADDC, CONST),
    # (ADDC, M_CONST),
    (SUB, A),
    (SUB, B),
    (SUB, C),
    (SUB, CONST),
    (SUB, M_CONST),
    # (SUBB, A),
    # (SUBB, B),
    # (SUBB, C),
    # (SUBB, CONST),
    # (SUBB, M_CONST),
    # (LSHIFT, ACC),
    # (LSHIFT, A),
    # (LSHIFT, B),
    # (LSHIFT, C),
    # (LSHIFTC, ACC),
    # (LSHIFTC, A),
    # (LSHIFTC, B),
    # (LSHIFTC, C),
    (INCR, ACC),
    (INCR, A),
    (INCR, B),
    (INCR, C),
    (DECR, ACC),
    (DECR, A),
    (DECR, B),
    (DECR, C),
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
    (LOAD, M_ACC, ACC),
    (LOAD, M_ACC, A),
    (LOAD, M_ACC, B),
    (LOAD, M_ACC, C),
    (LOAD, M_A, ACC),
    (LOAD, M_A, A),
    (LOAD, M_A, B),
    (LOAD, M_A, C),
    (LOAD, M_B, ACC),
    (LOAD, M_B, A),
    (LOAD, M_B, B),
    (LOAD, M_B, C),
    (LOAD, M_C, ACC),
    (LOAD, M_C, A),
    (LOAD, M_C, B),
    (LOAD, M_C, C),
    (LOAD, M_SP, ACC),
    (LOAD, M_SP, A),
    (LOAD, M_SP, B),
    (LOAD, M_SP, C),
    (LOAD, M_CONST, ACC),
    (LOAD, M_CONST, A),
    (LOAD, M_CONST, B),
    (LOAD, M_CONST, C),
    (STORE, ACC, M_ACC),
    (STORE, ACC, M_A),
    (STORE, ACC, M_B),
    (STORE, ACC, M_C),
    (STORE, ACC, M_SP),
    (STORE, ACC, M_CONST),
    (STORE, A, M_ACC),
    (STORE, A, M_A),
    (STORE, A, M_B),
    (STORE, A, M_C),
    (STORE, A, M_SP),
    (STORE, A, M_CONST),
    (STORE, B, M_ACC),
    (STORE, B, M_A),
    (STORE, B, M_B),
    (STORE, B, M_C),
    (STORE, B, M_SP),
    (STORE, B, M_CONST),
    (STORE, C, M_ACC),
    (STORE, C, M_A),
    (STORE, C, M_B),
    (STORE, C, M_C),
    (STORE, C, M_SP),
    (STORE, C, M_CONST),
    (STORE, SP, M_ACC),
    (STORE, SP, M_A),
    (STORE, SP, M_B),
    (STORE, SP, M_C),
    (STORE, SP, M_SP),
    (STORE, SP, M_CONST),
    (PUSH, ACC),
    (PUSH, A),
    (PUSH, B),
    (PUSH, C),
    (POP, ACC),
    (POP, A),
    (POP, B),
    (POP, C),
    (SET, ACC, CONST),
    (SET, A, CONST),
    (SET, B, CONST),
    (SET, C, CONST),
    (SET, SP, CONST),
    (SET_ZERO, ACC),
    (SET_ZERO, A),
    (SET_ZERO, B),
    (SET_ZERO, C),
    (SET_ZERO, SP),
    (NOOP,),
    (JUMP, ACC),
    (JUMP, A),
    (JUMP, B),
    (JUMP, C),
    (JUMP, SP),
    (JUMP, CONST),
    (JUMP, M_ACC),
    (JUMP, M_A),
    (JUMP, M_B),
    (JUMP, M_C),
    (JUMP, M_SP),
    (JUMP, M_CONST),
    # (JUMP_IF_ACC_LT, A, CONST),
    # (JUMP_IF_ACC_LT, B, CONST),
    # (JUMP_IF_ACC_LT, C, CONST),
    # (JUMP_IF_ACC_LT, SP, CONST),
    # (JUMP_IF_ACC_LT, CONST, CONST),
    # (JUMP_IF_ACC_LTE, A, CONST),
    # (JUMP_IF_ACC_LTE, B, CONST),
    # (JUMP_IF_ACC_LTE, C, CONST),
    # (JUMP_IF_ACC_LTE, SP, CONST),
    # (JUMP_IF_ACC_LTE, CONST, CONST),
    (JUMP_IF_ACC_EQ, A, CONST),
    (JUMP_IF_ACC_EQ, B, CONST),
    (JUMP_IF_ACC_EQ, C, CONST),
    (JUMP_IF_ACC_EQ, SP, CONST),
    (JUMP_IF_ACC_EQ, CONST, CONST),
    (JUMP_IF_ACC_NEQ, A, CONST),
    (JUMP_IF_ACC_NEQ, B, CONST),
    (JUMP_IF_ACC_NEQ, C, CONST),
    (JUMP_IF_ACC_NEQ, SP, CONST),
    (JUMP_IF_ACC_NEQ, CONST, CONST),
    # (JUMP_IF_ACC_GTE, A, CONST),
    # (JUMP_IF_ACC_GTE, B, CONST),
    # (JUMP_IF_ACC_GTE, C, CONST),
    # (JUMP_IF_ACC_GTE, SP, CONST),
    # (JUMP_IF_ACC_GTE, CONST, CONST),
    # (JUMP_IF_ACC_GT, A, CONST),
    # (JUMP_IF_ACC_GT, B, CONST),
    # (JUMP_IF_ACC_GT, C, CONST),
    # (JUMP_IF_ACC_GT, SP, CONST),
    # (JUMP_IF_ACC_GT, CONST, CONST),
    (JUMP_IF_EQ_ZERO, ACC, CONST),
    (JUMP_IF_EQ_ZERO, A, CONST),
    (JUMP_IF_EQ_ZERO, B, CONST),
    (JUMP_IF_EQ_ZERO, C, CONST),
    (JUMP_IF_EQ_ZERO, SP, CONST),
    (JUMP_IF_NEQ_ZERO, ACC, CONST),
    (JUMP_IF_NEQ_ZERO, A, CONST),
    (JUMP_IF_NEQ_ZERO, B, CONST),
    (JUMP_IF_NEQ_ZERO, C, CONST),
    (JUMP_IF_NEQ_ZERO, SP, CONST),
    # (JUMP_IF_NEGATIVE_FLAG, CONST),
    # (JUMP_IF_NOT_NEGATIVE_FLAG, CONST),
    # (JUMP_IF_CARRY_FLAG, CONST),
    # (JUMP_IF_NOT_CARRY_FLAG, CONST),
    # (JUMP_IF_BORROW_FLAG, CONST),
    # (JUMP_IF_NOT_BORROW_FLAG, CONST),
    # (JUMP_IF_ZERO_FLAG, CONST),
    # (JUMP_IF_NOT_ZERO_FLAG, CONST),
    # (CALL, ACC),
    # (CALL, A),
    # (CALL, B),
    # (CALL, C),
    # (CALL, CONST),
    # (RETURN,),
    (HALT,),
    (NOT, ACC),
    (NOT, A),
    (NOT, B),
    (NOT, C),
    (AND, A),
    (AND, B),
    (AND, C),
    (AND, CONST),
    (AND, M_CONST),
    (NAND, A),
    (NAND, B),
    (NAND, C),
    (NAND, CONST),
    (NAND, M_CONST),
    (OR, A),
    (OR, B),
    (OR, C),
    (OR, CONST),
    (OR, M_CONST),
    (NOR, A),
    (NOR, B),
    (NOR, C),
    (NOR, CONST),
    (NOR, M_CONST),
    (XOR, A),
    (XOR, B),
    (XOR, C),
    (XOR, CONST),
    (XOR, M_CONST),
    (NXOR, A),
    (NXOR, B),
    (NXOR, C),
    (NXOR, CONST),
    (NXOR, M_CONST),
    # (ROT_LEFT, ACC),
    # (ROT_LEFT, A),
    # (ROT_LEFT, B),
    # (ROT_LEFT, C),
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
