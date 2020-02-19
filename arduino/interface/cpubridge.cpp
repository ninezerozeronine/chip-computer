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

    lcd.draw_address(current_address, number_base_index);
    lcd.draw_data(current_data, number_base_index, signed_mode);
    lcd.draw_number_base_indicator(number_base_index);
    _clear_queued_address();
    _clear_queued_data();
}


// Toggle whether the bridge is in signed mode or not and update LCD
void CPUBridge::toggle_signed_mode() {
    signed_mode = !signed_mode;

    lcd.draw_data(current_data, number_base_index, signed_mode);
    lcd.draw_signed_mode_indicator(signed_mode);
    _clear_queued_address();
    _clear_queued_data();
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
    read_data_update_bridge();
}


// Propose a character to add to the queued address
void CPUBridge::propose_address_character(char character) {
    if (character_is_valid_for_number_base(character)) {
        if (queued_address_str.length() <= 8) {
            String proposed_address_str = queued_address_str + character;
            int proposed_address_value = string_to_value(proposed_address_str);
            if is_within_range(proposed_address_value) {
                queued_address_str = proposed_address_value;
                lcd.draw_queued_address(queued_address_str);
            }
        }
    }
}

// Confirm the queued address
void CPUBridge::confirm_address() {
    if (queued_address_str.length() > 0) {
        // Convert queued address to value
        current_address = string_to_value(queued_address_str);

        // Update LCD
        lcd.draw_address(current_address, number_base_index);

        // Send address to computer
        send_address_to_computer(address);

        // Read data and update bridge
        read_data_update_bridge();

        // Clear queued address
        _clear_queued_address();
    }
}


// Cancel queued address
void CPUBridge::clear_queued_address() {
    // Clear queued address
    _clear_queued_address();
}


// Increment the address by 1
void CPUBridge::incr_address() {
    // Increment the address
    current_address = (current_address + 1) % 256;

    // Update LCD
    lcd.draw_address(current_address, number_base_index);

    // Send address to computer
    send_address_to_computer(address);

    // Read data and update bridge
    read_data_update_bridge();
}


// Decrement the address by 1
void CPUBridge::incr_address() {
    // Decrement the address, wrapping round
    current_address -= 1;
    if (current_address < 0) {
        current_address = 255;
    }

    // Update LCD
    lcd.draw_address(current_address, number_base_index);

    // Send address to computer
    send_address_to_computer(address);

    // Read data and update bridge
    read_data_update_bridge();
}


// Write the currently queued data to the computer
void CPUBridge::write_data() {
    if (computer_not_running) {
        if data_str_is_valid(queued_data_str) {
            int data = string_to_value(queued_data_str);
            send_data_to_computer(data);
        }
    }
}


// Clear the currently queued data
void CPUBridge::clear_queued_data() {
    _clear_queued_data();
}


// Add a character to the currently queued data value. If the character is
// invalid for the current base, 
void CPUBridge::propose_data_character(char character) {
    // If its a valid character or a minus
    if (character_is_valid_for_number_base(character) || character == '-') {
        int current_length = queued_data_str.length()

        // If theres nothing queued
        if (current_length == 0) {

            // Add it!
            queued_data_str += character;
            lcd.draw_queued_data(queued_data_str);

        // Else there's something queued
        } else {

            // If the character isnt a dash
            if (character != '-') {

                // If there's a dash in the queued value
                if (queued_data_str.indexOf('-') > 0) {

                    // If there's less than 9 charartcers
                    if (current_length < 9) {

                        // Test the proposed update and add it if it's good
                        String proposed_data_str = queued_data_str + character;
                        int proposed_data_value = string_to_value(proposed_data_str);
                        if is_within_range(proposed_data_value) {
                            queued_data_str = proposed_data_str;
                            lcd.draw_queued_data(queued_data_str);
                        }
                    }

                // Else there's no dash
                } else {

                    // If there's less than 8 characters
                    if (current_length < 8) {

                        // Test the proposed update and add it if it's good
                        String proposed_data_str = queued_data_str + character;
                        int proposed_data_value = string_to_value(proposed_data_str);
                        if is_within_range(proposed_data_value) {
                            queued_data_str = proposed_data_str;
                            lcd.draw_queued_data(queued_data_str);
                        }
                    }
                }
            }
        }
    }
}


