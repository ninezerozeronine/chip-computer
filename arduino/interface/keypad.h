// Convenience class to use a keypad with Arduino

#ifndef KEYPAD_H
#define KEYPAD_H

#include "Arduino.h"

class Keypad {
    public:
        Keypad();
        Keypad(byte pin_, byte debounce_time_=10);
        void init();
        void set_pin(byte pin_);
        void set_debounce_time(byte debounce_time);
        int get_current_key();
        void update(
            void (*key_pressed_callback)()=NULL,
            void (*key_released_callback)()=NULL,
            void (*key_repeat_callback)()=NULL,
        );

    private:
        void constructor_defaults();

        // The pin the keypad is connected to
        byte pin;
  
        // The time in milliseconds for the state to be held before considering it to be on
        byte debounce_time;

        // The time in milliseconds that a key needs to be held for before repeating
        unsigned long repeat_delay;

        // The time in milliseconds to between each call of the repeat callback
        unsigned long repeat_frequency;

        // Whether the held key is currently repeating
        bool repeating;

        // The current state of the keypad (i.e. which key is pressed) after correcting for debounce
        int stable_key;
    
        // The state of the keypad at the last update
        int last_key_state;
    
        // When the current key last changed state (as directly read)
        unsigned long last_state_change;

        // When the repeat callback was last called
        unsigned long last_repeat_time;
};

#endif