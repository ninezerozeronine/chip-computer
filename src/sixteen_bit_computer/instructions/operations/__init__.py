def all_operations():
    # Need to import in the function to avoid cicular import
    from . import (
        noop_op,
        set_zero_op,
    )

    return [
        noop_op,
        set_zero_op,
    ]
