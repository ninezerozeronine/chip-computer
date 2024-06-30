def get_all_operations():
    # Need to import in the function to avoid cicular import
    from . import (
        noop_op,
        set_zero_op,
        set_op,
        simple_alu_ops,
        halt_op,
        copy_op,
        jump_if_eq_neq_zero_ops,
        jump_if_acc_eq_neq_ops,
        jump_op,
        incr_decr_ops,
        load_store_ops,
        push_pop_ops,
        not_op,
        rot_left_op,
        call_return_ops,
        jump_if_acc_cmp_ops,
        jump_if_flag_not_flag_ops,
        lshift_op,
    )

    return [
        noop_op,
        set_zero_op,
        set_op,
        simple_alu_ops,
        halt_op,
        copy_op,
        jump_if_eq_neq_zero_ops,
        jump_if_acc_eq_neq_ops,
        jump_op,
        incr_decr_ops,
        load_store_ops,
        push_pop_ops,
        not_op,
        rot_left_op,
        call_return_ops,
        jump_if_acc_cmp_ops,
        jump_if_flag_not_flag_ops,
        lshift_op,
    ]
