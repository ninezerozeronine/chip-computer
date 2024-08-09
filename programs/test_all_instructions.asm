&start
    NOOP

    ////////////////////////////////////////////////////////////////
    // NOOP
    ////////////////////////////////////////////////////////////////

&noop_0
    // NOOP
    NOOP

    ////////////////////////////////////////////////////////////////
    // SET_ZERO
    ////////////////////////////////////////////////////////////////

&set_zero_0
    SET_ZERO ACC
    JUMP_IF_NEQ_ZERO ACC &set_zero_halt0

    SET_ZERO A
    JUMP_IF_NEQ_ZERO A &set_zero_halt1

    SET_ZERO B
    JUMP_IF_NEQ_ZERO B &set_zero_halt2

    SET_ZERO C
    JUMP_IF_NEQ_ZERO C &set_zero_halt3

    JUMP &set_zero_done

&set_zero_halt0
    HALT
&set_zero_halt1
    HALT
&set_zero_halt2
    HALT
&set_zero_halt3
    HALT

&set_zero_done
    NOOP

    ////////////////////////////////////////////////////////////////
    // SET
    ////////////////////////////////////////////////////////////////

&set_0
    SET ACC #32642
    SET A #32642
    JUMP_IF_ACC_NEQ A &set_halt0

    SET ACC #9878
    SET B #9878
    JUMP_IF_ACC_NEQ B &set_halt1

    SET ACC #1234
    SET C #1234
    JUMP_IF_ACC_NEQ C &set_halt2   

    SET SP #4321
    COPY SP ACC
    JUMP_IF_ACC_NEQ #4321 &set_halt3

    JUMP &set_done

&set_halt0
    HALT
&set_halt1
    HALT
&set_halt2
    HALT
&set_halt3
    HALT

&set_done
    NOOP

    ////////////////////////////////////////////////////////////////
    // ADD
    ////////////////////////////////////////////////////////////////

&add_0
    SET ACC #1
    SET A #2
    ADD A
    JUMP_IF_ACC_EQ #3 &add_1
    HALT

&add_1
    SET ACC #456
    SET B #111
    ADD B
    JUMP_IF_ACC_EQ #567 &add_2
    HALT

&add_2
    SET ACC #3333
    SET C #2222
    ADD C
    JUMP_IF_ACC_EQ #5555 &add_3
    HALT

&add_3
    SET ACC #123
    ADD #-23
    JUMP_IF_ACC_EQ #100 &add_4
    HALT

$v_add_0 #42
&add_4
    SET ACC #42
    ADD [$v_add_0]
    JUMP_IF_ACC_EQ #84 &add_5
    HALT

&add_5
    // Test carry flag
    SET ACC #60000
    ADD #60000
    JUMP_IF_CARRY &add_6
    HALT

&add_6
    // Test no carry flag
    SET ACC #5
    ADD #10
    JUMP_IF_NOT_CARRY &sub_0
    HALT

    ////////////////////////////////////////////////////////////////
    // SUB
    ////////////////////////////////////////////////////////////////

&sub_0
    SET ACC #1
    SET A #2
    SUB A
    JUMP_IF_ACC_EQ #-1 &sub_1
    HALT

&sub_1
    SET ACC #456
    SET B #111
    SUB B
    JUMP_IF_ACC_EQ #345 &sub_2
    HALT

&sub_2
    SET ACC #3333
    SET C #2222
    SUB C
    JUMP_IF_ACC_EQ #1111 &sub_3
    HALT

&sub_3
    SET_ZERO ACC
    SUB #1
    JUMP_IF_ACC_EQ #0xFFFF &sub_4
    HALT

$v_sub_0 #42
&sub_4
    SET ACC #42
    SUB [$v_sub_0]
    JUMP_IF_EQ_ZERO ACC &sub_5
    HALT

&sub_5
    // Test borrow flag
    SET ACC #34
    SUB #500
    JUMP_IF_BORROW &sub_6
    HALT

&sub_6
    // Test no carry flag
    SET ACC #34
    SUB #3
    JUMP_IF_NOT_BORROW &and_0
    HALT

    ////////////////////////////////////////////////////////////////
    // AND
    ////////////////////////////////////////////////////////////////

&and_0
    SET ACC        #0b1111
    SET A          #0b0101
    AND A
    JUMP_IF_ACC_EQ #0b0101 &and_1
    HALT

&and_1
    SET ACC        #0b1111_0000_1111_0000
    SET B          #0b1111_1111_1111_1111
    AND B
    JUMP_IF_ACC_EQ #0b1111_0000_1111_0000 &and_2
    HALT

&and_2
    SET ACC        #0b1100_1111
    SET C          #0b0000_0000
    AND C
    JUMP_IF_ACC_EQ #0b0000_0000 &and_3
    HALT

&and_3
    SET ACC        #0b0011_1100_1111_0000
    AND            #0b1111_1111_0000_1111
    JUMP_IF_ACC_EQ #0b0011_1100_0000_0000 &and_4
    HALT

$v_and_0           #0b1
&and_4
    SET ACC        #0b1
    AND [$v_and_0]
    JUMP_IF_ACC_EQ #0b1 &nand_0
    HALT

    ////////////////////////////////////////////////////////////////
    // NAND
    ////////////////////////////////////////////////////////////////

&nand_0
    SET ACC        #0b0000_0000_0000_1111
    SET A          #0b1111_1111_1111_0101
    NAND A
    JUMP_IF_ACC_EQ #0b1111_1111_1111_1010 &nand_1
    HALT

&nand_1
    SET ACC        #0b1111_0000_1111_0000
    SET B          #0b1111_1111_1111_1111
    NAND B
    JUMP_IF_ACC_EQ #0b0000_1111_0000_1111 &nand_2
    HALT

&nand_2
    SET ACC        #0b1111_1111_1100_1111
    SET C          #0b1111_1111_0000_0000
    NAND C
    JUMP_IF_ACC_EQ #0b0000_0000_1111_1111 &nand_3
    HALT

&nand_3
    SET ACC        #0b0011_1100_1111_0000
    NAND           #0b1111_1111_0000_1111
    JUMP_IF_ACC_EQ #0b1100_0011_1111_1111 &nand_4
    HALT

$v_nand_0          #0b0000_0000_0000_0001
&nand_4
    SET ACC        #0b0000_0000_0000_0001
    NAND [$v_nand_0]
    JUMP_IF_ACC_EQ #0b1111_1111_1111_1110 &or_0
    HALT

    ////////////////////////////////////////////////////////////////
    // OR
    ////////////////////////////////////////////////////////////////

&or_0
    SET ACC        #0b1111
    SET A          #0b0101
    OR A
    JUMP_IF_ACC_EQ #0b1111 &or_1
    HALT

&or_1
    SET ACC        #0b1111_0000_1111_0000
    SET B          #0b1111_1111_1111_1111
    OR B
    JUMP_IF_ACC_EQ #0b1111_1111_1111_1111 &or_2
    HALT

&or_2
    SET ACC        #0b1100_1111
    SET C          #0b0000_0000
    OR C
    JUMP_IF_ACC_EQ #0b1100_1111 &or_3
    HALT

&or_3
    SET ACC        #0b0011_1100_1111_0000
    OR             #0b1111_1111_0000_1111
    JUMP_IF_ACC_EQ #0b1111_1111_1111_1111 &or_4
    HALT

$v_or_0            #0b1
&or_4
    SET ACC        #0b1
    OR [$v_or_0]
    JUMP_IF_ACC_EQ #0b1 &nor_0
    HALT

    ////////////////////////////////////////////////////////////////
    // NOR
    ////////////////////////////////////////////////////////////////

