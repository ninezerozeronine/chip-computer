#ifndef HARDWARE_BRIDGE_H
#define HARDWARE_BRIDGE_H

#include "Arduino.h"
#include "TimerOne.h"

#include "pindefs.h"
#include "enums.h"

// Low level direct control of computer via arduino.
// Very little logic to make sure nothing silly happens.
class HardwareBridge {
    public:
        HardwareBridge();
        void init();

        e_mem_region get_ram_region();
        void set_ram_region(e_ram_region ram_region_);

        e_ram_control_mode get_ram_control_mode();
        void set_ram_control_mode(e_ram_control_mode ram_control_mode_);

        e_clock_source get_clock_source();
        void set_clock_source(e_clock_source clock_source_);

        e_arduino_clock_type get_arduino_clock_type();
        void set_arduino_clock_type(e_arduino_clock_type arduino_clock_type_);

        bool get_reset();
        void set_reset(bool reset_);

        bool get_clock_enabled();
        void set_clock_enabled(bool clock_enabled_);

        int get_address();
        void set_address(int address_);

        int get_data();
        void set_staged_data(int _data);

        float get_clock_frequency();
        void set_clock_frequency(float clock_frequency_);

        void send_clock_pulses(int num_pulses);

        void send_ram_write_pulse();

    private:
        void constructor_defaults();

        e_mem_region ram_region;
        e_ram_control_mode ram_control_mode;
        e_clock_source clock_source;
        e_arduino_clock_type arduino_clock_type;
        bool reset;
        bool clock_enabled;
        int address;
        float clock_frequency;
};

#endif