"""
GPIO numbers used by the various parts of the system.

Note that pin numbers on the device and GPIO numbers used to set up
Pin objects are different. E.g. Physical pin 5 on the Raspberry Pi
Pico W corresponds to GPIO 3.

All stored here in one place so it's harder for there to be a pin clash.
"""

# Pins used to read the keypad
KEYPAD_GPIOS = [
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
]

# Pins that control the 74HC597s that read data from the computer.
INPUT_STORAGE_CLOCK_GPIO_NO = 12
INPUT_PARALLEL_LOAD_GPIO_NO = 13
INPUT_SHIFT_CLOCK_GPIO_NO = 14
INPUT_SERIAL_READ_GPIO_NO = 22

# Pins that control the 74HC595s that output to the computer.
OUTPUT_SERIAL_OUT_GPIO_NO = 15
OUTPUT_SHIFT_CLOCK_GPIO_NO = 16
OUTPUT_OUTPUT_CLOCK_GPIO_NO = 17

# Pin on the microcontroller that outputs a signal to advance the CPU
# clock.
CPU_CLOCK_GPIO_NO = 18

# Pins for the OLED display I2C interface
OLED_SDA_GPIO_NO = 20
OLED_SCL_GPIO_NO = 21