&nor_0
    SET ACC        #0b1111_0101_0000_1111
    SET A          #0b0010_0010_1111_0101
    NOR A
    JUMP_IF_ACC_EQ #0b0000_1000_0000_0000 &nor_1
    HALT

&nor_1
    SET ACC        #0b1111_0000_1111_0000
    SET B          #0b1111_1111_1111_1111
    NOR B
    JUMP_IF_ACC_EQ #0b0000_0000_0000_0000 &nor_2
    HALT

&nor_2
    SET ACC        #0b0000_0000_1100_1111
    SET C          #0b0000_1111_0000_0000
    NOR C
    JUMP_IF_ACC_EQ #0b1111_0000_0011_0000 &nor_3
    HALT

&nor_3
    SET ACC        #0b0011_1100_1111_0000
    NOR            #0b0111_1110_0000_1110
    JUMP_IF_ACC_EQ #0b1000_0001_0000_0001 &nor_4
    HALT

$v_nor_0           #0b0100_0000_0000_0001
&nor_4
    SET ACC        #0b0000_0010_0000_0001
    NOR [$v_nor_0]
    JUMP_IF_ACC_EQ #0b1011_1101_1111_1110 &xor_0
    HALT

    ////////////////////////////////////////////////////////////////
    // XOR
    ////////////////////////////////////////////////////////////////

&xor_0
    SET ACC        #0b1111
    SET A          #0b0101
    XOR A
    JUMP_IF_ACC_EQ #0b1010 &xor_1
    HALT

&xor_1
    SET ACC        #0b0011
    SET B          #0b0101
    XOR B
    JUMP_IF_ACC_EQ #0b0110 &xor_2
    HALT

&xor_2
    SET ACC        #0b1100_1111
    SET C          #0b0000_0000
    XOR C
    JUMP_IF_ACC_EQ #0b1100_1111 &xor_3
    HALT

&xor_3
    SET ACC        #0b0011_1100_1011_0001
    XOR            #0b1111_1111_0000_1111
    JUMP_IF_ACC_EQ #0b1100_0011_1011_1110 &xor_4
    HALT

$v_xor_0           #0b1
&xor_4
    SET ACC        #0b1
    XOR [$v_xor_0]
    JUMP_IF_ACC_EQ #0b0 &nxor_0
    HALT

    ////////////////////////////////////////////////////////////////
    // NXOR
    ////////////////////////////////////////////////////////////////

&nxor_0
    SET ACC        #0b1111_1111_1111_1111
    SET A          #0b0000_0000_0000_0101
    NXOR A
    JUMP_IF_ACC_EQ #0b0000_0000_0000_0101 &nxor_1
    HALT

&nxor_1
    SET ACC        #0b1111_1111_1111_0011
    SET B          #0b1111_1111_1111_0101
    NXOR B
    JUMP_IF_ACC_EQ #0b1111_1111_1111_1001 &nxor_2
    HALT

&nxor_2
    SET ACC        #0b0111_1100_1100_1111
    SET C          #0b1011_0000_0000_0000
    NXOR C
    JUMP_IF_ACC_EQ #0b0011_0011_0011_0000 &nxor_3
    HALT

&nxor_3
    SET ACC        #0b0011_1100_1011_0001
    NXOR           #0b1111_1111_0000_1111
    JUMP_IF_ACC_EQ #0b0011_1100_0100_0001 &nxor_4
    HALT

$v_nxor_0          #0b1110_1111_1110_1111
&nxor_4
    SET ACC        #0b1111_1110_1110_1111
    NXOR [$v_nxor_0]
    JUMP_IF_ACC_EQ #0b1110_1110_1111_1111 &nxor_done
    HALT

&nxor_done
    NOOP

    ////////////////////////////////////////////////////////////////
    // HALT
    ////////////////////////////////////////////////////////////////

// It's hard to test a HALT!

    ////////////////////////////////////////////////////////////////
    // COPY
    ////////////////////////////////////////////////////////////////

    // COPY ACC A
&copy_0
    SET ACC #4799
    COPY ACC A
    JUMP_IF_ACC_EQ A &copy_1
    HALT

    // COPY ACC B
&copy_1
    SET ACC #52686
    COPY ACC B
    JUMP_IF_ACC_EQ B &copy_2
    HALT

    // COPY ACC C
&copy_2
    SET ACC #35304
    COPY ACC C
    JUMP_IF_ACC_EQ C &copy_3
    HALT

    // COPY ACC SP
    // COPY SP ACC
&copy_3
    SET ACC #555
    COPY ACC SP
    SET_ZERO ACC
    COPY SP ACC
    JUMP_IF_ACC_EQ #555 &copy_4
    HALT

    // COPY ACC X
    // COPY X ACC
&copy_4
    SET ACC #36
    SET A #36
    COPY ACC X
    SET_ZERO ACC
    COPY X ACC
    JUMP_IF_ACC_EQ A &copy_5
    HALT      

    // COPY ACC Y
    // COPY Y ACC
&copy_5
    SET ACC #4456
    SET A #4456
    COPY ACC Y
    SET_ZERO ACC
    COPY Y ACC
    JUMP_IF_ACC_EQ A &copy_7
    HALT 

    // COPY ACC Z
    // COPY Z ACC
&copy_7
    SET ACC #1234
    SET A #1234
    COPY ACC Z
    SET_ZERO ACC
    COPY Z ACC
    JUMP_IF_ACC_EQ A &copy_8
    HALT 

    // COPY A ACC
&copy_8
    SET A #15993
    COPY A ACC
    JUMP_IF_ACC_EQ #15993 &copy_9
    HALT

    // COPY A B
&copy_9
    SET A #28834
    SET ACC #28834
    COPY A B
    JUMP_IF_ACC_EQ B &copy_10
    HALT

    // COPY A C
&copy_10
    SET A #58775
    SET ACC #58775
    COPY A C
    JUMP_IF_ACC_EQ C &copy_11
    HALT

    // COPY B ACC
&copy_11
    SET B #15993
    COPY B ACC
    JUMP_IF_ACC_EQ #15993 &copy_12
    HALT

    // COPY B A
&copy_12
    SET ACC #145
    SET B #145
    COPY B A
    JUMP_IF_ACC_EQ A &copy_13
    HALT

    // COPY B C
&copy_13
    SET ACC #58775
    SET B #58775
    COPY B C
    JUMP_IF_ACC_EQ C &copy_14
    HALT

    // COPY C ACC
&copy_14
    SET C #48215
    COPY C ACC
    JUMP_IF_ACC_EQ #48215 &copy_15
    HALT

    // COPY C A
&copy_15
    SET C #10020
    SET ACC #10020
    COPY C A
    JUMP_IF_ACC_EQ A &copy_16
    HALT

    // COPY C B
&copy_16
    SET C #65463
    SET ACC #65463
    COPY C B
    JUMP_IF_ACC_EQ B &copy_17
    HALT

    // COPY PC ACC
&copy_17
    COPY PC ACC
&pc_should_be_this
    JUMP_IF_ACC_EQ &pc_should_be_this &copy_end
    HALT

&copy_end
    NOOP

    ////////////////////////////////////////////////////////////////
    // JUMP_IF_EQ_ZERO
    ////////////////////////////////////////////////////////////////

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
    SET ACC #1
    JUMP_IF_EQ_ZERO ACC &jiez_halt_0

    SET A #58767
    JUMP_IF_EQ_ZERO A &jiez_halt_1

    SET B #443
    JUMP_IF_EQ_ZERO B &jiez_halt_2

    SET C #7687
    JUMP_IF_EQ_ZERO C &jiez_halt_3

    JUMP &jinez_0

&jiez_halt_0
    NOOP
    NOOP
    HALT
    NOOP
    NOOP
&jiez_halt_1
    NOOP
    NOOP
    HALT
    NOOP
    NOOP
