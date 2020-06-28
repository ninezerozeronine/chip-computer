@set_initial
    SET A #1
    SET B #1

@fib_loop
    COPY A ACC
    ADD B
    JUMP_IF_OVERFLOW_FLAG @set_initial
    // STORE ACC [#0xFF] // To display in logisim
    COPY ACC C // To display in hardware
    COPY B A
    COPY ACC B
    JUMP @fib_loop