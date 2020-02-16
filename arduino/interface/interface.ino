// Code to make interfacing with the eight bit computer easier

// #include <Arduino.h>

// #include "button.h"
// #include "keypad.h"


// void setup() {
//     // Called once at Arduino startup.

//     Serial.begin(115200);
//     // wait for serial port to connect. Needed for native USB port only
//     while (!Serial) {
//     ; 
//     }
// }

// void loop() {
//     // Main loop function for arduino.
// }
























// Test code

#define KEYPAD_PIN A0
#define BUTTON_PIN 2

#include <Arduino.h>

#include "button.h"
#include "keypad.h"

const int keypad_values[] = {
    1023,
    930,
    853,
    787,

    675,
    633,
    596,
    563,

    504,
    480,
    459,
    439,

    402,
    323,
    270,
    232
};

Button test_button(BUTTON_PIN);
Keypad test_keypad(KEYPAD_PIN, keypad_values);

void setup() {
    // Called once at Arduino startup.

    test_button.init();
    test_keypad.init();

    Serial.begin(115200);
    // wait for serial port to connect. Needed for native USB port only
    while (!Serial) {
    ; 
    }
}

void loop() {
    // Main loop function for arduino.
    test_button.update(&button_pressed, &button_released, &button_repeating);
    test_keypad.update(&keypad_key_pressed, &keypad_key_released);
}

void button_pressed() {
    Serial.println("Button pressed.");
    Serial.println(analogRead(A0));
}

void button_released() {
    Serial.println("Button released.");
}

void button_repeating() {
    Serial.println("Button repeating.");
}

void keypad_key_pressed(int key) {
    Serial.print(key);
    Serial.println(" key on keypad pressed.");
}

void keypad_key_released(int key) {
    Serial.print(key);
    Serial.println(" key on keypad released.");
}

