#include "lcd.h"

Lcd::Lcd() {

}


void Lcd::init() {

}


void Lcd::draw_address(int address, e_number_base number_base) {

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


void Lcd::set_input_field(e_input_field input_field) {

}


void Lcd::update() {

}
