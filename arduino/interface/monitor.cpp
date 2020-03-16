// Provides convenient bridge between user and computer.

#include "monitor.h"


// Constructor
Monitor::Monitor() {
    constructor_defaults();
}


void Monitor::constructor_defaults() {
    bridge = HardwareBridge();
    lcd = Lcd();
    program_index = 0;
    num_programs = 2;
    clock_frequency = 0.1;

    num_program_bytes[0] = num_fibonacci_program_bytes;
    num_data_bytes[0] = num_fibonacci_data_bytes;
    program_bytes[0] = fibonacci_program_bytes;
    data_bytes[0] = fibonacci_data_bytes;
    program_names[0] = fibonacci_program_name;

    num_program_bytes[1] = num_foobar_program_bytes;
    num_data_bytes[1] = num_foobar_data_bytes;
    program_bytes[1] = foobar_program_bytes;
    data_bytes[1] = foobar_data_bytes;
    program_names[1] = foobar_program_name;

    strcpy(queued_address_str, "");
    strcpy(proposed_address_str, "");
    strcpy(queued_data_str, "");
    strcpy(proposed_data_str, "");

    run_mode = PAUSED;
    sign_mode = UNSIGNED;
    number_base = DECIMAL;
    address_update_mode = AUTO_INC;
}


void Monitor::init() {
    bridge.init();
    lcd.init();
    // Init into paused state
    _set_paused();

    lcd.draw_address(bridge.get_address(), number_base);
    lcd.draw_queued_address(queued_address_str);
    lcd.draw_data(bridge.get_data(), number_base, sign_mode);
    lcd.draw_queued_data(queued_data_str);
    lcd.draw_number_base_indicator(number_base);
    lcd.draw_sign_mode_indicator(sign_mode);
    lcd.draw_address_update_mode_indicator(address_update_mode);
    lcd.draw_ram_region_indicator(bridge.get_ram_region());
    lcd.draw_run_mode_indicator(run_mode);
    lcd.draw_clock_frequency(clock_frequency);
    lcd.draw_program_name(program_names[program_index]);
}

// Select the next stored program in the list
void Monitor::next_stored_pgm() {
    if (run_mode == PAUSED && !bridge.get_reset()) {

        program_index = (program_index + 1) % num_programs;

        lcd.draw_program_name(program_names[program_index]);
    }
}


// Transfer the selected program to the computer
void Monitor::transfer_stored_pgm() {
    if (run_mode == PAUSED && !bridge.get_reset()) {

        // Store initial memory region and address
        e_ram_region initial_ram_region = bridge.get_ram_region();
        byte initial_address = bridge.get_address();

        // Switch to setup mode
        bridge.set_ram_control_mode(USER);

        // Loop over program bytes, sending to computer (Don't update LCD)
        if (num_program_bytes[program_index] > 0) {

            // Set program memory
            bridge.set_ram_region(PROGRAM);

            for (byte index = 0; index < num_program_bytes[program_index]; ++index) {
                bridge.set_address(index);
                bridge.set_staged_data(pgm_read_byte_near(program_bytes[program_index] + index));
                bridge.send_ram_write_pulse();
            }
        }

        // Loop over data bytes, sending to computer (Don't update LCD)
        if (num_data_bytes[program_index] > 0) {
            // Set program memory
            bridge.set_ram_region(DATA);

            for (byte index = 0; index < num_data_bytes[program_index]; ++index) {
                bridge.set_address(index);
                bridge.set_staged_data(pgm_read_byte_near(data_bytes[program_index] + index));
                bridge.send_ram_write_pulse();
            }
        }

        // Restore initial address and memory region
        bridge.set_ram_region(initial_ram_region);
        bridge.set_address(initial_address);

        // Update LCD with new data at this address in case it's changed.
        lcd.draw_data(bridge.get_data(), number_base, sign_mode);
    }
}


