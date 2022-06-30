// This tests all the assembly operations, halting if something is not as expected

!zero_one #0b0101010101010101
!one_zero #0b1010101010101010


&start
    NOOP

    SET_ZERO ACC
    JUMP_IF_NEQ_ZERO ACC &halt

    SET_ZERO A
    JUMP_IF_NEQ_ZERO A &halt

    SET_ZERO B
    JUMP_IF_NEQ_ZERO B &halt

    SET_ZERO C
    JUMP_IF_NEQ_ZERO C &halt

    SET ACC !zero_one
    SET A !zero_one
    JUMP_IF_ACC_NEQ A &halt

    SET ACC !one_zero
    SET B !one_zero
    JUMP_IF_ACC_NEQ B &halt  

    SET ACC !zero_one
    SET C !zero_one
    JUMP_IF_ACC_NEQ C &halt   

    SET ACC !one_zero
    SET SP !one_zero
    JUMP_IF_ACC_NEQ SP &halt   

    JUMP &start

&halt
    JUMP &halt