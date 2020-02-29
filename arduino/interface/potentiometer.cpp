// Convenience class to use a potentiometer with Arduino
// 
// To use pots, connect the outer pins of the pot to ground and +5v, then the 
// middle pin to the analog input pin chosen.

#include "potentiometer.h"

// Constructor
// 
// pin - The pin the potentiometer is reading from
// update_period - How long to wait in milliseconds before re-reading the potentiometer value
// callback - the function to call when the value of the potentiometer changes
Potentiometer::Potentiometer(uint8_t pin, uint8_t update_period) {
    _pin = pin;
    _update_period = update_period;
    _last_update = 0;
    _newest_reading_index = NUM_READINGS - 1;
    for (uint8_t index = 0; index < NUM_READINGS; ++index) {
        _readings[index] = 0;
    }
}

// Initialise the object
//
// Don't do this in the constructor so we're in control
void Potentiometer::init() {
    pinMode(_pin, INPUT);
    _value = analogRead(_pin);
    _last_update = millis();
    for (uint8_t index = 0; index < NUM_READINGS; ++index) {
        _readings[index] = _value;
    }
}

// Get the last read value of the potentiometer
uint16_t Potentiometer::get_value(bool un_log) {
    uint16_t ret = _value;
    if (un_log) {
        if (_value <= 150) {
            ret = map(_value, 0, 150, 0, 511);
        } else {
            ret = map(_value, 151, 1023, 512, 1023);
        }
    }
    return ret;
}


bool Potentiometer::all_readings_same_as(uint16_t new_value){
    bool all_same = true;
    for (uint8_t index = 0; index < NUM_READINGS; ++index) {
        if (all_same) {
            if (new_value != _readings[index]) {
                all_same = false;
            }
        } else {
            break;
        }
    }
    return all_same;
}


// Update the potentiometer
//
// To be called once every time the main loop runs
void Potentiometer::update(void (*val_change_callback)(uint16_t)) {
    // Get current time
    unsigned long current_time = millis();

    // If it's time to re-read the pot
    if (current_time - _last_update > _update_period) {

        // Store this update time
        _last_update = current_time;

        // Get the current value
        uint16_t value = analogRead(_pin);

        // Update the most recent index
        _newest_reading_index = (_newest_reading_index + 1) % NUM_READINGS;

        // Store the reading in the array
        _readings[_newest_reading_index] = value;

        // find difference to last stable reading
        int8_t diff = value - _value;
        diff = abs(diff);

        if ( ((value != _value) && all_readings_same_as(value)) || diff > 2) {
            _value = value;
            if (val_change_callback != NULL) {
                val_change_callback(_value);
            }
        }
    }
}