// Switch to the next number base and update the LCD
void Monitor::next_number_base() {
    if (run_mode == PAUSED && !bridge.get_reset()) {
        switch (number_base) {
            case BINARY:
                number_base = DECIMAL;
                break;
            case DECIMAL:
                number_base = HEXADECIMAL;
                break;
            case HEXADECIMAL:
                number_base = BINARY;
                break;
        }

        lcd.draw_number_base_indicator(number_base);

        lcd.draw_address(bridge.get_address(), number_base);
        strcpy(queued_address_str, "");
        lcd.draw_queued_address(queued_address_str);
        
        lcd.draw_data(bridge.get_data(), number_base, sign_mode);
        strcpy(queued_data_str, "");
        lcd.draw_queued_data(queued_data_str);
    }
}


// Toggle whether the bridge is in signed mode or not and update LCD
void Monitor::toggle_sign_mode() {
    if (run_mode == PAUSED && !bridge.get_reset()) {
        switch (sign_mode) {
            case SIGNED:
                sign_mode = UNSIGNED;
                break;
            case UNSIGNED:
                sign_mode = SIGNED;
                break;
        }

        lcd.draw_data(bridge.get_data(), number_base, sign_mode);
        lcd.draw_sign_mode_indicator(sign_mode);

        strcpy(queued_address_str, "");
        lcd.draw_queued_address(queued_address_str);

        strcpy(queued_data_str, "");
        lcd.draw_queued_data(queued_data_str);
    }
}


// Toggle whether the bridge will auto increment the address after
// writing data. Update LCD to reflect this.
void Monitor::toggle_address_update_mode() {
    if (run_mode == PAUSED && !bridge.get_reset()) {
        switch (address_update_mode) {
            case AUTO_INC:
                address_update_mode = NO_INC;
                break;
            case NO_INC:
                address_update_mode = AUTO_INC;
                break;
        }

    lcd.draw_address_update_mode_indicator(address_update_mode);
    }
}


// Toggle whether the address is in program or data memory. Send to
// computer, read new data and update LCD.
void Monitor::toggle_ram_region() {
    if (run_mode == PAUSED && !bridge.get_reset()) {
        e_ram_region new_ram_region;
        switch (bridge.get_ram_region()) {
            case PROGRAM:
                new_ram_region = DATA;
                break;
            case DATA:
                new_ram_region = PROGRAM;
                break;
        }

    bridge.set_ram_region(new_ram_region);
    lcd.draw_ram_region_indicator(new_ram_region);
    lcd.draw_data(bridge.get_data(), number_base, sign_mode);
    }
}


void Monitor::toggle_input_field() {
    if (run_mode == PAUSED && !bridge.get_reset()) {
        switch (lcd.get_input_field()) {
            case ADDRESS_FIELD:
                lcd.set_input_field(DATA_FIELD);
                break;
            case DATA_FIELD:
                lcd.set_input_field(ADDRESS_FIELD);
                break;
        }
    }
}


void Monitor::propose_character(char character) {
    if (run_mode == PAUSED && !bridge.get_reset()) {
        switch (lcd.get_input_field()) {
            case ADDRESS_FIELD:
                _propose_address_character(character);
                break;
            case DATA_FIELD:
                _propose_data_character(character);
                break;
        }
    }
}


void Monitor::confirm_current_field() {
    if (run_mode == PAUSED && !bridge.get_reset()) {
        switch (lcd.get_input_field()) {
            case ADDRESS_FIELD:
                _confirm_address();
                break;
            case DATA_FIELD:
                _write_data();
                break;
        }
    }
}


void Monitor::erase_last_char() {
    if (run_mode == PAUSED && !bridge.get_reset()) {
        switch (lcd.get_input_field()) {
            case ADDRESS_FIELD:
                _erase_last_queued_address_char();
                break;
            case DATA_FIELD:
                _erase_last_queued_data_char();
                break;
        }
    }
}


// Increment the address by 1
void Monitor::incr_address() {
    if (run_mode == PAUSED && !bridge.get_reset()) {
        // Increment the address
        byte new_address = (bridge.get_address() + 1) % 256;

        // Update LCD
        lcd.draw_address(new_address, number_base);

        // Send address to computer
        bridge.set_address(new_address);

        // Read data and update bridge
        lcd.draw_data(bridge.get_data(), number_base, sign_mode);
    }
}


// Decrement the address by 1
void Monitor::decr_address() {
    if (run_mode == PAUSED && !bridge.get_reset()) {
        // Decrement the address, wrapping round
        byte new_address = bridge.get_address() - 1;

        // Update LCD
        lcd.draw_address(new_address, number_base);

        // Send address to computer
        bridge.set_address(new_address);

        // Read data and update bridge
        lcd.draw_data(bridge.get_data(), number_base, sign_mode);
    }
}


