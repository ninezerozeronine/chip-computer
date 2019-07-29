// Code to read and write data to an AT28C256 EEPROM chip

#include <Arduino.h>

#include "button.h"
#include "roms.h"

#define ROM_SEL_BUTTON_PIN A0
#define MODE_SEL_BUTTON_PIN A1
#define GO_BUTTON_PIN A2
#define _CE_PIN 16
#define _OE_PIN 14
#define _WE_PIN 6
#define NUM_DATA_PINS 8
#define NUM_ADDRESS_PINS 15
#define NUM_ADDRESSES 32768

//                                    0    1    2    3   4   5   6   7
const int DATA_PINS[NUM_DATA_PINS] = {A13, A14, A15, 21, 20, 19, 18, 17};
//                                          0    1    2    3   4   5   6   7   8  9  10  11  12  13 14
const int ADDRESS_PINS[NUM_ADDRESS_PINS] = {A12, A11, A10, A9, A8, A7, A6, A5, 4, 3, 15, 2,  A4, 5, A3};
const int ROM_INDICATOR_PINS[4] = {12,11,10,9};
const int MODE_INDICATOR_PINS[2] = {8,7};

Button rom_sel_button(ROM_SEL_BUTTON_PIN);
Button mode_sel_button(MODE_SEL_BUTTON_PIN);
Button go_button(GO_BUTTON_PIN);

int selected_rom = 0;
int mode = 0;

void setup() {
    // Called once at Arduino startup.
    digitalWrite(13, LOW);
    pinMode(13, OUTPUT);
    digitalWrite(_CE_PIN, HIGH);
    pinMode(_CE_PIN, OUTPUT);
    
    digitalWrite(_OE_PIN, HIGH);
    pinMode(_OE_PIN, OUTPUT);
    digitalWrite(_WE_PIN, HIGH);
    pinMode(_WE_PIN, OUTPUT);

    digitalWrite(_CE_PIN, LOW);

    set_datapins_mode(INPUT);

    // Set all the address pint to output and low
    for (int index = 0; index < NUM_ADDRESS_PINS; index++) {
        digitalWrite(ADDRESS_PINS[index], LOW);
        pinMode(ADDRESS_PINS[index], OUTPUT); 
    }

    rom_sel_button.init();
    mode_sel_button.init();
    go_button.init();

    Serial.begin(115200);
    // wait for serial port to connect. Needed for native USB port only
    while (!Serial) {
    ; 
    }

    set_rom_indicator_LED();
    set_mode_indicator_LED();


    // const byte foo[] PROGMEM = {0x00, 0x0F, 0xF0, 0xFF};
    // Serial.println(sizeof(ROM_0));
    // Serial.println(sizeof(ROM_0)/sizeof(ROM_0[0]));
}

void loop() {
    // Main loop function for arduino.
    rom_sel_button.update(&rom_sel_button_pressed, NULL);
    mode_sel_button.update(&mode_sel_button_pressed, NULL);
    go_button.update(&go_button_pressed, NULL);
}

void set_datapins_mode(int pin_mode) {
    // Set the mode of the data pins
    //
    // Args:
    //     mode: The mode to set the pins to. E.g. INPUT, INPUT_PULLUP or OUTPUT.
    for (int index = 0; index < NUM_DATA_PINS; index++) {
        pinMode(DATA_PINS[index], pin_mode);
    }
}

void set_datapins_value(byte value){
    // Set the datapins to represent a value in binary.
    //
    // Args:
    //     value: The value to set the data pins to.
    for (int index = 0; index < NUM_DATA_PINS; index++) {
        digitalWrite(DATA_PINS[index], value & 1);
        value = value >> 1;
    }
}

void set_addresspins_value(unsigned int address) {
    // Set an address on the address pins
    //
    // Args:
    //     address: The value to set the address pins to.
    // char buf[50];
    // sprintf(buf, "Setting Address %05d. (Reversed)", address);
    // Serial.println(buf);

    for (int index = 0; index < NUM_ADDRESS_PINS; index++) {
        digitalWrite(ADDRESS_PINS[index], address & 1);
        // Serial.print(address & 1);
        address = address >> 1;
    }
    // Serial.println(" ");
}

void write_eeprom_data(byte data[], byte last_byte) {
    set_datapins_mode(OUTPUT);

    byte value = 0;
    int chunk = 1;
    for (unsigned int address = 0; address < NUM_ADDRESSES; address++) {

        if ((address % 256) == 0) {
            char buf[40];
            sprintf(buf, "Writing chunk %03d of 128.", chunk);
            delay(200);
            Serial.println(buf);
            chunk += 1;
        }


        set_addresspins_value(address);
        delayMicroseconds(20);
        value = pgm_read_byte_near(data + address);
        set_datapins_value(value);

        if ((address > 24944) and (address < 24976)) {
            char buf[60]; 
            sprintf(buf, "Writing %02x to %05d.", value, address);
            Serial.println(buf);
        }

        digitalWrite(_WE_PIN, LOW);
        delayMicroseconds(20);
        digitalWrite(_WE_PIN, HIGH);
        delayMicroseconds(20);
    }

    // Write the last byte
    set_addresspins_value(NUM_ADDRESSES - 1);
    delayMicroseconds(20);
    set_datapins_value(last_byte);

    digitalWrite(_WE_PIN, LOW);
    delayMicroseconds(20);
    digitalWrite(_WE_PIN, HIGH);
    delayMicroseconds(20);

    set_datapins_value(0);
    set_datapins_mode(INPUT);
}


