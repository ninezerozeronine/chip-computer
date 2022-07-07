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

&add_4
$v_add_0 #42
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

&sub_4
$v_sub_0 #42
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

&and_4
$v_and_0           #0b1
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

&or_4
$v_or_0            #0b1
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

&xor_4
$v_xor_0           #0b1
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

&nand_4
$v_nand_0          #0b1
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

&nor_4
$v_nor_0           #0b1
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

&nxor_4
$v_nxor_0          #0b1
    SET ACC        #0b1
    NXOR [$v_nxor_0]
    JUMP_IF_ACC_EQ #0b1 &placeholder
    HALT

&placeholder
    JUMP &start