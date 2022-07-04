// This tests all the assembly operations, halting if something is not as expected

!zero_one #0b0101010101010101
!one_zero #0b1010101010101010


&start
    NOOP

    ////////////////////////////////////////////////////////////////
    // SET_ZERO
    ////////////////////////////////////////////////////////////////
    SET_ZERO ACC
    JUMP_IF_NEQ_ZERO ACC &sz_halt0

    SET_ZERO A
    JUMP_IF_NEQ_ZERO A &sz_halt1

    SET_ZERO B
    JUMP_IF_NEQ_ZERO B &sz_halt2

    SET_ZERO C
    JUMP_IF_NEQ_ZERO C &sz_halt3

    SET_ZERO SP
    JUMP_IF_NEQ_ZERO SP &sz_halt4

    JUMP &set_start

&sz_halt0
    HALT
&sz_halt1
    HALT
&sz_halt2
    HALT
&sz_halt3
    HALT
&sz_halt4
    HALT

    ////////////////////////////////////////////////////////////////
    // SET
    ////////////////////////////////////////////////////////////////

&set_start

    SET ACC !zero_one
    SET A !zero_one
    JUMP_IF_ACC_NEQ A &set_halt0

    SET ACC !one_zero
    SET B !one_zero
    JUMP_IF_ACC_NEQ B &set_halt1

    SET ACC !zero_one
    SET C !zero_one
    JUMP_IF_ACC_NEQ C &set_halt2   

    SET ACC !one_zero
    SET SP !one_zero
    JUMP_IF_ACC_NEQ SP &set_halt3

    JUMP &jiez_start

&set_halt0
    HALT
&set_halt1
    HALT
&set_halt2
    HALT
&set_halt3
    HALT

    ////////////////////////////////////////////////////////////////
    // JUMP_IF_EQ_ZERO
    ////////////////////////////////////////////////////////////////

&jiez_start

    SET_ZERO ACC
    JUMP_IF_EQ_ZERO ACC &jiez_0
    HALT

&jiez_0
    SET_ZERO ACC
    JUMP_IF_EQ_ZERO ACC &jiez_1
    HALT

&jiez_1
    SET_ZERO A
    JUMP_IF_EQ_ZERO A &jiez_2
    HALT

&jiez_2
    SET_ZERO B
    JUMP_IF_EQ_ZERO B &jiez_3
    HALT

&jiez_3
    SET_ZERO C
    JUMP_IF_EQ_ZERO C &jiez_4
    HALT

&jiez_4
    SET_ZERO SP
    JUMP_IF_EQ_ZERO SP &jiez_0
    HALT

    ////////////////////////////////////////////////////////////////
    // JUMP_IF_NEQ_ZERO
    ////////////////////////////////////////////////////////////////
&jinez_0
    SET ACC #1
    JUMP_IF_NEQ_ZERO ACC &jinez_1
    HALT

&jinez_1
    SET A #1
    JUMP_IF_NEQ_ZERO A &jinez_2
    HALT

&jinez_2
    SET B #1
    JUMP_IF_NEQ_ZERO B &jinez_3
    HALT

&jinez_3
    SET C #1
    JUMP_IF_NEQ_ZERO C &jinez_4
    HALT

&jinez_4
    SET SP #1
    JUMP_IF_NEQ_ZERO SP &jiae_0
    HALT


    ////////////////////////////////////////////////////////////////
    // JUMP_IF_ACC_EQ
    ////////////////////////////////////////////////////////////////
&jiae_0
    SET ACC #123
    SET A #123
    JUMP_IF_ACC_EQ A &jiae_1
    HALT

&jiae_1
    SET ACC #456
    SET B #456
    JUMP_IF_ACC_EQ B &jiae_2
    HALT

&jiae_2
    SET ACC #789
    SET C #789
    JUMP_IF_ACC_EQ C &jiae_3
    HALT

&jiae_3
    SET ACC #1011
    SET SP #1011
    JUMP_IF_ACC_EQ SP &jiae_4
    HALT

&jiae_4
    SET ACC #60123
    JUMP_IF_ACC_EQ #60123 &jiane_0
    HALT

    ////////////////////////////////////////////////////////////////
    // JUMP_IF_ACC_NEQ
    ////////////////////////////////////////////////////////////////

&jiane_0
    SET ACC #123
    SET A #1234
    JUMP_IF_ACC_NEQ A &jiane_1
    HALT

&jiane_1
    SET ACC #321
    SET B #55555
    JUMP_IF_ACC_NEQ B &jiane_2
    HALT

&jiane_2
    SET ACC #21454
    SET A #6874
    JUMP_IF_ACC_NEQ C &jiane_3
    HALT

&jiane_3
    SET ACC #3333
    SET A #4444
    JUMP_IF_ACC_NEQ SP &jiane_4
    HALT

&jiane_4
    SET ACC !one_zero
    JUMP_IF_ACC_NEQ !zero_one &jump_0
    HALT

    ////////////////////////////////////////////////////////////////
    // JUMP
    ////////////////////////////////////////////////////////////////

&jump_0
    SET ACC &jump_1
    JUMP ACC
    HALT

&jump_1
    SET A &jump_2
    JUMP A
    HALT

&jump_2
    SET B &jump_3
    JUMP B
    HALT

&jump_3
    SET C &jump_4
    JUMP C
    HALT

&jump_4
    SET SP &jump_5
    JUMP SP
    HALT

&jump_5
    JUMP &jump_6
    HALT

&jump_6
$v_jump_0 &jump7
    SET ACC $v_jump_0
    JUMP [ACC]
    HALT

&jump7
$v_jump_1 &jump8
    SET A $v_jump_1
    JUMP [A]
    HALT

&jump8
$v_jump_2 &jump9
    SET B $v_jump_2
    JUMP [B]
    HALT

&jump9
$v_jump_3 &jump10
    SET C $v_jump_3
    JUMP [C]
    HALT

&jump10
$v_jump_4 &jump11
    SET SP $v_jump_4
    JUMP [SP]
    HALT

&jump11
$v_jump_5 &copy_0
    JUMP [$v_jump_5]
    HALT

    ////////////////////////////////////////////////////////////////
    // COPY
    ////////////////////////////////////////////////////////////////

&copy_0
    NOOP

    JUMP &start