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

$v_jump_3 &jump10
&jump9
    SET C $v_jump_3
    JUMP [C]
    HALT

$v_jump_4 &jump11
&jump10
    SET SP $v_jump_4
    JUMP [SP]
    HALT

$v_jump_5 &copy_0
&jump11
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
    JUMP_IF_ACC_EQ C &add_0
    HALT

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
    JUMP_IF_ACC_EQ #84 &sub_0
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
    JUMP_IF_EQ_ZERO ACC &and_0
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
    JUMP_IF_ACC_EQ #0b1 &or_0
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
    JUMP_IF_ACC_EQ #0b1 &xor_0
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
    JUMP_IF_ACC_EQ #0b0 &xor_0
    HALT

    ////////////////////////////////////////////////////////////////
    // NAND
    ////////////////////////////////////////////////////////////////

&nand_0
    SET ACC        #0b1111
    SET A          #0b0101
    NAND A
    JUMP_IF_ACC_EQ #0b1010 &nand_1
    HALT

&nand_1
    SET ACC        #0b1111_0000_1111_0000
    SET B          #0b1111_1111_1111_1111
    NAND B
    JUMP_IF_ACC_EQ #0b000_1111_0000_1111 &nand_2
    HALT

&nand_2
    SET ACC         #0b1100_1111
    SET C          #0b0000_0000
    NAND C
    JUMP_IF_ACC_EQ #0b1111_1111 &nand_3
    HALT

&nand_3
    SET ACC        #0b0011_1100_1111_0000
    NAND           #0b1111_1111_0000_1111
    JUMP_IF_ACC_EQ #0b1100_0011_1111_1111 &nand_4
    HALT

$v_nand_0          #0b1
&nand_4
    SET ACC        #0b1
    NAND [$v_nand_0]
    JUMP_IF_ACC_EQ #0b0 &nor_0
    HALT

    ////////////////////////////////////////////////////////////////
    // OR
    ////////////////////////////////////////////////////////////////

&nor_0
    SET ACC        #0b1111
    SET A          #0b0101
    NOR A
    JUMP_IF_ACC_EQ #0b0000 &nor_1
    HALT

&nor_1
    SET ACC        #0b1111_0000_1111_0000
    SET B          #0b1111_1111_1111_1111
    NOR B
    JUMP_IF_ACC_EQ #0b0000_0000_0000_0000 &nor_2
    HALT

&nor_2
    SET ACC        #0b1100_1111
    SET C          #0b0000_0000
    NOR C
    JUMP_IF_ACC_EQ #0b0011_0000 &nor_3
    HALT

&nor_3
    SET ACC        #0b0011_1100_1111_0000
    NOR            #0b0111_1110_0000_1110
    JUMP_IF_ACC_EQ #0b1000_0001_0000_0001 &nor_4
    HALT

$v_nor_0           #0b1
&nor_4
    SET ACC        #0b1
    NOR [$v_nor_0]
    JUMP_IF_ACC_EQ #0b0 &nxor_0
    HALT

    ////////////////////////////////////////////////////////////////
    // NXOR
    ////////////////////////////////////////////////////////////////

&nxor_0
    SET ACC        #0b1111
    SET A          #0b0101
    NXOR A
    JUMP_IF_ACC_EQ #0b0101 &nxor_1
    HALT

&nxor_1
    SET ACC        #0b0011
    SET B          #0b0101
    NXOR B
    JUMP_IF_ACC_EQ #0b1001 &nxor_2
    HALT

&nxor_2
    SET ACC        #0b1100_1111
    SET C          #0b0000_0000
    NXOR C
    JUMP_IF_ACC_EQ #0b0011_0000 &nxor_3
    HALT

&nxor_3
    SET ACC        #0b0011_1100_1011_0001
    NXOR           #0b1111_1111_0000_1111
    JUMP_IF_ACC_EQ #0b0011_1100_0100_0001 &nxor_4
    HALT

$v_nxor_0          #0b1
&nxor_4
    SET ACC        #0b1
    NXOR [$v_nxor_0]
    JUMP_IF_ACC_EQ #0b1 &incr_0
    HALT

    ////////////////////////////////////////////////////////////////
    // INCR
    ////////////////////////////////////////////////////////////////

&incr_0
    SET ACC #32
    INCR ACC 
    JUMP_IF_ACC_EQ #33 &incr_1
    HALT

&incr_1
    SET ACC #-31
    SET A #-32
    INCR A
    JUMP_IF_ACC_EQ A &incr_2
    HALT

&incr_2
    SET ACC #256
    SET B #255
    INCR B
    JUMP_IF_ACC_EQ B &incr_3
    HALT

