// Convenience class to use a keypad with Arduino

#ifndef KEYPAD_H
#define KEYPAD_H

#include "Arduino.h"

#define NUM_KEYPAD_VALUES 16
#define KEYPAD_DELTA 6

class Keypad {
    public:
        Keypad();
        Keypad(byte pin_, int * keypad_values_, byte debounce_time_=10);
        void init();
        void set_pin(byte pin_);
        void set_debounce_time(byte debounce_time);
        void set_keypad_values(int * keypad_values);
        int get_current_key();
        void update(void (*key_pressed_callback)(int)=NULL, void (*key_released_callback)(int)=NULL);

    private:
        void constructor_defaults();

        int read_current_key();

        int keypad_value_to_key(int keypad_value);

        // The pin the keypad is connected to
        byte pin;
  
        // The time in milliseconds for the state to be held before considering it to be on
        byte debounce_time;

        int * keypad_values;

        // The current state of the keypad (i.e. which key is pressed) after correcting for debounce
        int stable_key;
    
        // The state of the keypad at the last update
        int last_current_key;

        // When the keypad last changed state (as directly read)
        unsigned long last_state_change_time;
};

#endif