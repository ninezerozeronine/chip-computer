// Provides convenient bridge between user and computer.

// TODO - change number base to data interpret and add raw mode.
// TODO - update so that changing base or signed mode doesn't clear.
// TODO - Delete last queued character rather then clear the whole thing.

#ifndef MONITOR_H
#define MONITOR_H

#include "Arduino.h"

#include "hardware_bridge.h"
#include "enums.h"
#include "lcd.h"
#include "prog_fibonacci.h"

class Monitor {
    public:
        Monitor();
        void init();

        void next_stored_pgm();
        void transfer_stored_pgm();

        void next_number_base();
        void toggle_sign_mode();
        void toggle_address_update_mode();
        void toggle_ram_region();
        
        void propose_address_character(char character);
        void confirm_address();
        void clear_queued_address();
        void incr_address();
        void decr_address();

        void propose_data_character(char character);
        void write_data();
        void clear_queued_data();

        void enable_reset();
        void disable_reset();

        void toggle_run_pause();
        void quarter_step();
        void half_step();
        void full_step();
        void set_speed(int speed);

    private:
        void constructor_defaults();

        Lcd lcd;
        HardwareBridge bridge;

        byte num_programs;
        byte num_program_bytes [8];
        byte num_data_bytes [8];
        byte * program_bytes [8];
        byte * data_bytes [8];
        char * program_names [8];
        byte program_index;

        char queued_address_str[12];
        char proposed_address_str[12];
        char queued_data_str[12];
        char proposed_data_str[12];

        e_run_mode run_mode;
        e_sign_mode sign_mode;
        e_number_base number_base;
        e_address_update_mode address_update_mode;

        bool _character_is_valid_for_number_base(char character, e_number_base number_base_);
        void _add_char_to_string(char existing_string[], char character);
        int _string_to_value(char in_string[], e_number_base number_base_);
        bool _is_within_range(int value);
        void _send_clock_pulses(int num_pulses);
};

#endif