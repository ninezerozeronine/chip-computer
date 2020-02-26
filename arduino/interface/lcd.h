#ifndef LCD_H
#define LCD_H

#include "Arduino.h"
#include <LiquidCrystal_I2C.h>

#include "enums.h"

#define CURSOR_BLINK_INTERVAL 750

// LCD cursor is defined with rows and columns starting top left
// e.g. setCursor(12, 2) sets the cursor on the 13 column, 3rd row.

class Lcd {
    public:
        Lcd();
        void init();

        void draw_address(int address, e_number_base number_base);
        void draw_queued_address(char queued_address_str[]);
        void draw_data(int data, e_number_base number_base, e_sign_mode sign_mode);
        void draw_queued_data(char queued_data_str[]);
        void draw_number_base_indicator(e_number_base number_base);
        void draw_sign_mode_indicator(e_sign_mode sign_mode);
        void draw_address_update_mode_indicator(e_address_update_mode address_update_mode);
        void draw_ram_region_indicator(e_ram_region ram_region);
        void draw_run_mode_indicator(e_run_mode run_mode);
        void draw_clock_frequency(float frequency);
        void draw_program_name(char program_name[]);
        e_input_field get_input_field();
        void set_input_field(e_input_field input_field);

        void update();

    private:
        LiquidCrystal_I2C display;
        e_input_field input_field;

        byte queued_address_cursor_row;
        byte queued_address_cursor_column;
        byte queued_data_cursor_row;
        byte queued_data_cursor_column;

        unsigned long last_cursor_toggle;
        bool cursor_on;

        char print_buf[16];

        void _draw_static_elements();
        void _reset_cursor();
        void _byte_to_binary(byte value, char buffer[]);
        int _data_to_signed_equiv(byte data, e_sign_mode sign_mode);
};

#endif
