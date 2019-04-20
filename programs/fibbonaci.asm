// Test using ACC
@set_initial
    SET A #1
    SET B #1

@fib_loop
    COPY A ACC
    ADD B
    JUMP_IF_OVERFLOW @set_initial
    COPY B A
    COPY ACC B

// Test using DAT
@set_initial
    SET A #1
    SET B #1

@fib_loop
    COPY B DAT
    ADD_DAT_TO A
    JUMP_IF_OVERFLOW @set_initial
    COPY A DAT
    COPY B A
    COPY DAT B