&incr_3
    SET ACC #0xFFFF
    SET C #0
    INCR C
    JUMP_IF_ACC_EQ C &decr_0
    HALT

    ////////////////////////////////////////////////////////////////
    // DECR
    ////////////////////////////////////////////////////////////////

&decr_0
    SET ACC #32
    DECR ACC 
    JUMP_IF_ACC_EQ #31 &decr_1
    HALT

&decr_1
    SET ACC #-33
    SET A #-32
    DECR A
    JUMP_IF_ACC_EQ A &decr_2
    HALT

&decr_2
    SET ACC #255
    SET B #256
    DECR B
    JUMP_IF_ACC_EQ B &decr_3
    HALT

&decr_3
    SET ACC #0xFFFF
    SET C #0
    DECR C
    JUMP_IF_ACC_EQ C &load_0
    HALT

    ////////////////////////////////////////////////////////////////
    // LOAD
    ////////////////////////////////////////////////////////////////

$v_load_0 #24004
&load_0
    SET ACC $v_load_0
    LOAD [ACC] ACC
    JUMP_IF_ACC_EQ #24004 &load_1
    HALT

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

$v_load_5 #51597
&load_5
    SET A $v_load_5
    LOAD [A] A
    SET ACC #51597
    JUMP_IF_ACC_EQ A &load_6
    HALT

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

$v_load_10 #57819
&load_10
    SET B $v_load_10
    LOAD [B] B
    SET ACC #57819
    JUMP_IF_ACC_EQ B &load_11
    HALT

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

$v_load_15 #20527
&load_15
    SET C $v_load_15
    LOAD [C] C
    SET ACC #20527
    JUMP_IF_ACC_EQ C &load_16
    HALT

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

$v_store_0
&store_0
    SET ACC $v_store_0
    STORE ACC [ACC]
    LOAD [ACC] ACC
    JUMP_IF_ACC_EQ $v_store_0 &store_1
    HALT

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
    LOAD [ACC] ACC
    JUMP_IF_ACC_EQ #11935 &store_7
    HALT

$v_store_7
&store_7
    SET A $v_store_7
    STORE A [A]
    LOAD [A] ACC
    JUMP_IF_ACC_EQ $v_store_7 &store_8
    HALT

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
    LOAD [ACC] ACC
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

$v_store_14
&store_14
    SET B $v_store_14
    STORE B [B]
    LOAD [B] ACC
    JUMP_IF_ACC_EQ $v_store_14 &store_15
    HALT

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
    LOAD [ACC] ACC
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

$v_store_21
&store_21
    SET C $v_store_21
    STORE C [C]
    LOAD [C] ACC
    JUMP_IF_ACC_EQ $v_store_21 &store_22
    HALT

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
    JUMP_IF_ACC_EQ #63220 &store_24
    HALT

$v_store_24
&store_24
    SET SP #50736
    SET ACC $v_store_24
    STORE SP [ACC]
    LOAD [ACC] ACC
    JUMP_IF_ACC_EQ #50736 &store_25
    HALT

$v_store_25
&store_25
    SET SP #44571
    SET A $v_store_25
    STORE SP [A]
    LOAD [A] ACC
    JUMP_IF_ACC_EQ #44571 &store_26
    HALT

$v_store_26
&store_26
    SET SP #28464
    SET B $v_store_26
    STORE SP [B]
    LOAD [B] ACC
    JUMP_IF_ACC_EQ #28464 &store_27
    HALT

$v_store_27
&store_27
    SET SP #34092
    SET C $v_store_27
    STORE SP [C]
    LOAD [C] ACC
    JUMP_IF_ACC_EQ #34092 &store_28
    HALT

$v_store_28
&store_28
    SET SP $v_store_28
    STORE SP [SP]
    LOAD [SP] ACC
    JUMP_IF_ACC_EQ $v_store_28 &store_29
    HALT

$v_store_29
&store_29
    SET SP #30456
    STORE SP [$v_store_29]
    LOAD [$v_store_29] ACC
    JUMP_IF_ACC_EQ #30456 &push_0
    HALT

    ////////////////////////////////////////////////////////////////
    // PUSH
    ////////////////////////////////////////////////////////////////

&push_0
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
    SET C !zero_one
    PUSH C
    LOAD [SP] ACC
    JUMP_IF_ACC_EQ !zero_one &pop_0
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

    SET ACC !one_zero
    PUSH ACC
    SET_ZERO ACC
    LOAD [SP] ACC
    JUMP_IF_ACC_EQ !one_zero &pop_2
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
    JUMP_IF_ACC_EQ #4242 &placeholder
    HALT

&placeholder
    JUMP &start