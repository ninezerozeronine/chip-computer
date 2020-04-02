#include "prog_fibonacci.h"

extern const byte num_fibonacci_program_bytes = 13;
extern const byte fibonacci_program_bytes[] PROGMEM = {
    // @set_initial
    0x39, // SET A #1
    0x01, 
    0x3A, // SET B #1
    0x01,

    // @fib_loop
    0x08, // COPY A ACC
    0xCE, // ADD B
    0x24, // JUMP_IF_OVERFLOW_FLAG @set_initial
    0x00, 
    0x03, // COPY ACC C (to display)
    0x11, // COPY B A
    0x02, // COPY ACC B
    0x3D, // JUMP @fib_loop
    0x04
};

extern const byte num_fibonacci_data_bytes = 0;
// Needs to be at least 1 byte in this array
extern const byte fibonacci_data_bytes[] PROGMEM = {
    0x00 // Placeholder...
};

// Max of seven characters
extern const char fibonacci_program_name[] = "Fbnacci";