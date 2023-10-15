"""
Main entry point for Micropython functionality
"""

from machine import Pin

from front_panel import FrontPanel
from keypad import Keypad
from gpiodefs import KEYPAD_GPIOS


# https://github.com/micropython/micropython-lib/blob/master/python-stdlib/functools/functools.py
def partial(func, *args, **kwargs):
    def _partial(*more_args, **more_kwargs):
        kw = kwargs.copy()
        kw.update(more_kwargs)
        return func(*(args + more_args), **kw)

    return _partial

def main():
    """

    """

    row_pins = [
        Pin(KEYPAD_GPIOS[0]),
        Pin(KEYPAD_GPIOS[1]),
        Pin(KEYPAD_GPIOS[2]),
        Pin(KEYPAD_GPIOS[3]),
    ]
    column_pins = [
        Pin(KEYPAD_GPIOS[4]),
        Pin(KEYPAD_GPIOS[5]),
        Pin(KEYPAD_GPIOS[6]),
        Pin(KEYPAD_GPIOS[7]),
        Pin(KEYPAD_GPIOS[8]),
        Pin(KEYPAD_GPIOS[9]),
        Pin(KEYPAD_GPIOS[10]),
        Pin(KEYPAD_GPIOS[11]),
    ]

    panel = FrontPanel()
    keypad = Keypad(row_pins, column_pins)

    # Digits on numpbers keypad
    keypad.set_pressed_callback(3, 3, partial(panel.propose_user_input_character, "1"))
    keypad.set_pressed_callback(3, 2, partial(panel.propose_user_input_character, "2"))
    keypad.set_pressed_callback(3, 1, partial(panel.propose_user_input_character, "3"))
    keypad.set_pressed_callback(2, 3, partial(panel.propose_user_input_character, "4"))
    keypad.set_pressed_callback(2, 2, partial(panel.propose_user_input_character, "5"))
    keypad.set_pressed_callback(2, 1, partial(panel.propose_user_input_character, "6"))
    keypad.set_pressed_callback(1, 3, partial(panel.propose_user_input_character, "7"))
    keypad.set_pressed_callback(1, 2, partial(panel.propose_user_input_character, "8"))
    keypad.set_pressed_callback(1, 1, partial(panel.propose_user_input_character, "9"))
    keypad.set_pressed_callback(0, 3, partial(panel.propose_user_input_character, "."))
    keypad.set_pressed_callback(0, 2, partial(panel.propose_user_input_character, "0"))

    # Functions on numbers keypad
    keypad.set_pressed_callback(0, 1, panel.delete_last_user_input_char)
    keypad.set_pressed_callback(0, 0, panel.clear_user_input)
    
    # Control keypad
    # keypad.set_pressed_callback(0, 4, panel.quarter_step)
    keypad.set_pressed_callback(3, 6, panel.half_step)
    keypad.set_pressed_callback(3, 5, panel.full_step)
    keypad.set_pressed_callback(3, 4, panel.step)

    keypad.set_pressed_callback(2, 7, panel.set_readwrite_address_from_user_input)
    keypad.set_pressed_callback(2, 6, panel.decr_readwrite_address)
    keypad.set_pressed_callback(2, 5, panel.incr_readwrite_address)
    keypad.set_pressed_callback(2, 4, panel.run)

    keypad.set_pressed_callback(1, 7, panel.set_word_from_user_input)
    keypad.set_pressed_callback(1, 6, panel.set_word_from_user_input_then_incr_addr)
    keypad.set_pressed_callback(1, 5, panel.next_clock_source)
    keypad.set_pressed_callback(1, 4, panel.stop)

    keypad.set_pressed_callback(0, 7, panel.set_frequency_from_user_input)
    keypad.set_pressed_callback(0, 6, panel.next_program)
    keypad.set_pressed_callback(0, 5, panel.set_current_program)
    keypad.set_pressed_callback(0, 4, partial(panel.set_reset, True))
    keypad.set_released_callback(0, 4, partial(panel.set_reset, False))

    while True:
        keypad.update()

main()
