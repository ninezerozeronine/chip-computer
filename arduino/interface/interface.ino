// Code to make interfacing with the eight bit computer easier
// 47036 loops per sec

#include <Arduino.h>
#include <Keypad.h>

#include "button.h"
#include "potentiometer.h"
#include "monitor.h"

#define DEBUG_PRINTS

#define NUM_ROWS 4
#define NUM_COLS 8
char keymap[NUM_ROWS][NUM_COLS] = {
    {'a','b','c','d', '0','1','2','3'},
    {'e','f','g','h', '4','5','6','7'},
    {'i','j','k','l', '8','9','A','B'},
    {'m','n','o','p', 'C','D','E','F'},
};
byte rowPins[NUM_ROWS] = {52, 50, 48, 46};
byte colPins[NUM_COLS] = {44, 42, 40, 38, 36, 34, 32, 30};
Keypad keypad(makeKeymap(keymap), rowPins, colPins, NUM_ROWS, NUM_COLS);

Monitor monitor;
Button minus_button(MINUS_BUTTON_PIN);
Potentiometer speed_pot(SPEED_POT_PIN, 50);
char key_convert_buffer[8];

unsigned long loopCount = 0;
unsigned long timer_ms = 0;
unsigned long last_blink = 0;
bool led_on = true;

void setup() {
    // Called once at Arduino startup.

    #ifdef DEBUG_PRINTS
        Serial.begin(9600);
        // Wait for serial port to connect. Needed for native USB port only
        while (!Serial) {
        ; 
        }
    #endif

    keypad.begin(makeKeymap(keymap));
    keypad.setDebounceTime(100);
    keypad.addEventListener(keypad_event);
    monitor.init();
    speed_pot.init();
    minus_button.init();
    monitor.set_speed(speed_pot.get_value());
    monitor.enable_reset();
    delayMicroseconds(10);
    monitor.disable_reset();
    pinMode(13, OUTPUT);
}

void loop() {
    // Main loop function for arduino.
    // Required to trigger callbacks
    keypad.getKey();
    speed_pot.update(&speed_value_changed);
    minus_button.update(&minus_button_pressed, NULL, NULL);
    monitor.update();

    #ifdef DEBUG_PRINTS
        if ((millis() - timer_ms) > 1000) {
            Serial.print("Your loop code ran ");
            Serial.print(loopCount);
            Serial.println(" times over the last second");
            loopCount = 0;
            timer_ms = millis();
        }
        loopCount++;
    #endif

    if ((millis() - last_blink) > 1000) {
        led_on = !led_on;
        digitalWrite(13, led_on);
        last_blink = millis();
    }

}


void keypad_event(KeypadEvent key_event) {
    switch (keypad.getState()) {
        case PRESSED:
            switch (key_event) {
                case 'a':
                    monitor.next_stored_pgm();
                    break;
                case 'b':
                    monitor.transfer_stored_pgm();
                    break;
                case 'c':
                    monitor.next_number_base();
                    break;
                case 'd':
                    monitor.toggle_sign_mode();
                    break;
                case 'e':
                    monitor.toggle_address_update_mode();
                    break;
                case 'f':
                    monitor.toggle_ram_region();
                    break;
                case 'g':
                    monitor.confirm_current_field();
                    break;
                case 'h':
                    monitor.erase_last_char();
                    break;
                case 'i':
                    monitor.toggle_input_field();
                    break;
                case 'j':
                    monitor.incr_address();
                    break;
                case 'k':
                    monitor.decr_address();
                    break;
                case 'l':
                    monitor.enable_reset();
                    break;
                case 'm':
                    monitor.toggle_run_pause();
                    break;
                case 'n':
                    monitor.quarter_step();
                    break;
                case 'o':
                    monitor.half_step();
                    break;
                case 'p':
                    monitor.full_step();
                    break;
                case '0':
                    monitor.propose_character(key_event);
                    break;
                case '1':
                    monitor.propose_character(key_event);
                    break;
                case '2':
                    monitor.propose_character(key_event);
                    break;
                case '3':
                    monitor.propose_character(key_event);
                    break;
                case '4':
                    monitor.propose_character(key_event);
                    break;
                case '5':
                    monitor.propose_character(key_event);
                    break;
                case '6':
                    monitor.propose_character(key_event);
                    break;
                case '7':
                    monitor.propose_character(key_event);
                    break;
                case '8':
                    monitor.propose_character(key_event);
                    break;
                case '9':
                    monitor.propose_character(key_event);
                    break;
                case 'A':
                    monitor.propose_character(key_event);
                    break;
                case 'B':
                    monitor.propose_character(key_event);
                    break;
                case 'C':
                    monitor.propose_character(key_event);
                    break;
                case 'D':
                    monitor.propose_character(key_event);
                    break;
                case 'E':
                    monitor.propose_character(key_event);
                    break;
                case 'F':
                    monitor.propose_character(key_event);
                    break;
            }
            break;
        case RELEASED :
            switch (key_event) {
                case 'l':
                    monitor.disable_reset();
                    break;
            }
    }
}


void speed_value_changed(int new_value) {
    #ifdef DEBUG_PRINTS
        Serial.println(new_value);
    #endif

    monitor.set_speed(new_value);
}


void minus_button_pressed() {
    monitor.propose_character('-');
}
