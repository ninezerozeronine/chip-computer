// Convenience class to use a button with Arduino

#ifndef BUTTON_H
#define BUTTON_H

#include "Arduino.h"

class Button {
    public:
        Button();
        Button(byte pin_, byte debounce_time_=10);
        void init();
        void set_pin(byte pin_);
        void set_debounce_time(byte debounce_time);
        byte get_state();
        void update(void (*low_to_high_callback)()=NULL, void (*high_to_low_callback)()=NULL);

    private:
        void constructor_defaults();

        // The pin this button is connected to
        byte pin;
  
        // The time in milliseconds for the state to be held before considering it to be on
        byte debounce_time;

        // Whether the button is pressed or not
        byte stable_state;
    
        // The state of the pin read at the last update
        byte last_read_state;
    
        // When the button last changes state (as directly read)
        unsigned long last_state_change;
};

#endif