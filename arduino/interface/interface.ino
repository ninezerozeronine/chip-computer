// Code to make interfacing with the eight bit computer easier

#include <Arduino.h>

#include "button.h"
#include "keypad.h"
#include "potentiometer.h"
#include "monitor.h"

#define CTL_KEY_NEXT_STORED_PRG 0
#define CTL_KEY_TRANSFER_STORED_PGM 1
#define CTL_KEY_BASE 2
#define CTL_KEY_SIGNED 3
#define CTL_KEY_AUTO_INC_ADDR 4
#define CTL_KEY_RAM_REGION 5
#define CTL_KEY_CONFIRM 6
#define CTL_KEY_CLEAR 7 
#define CTL_KEY_INPUT_FIELD 8
#define CTL_KEY_INCR_ADDR 9
#define CTL_KEY_DECR_ADDR 10
#define CTL_KEY_RESET 11
#define CTL_KEY_RUN_PAUSE 12
#define CTL_KEY_QUARTER_STEP 13
#define CTL_KEY_HALF_STEP 14
#define CTL_KEY_FULL_STEP 15

const int data_keypad_values[] = {
    1010,  918,  842,  778,
     668,  627,  590,  558,
     499,  476,  455,  435,
     399,  321,  269,  232
};

const int control_keypad_values[] = {
    1010,  918,  842,  778,
     668,  627,  590,  558,
     499,  476,  455,  435,
     399,  321,  269,  232
};

    // 1010,  918,  842,  778,
    //  668,  627,  590,  558,
    //  499,  476,  455,  435,
    //  399,  321,  269,  232

//     1015,  921,  846,  782,
//      671,  630,  594,  561,
//      502,  479,  457,  437,
//      401,  323,  271,  233



Monitor monitor;
Keypad data_keypad(DATA_KEYPAD_PIN, data_keypad_values);
Button minus_button(MINUS_BUTTON_PIN);
Keypad control_keypad(CONTROL_KEYPAD_PIN, control_keypad_values);
Potentiometer speed_pot(SPEED_POT_PIN, 10);
char key_convert_buffer[8];

void setup() {
    // Called once at Arduino startup.

    Serial.begin(9600);
    // Wait for serial port to connect. Needed for native USB port only
    while (!Serial) {
    ; 
    }

    monitor.init();
    data_keypad.init();
    control_keypad.init();
    speed_pot.init();
    minus_button.init();
    monitor.set_speed(speed_pot.get_value());

}

void loop() {
    // Main loop function for arduino.
    data_keypad.update(&data_keypad_key_pressed, NULL);
    control_keypad.update(&control_keypad_key_pressed, &control_keypad_key_released);
    speed_pot.update(&speed_value_changed);
    minus_button.update(&minus_button_pressed, NULL, NULL);
    monitor.update();
}


void data_keypad_key_pressed(int key) {
    if ((key >= 0) && (key <= 15)) {
        sprintf(key_convert_buffer, "%X", key);
        monitor.propose_character(key_convert_buffer[0]);
    }
}


void control_keypad_key_pressed(int key) {
    switch (key) {
        case CTL_KEY_NEXT_STORED_PRG:
            monitor.next_stored_pgm();
            break;
        case CTL_KEY_TRANSFER_STORED_PGM:
            monitor.transfer_stored_pgm();
            break;
        case CTL_KEY_BASE:
            monitor.next_number_base();
            break;
        case CTL_KEY_SIGNED:
            monitor.toggle_sign_mode();
            break;
        case CTL_KEY_AUTO_INC_ADDR:
            monitor.toggle_address_update_mode();
            break;
        case CTL_KEY_RAM_REGION:
            monitor.toggle_ram_region();
            break;
        case CTL_KEY_CONFIRM:
            monitor.confirm_current_field();
            break;
        case CTL_KEY_CLEAR:
            monitor.clear_curent_field();
            break;
        case CTL_KEY_INPUT_FIELD:
            monitor.toggle_input_field();
            break;
        case CTL_KEY_INCR_ADDR:
            monitor.incr_address();
            break;
        case CTL_KEY_DECR_ADDR:
            monitor.decr_address();
            break;
        case CTL_KEY_RESET:
            monitor.enable_reset();
            break;
        case CTL_KEY_RUN_PAUSE:
            monitor.toggle_run_pause();
            break;
        case CTL_KEY_QUARTER_STEP:
            monitor.quarter_step();
            break;
        case CTL_KEY_HALF_STEP:
            monitor.half_step();
            break;
        case CTL_KEY_FULL_STEP:
            monitor.full_step();
            break;
    }
}


void control_keypad_key_released(int key) {
    if (key == CTL_KEY_RESET) {
        monitor.disable_reset();
    }
}


void speed_value_changed(int new_value) {
    // Serial.println(new_value);
    monitor.set_speed(new_value);
}


void minus_button_pressed() {
    Serial.print("Data: ");
    Serial.println(analogRead(A0));
    Serial.print("Control: ");
    Serial.println(analogRead(A1));
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


