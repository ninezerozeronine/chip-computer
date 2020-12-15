#include "prog_test_rot.h"

extern const byte num_test_rot_program_bytes = 6;
extern const byte test_rot_program_bytes[] PROGMEM = {
    0x39, // 000 SET A #1
    0x01, // 001 (1)
    0xA7, // 002 ROT_LEFT A (@loop)
    0x0B, // 003 COPY A C
    0x3D, // 004 JUMP @loop
    0x02  // 005 (2)
};

extern const byte num_test_rot_data_bytes = 0;

// Needs to be at least 1 byte in this array
extern const byte test_rot_data_bytes[] PROGMEM = {
    0x00 // Placeholder.
};

// Max of seven characters
extern const char test_rot_program_name[] = "tstrot";
