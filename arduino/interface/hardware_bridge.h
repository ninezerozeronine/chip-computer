#ifndef HARDWARE_BRIDGE_H
#define HARDWARE_BRIDGE_H

#include "Arduino.h"
#include "TimerOne.h"

#include "pindefs.h"
#include "enums.h"

#define CLOCK_SOURCE_BIT_INDEX 0
#define CLOCK_ENABLE_BIT_INDEX 1
#define RESET_BIT_INDEX 2
#define RAM_WRITE_BIT_INDEX 3
#define RAM_CONTROL_BIT_INDEX 4
#define RAM_REGION_BIT_INDEX 5

// Low level direct control of computer via arduino.
// Very little logic to make sure nothing silly happens.
class HardwareBridge {
    public:
        HardwareBridge();
        void init();

        e_ram_region get_ram_region();
        void set_ram_region(e_ram_region ram_region_);

        e_ram_control_mode get_ram_control_mode();
        void set_ram_control_mode(e_ram_control_mode ram_control_mode_);

        e_clock_source get_clock_source();
        void set_clock_source(e_clock_source clock_source_);

        bool get_reset();
        void set_reset(bool reset_);

        bool get_clock_enabled();
        void set_clock_enabled(bool clock_enabled_);

        byte get_address();
        void set_address(byte address_);

        byte get_data();
        void set_staged_data(byte _data);

        void send_clock_pulses(int num_pulses);

        void send_ram_write_pulse();

        void set_clock_to_pulse_mode();
        void set_clock_to_pwm_mode(float frequency);

    private:
        void constructor_defaults();

        e_ram_region ram_region;
        e_ram_control_mode ram_control_mode;
        e_clock_source clock_source;
        bool reset;
        bool clock_enabled;
        byte address;
        float clock_frequency;
        long adjusted_period_in_usecs;
        byte control_bits;
        byte staged_data;

        byte _shift_in(byte data_pin, byte clock_pin, byte shiftload_pin);
        byte _shift_out(byte data, byte data_pin, byte clock_pin, byte latchout_pin, bool latchout);
        void _update_shift_outs();
};

#endif