#ifndef HARDWARE_BRIDGE_H
#define HARDWARE_BRIDGE_H

#define ADDRESS_SERIAL_LATCH_PIN -1
#define ADDRESS_SERIAL_CLOCK_PIN -1
#define ADDRESS_SERIAL_PIN -1

#define STAGED_DATA_SERIAL_LATCH_PIN -1
#define STAGED_DATA_SERIAL_CLOCK_PIN -1
#define STAGED_DATA_SERIAL_PIN -1

#define READ_DATA_SERIAL_LATCH_PIN -1
#define READ_DATA_SERIAL_CLOCK_PIN -1
#define READ_DATA_SERIAL_PIN -1

#define RAM_REGION_PIN -1
#define RAM_CONTROL_MODE_PIN -1
#define RESET_PIN -1
#define RAM_WRITE_SIGNAL_PIN -1
#define CLOCK_TYPE_PIN -1
#define CLOCK_ENABLED_PIN -1
#define CLOCK_PIN 9 

#include "Arduino.h"
#include "TimerOne.h"

#include "enums.h"

// Low level direct control of computer via arduino.
// Very little logic to make sure nothing silly happens.
class HardwareBridge {
    public:
        HardwareBridge();
        void constructor_defaults();
        void init();

        e_mem_region get_ram_region();
        void set_ram_region(e_mem_region mem_region_);

        e_ram_control_mode get_ram_control_mode();
        void set_ram_control_mode(e_ram_control_mode ram_control_mode_);

        e_clock_type get_clock_type();
        void set_clock_type(e_clock_type clock_type);

        bool get_reset();
        void set_reset(bool reset_);

        bool get_clock_enabled();
        void set_clock_enabled(bool clock_enabled_);

        int get_address();
        void set_address(int address_);

        int get_data();
        void set_staged_data(int _data);

        float get_clock_frequency();
        void set_clock_frequency(float clock_speed_)

        void send_clock_pulses(int num_pulses);

        void send_ram_write_pulse();

    private:
        e_mem_region ram_region;
        e_ram_control_mode ram_control_mode;
        e_clock_type clock_type;
        bool reset;
        bool clock_enabled;
        int address;
        float clock_speed;
};

#endif