// Set the reset signal going to the computer high.
void Monitor::enable_reset(){
    bridge.set_reset(true);
}


// Set the reset signal going to the computer low
void Monitor::disable_reset(){
    bridge.set_reset(false);
}


// Toggle the computer between run and pause mode
void Monitor::toggle_run_pause() {
    if (!bridge.get_reset()) {
        switch (run_mode) {
            case RUNNING:
                _set_paused();
                break;
            case PAUSED:
                _set_running();
        }
    }
}


// Advance the clock a quarter step
void Monitor::quarter_step() {
    if (run_mode == PAUSED && !bridge.get_reset()) {
        _send_clock_pulses(1);
    }
}


// Advance the clock a half step
void Monitor::half_step() {
    if (run_mode == PAUSED && !bridge.get_reset()) {
        _send_clock_pulses(2);
    }
}


// Advance the clock a full step
void Monitor::full_step() {
    if (run_mode == PAUSED && !bridge.get_reset()) {
        _send_clock_pulses(4);
    }
}


// Set the clock speed
//
// speed: value returned from reading the potentiometer. 0 - 1023.
void Monitor::set_speed(int speed) {
    if (!bridge.get_reset()) {
        clock_frequency = _map_pot_val_to_frequency(speed);
        lcd.draw_clock_frequency(clock_frequency);

        // Need to briefly disable to clock to avoid noisy/out of spec
        // clock frequency pulses making it to the computer while
        // changing frequency/clock sources
        if (run_mode == RUNNING) {
            bridge.set_clock_enabled(false);
            delayMicroseconds(5);

            _set_clock_to_frequency(clock_frequency);
            delayMicroseconds(5);

            bridge.set_clock_enabled(true);
            delayMicroseconds(5);
        }
    }
}


void Monitor::update() {
    lcd.update();
}


bool Monitor::_character_is_valid_for_input_settings(char character, e_number_base number_base_, e_sign_mode sign_mode_) {
    if ((sign_mode_ == UNSIGNED) && (character == '-')) {
        return false;
    }
    switch (number_base_) {
        case BINARY:
            if ((character == '-') || (character == '0') || (character == '1')) {
                return true;
            } else {
                return false;
            }
            break;
        case DECIMAL:
            if (isDigit(character) || character == '-') {
                return true;
            } else {
                return false;
            }
            break;
        case HEXADECIMAL:
            if (isHexadecimalDigit(character) || character == '-') {
                return true;
            } else {
                return false;
            }
            break;
    }
}


void Monitor::_add_char_to_string(char existing_string[], char character) {
    int current_length = strlen(existing_string);
    existing_string[current_length] = character;
    existing_string[current_length + 1] = '\0';
}


int Monitor::_string_to_value(char in_string[], e_number_base number_base_) {
    switch (number_base_) {
        case BINARY:
            return strtol(in_string, NULL, 2);
            break;
        case DECIMAL:
            return strtol(in_string, NULL, 10);
            break;
        case HEXADECIMAL:
            return strtol(in_string, NULL, 16);
            break;
    }
}

// Convert a string representation of a value (e.g. "-37") to it's equivalent 
// value if the bits are to be read as an unsigned 8 bit value.
// 
// Uses 2's complement where necessary
//
// E.g. 
// 10   = 00001010 = 10
// -1   = 11111111 = 255
// -128 = 10000000 = 128
// -37  = 11011011 = 219
// 255  = 11111111 = 255
// 0    = 00000000 = 0
//
// Returns 0 if -128 <= number <= 255
//
//  2 0000 0010 2
//  1 0000 0001 1
//  0 0000 0000 0
// -1 1111 1111 255
// -2 1111 1110 254
// -3 1111 1101 253
byte Monitor::_string_to_raw_value(char in_string[], e_number_base number_base_) {
    int value = _string_to_value(in_string, number_base_);
    if ((value >= 0) && (value <= 255)) {
        return value;
    } else {
        if (value >= -128) {
            return 256 - (value * - 1);
        } else {
            return 0;
        }
    }
}