&jiez_halt_2
    NOOP
    NOOP
    HALT
    NOOP
    NOOP
&jiez_halt_3
    NOOP
    NOOP
    HALT
    NOOP
    NOOP

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
    SET_ZERO ACC
    JUMP_IF_NEQ_ZERO ACC &jinez_halt_0

    SET_ZERO A
    JUMP_IF_NEQ_ZERO A &jinez_halt_1

    SET_ZERO B
    JUMP_IF_NEQ_ZERO B &jinez_halt_2

    SET_ZERO C
    JUMP_IF_NEQ_ZERO C &jinez_halt_3

    JUMP &jinez_done

&jinez_halt_0
    NOOP
    NOOP
    HALT
    NOOP
    NOOP
&jinez_halt_1
    NOOP
    NOOP
    HALT
    NOOP
    NOOP
&jinez_halt_2
    NOOP
    NOOP
    HALT
    NOOP
    NOOP
&jinez_halt_3
    NOOP
    NOOP
    HALT
    NOOP
    NOOP

&jinez_done
    NOOP

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
    SET ACC #60123
    JUMP_IF_ACC_EQ #60123 &jiae_4
    HALT

$v_jiae_0 #37
&jiae_4
    SET ACC #37
    JUMP_IF_ACC_EQ [$v_jiae_0] &jiae_5
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
    JUMP_IF_ACC_EQ #999 &jiae_halt_3
    JUMP &jiae_6

$v_jiae_1 #37
&jiae_6
    SET ACC #60123
    JUMP_IF_ACC_EQ [$v_jiae_1] &jiae_halt_4

    JUMP &jiane_0

&jiae_halt_0
    NOOP
    NOOP
    HALT
    NOOP
    NOOP
&jiae_halt_1
    NOOP
    NOOP
    HALT
    NOOP
    NOOP
&jiae_halt_2
    NOOP
    NOOP
    HALT
    NOOP
    NOOP
&jiae_halt_3
    NOOP
    NOOP
    HALT
    NOOP
    NOOP
&jiae_halt_4
    NOOP
    NOOP
    HALT
    NOOP
    NOOP

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
    SET ACC #34
    JUMP_IF_ACC_NEQ #0xFFFF &jiane_4
    HALT

$v_jiane_0 #12345
&jiane_4
    SET ACC #48143
    JUMP_IF_ACC_NEQ [$v_jiane_0] &jiane_5
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

    SET ACC #3345
    JUMP_IF_ACC_NEQ #3345 &jiane_halt_3
    JUMP &jiane_6

$v_jiane_1 #12345
&jiane_6
    SET ACC #12345
    JUMP_IF_ACC_NEQ [$v_jiane_1] &jiane_halt_4

    JUMP &jiane_done

&jiane_halt_0
    NOOP
    NOOP
    HALT
    NOOP
    NOOP
&jiane_halt_1
    NOOP
    NOOP
    HALT
    NOOP
    NOOP
&jiane_halt_2
    NOOP
    NOOP
    HALT
    NOOP
    NOOP
&jiane_halt_3
    NOOP
    NOOP
    HALT
    NOOP
    NOOP
&jiane_halt_4
    NOOP
    NOOP
    HALT
    NOOP
    NOOP

&jiane_done
    NOOP

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
    SET C &jump_5
    JUMP C
    HALT

&jump_5
    JUMP &jump_6
    HALT

$v_jump_0 &jump7
&jump_6
    SET ACC $v_jump_0
    JUMP [ACC]
    HALT

$v_jump_1 &jump8
&jump7
    SET A $v_jump_1
    JUMP [A]
    HALT

$v_jump_2 &jump9
&jump8
    SET B $v_jump_2
    JUMP [B]
    HALT

$v_jump_3 &jump11
&jump9
    SET C $v_jump_3
    JUMP [C]
    HALT

$v_jump_5 &jump_done
&jump11
    JUMP [$v_jump_5]
    HALT

&jump_done
    NOOP

    ////////////////////////////////////////////////////////////////
    // INCR
    ////////////////////////////////////////////////////////////////

// INCR ACC
&incr_0
    SET ACC #32
    INCR ACC 
    JUMP_IF_ACC_EQ #33 &incr_1
    HALT

// INCR A
&incr_1
    SET ACC #-31
    SET A #-32
    INCR A
    JUMP_IF_ACC_EQ A &incr_2
    HALT

// INCR B
&incr_2
    SET ACC #256
    SET B #255
    INCR B
    JUMP_IF_ACC_EQ B &incr_3
    HALT

// INCR C
&incr_3
    SET ACC #0
    SET C #0xFFFF
    INCR C
    JUMP_IF_ACC_EQ C &incr_4
    HALT

// INCR M_CONST
$incr_const_1 #35
&incr_4
    INCR [$incr_const_1]
    LOAD [$incr_const_1] ACC
    JUMP_IF_ACC_EQ #36 &incr_5
    HALT

// INCR M_CONST (carry flag)
$incr_const_2 #0b1111_1111_1111_1111
&incr_5
    INCR [$incr_const_2]
    JUMP_IF_CARRY &decr_0
    HALT

    ////////////////////////////////////////////////////////////////
    // DECR
    ////////////////////////////////////////////////////////////////

// DECR ACC
&decr_0
    SET ACC #32
    DECR ACC 
    JUMP_IF_ACC_EQ #31 &decr_1
    HALT

// DECR A
&decr_1
    SET ACC #-33
    SET A #-32
    DECR A
    JUMP_IF_ACC_EQ A &decr_2
    HALT

// DECR B
&decr_2
    SET ACC #255
    SET B #256
    DECR B
    JUMP_IF_ACC_EQ B &decr_3
    HALT

// DECR C
&decr_3
    SET ACC #0xFFFF
    SET C #0
    DECR C
    JUMP_IF_ACC_EQ C &decr_4
    HALT

// DECR M_CONST
$decr_const_1 #50
&decr_4
    DECR [$decr_const_1]
    LOAD [$decr_const_1] ACC
    JUMP_IF_ACC_EQ #49 &decr_5
    HALT

// DECR M_CONST (borrow flag)
$decr_const_2 #0
&decr_5
    DECR [$decr_const_2]
    JUMP_IF_BORROW &decr_end
    HALT

&decr_end
    NOOP

    ////////////////////////////////////////////////////////////////
    // LOAD
    ////////////////////////////////////////////////////////////////

&load_0
    NOOP

$v_load_1 #11709
&load_1
    SET ACC $v_load_1
    LOAD [ACC] A
    SET ACC #11709
    JUMP_IF_ACC_EQ A &load_2
    HALT

$v_load_2 #59692
&load_2
    SET ACC $v_load_2
    LOAD [ACC] B
    SET ACC #59692
    JUMP_IF_ACC_EQ B &load_3
    HALT

$v_load_3 #12087
&load_3
    SET ACC $v_load_3
    LOAD [ACC] C
    SET ACC #12087
    JUMP_IF_ACC_EQ C &load_4
    HALT

$v_load_4 #20982
&load_4
    SET A $v_load_4
    LOAD [A] ACC
    JUMP_IF_ACC_EQ #20982 &load_5
    HALT

&load_5
    NOOP

$v_load_6 #22009
&load_6
    SET A $v_load_6
    LOAD [A] B
    SET ACC #22009
    JUMP_IF_ACC_EQ B &load_7
    HALT

$v_load_7 #11703
&load_7
    SET A $v_load_7
    LOAD [A] C
    SET ACC #11703
    JUMP_IF_ACC_EQ C &load_8
    HALT

$v_load_8 #57854
&load_8
    SET B $v_load_8
    LOAD [B] ACC
    JUMP_IF_ACC_EQ #57854 &load_9
    HALT

