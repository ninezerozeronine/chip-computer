// Test using ACC
@set_initial
    SET A #1
    SET B #1

@fib_loop
    COPY A ACC
    ADD B
    JUMP_IF_OVERFLOW_FLAG @set_initial
    COPY B A
    COPY ACC B
    JUMP @fib_loop