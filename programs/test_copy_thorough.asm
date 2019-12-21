// Tests that the copy operation works

$test_num
SET ACC #1
STORE ACC [$test_num]

@test_start
    LOAD [$test_num] ACC
    COPY ACC A
    SET ACC #255
    COPY A ACC
    SET A #255
    COPY ACC B
    SET ACC #255
    COPY B ACC
    SET B #255
    COPY ACC C
    SET ACC #255
    COPY C ACC
    SET C #255
    COPY ACC SP
    SET ACC #255
    COPY SP ACC
    SET SP #255
    COPY ACC A
    SET ACC #255
    COPY A B
    SET A #255
    COPY B A
    SET B #255
    COPY A C
    SET A #255
    COPY C A
    SET C #255
    COPY A SP
    SET A #255
    COPY SP A
    SET SP #255
    COPY A B
    SET A #255
    COPY B C
    SET B #255
    COPY C B
    SET C #255
    COPY B SP
    SET B #255
    COPY SP B
    SET SP #255
    COPY B C
    SET B #255
    COPY C SP
    SET C #255
    COPY SP C
    SET SP #255
    LOAD [$test_num] ACC
    JUMP_IF_EQ_ACC C @next_number
    HALT
@next_number
    ROT_LEFT ACC
    STORE ACC [$test_num]
    JUMP @test_start