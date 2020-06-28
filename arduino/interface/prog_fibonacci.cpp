#include "prog_fibonacci.h"

extern const byte num_fibonacci_program_bytes = 13;
extern const byte fibonacci_program_bytes[] PROGMEM = {
    0x39, // 000 SET A #1 (@set_initial)
    0x01, // 001 (1)
    0x3A, // 002 SET B #1
    0x01, // 003 (1)
    0x08, // 004 COPY A ACC (@fib_loop)
    0xCE, // 005 ADD B
    0x24, // 006 JUMP_IF_OVERFLOW_FLAG @set_initial
    0x00, // 007 (0)
    0x03, // 008 COPY ACC C
    0x11, // 009 COPY B A
    0x02, // 010 COPY ACC B
    0x3D, // 011 JUMP @fib_loop
    0x04  // 012 (4)
};

extern const byte num_fibonacci_data_bytes = 0;

// Needs to be at least 1 byte in this array
extern const byte fibonacci_data_bytes[] PROGMEM = {
    0x00 // Placeholder.
};

// Max of seven characters
extern const char fibonacci_program_name[] = "Fbnacci";
