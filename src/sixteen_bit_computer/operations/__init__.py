def get_all_operations():
    # Need to import in the function to avoid cicular import
    from . import (
        noop_op,
        set_zero_op,
        simple_alu_ops,
        halt_op,
        copy_op,
    )

    return [
        noop_op,
        set_zero_op,
        simple_alu_ops,
        halt_op,
        copy_op,
    ]
