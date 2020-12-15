#include "prog_test_mem.h"

extern const byte num_test_mem_program_bytes = 17;
extern const byte test_mem_program_bytes[] PROGMEM = {
    0xC1, // 000 SET_ZERO A (@init)
    0xC2, // 001 SET_ZERO B
    0xC3, // 002 SET_ZERO C
    0x91, // 003 STORE B [A] (@test_val)
    0x48, // 004 LOAD [A] ACC
    0x17, // 005 JUMP_IF_EQ_ACC B @next_val
    0x08, // 006 (8)
    0xB6, // 007 HALT
    0xC6, // 008 INCR B (@next_val)
    0x2D, // 009 JUMP_IF_NOT_OVERFLOW_FLAG @test_val
    0x03, // 010 (3)
    0xC5, // 011 INCR A
    0x2D, // 012 JUMP_IF_NOT_OVERFLOW_FLAG @test_val
    0x03, // 013 (3)
    0xC7, // 014 INCR C
    0x3D, // 015 JUMP @test_val
    0x03  // 016 (3)
};

extern const byte num_test_mem_data_bytes = 0;

// Needs to be at least 1 byte in this array
extern const byte test_mem_data_bytes[] PROGMEM = {
    0x00 // Placeholder.
};

// Max of seven characters
extern const char test_mem_program_name[] = "tstmem";
