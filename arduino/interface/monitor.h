// Provides convenient bridge between user and computer.


#ifndef MONITOR_H
#define MONITOR_H

#include "Arduino.h"

#include "hardware_bridge.h"
#include "enums.h"

class Monitor {
    public:
        Monitor();
        void constructor_defaults();

        void next_stored_pgm();
        void transfer_stored_pgm();

        void next_number_base();
        void toggle_signed_mode();
        void toggle_address_inc_mode();
        void toggle_ram_region();
        
        void propose_addr_character();
        void confirm_adddress();
        void clear_queued_address();
        void incr_address();
        void decr_address();

        void propose_data_character();
        void write_data();
        void clear_queued_data();

        void enable_reset();
        void disable_reset();

        void toggle_run_pause();
        void quarter_step();
        void half_step();
        void full_step();
        void set_speed(int speed_);





        void update();

    private:
        void constructor_defaults();

        HardwareBridge bridge;

        byte num_programs;
        byte num_program_bytes [];
        byte num_data_bytes [];
        byte * program_bytes [];
        byte * data_bytes [];
        char * program_names [];
        byte program_index;

        byte num_number_bases;
        byte number_base_index;

        byte num_mem_types;
        byte mem_type_index;

        bool signed_mode;
        bool address_inc_mode;

        bool running;

        Lcd lcd;

        void set_user_ram_control();
        void set_computer_ram_control();

        void set_program_memory_active();
        void set_data_memory_active();

        void send_mem_type_to_computer();

        bool queued_data_is_neg;

        void read_and_update_data();

        void set_signed_mode();

        void set_running();
        void set_paused();
};

#endif