// Set the reset signal going to the computer high.
void CPUBridge::enable_reset(){
    digitalWrite(RESET_OUT_PIN, HIGH);
}


// Set the reset signal going to the computer low
void CPUBridge::disable_reset(){
    digitalWrite(RESET_OUT_PIN, LOW);
}


// Toggle the computer between run and pause mode
void CPUBridge::toggle_run_pause() {
    if (running) {
        set_paused();
    } else {
        set_running();
    }
}


// Set the computer to be running
void CPUBridge::set_running() {
    running = true;
    set_clock_enable(true);
}


// Set the computer to be paused
void CPUBridge::set_paused() {
    running = false;
    set_clock_enable(false);
}


// Advance the clock a quarter step
void CPUBridge::quarter_step() {
    if (!running) {
        send_clock_pulses(1);
    }
}


// Advance the clock a half step
void CPUBridge::half_step() {
    if (!running) {
        send_clock_pulses(2);
    }
}


// Advance the clock a full step
void CPUBridge::full_step() {
    if (!running) {
        send_clock_pulses(4);
    }
}


// Set the clock speed
//
// 
void CPUBridge::set_speed(int speed) {
    if (current_speed < 1012) && (speed >= 1012) {
        switch_from_ardiuno_to_crystal_clock();
    if (current_speed >= 1012) && (speed < 1012) {
        switch_from_crystal_to_arduino_clock();
    }

    current_speed = speed;
    float new_frequency = 0.1;
    // Min zone - lock frequency to 1/10 Hz
    if (speed < 12) {
        new_frequency = 0.1;
    }

    // Min Zone - 1/5 - frequency between 1/10 and 0.99 Hz
    if ((speed >= 12) && (speed < 212)) {
        float in_min = 12;
        float in_max = 211;
        float out_min = 0.1;
        float out_max = 0.99;
        float new_frequency = ((float(speed) - in_min) * (out_max - out_min) / (in_max - in_min)) + out_min;
    }

    // 1/5 - 2/5 - frequency between 1 and 5.99 Hz
    if ((speed >= 212) && (speed < 412)) {
        float in_min = 212;
        float in_max = 411;
        float out_min = 1;
        float out_max = 5.99;
        float new_frequency = ((float(speed) - in_min) * (out_max - out_min) / (in_max - in_min)) + out_min;
    }

    // 2/5 - 3/5 - frequency between 6 and 10.99 Hz
    if ((speed >= 412) && (speed < 612)) {
        float in_min = 412;
        float in_max = 611;
        float out_min = 6;
        float out_max = 10.99;
        float new_frequency = ((float(speed) - in_min) * (out_max - out_min) / (in_max - in_min)) + out_min;
    }

    // 3/5 - 4/5 - frequency between 11 and 100 Hz
    if ((speed >= 612) && (speed < 812)) {
        float new_frequency = float(map(speed, 612, 811, 11, 100));
    }

    // 4/5 - Max Zone - frequency between 101 and 10000 Hz
    if ((speed >= 812) && (speed < 1012)) {
        float new_frequency = float(map(speed, 812, 1011, 101, 10000));
    }

    // Max Zone - lock frequency to 1Mhz
    if (speed >= 1012) {
        new_frequency = 1000000.0;
    }


    lcd.draw_clock_frequency(new_frequency);

    // No need to set if fastest setting, we've already switched to the crytsal.
    if (new_frequency < 10000) {
        set_frequency(new_frequency);
    }
}


void CPUBridge::read_data_update_bridge() {
    current_data = read_data_from_computer();
    lcd.draw_data(current_data, number_base_index, signed_mode);
}


void CPUBridge::_clear_queued_address() {
    unfinished = true
    queued_address_str = "";
    lcd.draw_queued_address(queued_address_str);
}