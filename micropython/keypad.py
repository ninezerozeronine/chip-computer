"""
Handle keypad presses

# 2 rows, 4 columns
[
    [A, B, C, D],
    [E, F, G, H]
]

array[0][2] = C
array[1][3] = H

array[row_index * num_columns + column_index]

"""

from machine import Pin

class Keypad():
    def __init__(self, row_pins, column_pins):
        """
        Initialise the keypad
        """

        self._num_rows = len(row_pins)
        self._num_columns = len(column_pins)

        self._row_pins = row_pins
        self._column_pins = column_pins

        # Set all pins to input pulldown

        self._last_states = []
        for _ in range(self._num_rows):
            self._last_states.append([0] * self.num_columns)

    def scan(self):
        """
        Scan the keypad and look for buttons getting pressed
        """

        current_states = []
        for _ in range(self._num_rows):
            current_states.append([False] * self._num_columns)

        for row_index, row_pin in enumerate(self._row_pins):
            for column_index, column_pin in enumnerate(self._column_pins):
                column_pin.init(Pin.OUT)
                column_pin.value(1)
                current_states = row_pin.value()
                column_pin.init(Pin.IN, Pin.PULL_DOWN)

        

        self._last_states = current_states




























