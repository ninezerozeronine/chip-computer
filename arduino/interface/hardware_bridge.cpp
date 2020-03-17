#include "hardware_bridge.h"


HardwareBridge::HardwareBridge() {
    constructor_defaults();
}


void HardwareBridge::constructor_defaults() {
    ram_region = PROGRAM;
    ram_control_mode = USER;
    clock_source = ARDUINO_PIN;
    reset = false;
    clock_enabled = false;
    address = 0;
    clock_frequency = 0.1;
    adjusted_period_in_usecs = 1000000;
    control_bits = 0;
}


void HardwareBridge::HardwareBridge::init() {
    pinMode(SHIFT_TO_CPU_DATA_PIN, OUTPUT);
    pinMode(SHIFT_TO_CPU_CLOCK_PIN, OUTPUT);
    pinMode(SHIFT_TO_CPU_LATCHOUT_PIN, OUTPUT);

    pinMode(SHIFT_FROM_CPU_DATA_PIN, INPUT);
    pinMode(SHIFT_FROM_CPU_CLOCK_PIN, OUTPUT);
    pinMode(SHIFT_FROM_CPU_SHIFTLOAD_PIN, OUTPUT);

    pinMode(CLOCK_PIN, OUTPUT);

    Timer1.initialize(1000000);

    digitalWrite(SHIFT_TO_CPU_DATA_PIN, LOW);
    digitalWrite(SHIFT_TO_CPU_CLOCK_PIN, LOW);
    digitalWrite(SHIFT_TO_CPU_LATCHOUT_PIN, LOW);

    digitalWrite(SHIFT_FROM_CPU_CLOCK_PIN, LOW);
    digitalWrite(SHIFT_FROM_CPU_SHIFTLOAD_PIN, HIGH);

    _update_shift_outs();
}


e_ram_region HardwareBridge::get_ram_region() {
    return ram_region;
}


void HardwareBridge::set_ram_region(e_ram_region ram_region_) {
    if (ram_region != ram_region_) {
        ram_region = ram_region_;
        switch (ram_region) {
            case PROGRAM:
                bitWrite(control_bits, RAM_REGION_BIT_INDEX, 0);
                break;
            case DATA:
                bitWrite(control_bits, RAM_REGION_BIT_INDEX, 1);
                break;
        }
        _update_shift_outs();
    }
}


e_ram_control_mode HardwareBridge::get_ram_control_mode() {
    return ram_control_mode;
}


void HardwareBridge::set_ram_control_mode(e_ram_control_mode ram_control_mode_) {
    if (ram_control_mode != ram_control_mode_) {
        ram_control_mode = ram_control_mode_;
        switch (ram_control_mode) {
            case USER:
                bitWrite(control_bits, RAM_CONTROL_BIT_INDEX, 0);
                break;
            case CONTROL_UNIT:
                bitWrite(control_bits, RAM_CONTROL_BIT_INDEX, 1);
                break;
        }
        _update_shift_outs();
    }
}


e_clock_source HardwareBridge::get_clock_source() {
    return clock_source;
}


void HardwareBridge::set_clock_source(e_clock_source clock_source_) {
    if (clock_source != clock_source_) {
        clock_source = clock_source_;
        switch (clock_source) {
            case ARDUINO_PIN:
                bitWrite(control_bits, CLOCK_SOURCE_BIT_INDEX, 0);
                break;
            case CRYSTAL:
                bitWrite(control_bits, CLOCK_SOURCE_BIT_INDEX, 1);
                break;
        }
        _update_shift_outs();
    }
}


bool HardwareBridge::get_reset() {
    return reset;
}


void HardwareBridge::set_reset(bool reset_) {
    if (reset != reset_) {
        reset = reset_;
        if (reset) {
            bitWrite(control_bits, RESET_BIT_INDEX, 1);
        } else {
            bitWrite(control_bits, RESET_BIT_INDEX, 0);
        }
        _update_shift_outs();
    }
}


bool HardwareBridge::get_clock_enabled() {
    return clock_enabled;
}


void HardwareBridge::set_clock_enabled(bool clock_enabled_) {
    if (clock_enabled != clock_enabled_) {
        clock_enabled = clock_enabled_;
        if (clock_enabled) {
            bitWrite(control_bits, CLOCK_ENABLE_BIT_INDEX, 1);
        } else {
            bitWrite(control_bits, CLOCK_ENABLE_BIT_INDEX, 0);
        }
        _update_shift_outs();
    }
}


byte HardwareBridge::get_address() {
    return address;
}


void HardwareBridge::set_address(byte address_) {
    address = address_;
    _update_shift_outs();
}


byte HardwareBridge::get_data() {
    return _shift_in(SHIFT_FROM_CPU_DATA_PIN, SHIFT_FROM_CPU_CLOCK_PIN, SHIFT_FROM_CPU_SHIFTLOAD_PIN);
}


void HardwareBridge::set_staged_data(byte data) {
    staged_data = data;
    _update_shift_outs();

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
    bitWrite(control_bits, RAM_WRITE_BIT_INDEX, 1);
    _update_shift_outs();
    delayMicroseconds(5);
    bitWrite(control_bits, RAM_WRITE_BIT_INDEX, 0);
    _update_shift_outs();
    delayMicroseconds(5);
}


void HardwareBridge::set_clock_to_pulse_mode() {
    Timer1.disablePwm(CLOCK_PIN);
    digitalWrite(CLOCK_PIN, LOW);
}

// Set the clock to pwn mode with a frequency in hertz
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
void HardwareBridge::set_clock_to_pwm_mode(float frequency) {
    unsigned long adjusted_period_in_usecs = 250000.0/frequency;
    Timer1.pwm(CLOCK_PIN, 512, adjusted_period_in_usecs);
}


byte HardwareBridge::_shift_in(byte data_pin, byte clock_pin, byte shiftload_pin) {
    byte current_bit = 0;
    byte result = 0;

    digitalWrite(clock_pin, LOW);

    digitalWrite(shiftload_pin, LOW);
    delayMicroseconds(5);
    digitalWrite(shiftload_pin, HIGH);

    for(int bit_index = 0; bit_index < 8; ++bit_index) {
        current_bit = digitalRead(data_pin);
        result |= current_bit << bit_index;
        digitalWrite(clock_pin, HIGH);
        delayMicroseconds(5);
        digitalWrite(clock_pin, LOW);
        delayMicroseconds(5);
    }

    return result;
}


byte HardwareBridge::_shift_out(byte data, byte data_pin, byte clock_pin, byte latchout_pin, bool latchout) {
    shiftOut(data_pin, clock_pin, LSBFIRST, data);
    digitalWrite(clock_pin, LOW);
    delayMicroseconds(5);
    if (latchout) {
        digitalWrite(latchout_pin, HIGH);
        delayMicroseconds(5);
        digitalWrite(latchout_pin, LOW);
        delayMicroseconds(5);
    }
}

void HardwareBridge::_update_shift_outs() {
    _shift_out(control_bits, SHIFT_TO_CPU_DATA_PIN, SHIFT_TO_CPU_CLOCK_PIN, SHIFT_TO_CPU_LATCHOUT_PIN, false);
    _shift_out(address, SHIFT_TO_CPU_DATA_PIN, SHIFT_TO_CPU_CLOCK_PIN, SHIFT_TO_CPU_LATCHOUT_PIN, false);
    _shift_out(staged_data, SHIFT_TO_CPU_DATA_PIN, SHIFT_TO_CPU_CLOCK_PIN, SHIFT_TO_CPU_LATCHOUT_PIN, true);
}