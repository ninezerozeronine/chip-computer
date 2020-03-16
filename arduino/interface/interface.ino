// Code to make interfacing with the eight bit computer easier
// 47036 loops per sec

#include <Arduino.h>
#include <Keypad.h>

#include "button.h"
#include "potentiometer.h"
#include "monitor.h"


#define NUM_ROWS 4
#define NUM_COLS 8
char keymap[NUM_ROWS][NUM_COLS] = {
    {'a','b','c','d', '0','1','2','3'},
    {'e','f','g','h', '4','5','6','7'},
    {'i','j','k','l', '8','9','A','B'},
    {'m','n','o','p', 'C','D','E','F'},
};
byte rowPins[NUM_ROWS] = {30, 32, 34, 36};
byte colPins[NUM_COLS] = {38, 40, 42, 44, 46, 48, 50, 52};
Keypad keypad(makeKeymap(keymap), rowPins, colPins, NUM_ROWS, NUM_COLS);

Monitor monitor;
Button minus_button(MINUS_BUTTON_PIN);
Potentiometer speed_pot(SPEED_POT_PIN, 50);
char key_convert_buffer[8];

unsigned long loopCount = 0;
unsigned long timer_ms = 0;

void setup() {
    // Called once at Arduino startup.

    Serial.begin(9600);
    // Wait for serial port to connect. Needed for native USB port only
    while (!Serial) {
    ; 
    }

    keypad.begin(makeKeymap(keymap));
    keypad.setDebounceTime(100);
    keypad.addEventListener(keypad_event);
    monitor.init();
    speed_pot.init();
    minus_button.init();
    monitor.set_speed(speed_pot.get_value());
}

void loop() {
    // Main loop function for arduino.
    // Required to trigger callbacks
    keypad.getKey();
    speed_pot.update(&speed_value_changed);
    minus_button.update(&minus_button_pressed, NULL, NULL);
    monitor.update();

    if ((millis() - timer_ms) > 1000) {
        Serial.print("Your loop code ran ");
        Serial.print(loopCount);
        Serial.println(" times over the last second");
        loopCount = 0;
        timer_ms = millis();
    }
    loopCount++;
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
    Serial.println(new_value);
    monitor.set_speed(new_value);
}


void minus_button_pressed() {
    monitor.propose_character('-');
}





























































































// Test code

// #define KEYPAD_PIN A0
// #define BUTTON_PIN 2

// #include <Arduino.h>

// #include "button.h"
// #include "keypad.h"
// #include "monitor.h"

// const int keypad_values[] = {
//     1023,
//     930,
//     853,
//     787,

//     675,
//     633,
//     596,
//     563,

//     504,
//     480,
//     459,
//     439,

//     402,
//     323,
//     270,
//     232
// };

// Button test_button(BUTTON_PIN);
// Keypad test_keypad(KEYPAD_PIN, keypad_values);
// Monitor test_monitor;

// void setup() {
//     // Called once at Arduino startup.

//     test_button.init();
//     test_keypad.init();
//     test_monitor.init();

//     Serial.begin(115200);
//     // wait for serial port to connect. Needed for native USB port only
//     while (!Serial) {
//     ; 
//     }

//     test_monitor.toggle_sign_mode();
// }

// void loop() {
//     // Main loop function for arduino.
//     test_button.update(&button_pressed, &button_released, &button_repeating);
//     test_keypad.update(&keypad_key_pressed, &keypad_key_released);
// }

// void button_pressed() {
//     Serial.println("Button pressed.");
//     Serial.println(analogRead(A0));
// }

// void button_released() {
//     Serial.println("Button released.");
// }

// void button_repeating() {
//     Serial.println("Button repeating.");
// }

// void keypad_key_pressed(int key) {
//     Serial.print(key);
//     Serial.println(" key on keypad pressed.");
// }

// void keypad_key_released(int key) {
//     Serial.print(key);
//     Serial.println(" key on keypad released.");
// }


