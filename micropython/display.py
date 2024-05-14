from machine import Pin, I2C
import asyncio

import ssd1306
from gpiodefs import OLED_SDA_GPIO_NO, OLED_SCL_GPIO_NO

from programs import PROGRAMS

from constants import (
    PANEL_MODE_STEP,
    PANEL_MODE_RUN,
    PANEL_MODE_STOP,
    PANEL_MODE_READ_MEMORY,
    CPU_CLK_SRC_PANEL,
    CPU_CLK_SRC_CRYSTAL
)

class Display():
    """
    Manages the OLED and remote display of the panel state.

    Almost all of the methods are protected with an asyncio Lock as
    more than one task can interact with this class at once (panel method
    call processor, and wifi connector). (Albeit rarely)

    """
    def __init__(self):
        """
        Initialise the class.
        """
        self._display = ssd1306.SSD1306_I2C(
            128,
            64,
            I2C(0, sda=Pin(OLED_SDA_GPIO_NO), scl=Pin(OLED_SCL_GPIO_NO))
        )
        self._connection_ref = None
        self._lock = asyncio.Lock()

        self.panel_mode_to_display = {
            PANEL_MODE_STEP: "STEP",
            PANEL_MODE_RUN: "RUN",
            PANEL_MODE_STOP: "STOP",
            PANEL_MODE_READ_MEMORY: "RDMEM",
        }

        self._address = 0
        self._address_str = ""

        self._data = 0
        self._data_str = ""

        self._user_input_str = ""

        self._mode = PANEL_MODE_STOP
        self._mode_str = ""

        self._program_name_str = ""

        self._frequency = 10

        self._ip_str = ""
        self._port_str = ""

        self._cpu_clock_source = CPU_CLK_SRC_PANEL
        self._redraw()

    def set_connection_ref(self, connection):
        self._connection_ref = connection

    async def send_data(self, data):
        if self._connection_ref is not None:
            if self._connection_ref.connected:
                await self._connection_ref.write(data)

    async def initialise_client(self):
        """
        Set the client to represent the current state if the display

        """
        await self.send_data(
            {
                "purpose":"display_update",
                "body": {
                    "address": self._address,
                    "data": self._data,
                    "panel_mode": self._mode,
                    "clock_source": self._cpu_clock_source,
                    "frequency": self._frequency
                }
            }
        )

    async def set_address(self, value):
        """
        Set the value for the address
        """

        async with self._lock:
            self._address = value

            # Set the OLED display
            self._address_str = f"{value:d}"
            self._redraw()

            # Set the remote display
            await self.send_data(
                {
                    "purpose":"display_update",
                    "body": {
                        "address":value
                    }
                }
            )

    async def set_data(self, value):
        """
        Set the value for the data
        """

        async with self._lock:
            self._data = value

            # Set the OLED display
            self._data_str = f"{value:d}"
            self._redraw()

            # Set the remote display
            await self.send_data(
                {
                    "purpose":"display_update",
                    "body": {
                        "data":value
                    }
                }
            )

    async def set_user_input(self, user_input):
        """
        Set the value of the current user input.

        Has no equivalent on the client but still needs to be async
        as all display calls are awaited.
        """
        async with self._lock:
            self._user_input_str = user_input
            self._redraw()

    async def set_run_mode(self, mode):
        """
        Set the current run mode.

        Args:
            source (int): Id of the run mode as per the run modes
                defined in constants.
        """
        async with self._lock:
            self._mode = mode

            # Set OLED
            self._mode_str = self.panel_mode_to_display.get(mode, "???")
            self._redraw()

            # Set the remote display
            await self.send_data(
                {
                    "purpose":"display_update",
                    "body": {
                        "panel_mode": mode
                    }
                }
            )

    async def set_program(self, program_index):
        """
        Set the program.

        Args:
            program_index (int): Index of the program as per the
                programs module.
        """
        async with self._lock:
            self._program_name_str = PROGRAMS[program_index]["oled_name"]
            self._redraw()

    async def set_frequency(self, frequency):
        """
        Set the value of the arbitrary frequency

        Args:
            frequency (float): The new frequency
        """

        async with self._lock:
            self._frequency = frequency
            self._redraw()

            # Set the remote display
            await self.send_data(
                {
                    "purpose":"display_update",
                    "body": {
                        "frequency":self._frequency
                    }
                }
            )

    async def set_cpu_clock_source(self, source):
        """
        Set the clock source for the CPU

        Args:
            source (int): ID of the clock source as per the clock
                sources defined in constants.
        """

        async with self._lock:
            self._cpu_clock_source = source
            self._redraw()

            # Set the remote display
            await self.send_data(
                {
                    "purpose":"display_update",
                    "body": {
                        "clock_source":source
                    }
                }
            )

    async def set_ip(self, ip):
        async with self._lock:
            self._ip_str = ip
            self._redraw()

    async def set_port(self, port):
        async with self._lock:
            self._port_str = port
            self._redraw()

    def _frequency_to_str(self, frequency):
        """
        Convert a frequency value to a string
        """

        frequency_str = "ERROR"

        if frequency < 10.0:
            frequency_str = f"{frequency:.2f}Hz"
        elif frequency < 100.0:
            frequency_str = f"{frequency:.1f}Hz"
        elif frequency < 1000.0:
            rounded = round(frequency)
            frequency_str = f"{rounded:d}Hz"
        elif frequency < 1000000.0:
            khz = frequency / 1000.0
            if khz < 10.0:
                frequency_str = f"{khz:.1f}KHz"
            else:
                rounded = round(khz)
                frequency_str = f"{rounded:d}KHz"
        else:
            mhz = frequency / 1000000.0
            frequency_str = f"{mhz:.1f}MHz"

        return frequency_str

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
        display_str = "???"
        if self._cpu_clock_source == CPU_CLK_SRC_CRYSTAL:
            display_str = "XTAL"
        if self._cpu_clock_source == CPU_CLK_SRC_PANEL:
            display_str = self._frequency_to_str(self._frequency)
        self._display.text(display_str, 80, 16, 1)

        #IP and port
        self._display.text(self._ip_str, 0, 24, 1)
        self._display.text(self._port_str, 0, 32, 1)
        # self._display.text("foo", 0, 40, 1)
        # self._display.text("bar", 0, 48, 1)
        # self._display.text("baz", 0, 56, 1)

        self._display.show()
