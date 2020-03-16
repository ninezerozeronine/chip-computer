#include "lcd.h"

// The Display has the following layout:
//
// A:       240 PRG INC
//  >  104_     DEC SIG
// D:       -34 RUN   1
//  > -25_      PRGNAME
//
// or with different data
//
// A:  00001111 DAT ---
//  >  _        BIN UNS
// D: -00001111 PSE 
//  >  _        PRGNAME


Lcd::Lcd() : display(0x27, 20, 4) {
    input_field = ADDRESS_FIELD;
    queued_address_cursor_row = 1;
    queued_address_cursor_column = 4;
    queued_data_cursor_row = 3;
    queued_data_cursor_column = 4;
    cursor_on = true;
    last_cursor_toggle = 0;
    strcpy(print_buf, "");
    strcpy(freq_buf, "");
}


void Lcd::init() {
    display.init();
    display.clear();
    display.backlight();
    _draw_static_elements();
    last_cursor_toggle = millis();
}


void Lcd::draw_address(int address, e_number_base number_base) {
    switch (number_base) {
        case BINARY:
            _byte_to_binary_string(address, print_buf);
            break;
        case DECIMAL:
            sprintf(print_buf, "%8d", address);
            break;
        case HEXADECIMAL:
            sprintf(print_buf, "%8X", address);
            break;
    }
    display.setCursor(4,0);
    display.print(print_buf);
    _reset_cursor();
}


void Lcd::draw_queued_address(char queued_address_str[]) {
    sprintf(print_buf, "%-8s", queued_address_str);
    display.setCursor(4,1);
    display.print(print_buf);
    queued_address_cursor_column = 4 + strlen(queued_address_str);
    queued_address_cursor_column = min(queued_address_cursor_column, 11);
    _reset_cursor();
}


void Lcd::draw_data(int data, e_number_base number_base, e_sign_mode sign_mode) {
    int display_equiv = _data_to_signed_equiv(data, sign_mode);
    switch (number_base) {
        case BINARY:
            if (display_equiv < 0) {
                _byte_to_binary_string((display_equiv * -1), print_buf);
                display.setCursor(3, 2);
                display.print("-");
            } else {
                _byte_to_binary_string(display_equiv, print_buf);
                display.setCursor(3, 2);
                display.print(" ");
            }
            display.setCursor(4, 2);
            display.print(print_buf);
            _reset_cursor();
            break;
        case DECIMAL:
            sprintf(print_buf, "%9d", display_equiv);
            display.setCursor(3, 2);
            display.print(print_buf);
            _reset_cursor();
            break;
        case HEXADECIMAL:
            sprintf(print_buf, "%9X", display_equiv);
            display.setCursor(3, 2);
            display.print(print_buf);
            _reset_cursor();
            break;
    }
}

// A:       240 PRG INC
//  >  104_     DEC SIG
// D:       -34 RUN   1
// 01234567890123456789
//  > -25_      PRGNAME
void Lcd::draw_queued_data(char queued_data_str[]) {
    byte string_length = strlen(queued_data_str);
    if (string_length == 0) {
        display.setCursor(3, 3);
        display.print("         ");
        queued_data_cursor_column = 4;
        _reset_cursor();
    } else {
        bool starts_with_minus = queued_data_str[0] == '-';
        if (string_length == 1) {
            if (starts_with_minus) {
                sprintf(print_buf, "%-9s", queued_data_str);
                display.setCursor(3, 3);
                display.print(print_buf);
                queued_data_cursor_column = 4;
                _reset_cursor();
            } else {
                sprintf(print_buf, "%-9s", queued_data_str);
                display.setCursor(4, 3);
                display.print(print_buf);
                queued_data_cursor_column = 5;
                _reset_cursor();
            }
        } else {
            if (starts_with_minus) {
                sprintf(print_buf, "%-9s", queued_data_str);
                display.setCursor(3, 3);
                display.print(print_buf);
                queued_data_cursor_column = string_length + 3;
                queued_data_cursor_column = min(queued_data_cursor_column, 11);
                _reset_cursor();
            } else {
                sprintf(print_buf, "%-9s", queued_data_str);
                display.setCursor(4, 3);
                display.print(print_buf);
                queued_data_cursor_column = string_length + 4;
                queued_data_cursor_column = min(queued_data_cursor_column, 11);
                _reset_cursor();
            }
        }
    }
}


void Lcd::draw_number_base_indicator(e_number_base number_base) {
    display.setCursor(13, 1);
    switch (number_base) {
        case BINARY:
            display.print("BIN");
            break;
        case DECIMAL:
            display.print("DEC");
            break;
        case HEXADECIMAL:
            display.print("HEX");
            break;
    }
    _reset_cursor();
}


void Lcd::draw_sign_mode_indicator(e_sign_mode sign_mode) {
    display.setCursor(17, 1);
    switch (sign_mode) {
        case SIGNED:
            display.print("SIG");
            break;
        case UNSIGNED:
            display.print("UNS");
            break;
    }
    _reset_cursor();
}