$v_load_9 #37360
&load_9
    SET B $v_load_9
    LOAD [B] A
    SET ACC #37360
    JUMP_IF_ACC_EQ A &load_10
    HALT

&load_10
    NOOP

$v_load_11 #60912
&load_11
    SET B $v_load_11
    LOAD [B] C
    SET ACC #60912
    JUMP_IF_ACC_EQ C &load_12
    HALT

$v_load_12 #38245
&load_12
    SET C $v_load_12
    LOAD [C] ACC
    JUMP_IF_ACC_EQ #38245 &load_13
    HALT

$v_load_13 #25454
&load_13
    SET C $v_load_13
    LOAD [C] A
    SET ACC #25454
    JUMP_IF_ACC_EQ A &load_14
    HALT

$v_load_14 #25444
&load_14
    SET C $v_load_14
    LOAD [C] B
    SET ACC #25444
    JUMP_IF_ACC_EQ B &load_15
    HALT

&load_15
    NOOP

$v_load_16 #60336
&load_16
    SET SP $v_load_16
    LOAD [SP] ACC
    JUMP_IF_ACC_EQ #60336 &load_17
    HALT

$v_load_17 #56769
&load_17
    SET SP $v_load_17
    LOAD [SP] A
    SET ACC #56769
    JUMP_IF_ACC_EQ A &load_18
    HALT

$v_load_18 #49044
&load_18
    SET SP $v_load_18
    LOAD [SP] B
    SET ACC #49044
    JUMP_IF_ACC_EQ B &load_19
    HALT

$v_load_19 #34177
&load_19
    SET SP $v_load_19
    LOAD [SP] C
    SET ACC #34177
    JUMP_IF_ACC_EQ C &load_20
    HALT

$v_load_20 #56580
&load_20
    LOAD [$v_load_20] ACC
    JUMP_IF_ACC_EQ #56580 &load_21
    HALT

$v_load_21 #47253
&load_21
    LOAD [$v_load_21] A
    SET ACC #47253
    JUMP_IF_ACC_EQ A &load_22
    HALT

$v_load_22 #55439
&load_22
    LOAD [$v_load_22] B
    SET ACC #55439
    JUMP_IF_ACC_EQ B &load_23
    HALT

$v_load_23 #7661
&load_23
    LOAD [$v_load_23] C
    SET ACC #7661
    JUMP_IF_ACC_EQ C &store_0
    HALT

    ////////////////////////////////////////////////////////////////
    // STORE
    ////////////////////////////////////////////////////////////////

&store_0
    NOOP

$v_store_1
&store_1
    SET ACC #31763
    SET A $v_store_1
    STORE ACC [A]
    LOAD [A] ACC
    JUMP_IF_ACC_EQ #31763 &store_2
    HALT

$v_store_2
&store_2
    SET ACC #35606
    SET B $v_store_2
    STORE ACC [B]
    LOAD [B] ACC
    JUMP_IF_ACC_EQ #35606 &store_3
    HALT

$v_store_3
&store_3
    SET ACC #27292
    SET C $v_store_3
    STORE ACC [C]
    LOAD [C] ACC
    JUMP_IF_ACC_EQ #27292 &store_4
    HALT

$v_store_4
&store_4
    SET ACC #13156
    SET SP $v_store_4
    STORE ACC [SP]
    LOAD [SP] ACC
    JUMP_IF_ACC_EQ #13156 &store_5
    HALT

$v_store_5
&store_5
    SET ACC #36181
    STORE ACC [$v_store_5]
    LOAD [$v_store_5] ACC
    JUMP_IF_ACC_EQ #36181 &store_6
    HALT

$v_store_6
&store_6
    SET A #11935
    SET ACC $v_store_6
    STORE A [ACC]
    LOAD [ACC] B
    COPY B ACC
    JUMP_IF_ACC_EQ #11935 &store_7
    HALT

&store_7
    NOOP

$v_store_8
&store_8
    SET A #27215
    SET B $v_store_8
    STORE A [B]
    LOAD [B] ACC
    JUMP_IF_ACC_EQ #27215 &store_9
    HALT

$v_store_9
&store_9
    SET A #31533
    SET C $v_store_9
    STORE A [C]
    LOAD [C] ACC
    JUMP_IF_ACC_EQ #31533 &store_10
    HALT

$v_store_10
&store_10
    SET A #65214
    SET SP $v_store_10
    STORE A [SP]
    LOAD [SP] ACC
    JUMP_IF_ACC_EQ #65214 &store_11
    HALT

$v_store_11
&store_11
    SET A #25149
    STORE A [$v_store_11]
    LOAD [$v_store_11] ACC
    JUMP_IF_ACC_EQ #25149 &store_12
    HALT

$v_store_12
&store_12
    SET B #61844
    SET ACC $v_store_12
    STORE B [ACC]
    LOAD [ACC] A
    COPY A ACC
    JUMP_IF_ACC_EQ #61844 &store_13
    HALT

$v_store_13
&store_13
    SET B #22749
    SET A $v_store_13
    STORE B [A]
    LOAD [A] ACC
    JUMP_IF_ACC_EQ #22749 &store_14
    HALT

&store_14
    NOOP

$v_store_15
&store_15
    SET B #21277
    SET C $v_store_15
    STORE B [C]
    LOAD [C] ACC
    JUMP_IF_ACC_EQ #21277 &store_16
    HALT

$v_store_16
&store_16
    SET B #64660
    SET SP $v_store_16
    STORE B [SP]
    LOAD [SP] ACC
    JUMP_IF_ACC_EQ #64660 &store_17
    HALT

$v_store_17
&store_17
    SET B #54157
    STORE B [$v_store_17]
    LOAD [$v_store_17] ACC
    JUMP_IF_ACC_EQ #54157 &store_18
    HALT

$v_store_18
&store_18
    SET C #46522
    SET ACC $v_store_18
    STORE C [ACC]
    LOAD [ACC] A
    COPY A ACC
    JUMP_IF_ACC_EQ #46522 &store_19
    HALT

$v_store_19
&store_19
    SET C #7117
    SET A $v_store_19
    STORE C [A]
    LOAD [A] ACC
    JUMP_IF_ACC_EQ #7117 &store_20
    HALT

$v_store_20
&store_20
    SET C #49497
    SET B $v_store_20
    STORE C [B]
    LOAD [B] ACC
    JUMP_IF_ACC_EQ #49497 &store_21
    HALT

&store_21
    NOOP

$v_store_22
&store_22
    SET C #12486
    SET SP $v_store_22
    STORE C [SP]
    LOAD [SP] ACC
    JUMP_IF_ACC_EQ #12486 &store_23
    HALT

$v_store_23
&store_23
    SET C #63220
    STORE C [$v_store_23]
    LOAD [$v_store_23] ACC
    JUMP_IF_ACC_EQ #63220 &store_done
    HALT

&store_done
    NOOP

    ////////////////////////////////////////////////////////////////
    // PUSH
    ////////////////////////////////////////////////////////////////

&push_0
    NOOP
    NOOP
    NOOP
&push_1
    NOOP
    NOOP
    NOOP
    SET SP &push_1    

    SET ACC #567
    PUSH ACC
    SET_ZERO ACC
    LOAD [SP] ACC
    JUMP_IF_ACC_EQ #567 &push_2
    HALT

&push_2
    SET SP &push_1 
    SET A #123
    PUSH A
    LOAD [SP] ACC
    JUMP_IF_ACC_EQ #123 &push_3
    HALT

&push_3
    SET SP &push_1 
    SET B #333
    PUSH B
    LOAD [SP] ACC
    JUMP_IF_ACC_EQ #333 &push_4
    HALT

