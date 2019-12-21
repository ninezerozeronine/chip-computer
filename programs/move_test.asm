// Tests that the copy operation works

$test_num
SET ACC #1
STORE ACC [$test_num]

@test_start
    LOAD [$test_num] ACC
    COPY ACC A
    COPY A ACC
    COPY ACC B
    COPY B ACC
    COPY ACC C
    COPY C ACC
    COPY ACC SP
    COPY SP ACC
    COPY ACC A
    COPY A B
    COPY B A
    COPY A C
    COPY C A
    COPY A SP
    COPY SP A
    COPY A B
    COPY B C
    COPY C B
    COPY B SP
    COPY SP B
    COPY B C
    COPY C SP
    COPY SP C
    LOAD [$test_num] ACC
    JUMP_IF_EQ_ACC C @next_number
    HALT
@next_number
    ROT_LEFT ACC
    STORE ACC [$test_num]
    JUMP @test_start