// This tests all the assembly operations, halting if something is not as expected

&start
    NOOP

    SET_ZERO ACC
    JUMP_IF_NEQ_ZERO ACC &halt

    SET_ZERO A
    JUMP_IF_NEQ_ZERO A &halt

    JUMP &start

&halt
    JUMP &halt