&push_4
    SET SP &push_1 
    SET C #22341
    PUSH C
    LOAD [SP] ACC
    JUMP_IF_ACC_EQ #22341 &pop_0
    HALT

    ////////////////////////////////////////////////////////////////
    // POP
    ////////////////////////////////////////////////////////////////

&pop_0
    NOOP
    NOOP
&pop_1
    NOOP
    NOOP
    NOOP
    SET SP &pop_1    

    SET ACC #6381
    PUSH ACC
    SET_ZERO ACC
    LOAD [SP] ACC
    JUMP_IF_ACC_EQ #6381 &pop_2
    HALT

&pop_2
    SET SP &pop_1 
    SET A #5681
    PUSH A
    LOAD [SP] ACC
    JUMP_IF_ACC_EQ #5681 &pop_3
    HALT

&pop_3
    SET SP &pop_1 
    SET B #22222
    PUSH B
    LOAD [SP] ACC
    JUMP_IF_ACC_EQ #22222 &pop_4
    HALT

&pop_4
    SET SP &pop_1 
    SET C #4242
    PUSH C
    LOAD [SP] ACC
    JUMP_IF_ACC_EQ #4242 &pop_done
    HALT

&pop_done
    NOOP

    ////////////////////////////////////////////////////////////////
    // NOT
    ////////////////////////////////////////////////////////////////

&not_0
    SET ACC        #0b1001_0100_0011_1111
    NOT ACC
    JUMP_IF_ACC_EQ #0b0110_1011_1100_0000 &not_1
    HALT

&not_1
    SET A   #0b1010_1010_0101_0101
    SET ACC #0b0101_0101_1010_1010
    NOT A
    JUMP_IF_ACC_EQ A &not_2
    HALT

&not_2
    SET B   #0b1111_1111_1111_1111
    SET ACC #0b0000_0000_0000_0000
    NOT B
    JUMP_IF_ACC_EQ B &not_3
    HALT

&not_3
    SET C   #0b0000_0000_0000_0000
    SET ACC #0b1111_1111_1111_1111
    NOT C
    JUMP_IF_ACC_EQ C &not_4
    HALT

$v_not_0 #0b1111_0000_0101_1010
&not_4
    NOT [$v_not_0]
    LOAD [$v_not_0] ACC
    JUMP_IF_ACC_EQ #0b0000_1111_1010_0101 &not_done
    HALT

&not_done
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

    JUMP &call_0

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
    // JUMP_IF_ACC_LT
    ////////////////////////////////////////////////////////////////

    // Test true cases
    // JUMP_IF_ACC_LT A CONST (true)
&jialt_0
    SET A #12
    SET ACC #2
    JUMP_IF_ACC_LT A &jialt_1
    HALT

    // JUMP_IF_ACC_LT B CONST (true)
&jialt_1
    SET B #123
    SET ACC #0
    JUMP_IF_ACC_LT B &jialt_2
    HALT

    // JUMP_IF_ACC_LT C CONST (true)
&jialt_2
    SET C #12345
    SET ACC #1234
    JUMP_IF_ACC_LT C &jialt_3
    HALT

    // JUMP_IF_ACC_LT CONST CONST (true)
&jialt_3
    SET ACC #1000
    JUMP_IF_ACC_LT #1001 &jialt_4
    HALT

    // JUMP_IF_ACC_LT M_CONST CONST (true)
$v_jialt_const_1 #456
&jialt_4
    SET ACC #13
    JUMP_IF_ACC_LT [$v_jialt_const_1] &jialt_5
    HALT

    // Test false cases
&jialt_5
    // JUMP_IF_ACC_LT A CONST (false)
    SET A #2
    SET ACC #2
    JUMP_IF_ACC_LT A &jialt_halt_0

    // JUMP_IF_ACC_LT B CONST (false)
    SET B #1
    SET ACC #123
    JUMP_IF_ACC_LT B &jialt_halt_1

    // JUMP_IF_ACC_LT C CONST (false)
    SET C #123
    SET ACC #12345
    JUMP_IF_ACC_LT C &jialt_halt_2

    // JUMP_IF_ACC_LT CONST CONST (false)
    SET ACC #1001
    JUMP_IF_ACC_LT #1000 &jialt_halt_3
    JUMP &jialt_6

    // JUMP_IF_ACC_LT M_CONST CONST (false)
$v_jialt_const_2 #113
&jialt_6
    SET ACC #200
    JUMP_IF_ACC_LT [$v_jialt_const_2] &jialt_halt_4
    JUMP &jialte_0

&jialt_halt_0
    NOOP
    NOOP
    HALT
    NOOP
    NOOP
&jialt_halt_1
    NOOP
    NOOP
    HALT
    NOOP
    NOOP
&jialt_halt_2
    NOOP
    NOOP
    HALT
    NOOP
    NOOP
&jialt_halt_3
    NOOP
    NOOP
    HALT
    NOOP
    NOOP
&jialt_halt_4
    NOOP
    NOOP
    HALT
    NOOP
    NOOP

    ////////////////////////////////////////////////////////////////
    // JUMP_IF_ACC_LTE
    ////////////////////////////////////////////////////////////////

    // Test true cases
    // JUMP_IF_ACC_LTE A CONST (less than, true)
&jialte_0
    SET A #12
    SET ACC #2
    JUMP_IF_ACC_LTE A &jialte_1
    HALT

    // JUMP_IF_ACC_LTE A CONST (equal to, true)
&jialte_1
    SET A #123
    SET ACC #123
    JUMP_IF_ACC_LTE A &jialte_2
    HALT

    // JUMP_IF_ACC_LTE B CONST (less than, true)
&jialte_2
    SET B #12345
    SET ACC #1234
    JUMP_IF_ACC_LTE B &jialte_3
    HALT

    // JUMP_IF_ACC_LTE B CONST (equal to, true)
&jialte_3
    SET B #6000
    SET ACC #6000
    JUMP_IF_ACC_LTE B &jialte_4
    HALT

    // JUMP_IF_ACC_LTE C CONST (less than, true)
&jialte_4
    SET C #12345
    SET ACC #1234
    JUMP_IF_ACC_LTE C &jialte_5
    HALT

    // JUMP_IF_ACC_LTE C CONST (equal to, true)
&jialte_5
    SET C #4321
    SET ACC #4321
    JUMP_IF_ACC_LTE C &jialte_6
    HALT

    // JUMP_IF_ACC_LTE CONST CONST (less than, true)
&jialte_6
    SET ACC #1000
    JUMP_IF_ACC_LTE #1001 &jialte_7
    HALT

    // JUMP_IF_ACC_LTE CONST CONST (equal to, true)
&jialte_7
    SET ACC #1111
    JUMP_IF_ACC_LTE #1111 &jialte_8
    HALT

    // JUMP_IF_ACC_LTE M_CONST CONST (less than, true)
$v_jialte_const_1 #113
&jialte_8
    SET ACC #10
    JUMP_IF_ACC_LTE [$v_jialte_const_1] &jialte_9
    HALT

    // JUMP_IF_ACC_LTE M_CONST CONST (equal to, true)
$v_jialte_const_2 #4444
&jialte_9
    SET ACC #4444
    JUMP_IF_ACC_LTE [$v_jialte_const_2] &jialte_10
    HALT

    // Test false cases
&jialte_10
    // JUMP_IF_ACC_LTE A CONST (false)
    SET A #2
    SET ACC #12
    JUMP_IF_ACC_LTE A &jialte_halt_0

    // JUMP_IF_ACC_LTE B CONST (false)
    SET B #1
    SET ACC #123
    JUMP_IF_ACC_LTE B &jialte_halt_1

    // JUMP_IF_ACC_LTE C CONST (false)
    SET C #123
    SET ACC #12345
    JUMP_IF_ACC_LTE C &jialte_halt_2

    // JUMP_IF_ACC_LTE CONST CONST (false)
    SET ACC #1001
    JUMP_IF_ACC_LTE #1000 &jialte_halt_3
    JUMP &jialte_11

    // JUMP_IF_ACC_LTE M_CONST CONST (false)
