"""
Manages the OLED display on the front panel
"""
from machine import Pin, I2C

import ssd1306
from gpiodefs import OLED_SDA_GPIO_NO, OLED_SCL_GPIO_NO

class Display():
    def __init__(self):
        self._display = ssd1306.SSD1306_I2C(
            128,
            64,
            I2C(1, sda=Pin(OLED_SDA_GPIO_NO), scl=Pin(OLED_SCL_GPIO_NO))
        )
        self._address_str = ""
        self._data_str = ""
        self._user_input_str = ""
        self._mode_str = ""
        self._program_name_str = ""
        self._frequency_str = ""
        self._ip_str = ""
        self._port_str = ""
        self._redraw()

    def set_address(self, address):
        """
        Set the address displayed.
        """
        self._address_str = f"{address:d}"
        self._redraw()

    def set_data(self, data):
        """
        Set the data displayed.
        """
        self._data_str = f"{data:d}"
        self._redraw()

    def set_user_input(self, user_input):
        """
        Set the value of the current user input.
        """
        self._user_input_str = user_input
        self._redraw()

    def set_mode(self, mode):
        """
        Set the current mode.
        """
        self._mode_str = mode
        self._redraw()

    def set_program_name(self, program_name):
        """
        Set the program name.
        """
        self._program_name_str = program_name
        self._redraw()

    def set_frequency_to_value(self, frequency):
        """
        Set the frequency
        """

        if frequency < 10.0:
            self._frequency_str = f"{frequency:.2f}Hz"
        elif frequency < 100.0:
            self._frequency_str = f"{frequency:.1f}Hz"
        elif frequency < 1000.0:
            rounded = round(frequency)
            self._frequency_str = f"{rounded:d}Hz"
        elif frequency < 1000000.0:
            khz = frequency / 1000.0
            if khz < 10.0:
                self._frequency_str = f"{khz:.1f}KHz"
            else:
                rounded = round(khz)
                self._frequency_str = f"{rounded:d}KHz"
        else:
            mhz = frequency / 1000000.0
            self._frequency_str = f"{mhz:.1f}MHz"

        self._redraw()

    def set_frequency_to_crystal(self):
        self._frequency_str = "XTAL"
        self._redraw()

    def set_ip(self, ip):
        self._ip_str = ip
        self._redraw()

    def set_port(self, port):
        self._port_str = port
        self._redraw()

    # def update_panel_state(self, state):
    #     address
    #     data
    #     user_input
    #     mode
    #     prog_name
    #     frequency


    def _redraw(self):
        """
        Redraw the display

        It looks like this:
        
        |A:xxxxx D:xxxxx |
        |>xxxxxxxM:xxxx  |
        |P:xxxxx F:xxxxxx|
        |255.255.255.255 | <- IP
        |65535           | <- Port

        """

        # Clear display
        self._display.fill(0)

        # Address
        self._display.text("A:", 0, 0, 1)
        self._display.text(self._address_str, 16, 0, 1)

        # Data
        self._display.text("D:", 64, 0, 1)
        self._display.text(self._data_str, 80, 0, 1)

        # User input
        self._display.text(">", 0, 8, 1)
        self._display.text(self._user_input_str, 8, 8, 1)

        # Mode
        self._display.text("M:", 64, 8, 1)
        self._display.text(self._mode_str, 80, 8, 1)

        # Program Name
        self._display.text("P:", 0, 16, 1)
        self._display.text(self._program_name_str, 16, 16, 1)

        # Frequency
        self._display.text("F:", 64, 16, 1)
        self._display.text(self._frequency_str, 80, 16, 1)

        #IP and port
        self._display.text(self._ip_str, 0, 24, 1)
        self._display.text(self._port_str, 0, 32, 1)

        self._display.show()
