#include "prog_test_membug.h"

extern const byte num_test_membug_program_bytes = 18;
extern const byte test_membug_program_bytes[] PROGMEM = {
    0xC1, // 000 SET_ZERO A (@init)
    0x3A, // 001 SET B #110
    0x6E, // 002 (110)
    0xC3, // 003 SET_ZERO C
    0x91, // 004 STORE B [A] (@test_val)
    0x48, // 005 LOAD [A] ACC
    0x17, // 006 JUMP_IF_EQ_ACC B @next_val
    0x09, // 007 (9)
    0xB6, // 008 HALT
    0xC6, // 009 INCR B (@next_val)
    0x2D, // 010 JUMP_IF_NOT_OVERFLOW_FLAG @test_val
    0x04, // 011 (4)
    0xC5, // 012 INCR A
    0x2D, // 013 JUMP_IF_NOT_OVERFLOW_FLAG @test_val
    0x04, // 014 (4)
    0xC7, // 015 INCR C
    0x3D, // 016 JUMP @test_val
    0x04  // 017 (4)
};

extern const byte num_test_membug_data_bytes = 0;

// Needs to be at least 1 byte in this array
extern const byte test_membug_data_bytes[] PROGMEM = {
    0x00 // Placeholder.
};

// Max of seven characters
extern const char test_membug_program_name[] = "tstmemb";
