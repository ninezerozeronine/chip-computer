// Tests that the copy operation works

$test

@zero_test
    SET_ZERO ACC
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

