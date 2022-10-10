import keypad
from machine import Pin
import time

# https://github.com/micropython/micropython-lib/blob/master/python-stdlib/functools/functools.py
def partial(func, *args, **kwargs):
    def _partial(*more_args, **more_kwargs):
        kw = kwargs.copy()
        kw.update(more_kwargs)
        return func(*(args + more_args), **kw)

    return _partial


def button_pressed(row_index, column_index):
    print("Button at row index {row_index}, column index {column_index} pressed.".format(
        row_index=row_index,
        column_index=column_index
    ))

def main():
    freq_pin = Pin(15, mode=Pin.OUT, value=0)
    row_pins = [
        Pin(0),
        Pin(1),
        Pin(2),
        Pin(3),
    ]
    column_pins = [
        Pin(4),
        Pin(5),
        Pin(6),
        Pin(7),
        Pin(8),
        Pin(9),
        Pin(10),
        Pin(11),
    ]

    kp = keypad.Keypad(row_pins, column_pins)
    for row_index in range(4):
        for column_index in range(8):
            kp.set_callback(row_index, column_index, partial(button_pressed, row_index, column_index))

    while True:
        kp.update()
        freq_pin.toggle()
        # time.sleep(0.5)

main()