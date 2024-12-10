!status_word_addr #0b1111_1111_1111_1010

// #0b1111_1111_1111_1111
// #0b1111_1111_1111_1110
// #0b1111_1111_1111_1101
// #0b1111_1111_1111_1100
// #0b1111_1111_1111_1011
// #0b1111_1111_1111_1010
// #0b1111_1111_1111_1001
// #0b1111_1111_1111_1000

&set_initial
    SET A #1
    SET B #1
    STORE A [!status_word_addr]

&fib_loop
    COPY A ACC
    ADD B
    JUMP_IF_ACC_GT #1597 &set_initial
    STORE A [!status_word_addr] // To display
    COPY B A
    COPY ACC B
    JUMP &fib_loop

// &set_initial
//     SET SP #1
//     SET A #1
// 
// &fib_loop
//     COPY SP ACC
//     ADD A
//     JUMP_IF_ACC_GT #1597 &set_initial
//     COPY A SP
//     COPY ACC A
//     JUMP &fib_loop