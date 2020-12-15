#include "prog_test_copy.h"

extern const byte num_test_copy_program_bytes = 39;
extern const byte test_copy_program_bytes[] PROGMEM = {
    0x38, // 000 SET ACC #1
    0x01, // 001 (1)
    0x87, // 002 STORE ACC [$test_num]
    0x10, // 003 (16)
    0x78, // 004 LOAD [$test_num] ACC (@test_start)
    0x10, // 005 (16)
    0x01, // 006 COPY ACC A
    0x08, // 007 COPY A ACC
    0x02, // 008 COPY ACC B
    0x10, // 009 COPY B ACC
    0x03, // 010 COPY ACC C
    0x18, // 011 COPY C ACC
    0x04, // 012 COPY ACC SP
    0x20, // 013 COPY SP ACC
    0x01, // 014 COPY ACC A
    0x0A, // 015 COPY A B
    0x11, // 016 COPY B A
    0x0B, // 017 COPY A C
    0x19, // 018 COPY C A
    0x0C, // 019 COPY A SP
    0x21, // 020 COPY SP A
    0x0A, // 021 COPY A B
    0x13, // 022 COPY B C
    0x1A, // 023 COPY C B
    0x14, // 024 COPY B SP
    0x22, // 025 COPY SP B
    0x13, // 026 COPY B C
    0x1C, // 027 COPY C SP
    0x23, // 028 COPY SP C
    0x78, // 029 LOAD [$test_num] ACC
    0x10, // 030 (16)
    0x1F, // 031 JUMP_IF_EQ_ACC C @next_number
    0x22, // 032 (34)
    0xB6, // 033 HALT
    0xA6, // 034 ROT_LEFT ACC (@next_number)
    0x87, // 035 STORE ACC [$test_num]
    0x10, // 036 (16)
    0x3D, // 037 JUMP @test_start
    0x04  // 038 (4)
};

extern const byte num_test_copy_data_bytes = 17;

// Needs to be at least 1 byte in this array
extern const byte test_copy_data_bytes[] PROGMEM = {
    0x00, // 000 (placeholder).
    0x00, // 001 (placeholder).
    0x00, // 002 (placeholder).
    0x00, // 003 (placeholder).
    0x00, // 004 (placeholder).
    0x00, // 005 (placeholder).
    0x00, // 006 (placeholder).
    0x00, // 007 (placeholder).
    0x00, // 008 (placeholder).
    0x00, // 009 (placeholder).
    0x00, // 010 (placeholder).
    0x00, // 011 (placeholder).
    0x00, // 012 (placeholder).
    0x00, // 013 (placeholder).
    0x00, // 014 (placeholder).
    0x00, // 015 (placeholder).
    0x10  // 016 $test_num
};

// Max of seven characters
extern const char test_copy_program_name[] = "tstcp";
