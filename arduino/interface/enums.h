#ifndef ENUMS_H
#define ENUMS_H

enum e_run_mode {
    RUNNING,
    PAUSED
};

enum e_mem_region {
    PROGRAM,
    DATA
};

enum e_mem_control_mode {
    USER,
    CONTROL_UNIT
};

enum e_signed_mode {
    SIGNED,
    UNSIGNED
};

enum e_number_base {
    BINARY,
    DECIMAL,
    HEXADECIMAL
}

enum e_clock_type {
    PULSES,
    FREQUENCY,
    CRYSTAL
}

#endif