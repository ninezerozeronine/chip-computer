// Provides convenient bridge between user and computer.


// Address cancel
// Address confirm
// Prog/Data mem
// Auto Inc
// Address Up
// Address Down

// Data cancel
// Write data

// Reset
// Run/Pause
// 1/4 step
// 1/2 step
// Full step

// Base select
// Signed select
// 


#ifndef CPUBRIDGE_H
#define CPUBRIDGE_H

#include "Arduino.h"

class CPUBridge {
    public:
        CPUBridge();
        void constructor_defaults();

        void next_stored_pgm();
        void transfer_stored_pgm();

        void next_number_base();
        void toggle_signed_mode();
        void toggle_address_inc_mode();
        void toggle_mem_type();
        
        void propose_addr_character();
        void confirm_adddress();
        void cancel_address();
        void incr_address();
        void decr_address();

        void write_data();
        void cancel_data();
        void propose_data_character();
        void propose_data_negative_toggle();

        void enable_reset();
        void disable_reset();

        void toggle_run_pause();
        void set_running();
        void set_paused();
        void quarter_step();
        void half_step();
        void full_step();





        void update();

    private:
        void constructor_defaults();

        byte num_programs;
        byte program_index;

        byte num_number_bases;
        byte number_base_index;

        byte num_mem_types;
        byte mem_type_index;

        bool signed_mode;
        bool address_inc_mode;

        bool reset;
        Lcd lcd;

        void send_mem_type_to_computer();\



};

#endif