$v_jialte_const_3 #15
&jialte_11
    SET ACC #5555
    JUMP_IF_ACC_LTE [$v_jialte_const_3] &jialte_halt_4
    JUMP &jiagte_0

&jialte_halt_0
    NOOP
    NOOP
    HALT
    NOOP
    NOOP
&jialte_halt_1
    NOOP
    NOOP
    HALT
    NOOP
    NOOP
&jialte_halt_2
    NOOP
    NOOP
    HALT
    NOOP
    NOOP
&jialte_halt_3
    NOOP
    NOOP
    HALT
    NOOP
    NOOP
&jialte_halt_4
    NOOP
    NOOP
    HALT
    NOOP
    NOOP

    ////////////////////////////////////////////////////////////////
    // JUMP_IF_ACC_GTE
    ////////////////////////////////////////////////////////////////

    // Test true cases
    // JUMP_IF_ACC_GTE A CONST (greater than, true)
&jiagte_0
    SET A #12
    SET ACC #20
    JUMP_IF_ACC_GTE A &jiagte_1
    HALT

    // JUMP_IF_ACC_GTE A CONST (equal to, true)
&jiagte_1
    SET A #123
    SET ACC #123
    JUMP_IF_ACC_GTE A &jiagte_2
    HALT

    // JUMP_IF_ACC_GTE B CONST (greater than, true)
&jiagte_2
    SET B #1234
    SET ACC #12341
    JUMP_IF_ACC_GTE B &jiagte_3
    HALT

    // JUMP_IF_ACC_GTE B CONST (equal to, true)
&jiagte_3
    SET B #6000
    SET ACC #6000
    JUMP_IF_ACC_GTE B &jiagte_4
    HALT

    // JUMP_IF_ACC_GTE C CONST (greater than, true)
&jiagte_4
    SET C #123
    SET ACC #1234
    JUMP_IF_ACC_GTE C &jiagte_5
    HALT

    // JUMP_IF_ACC_GTE C CONST (equal to, true)
&jiagte_5
    SET C #555
    SET ACC #555
    JUMP_IF_ACC_GTE C &jiagte_6
    HALT

    // JUMP_IF_ACC_GTE CONST CONST (greater than, true)
&jiagte_6
    SET ACC #1000
    JUMP_IF_ACC_GTE #3 &jiagte_7
    HALT

    // JUMP_IF_ACC_GTE CONST CONST (equal to, true)
&jiagte_7
    SET ACC #1111
    JUMP_IF_ACC_GTE #1111 &jiagte_8
    HALT

    // JUMP_IF_ACC_GTE M_CONST CONST (greater than, true)
$v_jiagte_const_0 #111
&jiagte_8
    SET ACC #222
    JUMP_IF_ACC_GTE [$v_jiagte_const_0] &jiagte_9
    HALT

    // JUMP_IF_ACC_GTE M_CONST CONST (equal to, true)
$v_jiagte_const_1 #999
&jiagte_9
    SET ACC #999
    JUMP_IF_ACC_GTE [$v_jiagte_const_1] &jiagte_10
    HALT

    // Test false cases
&jiagte_10

    // JUMP_IF_ACC_GTE A CONST (false)
    SET A #24
    SET ACC #12
    JUMP_IF_ACC_GTE A &jiagte_halt_0

    // JUMP_IF_ACC_GTE B CONST (false)
    SET B #1
    SET ACC #0
    JUMP_IF_ACC_GTE B &jiagte_halt_1

    // JUMP_IF_ACC_GTE C CONST (false)
    SET C #987
    SET ACC #654
    JUMP_IF_ACC_GTE C &jiagte_halt_2

    // JUMP_IF_ACC_GTE CONST CONST (false)
    SET ACC #10001
    JUMP_IF_ACC_GTE #12000 &jiagte_halt_3
    JUMP &jiagte_11

    // JUMP_IF_ACC_GTE M_CONST CONST (false)
$v_jiagte_const_2 #999
&jiagte_11
    SET ACC #0
    JUMP_IF_ACC_GTE [$v_jiagte_const_2] &jiagte_halt_4
    JUMP &jiagt_0

&jiagte_halt_0
    NOOP
    NOOP
    HALT
    NOOP
    NOOP
&jiagte_halt_1
    NOOP
    NOOP
    HALT
    NOOP
    NOOP
&jiagte_halt_2
    NOOP
    NOOP
    HALT
    NOOP
    NOOP
&jiagte_halt_3
    NOOP
    NOOP
    HALT
    NOOP
    NOOP
&jiagte_halt_4
    NOOP
    NOOP
    HALT
    NOOP
    NOOP

    ////////////////////////////////////////////////////////////////
    // JUMP_IF_ACC_GT
    ////////////////////////////////////////////////////////////////

    // Test true cases
    // JUMP_IF_ACC_GT A CONST (true)
&jiagt_0
    SET A #12
    SET ACC #200
    JUMP_IF_ACC_GT A &jiagt_1
    HALT

    // JUMP_IF_ACC_GT B CONST (true)
&jiagt_1
    SET B #123
    SET ACC #9999
    JUMP_IF_ACC_GT B &jiagt_2
    HALT

    // JUMP_IF_ACC_GT C CONST (true)
&jiagt_2
    SET C #100
    SET ACC #10000
    JUMP_IF_ACC_GT C &jiagt_3
    HALT

    // JUMP_IF_ACC_GT CONST CONST (true)
&jiagt_3
    SET ACC #7000
    JUMP_IF_ACC_GT #3447 &jiagt_4
    HALT

   // JUMP_IF_ACC_GT M_CONST CONST (true)
$v_jiagt_const_0 #4523
&jiagt_4
    SET ACC #9856
    JUMP_IF_ACC_GT [$v_jiagt_const_0] &jiagt_5
    HALT

    // Test false cases
&jiagt_5

    // JUMP_IF_ACC_GT A CONST (false)
    SET A #2
    SET ACC #2
    JUMP_IF_ACC_GT A &jiagt_halt_0

    // JUMP_IF_ACC_GT B CONST (false)
    SET B #1112
    SET ACC #12
    JUMP_IF_ACC_GT B &jiagt_halt_1

    // JUMP_IF_ACC_GT C CONST (false)
    SET C #9987
    SET ACC #345
    JUMP_IF_ACC_GT C &jiagt_halt_2

    // JUMP_IF_ACC_GT CONST CONST (false)
    SET ACC #10
    JUMP_IF_ACC_GT #15 &jiagt_halt_3
    JUMP &jiagt_6

    // JUMP_IF_ACC_GT M_CONST CONST (false)
$jiagt_const_1 #3214
&jiagt_6
    SET ACC #1554
    JUMP_IF_ACC_GT [$jiagt_const_1] &jiagt_halt_4
    JUMP &jiagt_done

&jiagt_halt_0
    NOOP
    NOOP
    HALT
    NOOP
    NOOP
&jiagt_halt_1
    NOOP
    NOOP
    HALT
    NOOP
    NOOP
&jiagt_halt_2
    NOOP
    NOOP
    HALT
    NOOP
    NOOP
&jiagt_halt_3
    NOOP
    NOOP
    HALT
    NOOP
    NOOP
&jiagt_halt_4
    NOOP
    NOOP
    HALT
    NOOP
    NOOP

&jiagt_done
    NOOP

    ////////////////////////////////////////////////////////////////
    // JUMP_IF_NEGATIVE_FLAG
    ////////////////////////////////////////////////////////////////

&jinf_0
    SET ACC #10
    SUB #20
    JUMP_IF_NEGATIVE_FLAG &jinf_1
    HALT

