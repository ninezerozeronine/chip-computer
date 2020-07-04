#include "prog_test_membug.h"

extern const byte num_test_membug_program_bytes = 19;
extern const byte test_membug_program_bytes[] PROGMEM = {
    0x39, // 000 SET A #0 (@init)
    0x00, // 001 (0)
    0x3A, // 002 SET B #0b11111101
    0xFD, // 003 (253)
    0xC3, // 004 SET_ZERO C
    0x91, // 005 STORE B [A] (@test_val)
    0x48, // 006 LOAD [A] ACC
    0x17, // 007 JUMP_IF_EQ_ACC B @next_val
    0x0A, // 008 (10)
    0xB6, // 009 HALT
    0xC6, // 010 INCR B (@next_val)
    0x2D, // 011 JUMP_IF_NOT_OVERFLOW_FLAG @test_val
    0x05, // 012 (5)
    0xC5, // 013 INCR A
    0x2D, // 014 JUMP_IF_NOT_OVERFLOW_FLAG @test_val
    0x05, // 015 (5)
    0xC7, // 016 INCR C
    0x3D, // 017 JUMP @test_val
    0x05  // 018 (5)
};

extern const byte num_test_membug_data_bytes = 0;

// Needs to be at least 1 byte in this array
extern const byte test_membug_data_bytes[] PROGMEM = {
    0x00 // Placeholder.
};

// Max of seven characters
extern const char test_membug_program_name[] = "tetmemb";
