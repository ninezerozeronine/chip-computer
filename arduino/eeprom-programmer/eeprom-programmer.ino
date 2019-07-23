#include <Arduino.h>

#include "button.h"
#include "rom_0.h"

#define ROM_SEL_BUTTON_PIN 1
#define MODE_SEL_BUTTON_PIN 2
#define GO_BUTTON_PIN 3
#define _CE_PIN 4
#define _OE_PIN 5
#define _WE_PIN 6

const int DATA_PINS[] = {1,2,3,4,5,6,7,8};
const int ADDRESS_PINS[] = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};
const byte* ROMS[] = {ROM_0};

Button rom_sel_button(ROM_SEL_BUTTON_PIN);
Button mode_sel_button(MODE_SEL_BUTTON_PIN);
Button go_button(GO_BUTTON_PIN);

int selected_rom = 0;
int mode = 0;

void setup() {
    digitalWrite(_CE_PIN, HIGH);
    pinMode(_CE_PIN, OUTPUT);
    
    digitalWrite(_OE_PIN, HIGH);
    pinMode(_OE_PIN, OUTPUT);
    digitalWrite(_WE_PIN, HIGH);
    pinMode(_WE_PIN, OUTPUT);

    digitalWrite(_CE_PIN, LOW);

    for (int index = 0; index <= 7; index++) {
        pinMode(DATA_PINS[index], INPUT);
    }

    for (int index = 0; index <= 15; index++) {
        digitalWrite(ADDRESS_PINS[index], LOW);
        pinMode(ADDRESS_PINS[index], OUTPUT);
        
    }

    rom_sel_button.init();
    mode_sel_button.init();
    go_button.init();
}

void loop() {
    rom_sel_button.update(&rom_sel_button_pressed, NULL);
    mode_sel_button.update(&mode_sel_button_pressed, NULL);
    go_button.update(&go_button_pressed, NULL);
}



void set_address(int address) {
    // Set the address on the address pins
}

void write_eeprom_data(byte* data) {
  digitalWrite(_WE_PIN, LOW);
  delayMicroseconds(1);
  digitalWrite(_WE_PIN, HIGH);
  delayMicroseconds(5);
}

void read_eeprom_data() {
    byte foo = pgm_read_byte_near(ROM_0 + 3);
}

void rom_sel_button_pressed(){
    
}

void mode_sel_button_pressed(){
    
}

void go_button_pressed(){
    
}