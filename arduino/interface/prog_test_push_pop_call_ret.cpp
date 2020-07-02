#include "prog_test_push_pop_call_ret.h"

extern const byte num_test_push_pop_call_ret_program_bytes = 17;
extern const byte test_push_pop_call_ret_program_bytes[] PROGMEM = {
    0xC1, // 000 SET_ZERO A
    0x3C, // 001 SET SP #0
    0x00, // 002 (0)
    0x8E, // 003 PUSH A
    0x7E, // 004 CALL @incr_top_of_stack (@loop)
    0x08, // 005 (8)
    0x3D, // 006 JUMP @loop
    0x04, // 007 (4)
    0x72, // 008 POP B (@incr_top_of_stack)
    0xC6, // 009 INCR B
    0x96, // 010 PUSH B
    0x7E, // 011 CALL @copy_top_of_stack_to_C
    0x0E, // 012 (14)
    0x75, // 013 RETURN
    0x73, // 014 POP C (@copy_top_of_stack_to_C)
    0x9E, // 015 PUSH C
    0x75  // 016 RETURN
};

extern const byte num_test_push_pop_call_ret_data_bytes = 0;

// Needs to be at least 1 byte in this array
extern const byte test_push_pop_call_ret_data_bytes[] PROGMEM = {
    0x00 // Placeholder.
};

// Max of seven characters
extern const char test_push_pop_call_ret_program_name[] = "tstppcr";
