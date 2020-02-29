// Convenience class to use a potentiometer with Arduino

#ifndef potentiometer_h
#define potentiometer_h

#include "Arduino.h"

#define NUM_READINGS 5

class Potentiometer {
    public:
        Potentiometer(uint8_t pin, uint8_t update_period=10);
        void init();
        uint16_t get_value(bool un_log=false);
        void update(void (*val_change_callback)(uint16_t)=NULL);

    private:
        // Index of the most recent reading
        uint8_t _newest_reading_index;

        // The last few readings to smooth out noise
        uint16_t _readings[NUM_READINGS];

        // The pin this potentiometer is reading from
        uint8_t _pin;

        // The value of the potentiometer
        uint16_t _value;

        // How many millisecods to wait between updates
        uint8_t _update_period;

        // When the last update was
        unsigned long _last_update;

        bool all_readings_same_as(uint16_t new_value);
};

#endif