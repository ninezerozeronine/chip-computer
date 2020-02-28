#include "prog_fibonacci.h"

extern const byte num_fibonacci_program_bytes = 2;
extern const byte fibonacci_program_bytes[] PROGMEM = {
    0xFF, // SOME INSTRUCTION
    0x12  // SOME INSTRUCTION
};

extern const byte num_fibonacci_data_bytes = 0;
extern const byte fibonacci_data_bytes[] PROGMEM = {
    0x00 // Placeholder...
};


extern const char fibonacci_program_name[] = "Fbnacci";