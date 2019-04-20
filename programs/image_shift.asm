
//   byte 0   byte 1   byte 2
// 10010001 10001011 11110000 <- orig
// 00100011 00010111 11100001 <- shift 1
// 01000110 00101111 11000010 <- shift 2
// 10001100 01011111 10000100 <- shift 3
// 00011000 10111111 00001001 <- shift 4

// Load the leftmost byte into a reg
// set carry if leftmost bit is 1
// current_byte = num_bytes-1
// @loop
// Load the current_byte into a reg
// left shift
// add carry
// set carry if leftmost bit is 1
// current_byte -= 1
// jump to @loop if not underflow


//
// Testing if the ALU uses ACC to add other registers to
//
$byte0
$byte1
$byte2
$byte3
$numbytes
$next_wrap
$last_wrap



@shift_bytes_left_with_wrap
    LOAD [$byte0] ACC
    CALL @get_wrap
    STORE ACC [$last_wrap]

    LOAD [$numbytes] ACC
    SET A $byte0
    ADD A
    DECR ACC
    COPY ACC A

@bit_shift_loop
    LOAD [A] ACC
    COPY ACC B
    CALL @get_wrap
    STORE ACC [$current_wrap]
    LSHIFT B
    LOAD [$last_wrap] ACC
    ADD B
    STORE ACC [A]
    LOAD [$current_wrap] B
    STORE B [$last_wrap]
    DECR A
    JUMP_IF_OVERFLOW_FLAG @bit_shift_loop
    JUMP @shift_bytes_left_with_wrap

@get_wrap
    // Value to test is in ACC, wrap value to add is returned in ACC
    // Clobbers ACC
    PUSH A
    SET A #0b10000000
    AND A
    LSHIFT ACC
    LSHIFTC ACC
    POP A
    RETURN  





//
// Testing if the ALU uses DAT to add to other registers
//
$byte0
$byte1
$byte2
$byte3
$numbytes
$next_wrap
$last_wrap

@shift_bytes_left_with_wrap
    LOAD [$byte0] DAT
    CALL @get_wrap
    STORE DAT [$last_wrap]

    LOAD [$numbytes] A
    SET DAT $byte0
    ADD_DAT_TO A
    DECR A

@bit_shift_loop
    LOAD [A] DAT
    COPY DAT B
    CALL @get_wrap
    STORE DAT [$current_wrap]
    LOAD [$last_wrap] DAT
    LSHIFT B
    ADD_DAT_TO B
    STORE DAT [A]
    LOAD [$current_wrap] DAT
    STORE DAT [$last_wrap]
    DECR A
    JUMP_IF_OVERFLOW_FLAG @bit_shift_loop
    JUMP @shift_bytes_left_with_wrap

@get_wrap
    // Value to test is in DAT, carry to add is returned in DAT
    // Clobbers DAT
    PUSH A
    SET A #0b10000000
    AND_DAT_WITH A
    LSHIFT A
    LSHIFTC A
    COPY A DAT
    POP A
    RETURN    




