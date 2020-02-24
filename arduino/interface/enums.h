#ifndef ENUMS_H
#define ENUMS_H

enum e_run_mode {
    RUNNING,
    PAUSED
};

enum e_ram_region {
    PROGRAM,
    DATA
};

enum e_ram_control_mode {
    USER,
    CONTROL_UNIT
};

enum e_sign_mode {
    SIGNED,
    UNSIGNED
};

enum e_number_base {
    BINARY,
    DECIMAL,
    HEXADECIMAL
};

enum e_arduino_clock_type {
    PULSES,
    FREQUENCY
};

enum e_clock_source {
    ARDUINO_PIN,
    CRYSTAL,
};

enum e_address_update_mode {
    AUTO_INC,
    NO_INC
};

#endif