bool Monitor::_is_within_range(int value, e_sign_mode sign_mode_){
    if (sign_mode_ == SIGNED) {
        return ((value >= -128) && (value <= 127));
    } else {
        return ((value >= 0) && (value <= 255));
    }
    
}


// Send clock pulses to advance the computer
//
// Temporarily puts the computer back into a semi run mode.
void Monitor::_send_clock_pulses(int num_pulses) {
    bridge.set_ram_control_mode(CONTROL_UNIT);
    delayMicroseconds(5);
    bridge.set_clock_enabled(true);
    delayMicroseconds(5);
    bridge.send_clock_pulses(num_pulses);
    delayMicroseconds(5);
    bridge.set_ram_control_mode(USER);
    delayMicroseconds(5);
    bridge.set_clock_enabled(false);
    delayMicroseconds(5);
}


// Propose a character to add to the queued address
void Monitor::_propose_address_character(char character) {
    if (_character_is_valid_for_input_settings(character, number_base, sign_mode)) {
        if (character != '-') {
            if (strlen(queued_address_str) < 8) {
                strcpy(proposed_address_str, queued_address_str);
                _add_char_to_string(proposed_address_str, character);
                int proposed_address_value = _string_to_value(proposed_address_str, number_base);
                if (proposed_address_value <= 255) {
                    strcpy(queued_address_str, proposed_address_str);
                    lcd.draw_queued_address(queued_address_str);
                }
            }
        }
    }
}


// Confirm the queued address
void Monitor::_confirm_address() {
    if (strlen(queued_address_str) > 0) {
        // Convert queued address to value
        int new_address = _string_to_value(queued_address_str, number_base);

        // Update LCD
        lcd.draw_address(new_address, number_base);

        // Send address to computer
        bridge.set_address(new_address);

        // Read data and update LCD
        lcd.draw_data(bridge.get_data(), number_base, sign_mode);

        // Clear queued address
        strcpy(queued_address_str, "");

        // Update queued address on LCD
        lcd.draw_queued_address(queued_address_str);
    }
}


// Cancel queued address
void Monitor::_clear_queued_address() {
    strcpy(queued_address_str, "");
    lcd.draw_queued_address(queued_address_str);
}


// Add a character to the currently queued data value. If the character is
// invalid for the current base, 
void Monitor::_propose_data_character(char character) {
    // If its a valid character or a minus
    if (_character_is_valid_for_input_settings(character, number_base, sign_mode) || character == '-') {
        int current_length = strlen(queued_data_str);

        // If theres nothing queued
        if (current_length == 0) {

            // Add it unless it's a minus and we're in unsigned mode
            if ( !((character == '-') && (sign_mode == UNSIGNED)) ) {
                _add_char_to_string(queued_data_str, character);
                lcd.draw_queued_data(queued_data_str);
            }

        // Else there's something queued
        } else {

            // If the character isnt a dash
            if (character != '-') {

                // If there's a dash in the queued value
                if (strchr(queued_data_str, '-') != NULL) {

                    // If there's less than 9 charartcers
                    if (current_length < 9) {

                        // Test the proposed update and add it if it's good
                        strcpy(proposed_data_str, queued_data_str);
                        _add_char_to_string(proposed_data_str, character);
                        int proposed_data_value = _string_to_value(proposed_data_str, number_base);
                        if (_is_within_range(proposed_data_value, sign_mode)) {
                            strcpy(queued_data_str, proposed_data_str);
                            lcd.draw_queued_data(queued_data_str);
                        }
                    }

                // Else there's no dash
                } else {

                    // If there's less than 8 characters
                    if (current_length < 8) {

                        // Test the proposed update and add it if it's good
                        strcpy(proposed_data_str, queued_data_str);
                        _add_char_to_string(proposed_data_str, character);
                        int proposed_data_value = _string_to_value(proposed_data_str, number_base);
                        if (_is_within_range(proposed_data_value, sign_mode)) {
                            strcpy(queued_data_str, proposed_data_str);
                            lcd.draw_queued_data(queued_data_str);
                        }
                    }
                }
            }
        }
    }
}