void write_eeprom_range(unsigned int start, unsigned int end, byte data[]) {
    set_datapins_mode(OUTPUT);

    for (unsigned int address = start; address <= end; address++) {

        set_addresspins_value(address);
        delayMicroseconds(3);
        byte value = pgm_read_byte_near(data + address);
        set_datapins_value(value);

        digitalWrite(_WE_PIN, LOW);
        delayMicroseconds(3);
        digitalWrite(_WE_PIN, HIGH);
        delayMicroseconds(3);
    }

    set_datapins_value(0);
    set_datapins_mode(INPUT);
}


byte read_current_byte(){
    // Read the currently addressed byte.
    //
    // Expects:
    // * The address to already be set
    // * Time given for the address to settle
    // * The data pins to be in input mode

    byte current_byte = 0;
    for (int index = NUM_DATA_PINS - 1; index >= 0; index--) {
        current_byte = (current_byte << 1) + digitalRead(DATA_PINS[index]);
    }
    return current_byte;
}

void read_eeprom_data() {
    // Read all of the data on the EEPROM and print to serial.

    digitalWrite(_OE_PIN, LOW);
    set_datapins_mode(INPUT);

    byte byte_row[16];

    delayMicroseconds(5);
    for (unsigned int base = 0; base < NUM_ADDRESSES; base+=16) {

        for (unsigned int offset = 0; offset < 16; offset++) {
            delayMicroseconds(5);
            set_addresspins_value(base + offset);
            delayMicroseconds(5);
            byte_row[offset] = read_current_byte();
        }

        char buf[100];
        sprintf(buf, "%05d/32768 (%04X/7FFF):  %02x %02x %02x %02x  %02x %02x %02x %02x    %02x %02x %02x %02x  %02x %02x %02x %02x",
                base, base,
                byte_row[0], byte_row[1], byte_row[2], byte_row[3], byte_row[4], byte_row[5], byte_row[6], byte_row[7],
                byte_row[8], byte_row[9], byte_row[10], byte_row[11], byte_row[12], byte_row[13], byte_row[14], byte_row[15]);
        Serial.println(buf);

    }
    
    digitalWrite(_OE_PIN, HIGH);
}

void read_eeprom_range(unsigned int start, unsigned int end) {
    digitalWrite(_OE_PIN, LOW);
    set_datapins_mode(INPUT);
    delayMicroseconds(3);

    for (unsigned int address = start; address <= end; address++) {
        set_addresspins_value(address);
        delayMicroseconds(3);
        byte value = read_current_byte();
        char buf[30];
        sprintf(buf, "%05d (%04X):  %02x", address, address, value);
        Serial.println(buf);
    }
    digitalWrite(_OE_PIN, HIGH);
}


void rom_sel_button_pressed() {
    // Update state when rom select button is pressed
    selected_rom = (selected_rom + 1) % 4;
    set_rom_indicator_LED();
}

void mode_sel_button_pressed() {
    // Update state when mode select button is pressed
    mode = (mode + 1) % 2;
    set_mode_indicator_LED();
}

void go_button_pressed() {
    // Perform the correct action base on the current mode and rom
    switch (mode) {
        case 0: {
            Serial.println("Reading current ROM");
            switch (selected_rom) {
                case 0: {
                    // write_eeprom_data(ROM_0, ROM_0_last_byte);
                    read_eeprom_range(0, 15);
                    break;
                }
                case 1: {
                    read_eeprom_data();
                    break;
                } 
            }
            break;
        }
        case 1: {
            Serial.print("Writing ROM ");
            Serial.println(selected_rom);
            switch (selected_rom) {
                case 0: {
                    // write_eeprom_data(ROM_0, ROM_0_last_byte);
                    write_eeprom_range(0, 15, ROM_3);
                    break;
                }
                case 1: {
                    write_eeprom_data(ROM_3, ROM_3_last_byte);
                    break;
                }                
                case 2: {
                    write_eeprom_data(ROM_2, ROM_2_last_byte);
                    break;
                }                
                case 3: {
                    write_eeprom_data(ROM_3, ROM_3_last_byte);
                    break;
                }
            break;
            }
        }
    }
}

void set_rom_indicator_LED() {
    // Set the LEDs to indicate which ROM will be written.
    for (int led_index = 0; led_index < 4; led_index++){
        if (led_index == selected_rom) {
            digitalWrite(ROM_INDICATOR_PINS[led_index], HIGH);
        } else {
            digitalWrite(ROM_INDICATOR_PINS[led_index], LOW);
        }
    }
}

void set_mode_indicator_LED() {
    // Set the LEDs to indicate which mode is active (read or write).
    for (int led_index = 0; led_index < 2; led_index++){
        if (led_index == mode) {
            digitalWrite(MODE_INDICATOR_PINS[led_index], HIGH);
        } else {
            digitalWrite(MODE_INDICATOR_PINS[led_index], LOW);
        }
    }
}