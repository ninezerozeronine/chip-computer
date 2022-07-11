def get_all_operations():
    # Need to import in the function to avoid cicular import
    from . import (
        noop_op,
        set_zero_op,
        set_op,
        simple_alu_ops,
        halt_op,
        copy_op,
        jump_if_xxx_zero_op,
        jump_if_acc_xxx_op,
        jump_op,
        incr_decr_ops,
        load_store_ops,
        push_pop_ops,
        not_op,
    )

    return [
        noop_op,
        set_zero_op,
        set_op,
        simple_alu_ops,
        halt_op,
        copy_op,
        jump_if_xxx_zero_op,
        jump_if_acc_xxx_op,
        jump_op,
        incr_decr_ops,
        load_store_ops,
        push_pop_ops,
        not_op,
    ]
