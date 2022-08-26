"""
The low level hardware interface to the computer.
"""

MICROCONTROLLER = 100
CRYSYAL = 101

class Interface():
    """
    The low level hardware interface to the computer.
    """

    def __init__(self):
        """
        Initialise the interface.
        """
        self._data = 0
        self._interface_data_assert = False
        self._cpu_data_assert = False

        self._address = 0
        self._interface_address_assert = False
        self._cpu_address_assert = False

        self._read_from_mem = False
        self._interface_read_from_mem_assert = False
        self._cpu_read_from_mem_assert = False

        self._write_to_mem = False
        self._interface_write_to_mem_assert = False
        self._cpu_write_to_mem_assert = False

        self._data_clock = False
        self._control_clock = False
        self._interface_assert_clock_bus = False
        self._cpu_assert_clock_bus = False

        self._cpu_clock_input_enabled = False

        self._clock_source = MICROCONTROLLER

    def set_data(self, data):
        """
        Set the data to be output to the data bus.
        """
        pass

    def get_data(self):
        """
        Get the data currently on the data bus.
        """
        pass

    def set_interface_data_assert(self, state):
        """
        Set whether the interface should assert onto the data bus.
        """
        pass

    def set_cpu_data_assert(self, state):
        """
        Set whether the CPU should assert onto the data bus.
        """
        pass

    def set_address(self):
        """
        Set the address to put on the address bus.
        """
        pass

    def get_address(self):
        """
        Get the address currently on the address bus.
        """
        pass

    def set_interface_address_assert(self, state):
        """
        Set whether the interface should assert onto the address bus.
        """
        pass

    def set_cpu_address_assert(self, state):
        """
        Set whether the CPU should assert onto the address bus.
        """
        pass

    def get_read_from_mem(self):
        """
        Get the state of the read from memory bus.
        """
        pass

    def set_interface_read_from_mem_assert(self, state):
        """
        Set whether the interface should assert onto the read from
        memory bus.
        """
        pass

    def set_cpu_read_from_mem_assert(self, state):
        """
        Set whether the CPU should assert onto the read from memory bus.
        """
        pass

    def get_write_to_mem(self):
        """
        Get the state of the write to memory bus.
        """
        pass

    def set_interface_write_to_mem_assert(self, state):
        """
        Set whether the interface should assert onto the write to
        memory bus.
        """
        pass

    def set_cpu_write_to_mem_assert(self, state):
        """
        Set whether the CPU should assert onto the write to memory bus.
        """
        pass

    def get_data_clock(self):
        """
        Get the state of the data clock bus.
        """
        pass

    def get_control_clock(self):
        """
        Get the state of the control clock bus.
        """
        pass

    def set_interface_clock_assert(self, state):
        """
        Set whether the interface should assert onto the clock buses.
        """
        pass

    def set_cpu_clock_assert(self, state):
        """
        Set whether the CPU should assert onto the clock buses.
        """
        pass

    def set_cpu_clock_input_enabled(self, state):
        """
        Set whether the CPU clock input is enabled or not.
        """
        pass

    def set_clock_source(self, source):
        """
        Set the source for the clock.
        """
        pass