// Provides convenient bridge between user and computer.

#include "cpubridge.h"


// Constructor
CPUCPUBridge::CPUBridge() {
    constructor_defaults();
}


void CPUBridge::constructor_defaults() {
    program_index = 0;
    num_programs = 1;

    number_base_index = 0;
    num_number_bases = 3;
}


// Select the next stored program in the list
void CPUBridge::next_stored_pgm() {
    // Increment program index
    program_index = program_index + 1 % num_programs;
    int pretty_index = program_index + 1;

    // Update LCD based on current program
    switch (program_index) {
        case 0: {
            update_program_display(pretty_index, prog_name);
            break;
        }
    }
}


// Transfer the selected program to the computer
void CPUBridge::transfer_stored_pgm() {
    // Stop any clock pulses (i.e. Pause computer)

    // Switch to setup mode

    // Set program memory

    // Loop over program bytes, sending to computer (Don't update LCD)

    // Set data memory

    // Loop over data bytes, sending to computer (Don't update LCD)

    // Set addr and pgm/data mem back to what they were and send to computer

    // Re-read data from computer

    // Update data on LCD
}


// Switch to the next number base and update the LCD
void CPUBridge::next_number_base() {
    number_base_index = (number_base_index + 1) % num_number_bases;

    lcd.draw_addr(current_address, number_base_index);
    lcd.draw_queued_addr(queued_addr, number_base_index);
    lcd.draw_data(current_data, number_base_index, signed_mode);
    lcd.draw_queued_data(queued_data, number_base_index, signed_mode);
    lcd.draw_number_base_indicator(number_base_index);
}


// Toggle whether the bridge is in signed mode or not and update LCD
void CPUBridge::toggle_signed_mode() {
    signed_mode = !signed_mode;

    lcd.draw_data(current_data, number_base_index, signed_mode);
    lcd.draw_queued_data(queued_data, number_base_index, signed_mode);
    lcd.draw_signed_mode_indicator(signed_mode);
}


// Toggle whether the bridge will auto increment the address after
// writing data. Update LCD to reflect this.
void CPUBridge::toggle_address_inc_mode() {
    address_inc_mode = !address_inc_mode;

    lcd.draw_address_inc_mode_indicator(address_inc_mode);
}


// Toggle whether the address is in program or data memory. Send to
// computer, read new data and update LCD.
void CPUBridge::toggle_mem_type() {
    mem_type_index = (mem_type_index + 1) % num_mem_types;

    send_mem_type_to_computer();
    current_data = read_data_from_computer();
    lcd.draw_data(current_data, number_base_index, signed_mode);
    lcd.draw_mem_type_mode_indicator(mem_type_index);
}


// Propose a character to add to the queued address
void CPUBridge::propose_addr_character(char character) {
    if (character_is_valid_for_number_base(character)) {
        if (queued_addr > 0) {

        } else {
            String proposed_addr_str = value_to_string(queued_addr) + character;
            int proposed_addr_value = string_to_value(proposed_addr_str);
            if is_within_range(proposed_addr_value) {
                queued_addr = proposed_addr_value;
                lcd.draw_queued_data(queued_data, number_base_index, signed_mode);
            }
        }


            

    }
}




void CPUBridge::propose_data_character(char character) {
    if (character == '-') {
        if (queued_data_str.length() == 0) {
            queued_data_str = character;
        }
    } else {

    }
    if (character_is_valid_for_number_base(character)) {
        if (queued_data_str.length() == 0) {

        } else if (proposed_data_str == "-") {

        } else {

        }
    }
}

