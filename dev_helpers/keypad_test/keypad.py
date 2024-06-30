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

        # Set all column pins to Open drain mode
        for column_pin in self._column_pins:
            column_pin.init(mode=Pin.OPEN_DRAIN)
            column_pin.value(1)

        # Set all row pins to input pulldown
        for row_pin in self._row_pins:
            row_pin.init(mode=Pin.IN, pull=Pin.PULL_DOWN)

        self._last_states = []
        self._current_states = []
        self._callbacks = []
        for _ in range(self._num_rows):
            self._last_states.append([0] * self._num_columns)
            self._current_states.append([0] * self._num_columns)
            self._callbacks.append([None] * self._num_columns)

    def _update_current_states(self):
        """
        Scan the keypad and look for buttons getting pressed
        """

        for column_index, column_pin in enumerate(self._column_pins):
            column_pin.init(mode=Pin.OUT)
            column_pin.value(1)

            for row_index, row_pin in enumerate(self._row_pins):
                self._current_states[row_index][column_index] = row_pin.value()

            column_pin.init(mode=Pin.OPEN_DRAIN)
            column_pin.value(1)

    def _call_callbacks_from_presses(self):
        """

        """
        for row_index in range(self._num_rows):
            for column_index in range(self._num_columns):
                if (
                    self._last_states[row_index][column_index] == 0
                    and
                    self._current_states[row_index][column_index] == 1
                ):
                    callback = self._callbacks[row_index][column_index]
                    if callback is not None:
                        callback()

    def _print_current_state(self):
        for row_index in range(self._num_rows):
            for column_index in range(self._num_columns):
                print(self._current_states[row_index][column_index], end="")
            print("\n")

        print ("---")

    def _copy_current_to_last(self):
        for row_index in range(self._num_rows):
            for column_index in range(self._num_columns):
                    self._last_states[row_index][column_index] = self._current_states[row_index][column_index] == 1

    def update(self):
        self._update_current_states()
        self._call_callbacks_from_presses()
        self._copy_current_to_last()

    def set_callback(self, row_index, column_index, callback):
        """

        """
        self._callbacks[row_index][column_index] = callback




























