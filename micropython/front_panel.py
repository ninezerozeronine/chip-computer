import time

from . import interface


RUN = 100
STOP = 101

STEP = 200
FREQUENCY = 201
CRYSTAL = 202


class FrontPanel():
    """
    The user facing interface to the computer.
    """

    def __init__(self):
        """
        Initialise the class.
        """

        self._run_mode = STOP
        self._clock_mode = STEP
        self._frequency = 10000

    def run():
        """
        Put the computer into run mode.
        """
        if self._run_mode != RUN:
            # Disable any output onto the buses from the interface
            self._set_interface_bus_asserts(False)

            # Allow CPU to assert onto the buses.
            self._set_cpu_bus_asserts(True)

            # Enable the clock on the CPU
            interface.set_cpu_clock_input_enabled(True)

            self._run_mode = RUN

    def stop():
        """
        Put the computer into stop mode.
        """
        if self._run_mode != STOP:
            # Set the clock mode to STEP
            self.set_clock_mode(STEP)

            # Advance the clock so both clocks are low.
            while not self._at_beginning_of_clock_cycle():
                self.quarter_step()

            # Disable the clock on the CPU
            interface.set_cpu_clock_input_enabled(False)

            # Disable the CPU from asserting onto the buses.
            self._set_cpu_bus_asserts(False)

            # Disable any output onto the buses from the interface
            self._set_interface_bus_asserts(False)

            self._run_mode = STOP

    def toggle_run_stop():
        """
        Toggle the computer between run and stop mode.
        """
        if self._run_mode == RUN:
            self.stop()
        if self._run_mode == STOP:
            self.run()

    def reset():
        """
        Reset the computer.
        """
        interface.set_reset(True)
        time.sleep_ms(1)
        interface.set_reset(False)

    def quarter_step(self):
        """
        Advance the CPU by a quarter step.
        """
        if (self._clock_mode == STEP) and (self._run_mode == RUN):
             self._send_clock_pulses(1)

    def half_step(self):
        """
        Advance the CPU by a half step.
        """
        if (self._clock_mode == STEP) and (self._run_mode == RUN):
             self._send_clock_pulses(2)

    def full_step(self):
        """
        Advance the CPU by a full step.
        """
        if (self._clock_mode == STEP) and (self._run_mode == RUN):
             self._send_clock_pulses(4)

    def set_clock_frequency(self, frequency):
        """
        Set the clock frequency of the CPU (in Hz)
        """

        self._frequency = frequency

        if (self._clock_mode == FREQUENCY)
            if self._run_mode == RUN:
                interface.set_cpu_clock_input_enabled(False)
                interface.set_clock_pin_frequency(
                    self._adjust_clock_frequency(self._frequency)
                )
                interface.set_cpu_clock_input_enabled(True)

            if self._run_mode == STOP:
                interface.set_clock_pin_frequency(
                    self._adjust_clock_frequency(self._frequency)
                )

    def set_clock_mode(self, clock_mode):
        """
        Set the clock mode.

        The available modes are STEP, FREQUENCY, and CRYSTAL:

         - STEP: The clock is advanced 1, 2, or 4 steps at a time.
         - FREQUENCY: The clock can be set to a desired frequency in Hz.
         - CRYSTAL: The speed of the clock is determined by the crystal
           in the front panel.
        """
        if clock_mode == self._clock_mode:
            return

        if self._run_mode == RUN:
            interface.set_cpu_clock_input_enabled(False)

        if clock_mode == STEP:
            interface.set_clock_pin_static_state(False)
            interface.set_clock_source(interface.MICROCONTROLLER)

        if clock_mode == FREQUENCY:
            interface.set_clock_pin_frequency(
                self._adjust_clock_frequency(self._frequency)
            )
            interface.set_clock_source(interface.MICROCONTROLLER)

        if clock_mode == CRYTSAL:
            interface.set_clock_source(interface.CRYSTAL)

        if self._run_mode == RUN:
            interface.set_cpu_clock_input_enabled(True)

    def get_word(self, address):
        """
        Get a word from the device on the data bus at the given address.
        """

        word = 0

        if self._run_mode == STOP:
            interface.set_address(address)
            interface.set_read_from_mem(True)
            interface.set_write_to_mem(False)
            interface.set_interface_address_assert(True)
            interface.set_interface_read_write_mem_assert(True)
            time.sleep_us(10)
            word = interface.get_data()
            interface.set_read_from_mem(False)
            interface.set_write_to_mem(False)
            interface.set_interface_address_assert(False)
            interface.set_interface_read_write_mem_assert(False)

        return word

    def set_word(self, address, word):
        """
        Set a word on the device on the data bus at the given address.
        """
        if self._run_mode == STOP:
            interface.set_address(address)
            interface.set_data(word)
            interface.set_read_from_mem(False)
            interface.set_write_to_mem(True)
            interface.set_interface_address_assert(True)
            interface.set_interface_data_assert(True)
            interface.set_interface_read_write_mem_assert(True)
            interface.set_interface_clock_assert(True)
            time.sleep_us(10)
            self._send_cpu_like_clock_cycle()
            time.sleep_us(10)
            interface.set_read_from_mem(False)
            interface.set_write_to_mem(False)
            interface.set_interface_address_assert(False)
            interface.set_interface_data_assert(False)
            interface.set_interface_read_write_mem_assert(False)
            interface.set_interface_clock_assert(False)

    def set_words(self, addresses_and_words):
        """
        Set a number of addresses and words at once.
        """
        if self._run_mode == STOP:

            interface.set_read_from_mem(False)
            interface.set_write_to_mem(True)
            interface.set_interface_address_assert(True)
            interface.set_interface_data_assert(True)
            interface.set_interface_read_write_mem_assert(True)
            interface.set_interface_clock_assert(True)

            for address, word in addresses_and_words:
                interface.set_address(address)
                interface.set_data(word)
                time.sleep_us(1)
                self._send_cpu_like_clock_cycle()
                time.sleep_us(1)

            interface.set_read_from_mem(False)
            interface.set_write_to_mem(False)
            interface.set_interface_address_assert(False)
            interface.set_interface_data_assert(False)
            interface.set_interface_read_write_mem_assert(False)
            interface.set_interface_clock_assert(False)

    def _at_beginning_of_clock_cycle(self):
        """
        Test whether the CPU is at the beginning of a clock cycle.

        This happens when both the data and control clocks are low.
        """

        data_clock = interface.get_data_clock()
        control_clock = interface.get_control_clock()
        return not (data_clock or control_clock)

    def _set_interface_bus_asserts(self, state):
        """
        Set whether the interface should assert onto the buses.
        """
        interface.set_interface_data_assert(state)
        interface.set_interface_address_assert(state)
        interface.set_interface_read_write_mem_assert(state)
        interface.set_interface_clock_assert(state)

    def _set_cpu_bus_asserts(self, state):
        """
        Set whether the CPU should assert onto the buses.
        """
        interface.set_cpu_data_assert(state)
        interface.set_cpu_address_assert(state)
        interface.set_cpu_read_write_mem_assert(state)
        interface.set_cpu_clock_assert(state)

    def _send_clock_pulses(self, num_pulses):
        """
        Send the specified number of clock pulses.
        """
        for _ in range(num_pulses):
            interface.set_clock_pin_static_state(True)
            time.sleep_us(1)
            interface.set_clock_pin_static_state(False)
            time.sleep_us(1)

    def _adjust_clock_frequency(self, frequency):
        """
        Adjust the clock frequency to account for the clock processing
        in the CPU.
        """

        return frequency * 4

    def _send_cpu_like_clock_cycle(self):
        """
        Create a clock cycle comparable to that genertaed by the CPU.
        """
        interface.set_control_clock(True)
        time.sleep_us(1)
        interface.set_data_clock(True)
        time.sleep_us(1)
        interface.set_control_clock(False)
        time.sleep_us(1)
        interface.set_data_clock(False)
        time.sleep_us(1)