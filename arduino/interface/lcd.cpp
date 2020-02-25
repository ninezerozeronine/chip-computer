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
    address_cursor_row = 1;
    address_cursor_column = 4;
    data_cursor_row = 3;
    data_cursor_column = 4;
    cursor_on = true;
    last_cursor_toggle = 0;
    strcpy(print_buf, "");
}


void Lcd::init() {
    display.init();
    display.clear();
    _draw_static_elements();
    last_cursor_toggle = millis();
}


void Lcd::draw_address(int address, e_number_base number_base) {
    switch (number_base) {
        case BINARY:
            sprintf(print_buf, "%08");
            break;
        case DECIMAL:
            break;
        case HEXADECIMAL:
            break;
    }
}


void Lcd::draw_queued_address(char queued_address_str[]) {

}


void Lcd::draw_data(int data, e_number_base number_base, e_sign_mode sign_mode) {

}


void Lcd::draw_queued_data(char queued_data_str[]) {

}


void Lcd::draw_number_base_indicator(e_number_base number_base) {

}


void Lcd::draw_sign_mode_indicator(e_sign_mode sign_mode) {

}


void Lcd::draw_address_update_mode_indicator(e_address_update_mode address_update_mode) {

}


void Lcd::draw_ram_region_indicator(e_ram_region ram_region) {

}


void Lcd::draw_run_mode_indicator(e_run_mode run_mode) {

}


void Lcd::draw_clock_frequency(float frequency) {

}


void Lcd::draw_program_name(char program_name[]){
    // int name_length = strlen_P(program_name);
    // char name_char = pgm_read_byte_near(program_name + index);
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
            display.setCursor(address_cursor_column, address_cursor_row);
            break;
        case DATA_FIELD:
            display.setCursor(data_cursor_column, data_cursor_row);
            break;
    }
}