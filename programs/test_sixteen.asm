// This tests all the assembly operations, halting if something is not as expected

!zero_one #0b0101010101010101
!one_zero #0b1010101010101010


&start

    ////////////////////////////////////////////////////////////////
    // NOOP
    ////////////////////////////////////////////////////////////////

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
    SET_ZERO A
    JUMP_IF_EQ_ZERO A &jiez_1
    HALT

&jiez_1
    SET_ZERO B
    JUMP_IF_EQ_ZERO B &jiez_2
    HALT

&jiez_2
    SET_ZERO C
    JUMP_IF_EQ_ZERO C &jiez_3
    HALT

&jiez_3
    SET_ZERO SP
    JUMP_IF_EQ_ZERO SP &jiez_4
    HALT

&jiez_4
    SET ACC #1
    JUMP_IF_EQ_ZERO ACC &jiez_halt_0

    SET A #58767
    JUMP_IF_EQ_ZERO A &jiez_halt_1

    SET B #443
    JUMP_IF_EQ_ZERO B &jiez_halt_2

    SET C #7687
    JUMP_IF_EQ_ZERO C &jiez_halt_3

    SET SP #1536
    JUMP_IF_EQ_ZERO SP &jiez_halt_4

    JUMP &jinez_0

&jiez_halt_0
    HALT
&jiez_halt_1
    HALT
&jiez_halt_2
    HALT
&jiez_halt_3
    HALT
&jiez_halt_4
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
    JUMP_IF_NEQ_ZERO SP &jinez_5
    HALT

&jinez_5
    SET_ZERO ACC
    JUMP_IF_NEQ_ZERO ACC &jinez_halt_0

    SET_ZERO A
    JUMP_IF_NEQ_ZERO A &jinez_halt_1

    SET_ZERO B
    JUMP_IF_NEQ_ZERO B &jinez_halt_2

    SET_ZERO C
    JUMP_IF_NEQ_ZERO C &jinez_halt_3

    SET_ZERO SP
    JUMP_IF_NEQ_ZERO SP &jinez_halt_4

    JUMP &jiae_0

&jinez_halt_0
    HALT
&jinez_halt_1
    HALT
&jinez_halt_2
    HALT
&jinez_halt_3
    HALT
&jinez_halt_4
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
    JUMP_IF_ACC_EQ #60123 &jiane_5
    HALT

&jiae_5
    SET ACC #123
    SET A #345
    JUMP_IF_ACC_EQ A &jiae_halt_0
    
    SET ACC #456
    SET B #11111
    JUMP_IF_ACC_EQ B &jiae_halt_1

    SET ACC #789
    SET C #477
    JUMP_IF_ACC_EQ C &jiae_halt_2

    SET ACC #1011
    SET SP #4524
    JUMP_IF_ACC_EQ SP &jiae_halt_3

    SET ACC #60123
    JUMP_IF_ACC_EQ #999 &jiae_halt_4
    
    JUMP &jiane_0

&jiae_halt_0
    HALT
&jiae_halt_1
    HALT
&jiae_halt_2
    HALT
&jiae_halt_3
    HALT
&jiae_halt_4
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
    SET C #6874
    JUMP_IF_ACC_NEQ C &jiane_3
    HALT

&jiane_3
    SET ACC #3333
    SET SP #4444
    JUMP_IF_ACC_NEQ SP &jiane_4
    HALT

&jiane_4
    SET ACC !one_zero
    JUMP_IF_ACC_NEQ !zero_one &jiane_5
    HALT

&jiane_5
    SET ACC #456
    SET A #456
    JUMP_IF_ACC_NEQ A &jiane_halt_0

    SET ACC #1122
    SET B #1122
    JUMP_IF_ACC_NEQ B &jiane_halt_1

    SET ACC #3333
    SET C #3333
    JUMP_IF_ACC_NEQ C &jiane_halt_2

    SET ACC #5678
    SET SP #5678
    JUMP_IF_ACC_NEQ SP &jiane_halt_3

    SET ACC !one_zero
    JUMP_IF_ACC_NEQ !one_zero &jiane_halt_4
    
    JUMP &jump_0

&jiane_halt_0
    HALT
&jiane_halt_1
    HALT
&jiane_halt_2
    HALT
&jiane_halt_3
    HALT
&jiane_halt_4
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
    SET ACC #4799
    COPY ACC A
    JUMP_IF_ACC_EQ A &copy_1
    HALT

&copy_1
    SET ACC #52686
    COPY ACC B
    JUMP_IF_ACC_EQ B &copy_2
    HALT

&copy_2
    SET ACC #35304
    COPY ACC C
    JUMP_IF_ACC_EQ C &copy_3
    HALT

&copy_3
    SET ACC #36137
    COPY ACC SP
    JUMP_IF_ACC_EQ SP &copy_4
    HALT

&copy_4
    SET A #15993
    COPY A ACC
    JUMP_IF_ACC_EQ #15993 &copy_5
    HALT

&copy_5
    SET A #28834
    SET ACC #28834
    COPY A B
    JUMP_IF_ACC_EQ B &copy_6
    HALT

&copy_6
    SET A #58775
    SET ACC #58775
    COPY A C
    JUMP_IF_ACC_EQ C &copy_7
    HALT

&copy_7
    SET A #60244
    SET ACC #60244
    COPY A SP
    JUMP_IF_ACC_EQ SP &copy_8
    HALT

&copy_8
    SET B #17634
    COPY B ACC
    JUMP_IF_ACC_EQ #17634 &copy_9
    HALT

&copy_9
    SET B #56775
    SET ACC #56775
    COPY B A
    JUMP_IF_ACC_EQ A &copy_10
    HALT

&copy_10
    SET B #59278
    SET ACC #59278
    COPY B C
    JUMP_IF_ACC_EQ C &copy_11
    HALT

&copy_11
    SET B #22164
    SET ACC #22164
    COPY B SP
    JUMP_IF_ACC_EQ SP &copy_12
    HALT

&copy_12
    SET C #48215
    COPY C ACC
    JUMP_IF_ACC_EQ #48215 &copy_13
    HALT

&copy_13
    SET C #10020
    SET ACC #10020
    COPY C A
    JUMP_IF_ACC_EQ A &copy_14
    HALT

&copy_14
    SET C #65463
    SET ACC #65463
    COPY C B
    JUMP_IF_ACC_EQ B &copy_15
    HALT

&copy_15
    SET C #38525
    SET ACC #38525
    COPY C SP
    JUMP_IF_ACC_EQ SP &copy_16
    HALT

&copy_16
    SET SP #47483
    COPY SP ACC
    JUMP_IF_ACC_EQ #47483 &copy_17
    HALT

&copy_17
    SET SP #5944
    SET ACC #5944
    COPY SP A
    JUMP_IF_ACC_EQ A &copy_18
    HALT

&copy_18
    SET SP #57017
    SET ACC #57017
    COPY SP B
    JUMP_IF_ACC_EQ B &copy_19
    HALT

&copy_19
    SET SP #34392
    SET ACC #34392
    COPY SP C
    JUMP_IF_ACC_EQ C &placeholder
    HALT

&placeholder
    JUMP &start