&jinf_1
    SET ACC #222
    SUB #5
    JUMP_IF_NEGATIVE_FLAG &jinf_halt_0
    JUMP &jinnf_0

&jinf_halt_0
    HALT

    ////////////////////////////////////////////////////////////////
    // JUMP_IF_NOT_NEGATIVE_FLAG
    ////////////////////////////////////////////////////////////////

&jinnf_0
    SET ACC #10
    SUB #5
    JUMP_IF_NOT_NEGATIVE_FLAG &jinnf_1
    HALT

&jinnf_1
    SET ACC #5
    SUB #10
    JUMP_IF_NOT_NEGATIVE_FLAG &jinnf_halt_0
    JUMP &jic_0

&jinnf_halt_0
    HALT

    ////////////////////////////////////////////////////////////////
    // JUMP_IF_CARRY
    ////////////////////////////////////////////////////////////////

&jic_0
    SET ACC #0xFFFF
    ADD #1
    JUMP_IF_CARRY &jic_1
    HALT

&jic_1
    SET ACC #5
    ADD #10
    JUMP_IF_CARRY &jic_halt_0
    JUMP &jinc_0

&jic_halt_0
    HALT

    ////////////////////////////////////////////////////////////////
    // JUMP_IF_NOT_CARRY
    ////////////////////////////////////////////////////////////////

&jinc_0
    SET ACC #18
    ADD #5
    JUMP_IF_NOT_CARRY &jinc_1
    HALT

&jinc_1
    SET ACC #0xFFFF
    ADD #55
    JUMP_IF_NOT_CARRY &jinc_halt_0
    JUMP &jib_0

&jinc_halt_0
    HALT

    ////////////////////////////////////////////////////////////////
    // JUMP_IF_BORROW
    ////////////////////////////////////////////////////////////////

&jib_0
    SET ACC #0x25
    SUB #54
    JUMP_IF_BORROW &jib_1
    HALT

&jib_1
    SET ACC #5
    ADD #10
    JUMP_IF_BORROW &jib_halt_0
    JUMP &jinb_0

&jib_halt_0
    HALT

    ////////////////////////////////////////////////////////////////
    // JUMP_IF_NOT_BORROW
    ////////////////////////////////////////////////////////////////

&jinb_0
    SET ACC #18
    SUB #5
    JUMP_IF_NOT_BORROW &jinb_1
    HALT

&jinb_1
    SET ACC #0
    SUB #55
    JUMP_IF_NOT_BORROW &jinb_halt_0
    JUMP &jief_0

&jinb_halt_0
    HALT

    ////////////////////////////////////////////////////////////////
    // JUMP_IF_EQUAL_FLAG
    ////////////////////////////////////////////////////////////////

&jief_0
    // See the note on the ALU module because this is a bit magic.
    SET ACC #1
    SUB #2
    JUMP_IF_EQUAL_FLAG &jief_1
    HALT

&jief_1
    SET ACC #5
    ADD #10
    JUMP_IF_EQUAL_FLAG &jief_halt_0
    JUMP &jinef_0

&jief_halt_0
    HALT

    ////////////////////////////////////////////////////////////////
    // JUMP_IF_NOT_EQUAL_FLAG
    ////////////////////////////////////////////////////////////////

&jinef_0
    SET ACC #34
    ADD #5
    JUMP_IF_NOT_EQUAL_FLAG &jinef_1
    HALT

&jinef_1
    // See the note on the ALU module because this is a bit magic.
    SET ACC #1
    SUB #2
    JUMP_IF_NOT_EQUAL_FLAG &jinef_halt_0
    JUMP &jizf_0

&jinef_halt_0
    HALT

    ////////////////////////////////////////////////////////////////
    // JUMP_IF_ZERO_FLAG
    ////////////////////////////////////////////////////////////////

&jizf_0
    SET ACC #0
    ADD #0
    JUMP_IF_ZERO_FLAG &jizf_1
    HALT

&jizf_1
    SET ACC #1
    ADD #1
    JUMP_IF_ZERO_FLAG &jizf_halt_0
    JUMP &jinzf_0

&jizf_halt_0
    HALT

    ////////////////////////////////////////////////////////////////
    // JUMP_IF_NOT_ZERO_FLAG
    ////////////////////////////////////////////////////////////////

&jinzf_0
    SET ACC #1
    ADD #1
    JUMP_IF_NOT_ZERO_FLAG &jinzf_1
    HALT

&jinzf_1
    SET ACC #0
    ADD #0
    JUMP_IF_NOT_ZERO_FLAG &jinzf_halt_0
    JUMP &call_0

&jinzf_halt_0
    HALT

    ////////////////////////////////////////////////////////////////
    // ROT_LEFT
    ////////////////////////////////////////////////////////////////

    // ROT_LEFT ACC
    SET ACC #0b1000_0000_0100_0000
    ROT_LEFT ACC
    JUMP_IF_ACC_EQ #0b0000_0000_1000_0001 &rot_left_0
    HALT

&rot_left_0
    // ROT_LEFT A
    SET A #0b1111_0000_1111_0000
    ROT_LEFT A
    SET ACC #0b1110_0001_1110_0001
    JUMP_IF_ACC_EQ A &rot_left_1
    HALT

&rot_left_1
    // ROT_LEFT B
    SET B #0b0000_0000_1111_0000
    ROT_LEFT B
    SET ACC #0b0000_0001_1110_0000
    JUMP_IF_ACC_EQ B &rot_left_2
    HALT

&rot_left_2
    // ROT_LEFT C
    SET C #0b1111_1111_1111_1110
    ROT_LEFT C
    SET ACC #0b1111_1111_1111_1101
    JUMP_IF_ACC_EQ C &rot_left_3
    HALT

$v_rot_left_0 #0b0101_0101_1010_1010
&rot_left_3
    // ROT_LEFT M_CONST
    ROT_LEFT [$v_rot_left_0]
    LOAD [$v_rot_left_0] ACC
    JUMP_IF_ACC_EQ #0b1010_1011_0101_0100 &rot_left_4
    HALT

&rot_left_4
    // ROT_LEFT ACC (with carry)
    SET ACC #0b1000_0000_0000_0000
    ROT_LEFT ACC
    JUMP_IF_CARRY &rot_left_5
    HALT

&rot_left_5
    // ROT_LEFT ACC (no carry)
    SET ACC #0b0111_0000_0000_0000
    ROT_LEFT ACC
    JUMP_IF_NOT_CARRY &rot_right_0
    HALT

    ////////////////////////////////////////////////////////////////
    // ROT_RIGHT
    ////////////////////////////////////////////////////////////////

&rot_right_0
    // ROT_RIGHT ACC
    SET ACC #0b1000_0000_0100_0001
    ROT_RIGHT ACC
    JUMP_IF_ACC_EQ #0b1100_0000_0010_0000 &rot_right_1
    HALT

&rot_right_1
    // ROT_RIGHT A
    SET A #0b1111_0000_1111_0001
    ROT_RIGHT A
    SET ACC #0b1111_1000_0111_1000
    JUMP_IF_ACC_EQ A &rot_right_2
    HALT

&rot_right_2
    // ROT_RIGHT B
    SET B #0b1111_0000_1111_0000
    ROT_RIGHT B
    SET ACC #0b0111_1000_0111_1000
    JUMP_IF_ACC_EQ B &rot_right_3
    HALT

&rot_right_3
    // ROT_RIGHT C
    SET C #0b1111_1111_1111_1111
    ROT_RIGHT C
    SET ACC #0b1111_1111_1111_1111
    JUMP_IF_ACC_EQ C &rot_right_4
    HALT

