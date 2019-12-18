"""
Operations in the assembly language
"""


def get_all_operations():
    """
    Get a list of all the operations in the assembly language

    Deferring the import to the function so that importing the
    operations module doesn't mean automatically importing all the
    operations.

    Returns:
        list(module): All the modules that represent operations in the
        assembly language
    """

    from . import (
        and_op,
        nand_op,
        or_op,
        nor_op,
        xor_op,
        nxor_op,
        not_op,
        add,
        copy_op,
        load,
        store_op,
        progload_op,
        progstore_op,
        push_op,
        pop_op,
        set_op,
        jump,
        jump_if_positive_flag,
        jump_if_negative_flag,
        jump_if_overflow_flag,
        jump_if_not_overflow_flag,
        jump_if_underflow_flag,
        jump_if_not_underflow_flag,
        jump_if_zero_flag,
        jump_if_not_zero_flag,
        lshift_op,
        lshiftc_op,
        incr_op,
        decr_op,
        addc_op,
        subb_op
    )

    return [
        and_op,
        nand_op,
        or_op,
        nor_op,
        xor_op,
        nxor_op,
        not_op,
        add,
        copy_op,
        load,
        store_op,
        progload_op,
        progstore_op,
        push_op,
        pop_op,
        set_op,
        jump,
        jump_if_positive_flag,
        jump_if_negative_flag,
        jump_if_overflow_flag,
        jump_if_not_overflow_flag,
        jump_if_underflow_flag,
        jump_if_not_underflow_flag,
        jump_if_zero_flag,
        jump_if_not_zero_flag,
        lshift_op,
        lshiftc_op,
        incr_op,
        decr_op,
        addc_op,
        subb_op,
    ]