void Lcd::draw_address_update_mode_indicator(e_address_update_mode address_update_mode) {
    display.setCursor(17, 0);
    switch (address_update_mode) {
        case AUTO_INC:
            display.print("INC");
            break;
        case NO_INC:
            display.print("STA");
            break;
    }
    _reset_cursor();
}


void Lcd::draw_ram_region_indicator(e_ram_region ram_region) {
    display.setCursor(13, 0);
    switch (ram_region) {
        case PROGRAM:
            display.print("PRG");
            break;
        case DATA:
            display.print("DAT");
            break;
    }
    _reset_cursor();
}


void Lcd::draw_run_mode_indicator(e_run_mode run_mode) {
    display.setCursor(13, 2);
    switch (run_mode) {
        case RUNNING:
            display.print("RUN");
            break;
        case PAUSED:
            display.print("PSE");
            break;
    }
    _reset_cursor();
}


void Lcd::draw_clock_frequency(float frequency) {
    // 0.0 - 9.9
    if (frequency < 10.0) {
        int mult_frequency = frequency * 10;
        sprintf(freq_buf, "%02d", mult_frequency);
        print_buf[0] = freq_buf[0];
        print_buf[1] = '.';
        print_buf[2] = freq_buf[1];
        print_buf[3] = '\0';
        display.setCursor(17, 2);
        display.print(print_buf);
        _reset_cursor();

    // 10 - 999
    } else if (frequency < 1000.0) {
        sprintf(freq_buf, "%3ld", (long) frequency);
        strncpy(print_buf, freq_buf, 3);
        print_buf[3] = '\0';
        display.setCursor(17, 2);
        display.print(print_buf);
        _reset_cursor();

    // 1K - 99K
    } else if (frequency < 99999.999) {
        sprintf(freq_buf, "%5ld", (long) frequency);
        strncpy(print_buf, freq_buf, 3);
        print_buf[2] = 'K';
        print_buf[3] = '\0';
        display.setCursor(17, 2);
        display.print(print_buf);
        _reset_cursor();

    // .1M - .9M
    } else if (frequency < 999999.999) {
        sprintf(freq_buf, "%6ld", (long) frequency);
        print_buf[0] = '.';
        print_buf[1] = freq_buf[0];
        print_buf[2] = 'M';
        print_buf[3] = '\0';
        display.setCursor(17, 2);
        display.print(print_buf);
        _reset_cursor();

    // 1M - ??
    } else {
        sprintf(freq_buf, "%8ld", (long) frequency);
        strncpy(print_buf, freq_buf, 3);
        print_buf[2] = 'M';
        print_buf[3] = '\0';
        display.setCursor(17, 2);
        display.print(print_buf);
        _reset_cursor();
    }
}


void Lcd::draw_program_name(char program_name[]){
    display.setCursor(13, 3);
    display.print("       ");
    display.setCursor(13, 3);
    display.print(program_name);
    _reset_cursor();
}


e_input_field Lcd::get_input_field() {
    return input_field;
}


void Lcd::set_input_field(e_input_field input_field_) {
    input_field = input_field_;
    _reset_cursor();
}


void Lcd::update() {
    unsigned long current_millis = millis();
    if ((current_millis - last_cursor_toggle) > CURSOR_BLINK_INTERVAL) {
        if (cursor_on) {
            display.noCursor();
            cursor_on = false;
        } else {
            display.cursor();
            cursor_on = true;
        }
        last_cursor_toggle = current_millis;
    }
}



// Draw unchanging parts of the display
//
// The A:, D:, and >'s in the example below
//
// A:       240 PRG INC
//  >  104_     DEC SIG
// D:       -34 RUN   1
//  > -25_      PRGNAME
void Lcd::_draw_static_elements() {
    display.setCursor(0,0);
    display.print("A:");
    display.setCursor(1,1);
    display.print(">");
    display.setCursor(0,2);
    display.print("D:");
    display.setCursor(1,3);
    display.print(">");
}


void Lcd::_reset_cursor() {
    switch (input_field) {
        case ADDRESS_FIELD:
            display.setCursor(queued_address_cursor_column, queued_address_cursor_row);
            break;
        case DATA_FIELD:
            display.setCursor(queued_data_cursor_column, queued_data_cursor_row);
            break;
    }
}


void Lcd::_byte_to_binary_string(byte value, char buffer[]) {
    for (int bit_index = 7; bit_index >=0; bit_index--) {
        if ((value >> bit_index) & 1) {
            buffer[7 - bit_index] = '1';
        } else {
            buffer[7 - bit_index] = '0';
        }
    buffer[8] = '\0';
    }
}


int Lcd::_data_to_signed_equiv(byte data, e_sign_mode sign_mode) {
    if (sign_mode == SIGNED) {
        if (data <= 127) {
            return data;
        } else {
            return -1 * (256 - data);
        }
    } else {
        return data;
    }
}
