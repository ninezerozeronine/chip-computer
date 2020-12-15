#include "prog_test_copy_thorough.h"

extern const byte num_test_copy_thorough_program_bytes = 85;
extern const byte test_copy_thorough_program_bytes[] PROGMEM = {
    0x38, // 000 SET ACC #1
    0x01, // 001 (1)
    0x87, // 002 STORE ACC [$test_num]
    0x10, // 003 (16)
    0x78, // 004 LOAD [$test_num] ACC (@test_start)
    0x10, // 005 (16)
    0x01, // 006 COPY ACC A
    0x38, // 007 SET ACC #255
    0xFF, // 008 (255)
    0x08, // 009 COPY A ACC
    0x39, // 010 SET A #255
    0xFF, // 011 (255)
    0x02, // 012 COPY ACC B
    0x38, // 013 SET ACC #255
    0xFF, // 014 (255)
    0x10, // 015 COPY B ACC
    0x3A, // 016 SET B #255
    0xFF, // 017 (255)
    0x03, // 018 COPY ACC C
    0x38, // 019 SET ACC #255
    0xFF, // 020 (255)
    0x18, // 021 COPY C ACC
    0x3B, // 022 SET C #255
    0xFF, // 023 (255)
    0x04, // 024 COPY ACC SP
    0x38, // 025 SET ACC #255
    0xFF, // 026 (255)
    0x20, // 027 COPY SP ACC
    0x3C, // 028 SET SP #255
    0xFF, // 029 (255)
    0x01, // 030 COPY ACC A
    0x38, // 031 SET ACC #255
    0xFF, // 032 (255)
    0x0A, // 033 COPY A B
    0x39, // 034 SET A #255
    0xFF, // 035 (255)
    0x11, // 036 COPY B A
    0x3A, // 037 SET B #255
    0xFF, // 038 (255)
    0x0B, // 039 COPY A C
    0x39, // 040 SET A #255
    0xFF, // 041 (255)
    0x19, // 042 COPY C A
    0x3B, // 043 SET C #255
    0xFF, // 044 (255)
    0x0C, // 045 COPY A SP
    0x39, // 046 SET A #255
    0xFF, // 047 (255)
    0x21, // 048 COPY SP A
    0x3C, // 049 SET SP #255
    0xFF, // 050 (255)
    0x0A, // 051 COPY A B
    0x39, // 052 SET A #255
    0xFF, // 053 (255)
    0x13, // 054 COPY B C
    0x3A, // 055 SET B #255
    0xFF, // 056 (255)
    0x1A, // 057 COPY C B
    0x3B, // 058 SET C #255
    0xFF, // 059 (255)
    0x14, // 060 COPY B SP
    0x3A, // 061 SET B #255
    0xFF, // 062 (255)
    0x22, // 063 COPY SP B
    0x3C, // 064 SET SP #255
    0xFF, // 065 (255)
    0x13, // 066 COPY B C
    0x3A, // 067 SET B #255
    0xFF, // 068 (255)
    0x1C, // 069 COPY C SP
    0x3B, // 070 SET C #255
    0xFF, // 071 (255)
    0x23, // 072 COPY SP C
    0x3C, // 073 SET SP #255
    0xFF, // 074 (255)
    0x78, // 075 LOAD [$test_num] ACC
    0x10, // 076 (16)
    0x1F, // 077 JUMP_IF_EQ_ACC C @next_number
    0x50, // 078 (80)
    0xB6, // 079 HALT
    0xA6, // 080 ROT_LEFT ACC (@next_number)
    0x87, // 081 STORE ACC [$test_num]
    0x10, // 082 (16)
    0x3D, // 083 JUMP @test_start
    0x04  // 084 (4)
};

extern const byte num_test_copy_thorough_data_bytes = 17;

// Needs to be at least 1 byte in this array
extern const byte test_copy_thorough_data_bytes[] PROGMEM = {
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
extern const char test_copy_thorough_program_name[] = "tstcpt";
