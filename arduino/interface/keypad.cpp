// Convenience class to use a keypad with Arduino
// 

#include "keypad.h"

Keypad::Keypad() {
    constructor_defaults();
}

// Constructor
//
// pin_ - The pin the button is connected to
// debounce_time_ - The debounce time for the button.
Keypad::Keypad(byte pin_, int * keypad_values_, byte debounce_time_) {
    constructor_defaults();
    set_pin(pin_);
    set_keypad_values(keypad_values_);
    set_debounce_time(debounce_time_);

}

// Default values for the class
void Keypad::constructor_defaults() {
    pin = 0;
    debounce_time = 10;
    stable_key = -1;
    last_current_key = -1;
    last_state_change_time = 0;
}

// Set up keypad ready for use.
// Note that we're using INPUT_PULLUP to save on having to add a resistor
void Keypad::init() {
    pinMode(pin, INPUT);
    stable_key, last_current_key = read_current_key();
    last_state_change_time = millis();
}

void Keypad::set_pin(byte pin_){
    pin = pin_;
}

void Keypad::set_debounce_time(byte debounce_time_){
    debounce_time = debounce_time_;
}

void Keypad::set_keypad_values(int * keypad_values_){
    keypad_values = keypad_values_;
}


int Keypad::get_current_key(){
    return stable_key;
}

// Update the keypad.
//
// Should be called as frequently as possible. Although -1
// is a key state (no keys pressed) it isn't a key, so
// callbacks aren't triggered for it.
//
// Callbacks are passed the number of the key that was pressed
// or released.
//
// key_pressed_callback - called when a key is pressed
// key_released_callback - called when a key is released
void Keypad::update(
    void (*key_pressed_callback)(int),
    void (*key_released_callback)(int)
) {
    // Get current time
    unsigned long current_time = millis();

    // Read state of the keypad
    int current_key = read_current_key();

    // If the currently active key isn't the stable key
    if (current_key != stable_key) {

        // If the currently active key is the same as it was last update
        if (current_key == last_current_key) {

            // If the new key has been active for longer than the debounce,
            // time, update the stable key and call the callbacks
            if (current_time - last_state_change_time > debounce_time) {
                if (stable_key != -1) {
                    if (key_released_callback != NULL) {
                        key_released_callback(stable_key);
                    }
                }

                if (current_key != -1) {
                    if (key_pressed_callback != NULL) {
                        key_pressed_callback(current_key);
                    }
                }

                stable_key = current_key;
            }

        // Else the key has just changed (but isn't stable yet)
        } else {
            // Set the last state and record the time
            last_current_key = current_key;
            last_state_change_time = current_time;
        }
    }
}



// Read current key
// 
// A direct read from the keypad - this is the immediate, unfiltered,
// undebounced most up to date state of the keypad/key pressed.
int Keypad::read_current_key() {
    int keypad_value = analogRead(pin);
    return keypad_value_to_key(keypad_value);
}


// Convert the value read from the keypad into an int representing the key
//
// keypad_value - The value read from the keypad
// 
// returns int - The currently pressed key. -1 if no key is pressed.
int Keypad::keypad_value_to_key(int keypad_value) {
    // Iterate over keypad values, return index of value if value is within range
    for (int index = 0; index < NUM_KEYPAD_VALUES; ++index) {
        if (
            (keypad_value >= keypad_values[index] - KEYPAD_DELTA) &&
            (keypad_value <= keypad_values[index] + KEYPAD_DELTA)
        ){
            return index;
        }
    }

    // Otherwise no match
    return -1;
}
