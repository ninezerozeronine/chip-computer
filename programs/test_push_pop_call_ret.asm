    SET_ZERO A
    SET SP #0
    PUSH A

@loop
    CALL @incr_top_of_stack
    JUMP @loop

@incr_top_of_stack
    POP B
    INCR B
    PUSH B
    CALL @copy_top_of_stack_to_C
    RETURN

@copy_top_of_stack_to_C
    POP C
    PUSH C
    RETURN