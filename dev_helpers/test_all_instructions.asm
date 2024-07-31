@start
    NOOP

    ////////////////////////////////////////////////////////////////
    // CALL AND RETURN
    ////////////////////////////////////////////////////////////////

    NOOP
    NOOP
    NOOP
    NOOP
    NOOP
    NOOP
    NOOP
    NOOP
&safe_sp
    NOOP
    NOOP
    NOOP
    NOOP
    NOOP
    NOOP
    NOOP


&increment_acc
    INCR ACC
    RETURN
    HALT

&increment_a
    INCR A
    RETURN
    HALT

&call_0
    SET SP &safe_sp
    SET A #0
    SET ACC &increment_a
    CALL ACC
    SET ACC #1
    JUMP_IF_ACC_EQ A &call_1
    HALT

&call_1
    SET ACC #0
    SET A &increment_acc
    CALL A
    JUMP_IF_ACC_EQ #1 &call_2
    HALT

&call_2
    SET ACC #0
    SET B &increment_acc
    CALL B
    JUMP_IF_ACC_EQ #1 &call_3
    HALT

&call_3
    SET ACC #0
    SET C &increment_acc
    CALL C
    JUMP_IF_ACC_EQ #1 &call_4
    HALT

&call_4
    SET ACC #0
    CALL &increment_acc
    JUMP_IF_ACC_EQ #1 &call_end
    HALT

&call_end
    NOOP

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
    SET ACC #555
    COPY ACC SP
    SET_ZERO ACC
    COPY SP ACC
    JUMP_IF_ACC_EQ #555 &copy_4
    HALT

&copy_4
    SET ACC #36
    SET A #36
    COPY ACC X
    SET_ZERO ACC
    COPY X ACC
    JUMP_IF_ACC_EQ A &copy_5
    HALT      

&copy_5
    SET ACC #4456
    SET A #4456
    COPY ACC Y
    SET_ZERO ACC
    COPY Y ACC
    JUMP_IF_ACC_EQ A &copy_6
    HALT 

&copy_7
    SET ACC #1234
    SET A #1234
    COPY ACC Z
    SET_ZERO ACC
    COPY Z ACC
    JUMP_IF_ACC_EQ A &copy_8
    HALT 

&copy_8
    SET A #15993
    COPY A ACC
    JUMP_IF_ACC_EQ #15993 &copy_9
    HALT

&copy_9
    SET A #28834
    SET ACC #28834
    COPY A B
    JUMP_IF_ACC_EQ B &copy_10
    HALT

&copy_10
    SET A #58775
    SET ACC #58775
    COPY A C
    JUMP_IF_ACC_EQ C &copy_11
    HALT

&copy_11
    SET C #48215
    COPY C ACC
    JUMP_IF_ACC_EQ #48215 &copy_12
    HALT

&copy_12
    SET C #10020
    SET ACC #10020
    COPY C A
    JUMP_IF_ACC_EQ A &copy_13
    HALT

&copy_13
    SET C #65463
    SET ACC #65463
    COPY C B
    JUMP_IF_ACC_EQ B &copy_14
    HALT

&copy_13
    COPY PC ACC
&pc_should_be_this
    JUMP_IF_ACC_EQ &pc_should_be_this &copy_end
    HALT

&copy_end
    NOOP

JUMP @start
