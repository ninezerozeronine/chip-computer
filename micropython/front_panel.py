"""

step
run
stop

set_clock_source
set_clock_frequency

quarter_step
half_step
full_step

set_address
incr_address
decr_address
write_data
write_data_incr_addr

prog_sel
write_prog

"""



import time

import interface
import display

# The current mode the panel is in
# Allows single stepping of the CPU. The CPU is in full control
# of the peripherals.
STEP = 100

# Running at a given frequency. The CPU is in full control of the
# peripherals.
RUN = 101

# The CPU is stopped. Control of peripherals is given to the panel.
STOP = 102

# The clock source for the CPU 
FRONT_PANEL = 200
CRYSTAL = 201

# Maximum 16 bit value
_MAX_VALUE = 2**16 - 1

class FrontPanel():
    """
    The user facing interface to the computer.
    """

    def __init__(self):
        """
        Initialise the class.
        """

        self._panel_mode = STOP
        self._cpu_clock_source = FRONT_PANEL
        self._frequency = 10000
        self._readwrite_address = 0
        self._user_input = 0
        self._user_input_string = ""
        self._interface = interface.Interface()
        self._panel_mode = RUN
        self.stop()

        self._display = display.Display()

    def step():
        """
        Puts the panel into step mode.
        """

        if self._panel_mode != STEP:
            # Disable any output onto the address and data buses from
            # the interface
            self._interface.set_interface_data_assert(False)
            self._interface.set_interface_address_assert(False)

            # Set the source of the control and data clocks, and the
            # rfm/wtm lines to the CPU
            self._interface.set_control_data_clock_source(interface.CPU)
            self._interface.set_read_write_mem_source(interface.CPU)

            # Allow CPU to assert onto the buses.
            self._interface.set_cpu_data_assert(True)
            self._interface.set_cpu_address_assert(True)

            # Disable the clock on the CPU
            self._interface.set_cpu_clock_input_enabled(False)

            # Make sure the CPU gets clock pulses from the
            # microcontroller
            self._interface.set_cpu_clock_source(interface.MICROCONTROLLER)

            # Set the interface clock pin to a static state, ready for
            # stepping.
            self._interface.set_clock_pin_static_state(False)

            # Enable the clock on the CPU
            self._interface.set_cpu_clock_input_enabled(True)

            self._panel_mode = STEP

    def run():
        """
        Put the panel into run mode.
        """
        if self._panel_mode != RUN:
            # Disable any output onto the address and data buses from
            # the interface
            self._interface.set_interface_data_assert(False)
            self._interface.set_interface_address_assert(False)

            # Set the source of the control and data clocks, and the
            # rfm/wtm lines to the CPU
            self._interface.set_control_data_clock_source(interface.CPU)
            self._interface.set_read_write_mem_source(interface.CPU)

            # Allow CPU to assert onto the buses.
            self._interface.set_cpu_data_assert(True)
            self._interface.set_cpu_address_assert(True)

            # Disable the clock on the CPU
            self._interface.set_cpu_clock_input_enabled(False)

            # Set the clock source for the CPU
            self._set_clock_source()

            self._panel_mode = RUN

    def stop():
        """
        Put the panel into stop mode.
        """
        if self._panel_mode != STOP:
            # Disable the clock on the CPU
            self._interface.set_cpu_clock_input_enabled(False)

            # Make sure the CPU gets clock pulses from the
            # microcontroller
            self._interface.set_cpu_clock_source(interface.MICROCONTROLLER)

            # Set the interface clock pin to a static state, ready for
            # stepping.
            self._interface.set_clock_pin_static_state(False)

            # Enable the clock on the CPU
            self._interface.set_cpu_clock_input_enabled(True)

            # Advance the clock so both clocks are low.
            while not self._at_beginning_of_clock_cycle():
                self._send_clock_pulses(1)

            # Disable the clock on the CPU
            self._interface.set_cpu_clock_input_enabled(False)

            # Disable the CPU from asserting onto the buses.
            self._interface.set_cpu_data_assert(False)
            self._interface.set_cpu_address_assert(False)

            # Disable interface from asserting onto the or address bus
            self._interface.set_interface_data_assert(False)
            self._interface.set_interface_address_assert(False)

            # Set the control and data clocks as well as the read from
            # and write to memory lines low.
            self._interface.set_control_clock(False)
            self._interface.set_data_clock(False)
            self._interface.set_read_from_mem(False)
            self._interface.set_write_to_mem(False)

            # Set the source of the control and data clocks, and the
            # rfm/wtm lines to the Panel
            self._interface.set_control_data_clock_source(interface.FRONT_PANEL)
            self._interface.set_read_write_mem_source(interface.FRONT_PANEL)

            # Get and display the current word at the readwrite address
            self._get_and_display_current_word()

            self._panel_mode = STOP

    def reset():
        """
        Reset the computer.
        """
        self._interface.set_reset(True)
        time.sleep_ms(1)
        self._interface.set_reset(False)

    def quarter_step(self):
        """
        Advance the CPU by a quarter step.
        """
        if self._panel_mode == STEP:
            self._send_clock_pulses(1)

    def half_step(self):
        """
        Advance the CPU by a half step.
        """
        if self._panel_mode == STEP:
            self._send_clock_pulses(2)

    def full_step(self):
        """
        Advance the CPU by a full step.
        """
        if self._panel_mode == STEP:
            self._send_clock_pulses(4)

    def set_clock_frequency(self, frequency):
        """
        Set the clock frequency of the CPU (in Hz).

        Either sets the frequency immediately (when in run mode and with
        clock source set to panel) or when appropriate.
        """
        if frequency < 0.09:
            return

        self._frequency = frequency

        if (self._panel_mode == RUN and self._cpu_clock_source == FRONT_PANEL):
            self._interface.set_cpu_clock_input_enabled(False)
            self._interface.set_clock_pin_frequency(
                self._adjust_clock_frequency(self._frequency)
            )
            self._interface.set_cpu_clock_input_enabled(True)

    def set_clock_source(self, clock_source):
        """
        Set the clock source.

        The available sources are FRONT_PANEL and CRYSTAL:

         - FRONT_PANEL: The clock can be set to a desired frequency in
           Hz.
         - CRYSTAL: The speed of the clock is determined by the crystal.
        """
        if clock_source not in (FRONT_PANEL, CRYSTAL):
            return

        if clock_source == self._clock_source:
            return

        self._clock_source = clock_source

        if self._panel_mode == RUN:
            self._set_clock_source()

    def _set_clock_source(self):
        """
        Set the clock source for the CPU.

        No safe guards.
        """

        self._interface.set_cpu_clock_input_enabled(False)

        if self._clock_source == FRONT_PANEL:
            self._interface.set_clock_source(interface.MICROCONTROLLER)
            self._interface.set_clock_pin_frequency(
                self._adjust_clock_frequency(self._frequency)
            )
        if self.clock_source == CRYSTAL:
            self._interface.set_clock_source(interface.CRYSTAL)

        self._interface.set_cpu_clock_input_enabled(True)

    def set_readwrite_address_from_user_input(self):
        """
        Attempt to set the readwrite address from the user input.

        Nothing happens if the user input is invalid.

        If the user input is valid, that new address is set, the user
        input cleared and the word at the new address read and displayed.
        """

        if not self._is_valid_address(self._user_input):
            return

        self._readwrite_address = address
        self._display.

        if self._panel_mode == STOP:
            self._display.set_rwaddr(self._readwrite_address)
            self._get_and_display_current_word()

    def incr_readwrite_address(self):
        """
        Increment the current readwrite address by one.

        If the value is at the max, wrap back to zero.
        """
        
        # Increment, wrapping if necessary
        self._readwrite_address += 1
        if self._readwrite_address > _MAX_VALUE:
            self._readwrite_address = 0

        if self._panel_mode == STOP
            self._display.set_rwaddr(self._readwrite_address)
            self._get_and_display_current_word()

    def decr_readwrite_address(self):
        """
        Decrement the current readwrite address by one.

        If the value goes below zero, wrap back to the max
        """
        
        # Decrement, wrapping if necessary
        self._readwrite_address -= 1
        if self._readwrite_address < 0:
            self._readwrite_address = _MAX_VALUE

        if self._panel_mode == STOP:
            self._display.set_readwrite_address(self._readwrite_address)
            self._get_and_display_current_word()

    def set_word_from_user_input(self):
        """
        Set the word at the readwrite address from the current user
        input.
        """

        # Check user input is valid
        if not self._is_valid_word(self._user_input):
            return

        if self._panel_mode == STOP:
            # Set word at current readwrite address
            self._set_word(self._readwrite_address, int(self._user_input))

            # Read word at readwrite address and set to display
            self._get_and_display_current_word()

    def set_word_from_user_input_then_incr_addr(self):
        """
        Set word from user input, then increment readwrite addr.

        The readwrite addr will wrap if necessary
        """

        # Check user input is valid

        # Set word at current readwrite address

        # Increment readwrite, wrapping if necessary

        # Read word at readwrite address and set to display

        pass

    def propose_user_input_character(self, character):
        """

        """
        if character not in ".0123456789":
            return

        if len(self._user_input_string) >= 8:
            return

        self._user_input_string += character
        self._display.set_user_input(self._user_input_string)

    def clear_user_input(self):
        """

        """
        pass

    def set_frequency_from_user_input(self):
        """

        """
        pass      

    def set_words(self, addresses_and_words):
        """
        Set a number of addresses and words at once.
        """
        if self._panel_mode == STOP:

            self._interface.set_read_from_mem(False)
            self._interface.set_write_to_mem(True)
            self._interface.set_interface_address_assert(True)
            self._interface.set_interface_data_assert(True)
            self._interface.set_interface_read_write_mem_assert(True)
            self._interface.set_interface_clock_assert(True)

            for address, word in addresses_and_words:
                self._interface.set_address(address)
                self._interface.set_data(word)
                time.sleep_us(1)
                self._send_cpu_like_clock_cycle()
                time.sleep_us(1)

            self._interface.set_read_from_mem(False)
            self._interface.set_write_to_mem(False)
            self._interface.set_interface_address_assert(False)
            self._interface.set_interface_data_assert(False)
            self._interface.set_interface_read_write_mem_assert(False)
            self._interface.set_interface_clock_assert(False)

    def _at_beginning_of_clock_cycle(self):
        """
        Test whether the CPU is at the beginning of a clock cycle.

        This happens when both the data and control clocks are low.
        """

        data_clock = self._interface.get_data_clock()
        control_clock = self._interface.get_control_clock()
        return not (data_clock or control_clock)

    def _send_clock_pulses(self, num_pulses):
        """
        Send the specified number of clock pulses.
        """
        for _ in range(num_pulses):
            self._interface.set_clock_pin_static_state(True)
            time.sleep_us(1)
            self._interface.set_clock_pin_static_state(False)
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
        self._interface.set_control_clock(True)
        time.sleep_us(1)
        self._interface.set_data_clock(True)
        time.sleep_us(1)
        self._interface.set_control_clock(False)
        time.sleep_us(1)
        self._interface.set_data_clock(False)
        time.sleep_us(1)

    def _set_word(self, address, word):
        """
        Set a word on the device on the data bus at the given address.
        """
        if self._panel_mode == STOP:
            self._interface.set_address(address)
            self._interface.set_data(word)
            self._interface.set_read_from_mem(False)
            self._interface.set_write_to_mem(True)
            self._interface.set_interface_address_assert(True)
            self._interface.set_interface_data_assert(True)
            self._interface.set_interface_read_write_mem_assert(True)
            self._interface.set_interface_clock_assert(True)
            time.sleep_us(10)
            self._send_cpu_like_clock_cycle()
            time.sleep_us(10)
            self._interface.set_read_from_mem(False)
            self._interface.set_write_to_mem(False)
            self._interface.set_interface_address_assert(False)
            self._interface.set_interface_data_assert(False)
            self._interface.set_interface_read_write_mem_assert(False)
            self._interface.set_interface_clock_assert(False)

    def _get_word(self, address):
        """
        Get a word from the device on the data bus at the given address.
        """

        word = 0

        if self._panel_mode == STOP:
            self._interface.set_address(address)
            self._interface.set_read_from_mem(True)
            self._interface.set_write_to_mem(False)
            self._interface.set_interface_address_assert(True)
            self._interface.set_interface_read_write_mem_assert(True)
            time.sleep_us(10)
            word = self._interface.get_data()
            self._interface.set_read_from_mem(False)
            self._interface.set_write_to_mem(False)
            self._interface.set_interface_address_assert(False)
            self._interface.set_interface_read_write_mem_assert(False)

        return word

    def _is_valid_address(self, _address):
        """
        Check if the passed in address is valid
        """
        try
            address = int(_address)
        except
            return False

        if not 0 <= address <= _MAX_VALUE:
            return False

        return True

    def _is_valid_word(self, _word):
        """
        Check if the passed in word is valid
        """
        try
            word = int(_word)
        except
            return False

        if not 0 <= word <= _MAX_VALUE:
            return False

        return True






