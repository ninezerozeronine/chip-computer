"""
GPIO numbers used by the various parts of the system.

Note that pin numbers on the device and GPIO numbers used to set up
Pin objects are different. E.g. Physical pin 5 on the Raspberry Pi
Pico W corresponds to GPIO 3.

All stored here in one place so it's harder for there to be a pin clash.
"""

# Pins used to read the keypad
KEYPAD_ROW_GPIOS = [
    9,
    8,
    7,
    6,
]
KEYPAD_COL_GPIOS = [
    5,
    4,
    3,
    2,
]

# Pins for the OLED display I2C interface
OLED_SDA_GPIO_NO = 26
OLED_SCL_GPIO_NO = 27
