#ifndef LCD_H
#define LCD_H

#include "Arduino.h"

#include "enums.h"

class Lcd {
    public:
        Lcd();
        void constructor_defaults();

        void draw_address(int address, e_number_base number_base);
        void draw_data(int data, e_number_base number_base, e_signed_mode, signed_mode);
        void draw_number_base(e_number_base number_base);
}

#endif