$v_rot_right_0 #0b0101_0101_1010_1010
&rot_right_4
    // ROT_RIGHT M_CONST
    ROT_RIGHT [$v_rot_right_0]
    LOAD [$v_rot_right_0] ACC
    JUMP_IF_ACC_EQ #0b0010_1010_1101_0101 &rot_right_5
    HALT

&rot_right_5
    // ROT_RIGHT ACC (with carry)
    SET ACC #0b0000_0000_0000_0001
    ROT_RIGHT ACC
    JUMP_IF_CARRY &rot_right_6
    HALT

&rot_right_6
    // ROT_RIGHT ACC (no carry)
    SET ACC #0b1111_1111_1111_1110
    ROT_RIGHT ACC
    JUMP_IF_NOT_CARRY &shift_left_0
    HALT

    ////////////////////////////////////////////////////////////////
    // SHIFT_LEFT
    ////////////////////////////////////////////////////////////////

&shift_left_0
    // SHIFT_LEFT ACC
    SET ACC #0b1010_0000_0100_0000
    SHIFT_LEFT ACC
    JUMP_IF_ACC_EQ #0b0100_0000_1000_0000 &shift_left_1
    HALT

&shift_left_1
    // SHIFT_LEFT A
    SET A #0b1111_0000_1111_0010
    SHIFT_LEFT A
    SET ACC #0b1110_0001_1110_0100
    JUMP_IF_ACC_EQ A &shift_left_2
    HALT

&shift_left_2
    // SHIFT_LEFT B
    SET B #0b1111_0000_1111_0010
    SHIFT_LEFT B
    SET ACC #0b1110_0001_1110_0100
    JUMP_IF_ACC_EQ B &shift_left_3
    HALT

&shift_left_3
    // SHIFT_LEFT C
    SET C #0b0000_0101_1111_1111
    SHIFT_LEFT C
    SET ACC #0b0000_1011_1111_1110
    JUMP_IF_ACC_EQ B &shift_left_4
    HALT

$v_shift_left_0 #0b0101_0101_1010_1010
&shift_left_4
    // SHIFT_LEFT M_CONST
    SHIFT_LEFT [$v_shift_left_0]
    LOAD [$v_shift_left_0] ACC
    JUMP_IF_ACC_EQ #0b1010_1011_0101_0100 &shift_left_5
    HALT

&shift_left_5
    // SHIFT_LEFT ACC (with carry)
    SET ACC #0b1000_0000_0000_0000
    SHIFT_LEFT ACC
    JUMP_IF_CARRY &shift_left_6
    HALT

&shift_left_6
    // SHIFT_LEFT ACC (no carry)
    SET ACC #0b0111_0000_0000_0000
    SHIFT_LEFT ACC
    JUMP_IF_NOT_CARRY &shift_right_0
    HALT

    ////////////////////////////////////////////////////////////////
    // SHIFT_RIGHT
    ////////////////////////////////////////////////////////////////

&shift_right_0
    // SHIFT_RIGHT ACC
    SET ACC #0b1010_0000_0100_0000
    SHIFT_RIGHT ACC
    JUMP_IF_ACC_EQ #0b0101_0000_0010_0000 &shift_right_1
    HALT

&shift_right_1
    // SHIFT_RIGHT A
    SET A #0b1111_0000_1111_0010
    SHIFT_RIGHT A
    SET ACC #0b0111_1000_0111_1001
    JUMP_IF_ACC_EQ A &shift_right_2
    HALT

&shift_right_2
    // SHIFT_RIGHT B
    SET B #0b1111_0000_1111_0010
    SHIFT_RIGHT B
    SET ACC #0b0111_1000_0111_1001
    JUMP_IF_ACC_EQ B &shift_right_3
    HALT

&shift_right_3
    // SHIFT_RIGHT C
    SET C #0b0000_0101_1111_1111
    SHIFT_RIGHT C
    SET ACC #0b0000_0010_1111_1111
    JUMP_IF_ACC_EQ B &shift_right_4
    HALT

$v_shift_right_0 #0b0101_0101_1010_1010
&shift_right_4
    // SHIFT_RIGHT M_CONST
    SHIFT_RIGHT [$v_shift_right_0]
    LOAD [$v_shift_right_0] ACC
    JUMP_IF_ACC_EQ #0b0010_1010_1101_0101 &shift_right_5
    HALT

&shift_right_5
    // SHIFT_RIGHT ACC (with carry)
    SET ACC #0b0000_0000_0000_0001
    SHIFT_RIGHT ACC
    JUMP_IF_CARRY &shift_right_6
    HALT

&shift_right_6
    // SHIFT_RIGHT ACC (no carry)
    SET ACC #0b0000_0000_0000_0000
    SHIFT_RIGHT ACC
    JUMP_IF_NOT_CARRY &shift_right_done
    HALT

&shift_right_done
    NOOP

    ////////////////////////////////////////////////////////////////
    // STORE_INCR
    ////////////////////////////////////////////////////////////////

$store_incr_v0 #34
$store_incr_v1 #789
    // STORE_INCR ACC M_A M_B
    SET ACC #23
    SET A $store_incr_v0
    SET B $store_incr_v1
    STORE_INCR ACC [A] [B]
    LOAD [$store_incr_v0] ACC
    JUMP_IF_ACC_EQ #23 &store_incr_0
    HALT
&store_incr_0
    LOAD [$store_incr_v1] ACC
    JUMP_IF_ACC_EQ #790 &store_incr_1
    HALT

&store_incr_1
$store_incr_v2 #456
$store_incr_v3 #123
    // STORE_INCR CONST M_A M_B
    SET A $store_incr_v2
    SET B $store_incr_v3
    STORE_INCR #599 [A] [B]
    LOAD [$store_incr_v2] ACC
    JUMP_IF_ACC_EQ #599 &store_incr_2
    HALT
&store_incr_2
    LOAD [$store_incr_v3] ACC
    JUMP_IF_ACC_EQ #124 &store_incr_3
    HALT

&store_incr_3
$store_incr_v4 #456
$store_incr_v5 #0xFFFF
    // STORE_INCR CONST M_A M_B (test carry)
    SET A $store_incr_v4
    SET B $store_incr_v5
    STORE_INCR #599 [A] [B]
    JUMP_IF_CARRY &store_decr_0
    HALT

    ////////////////////////////////////////////////////////////////
    // STORE_DECR
    ////////////////////////////////////////////////////////////////

$store_decr_v0 #34
$store_decr_v1 #789
    // STORE_DECR ACC M_A M_B
    SET ACC #23
    SET A $store_decr_v0
    SET B $store_decr_v1
    STORE_DECR ACC [A] [B]
    LOAD [$store_decr_v0] ACC
    JUMP_IF_ACC_EQ #23 &store_decr_0
    HALT
&store_decr_0
    LOAD [$store_decr_v1] ACC
    JUMP_IF_ACC_EQ #790 &store_decr_1
    HALT

&store_decr_1
$store_decr_v2 #456
$store_decr_v3 #123
    // STORE_DECR CONST M_A M_B
    SET A $store_decr_v2
    SET B $store_decr_v3
    STORE_DECR #599 [A] [B]
    LOAD [$store_decr_v2] ACC
    JUMP_IF_ACC_EQ #599 &store_decr_2
    HALT
&store_decr_2
    LOAD [$store_decr_v3] ACC
    JUMP_IF_ACC_EQ #124 &store_decr_3
    HALT

&store_decr_3
$store_decr_v4 #456
$store_decr_v5 #1
    // STORE_DECR CONST M_A M_B (test zero)
    SET A $store_decr_v4
    SET B $store_decr_v5
    STORE_DECR #599 [A] [B]
    JUMP_IF_ZERO_FLAG &store_decr_done
    HALT

&store_decr_done
    NOOP

JUMP &start