// Write the currently queued data to the computer
void Monitor::_write_data() {
    int string_length = strlen(queued_data_str);
    // If the string isn't empty or just a minus sign
    if ((string_length > 1) || ((string_length == 1) && (queued_data_str[0] != '-'))) {
        byte data = _string_to_raw_value(queued_data_str, number_base);
        bridge.set_staged_data(data);
        bridge.send_ram_write_pulse();
        if (address_update_mode == AUTO_INC ) {
            incr_address();
        }
        lcd.draw_data(bridge.get_data(), number_base, sign_mode);
    }
}


// Clear the currently queued data
void Monitor::_clear_queued_data() {
    strcpy(queued_data_str, "");
    lcd.draw_queued_data(queued_data_str);
}


float Monitor::_map_pot_val_to_frequency(int pot_val) {
    float new_frequency = 0.1;
    // Min zone - lock frequency to 1/10 Hz
    if (pot_val < 24) {
        new_frequency = 0.1;
    }

    // Min Zone - 1/5 - frequency between 1/10 and 1 Hz
    if ((pot_val >= 24) && (pot_val < 212)) {
        float in_min = 12;
        float in_max = 211;
        float out_min = 0.1;
        float out_max = 0.99;
        new_frequency = ((float(pot_val) - in_min) * (out_max - out_min) / (in_max - in_min)) + out_min;
    }

    // 1/5 - 2/5 - frequency between 1 and 10 Hz
    if ((pot_val >= 212) && (pot_val < 412)) {
        float in_min = 212;
        float in_max = 411;
        float out_min = 1.0;
        float out_max = 10;
        new_frequency = ((float(pot_val) - in_min) * (out_max - out_min) / (in_max - in_min)) + out_min;
    }

    // 2/5 - 3/5 - frequency between 10 and 100 Hz
    if ((pot_val >= 412) && (pot_val < 612)) {
        float in_min = 412;
        float in_max = 611;
        float out_min = 10;
        float out_max = 100;
        new_frequency = ((float(pot_val) - in_min) * (out_max - out_min) / (in_max - in_min)) + out_min;
    }

    // 3/5 - 4/5 - frequency between 100 and 1000 Hz
    if ((pot_val >= 612) && (pot_val < 812)) {
        new_frequency = float(map(pot_val, 612, 811, 100, 1000));
    }

    // 4/5 - Max Zone - frequency between 1000 and 10000 Hz
    if ((pot_val >= 812) && (pot_val < 1000)) {
        new_frequency = float(map(pot_val, 812, 1011, 1000, 10000));
    }

    // Max Zone - lock frequency to 1Mhz
    if (pot_val >= 1000) {
        new_frequency = 1000000.0;
    }

    return new_frequency;
}


void Monitor::_set_clock_to_frequency(float frequency) {
    if (frequency > 10000) {
        bridge.set_clock_source(CRYSTAL);
    } else {
        bridge.set_clock_source(ARDUINO_PIN);
        bridge.set_clock_to_pwm_mode(frequency);
    }
}


void Monitor::_set_paused() {
    run_mode = PAUSED;
    bridge.set_clock_enabled(false);
    delayMicroseconds(5);
    bridge.set_clock_to_pulse_mode();
    delayMicroseconds(5);
    bridge.set_clock_source(ARDUINO_PIN);
    delayMicroseconds(5);
    bridge.set_ram_control_mode(USER);
    delayMicroseconds(5);
    lcd.draw_data(bridge.get_data(), number_base, sign_mode);
    lcd.draw_run_mode_indicator(run_mode);
}


void Monitor::_set_running() {
    run_mode = RUNNING;
    bridge.set_ram_control_mode(CONTROL_UNIT);
    delayMicroseconds(5);
    _set_clock_to_frequency(clock_frequency);
    delayMicroseconds(5);
    bridge.set_clock_enabled(true);
    lcd.draw_run_mode_indicator(run_mode);
}

void Monitor::_erase_last_queued_address_char() {
    int current_length = strlen(queued_address_str);
    if (current_length > 1) {
        queued_address_str[current_length - 1] = '\0';
        lcd.draw_queued_address(queued_address_str);
    }
}


void Monitor::_erase_last_queued_data_char() {
    int current_length = strlen(queued_data_str);
    if (current_length > 1) {
        queued_data_str[current_length - 1] = '\0';
        lcd.draw_queued_address(queued_data_str);
    }
}