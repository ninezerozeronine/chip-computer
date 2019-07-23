// Convenience class to use a button with Arduino
// 
// To use a button, have it ground the pin it's connected to when set to "on".

#include "button.h"

Button::Button() {
    constructor_defaults();
}

// Constructor
//
// pin - the pin the button is connected to
// debounce_time - the number of miliseconds for the button to be in it's new state before considering it pressed
// low_to_high_callback - the callback to call when the button goes from unpressed to pressed
// high_to_low_callback - the callback to call when the button goes from pressed to unpressed
Button::Button(byte pin_, byte debounce_time_) {
    constructor_defaults();
    set_pin(pin_);
    set_debounce_time(debounce_time_);
}

void Button::constructor_defaults() {
    pin = 0;
    debounce_time = 0;
    stable_state = LOW;
    last_read_state = LOW;
    last_state_change = 0;
}

void Button::set_pin(byte pin_){
    pin = pin_;
}

void Button::set_debounce_time(byte debounce_time_){
    debounce_time = debounce_time_;
}

byte Button::get_state(){
    return stable_state;
}

// Set up button ready for use.
// Note that we're using INPUT_PULLUP to save on having to add a resistor
void Button::init() {
    pinMode(pin, INPUT_PULLUP);
    stable_state, last_read_state = !digitalRead(pin);
    last_state_change = millis();
}

// Update the button each time round the main loop
void Button::update(void (*low_to_high_callback)(), void (*high_to_low_callback)()) {
    // Read state of the button (invert because we're using INPUT_PULLUP)
    byte current_state = !digitalRead(pin);

    // If the button is in a different state to the stable state
    if (current_state != stable_state) {

        // Get current time
        unsigned long current_time = millis();

        // If the button is in the same state as it was last time
        if (current_state == last_read_state) {

            // If it's been in this new state for longer that the debounce time, flip the state
            // and call the callbacks
            if (current_time - last_state_change > debounce_time) {
                stable_state = current_state;
                if (current_state == HIGH) {
                    if (low_to_high_callback != NULL) {
                        low_to_high_callback();
                    }
                } else {
                    if (high_to_low_callback != NULL) {
                        high_to_low_callback();
                    }
                }
            }

        // Else the button has just changed state
        } else {
            // Set the last state and record the time
            last_read_state = current_state;
            last_state_change = current_time;
        }
    }
}
