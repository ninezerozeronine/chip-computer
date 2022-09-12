"""
Manages the OLED display on the front panel
"""

import ssd1306

MAX_USER_INPUT_STRING_LENGTH = 8

class Display():
    def __init__(self, i2c):
        self._display = ssd1306.SSD1306_I2C(128, 32, i2c)

    def set_address(self, address):
        """
        Set the address displayed
        """
        self._address = address

    def set_data(self, data):
        """
        Set the data displayed
        """
        self._data = data

    def set_user_input(self, user_input):
        """
        Set the value of the current userinput
        """
        self._user_input = user_input
