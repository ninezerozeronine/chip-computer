#include "cpubridge.h"


HardwareBridge::HardwareBridge() {
    constructor_defaults();
}


void HardwareBridge::constructor_defaults() {
    ram_region = PROGRAM;
    ram_control_mode = USER;
    clock_type = MANUAL;
    reset = false;
    clock_enabled = false;
    int address = 0;
    clock_speed = 0;
}


void HardwareBridge::HardwareBridge::init() {
    pinMode(RAM_REGION_PIN, OUTPUT);
    pinMode(RAM_CONTROL_MODE_PIN, OUTPUT);
    pinMode(CLOCK_TYPE_PIN, OUTPUT);
    pinMode(RESET_PIN, OUTPUT);
    pinMode(ADDRESS_SERIAL_LATCH_PIN, OUTPUT);
    pinMode(ADDRESS_SERIAL_CLOCK_PIN, OUTPUT);
    pinMode(ADDRESS_SERIAL_PIN, OUTPUT);
    pinMode(ADDRESS_SERIAL_LATCH_PIN, OUTPUT);
    pinMode(DATA_SERIAL_CLOCK_PIN, OUTPUT);
    pinMode(DATA_SERIAL_PIN, INPUT);
    pinMode(CLOCK_ENABLED_PIN, OUTPUT);
    pinMode(CLOCK_PIN, OUTPUT);

    Timer1.initialize(1000000);
    Timer1.pwm(CLOCK_PIN, 512);
}


e_ram_region HardwareBridge::get_ram_region() {
    return ram_region;
}


void HardwareBridge::set_ram_region(e_ram_region ram_region_) {
    ram_region = ram_region_;
    switch (ram_region) {
        case PROGRAM:
            digitalWrite(MEM_REGION_PIN, LOW);
            break;
        case DATA:
            digitalWrite(MEM_REGION_PIN, HIGH);
            break;
    }
}


e_ram_control_mode HardwareBridge::get_ram_control_mode() {
    return ram_control_mode;
}


void HardwareBridge::set_ram_control_mode(e_ram_control_mode ram_control_mode_) {
    ram_control_mode = ram_control_mode_;
    switch (ram_control_mode) {
        case USER:
            digitalWrite(RAM_CONTROL_MODE_PIN, LOW);
            break;
        case CONTROL_UNIT:
            digitalWrite(RAM_CONTROL_MODE_PIN, HIGH);
            break;
    }
}


e_clock_type HardwareBridge::get_clock_type() {
    return clock_type;
}


void HardwareBridge::set_clock_type(e_clock_type clock_type) {
    clock_type = clock_type_;
    switch (clock_type) {
        case PULSES:
            digitalWrite(CLOCK_TYPE_PIN, LOW);
            TimerOne.disablePwm(CLOCK_PIN);
            digitalWrite(CLOCK_PIN, LOW);
            break;
        case FREQUENCY:
            digitalWrite(CLOCK_TYPE_PIN, LOW);
            TimerOne.pwm(CLOCK_PIN, 512);
            break;
        case CRYSTAL:
            digitalWrite(CLOCK_TYPE_PIN, HIGH);
            break;
    }
}


bool HardwareBridge::get_reset() {
    return reset;
}


void HardwareBridge::set_reset(bool reset_) {
    reset = reset_;
    if (reset) {
        digitalWrite(RESET_PIN, HIGH);
    } else {
        digitalWrite(RESET_PIN, LOW);
    }
}


bool HardwareBridge::get_clock_enabled() {
    return clock_enabled;
}


void HardwareBridge::set_clock_enabled(bool clock_enabled_) {
    clock_enabled = clock_enabled_;
    if (clock_enabled) {
        digitalWrite(CLOCK_ENABLED_PIN, HIGH);
    } else {
        digitalWrite(CLOCK_ENABLED_PIN, LOW);
    }
}


int HardwareBridge::get_address() {
    return address;
}


void HardwareBridge::set_address(int address_) {
    address = address_;
    digitalWrite(ADDRESS_SERIAL_LATCH_PIN, LOW);
    shiftOut(ADDRESS_SERIAL_DATA_PIN, ADDRESS_SERIAL_CLOCK_PIN, LSBFIRST, address);
    digitalWrite(ADDRESS_SERIAL_LATCH_PIN, HIGH);
}


int HardwareBridge::get_data() {
    digitalWrite(READ_DATA_SERIAL_CLOCK_PIN, LOW);
    delayMicroseconds(5);
    return shiftIn(READ_DATA_SERIAL_DATA_PIN, READ_DATA_SERIAL_CLOCK_PIN, MSBFIRST);
}


void HardwareBridge::set_staged_data(int _data) {
    digitalWrite(STAGED_DATA_SERIAL_LATCH_PIN, LOW);
    shiftOut(STAGED_DATA_SERIAL_DATA_PIN, STAGED_DATA_SERIAL_CLOCK_PIN, LSBFIRST, _data);
    digitalWrite(STAGED_DATA_SERIAL_LATCH_PIN, HIGH);
}


float HardwareBridge::get_clock_frequency() {
    return clock_frequency;
}


// Set the clock frequency in hertz
//
// The magic 250000 comes from:
// * TimerOne needs a period in micro seconds not a frequency in Hz
// * There are 1000000 microseconds in a second so dividing this by
//   the frequency in Hz gives us the period in micro seconds.
// * The clock mechanics mean that the output frequency (between
//   rising edges of the data clock) is 4 times slower than the 
//   input frequency.
// * Dividing 250000 rather than 1000000 by the frequency gives us an
//   answer/period 4 times smaller.
void HardwareBridge::set_clock_frequency(float clock_frequency_) {
    clock_frequency = clock_frequency_;
    int freq_in_usecs = 250000.0/clock_frequency;
    TimerOne.setPeriod(freq_in_usecs);
}

void HardwareBridge::send_clock_pulses(int num_pulses) {
    for (int i = 0; i < num_pulses; ++i) {
        digitalWrite(CLOCK_PIN, HIGH);
        delayMicroseconds(5);
        digitalWrite(CLOCK_PIN, LOW);
        delayMicroseconds(5);
    }
}

void HardwareBridge::send_ram_write_pulse() {
    digitalWrite(RAM_WRITE_SIGNAL_PIN, HIGH);
    delayMicroseconds(5);
    digitalWrite(RAM_WRITE_SIGNAL_PIN, LOW);
    delayMicroseconds(5);
}