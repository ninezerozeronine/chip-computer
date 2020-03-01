#include "prog_foobar.h"

extern const byte num_foobar_program_bytes = 4;
extern const byte foobar_program_bytes[] PROGMEM = {
    0xFF, // SOME INSTRUCTION
    0x12, // SOME INSTRUCTION
    0x00, // SOME INSTRUCTION
    0xA1  // SOME INSTRUCTION
};

extern const byte num_foobar_data_bytes = 3;
// Needs to be at least 1 byte in this array
extern const byte foobar_data_bytes[] PROGMEM = {
    0x00,
    0x01,
    0x02
};

// Max of seven characters
extern const char foobar_program_name[] = "Foobar";