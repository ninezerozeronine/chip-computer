#ifndef PINDEFS_H
#define PINDEFS_H

// Hardware Bridge Pins
#define ADDRESS_SERIAL_LATCH_PIN 3
#define ADDRESS_SERIAL_CLOCK_PIN 4
#define ADDRESS_SERIAL_DATA_PIN 5

#define STAGED_DATA_SERIAL_LATCH_PIN 6
#define STAGED_DATA_SERIAL_CLOCK_PIN 7
#define STAGED_DATA_SERIAL_DATA_PIN 8

#define READ_DATA_SERIAL_LATCH_PIN 10
#define READ_DATA_SERIAL_CLOCK_PIN 11
#define READ_DATA_SERIAL_DATA_PIN 12

#define RAM_REGION_PIN 14
#define RAM_CONTROL_MODE_PIN 15
#define RESET_PIN 16
#define RAM_WRITE_SIGNAL_PIN 17
#define CLOCK_SOURCE_PIN 18
#define CLOCK_ENABLED_PIN 19

/**
Note that timer1 can be used on a Mega but does not support all three
output pins OCR1A, OCR1B & OCR1C. Only A & B are supported. OCR1A is
connected to pin 11 of the Mega and OCR1B to pin 12. Using one of the
three calls that specify a pin, 1 will map to pin 11 on the Mega and
2 will map to pin 12. Timer3 has only been tested on the Mega.

https://playground.arduino.cc/Code/Timer1/
**/
#define CLOCK_PIN 11

// LCD Pins
// N/A SCA is pin 20 and SCL pin 21 on a Mega (A4 and A5 on a Nano/Uno)

// Monitor Pins
#define DATA_KEYPAD_PIN A0
#define MINUS_BUTTON_PIN 22
#define CONTROL_KEYPAD_PIN A1
#define SPEED_POT_PIN A2

#endif