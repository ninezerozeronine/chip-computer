"""

"""
import time

import interface
import display
from programs import PROGRAMS

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

        self._cpu_clock_sources = [
            FRONT_PANEL,
            CRYSTAL,
        ]
        self._cpu_clock_source_index = 0
        self._cpu_clock_source = self._cpu_clock_sources[self._cpu_clock_source_index]
        self._program_index = 0
        self._frequency = 10
        self._readwrite_address = 0
        self._user_input_string = ""
        self._interface = interface.Interface()
        self._display = display.Display()
        self._display.set_program_name(PROGRAMS[self._program_index]["name"][0:6])
        self._update_frequency_display()
        self._panel_mode = RUN
        self.stop()

    def half_step(self):
        """
        Advance the CPU by a half step.
        """
        if self._panel_mode == STEP:
            self._send_clock_pulses(1)

            # Read and display the address and data
            self._display.set_address(self._interface.get_address())
            self._display.set_data(self._interface.get_data())

    def full_step(self):
        """
        Advance the CPU by a full step.
        """
        if self._panel_mode == STEP:
            self._send_clock_pulses(2)

            # Read and display the address and data
            self._display.set_address(self._interface.get_address())
            self._display.set_data(self._interface.get_data())

    def step(self):
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

            # Read and display the address and data
            self._display.set_address(self._interface.get_address())
            self._display.set_data(self._interface.get_data())

            # Set Mode on dipslay
            self._display.set_mode("STEP")

            self._panel_mode = STEP

    def set_readwrite_address_from_user_input(self):
        """
        Attempt to set the readwrite address from the user input.

        Nothing happens if the user input is invalid.

        If the user input is valid, that new address is set, and the
        word at the new address read and displayed.
        """

        if self._panel_mode != STOP:
            return

        if not self._is_valid_address(self._user_input_string):
            return

        self._readwrite_address = int(self._user_input_string)
        self._display.set_address(self._readwrite_address)
        self._display.set_data(self._get_word(self._readwrite_address))

    def incr_readwrite_address(self):
        """
        Increment the current readwrite address by one.

        If the value is at the max, wrap back to zero.
        """
        
        if self._panel_mode != STOP:
            return

        # Increment, wrapping if necessary
        self._readwrite_address += 1
        if self._readwrite_address > _MAX_VALUE:
            self._readwrite_address = 0

        self._display.set_address(self._readwrite_address)
        self._display.set_data(self._get_word(self._readwrite_address))

    def decr_readwrite_address(self):
        """
        Decrement the current readwrite address by one.

        If the value goes below zero, wrap back to the max
        """
        
        if self._panel_mode != STOP:
            return

        # Decrement, wrapping if necessary
        self._readwrite_address -= 1
        if self._readwrite_address < 0:
            self._readwrite_address = _MAX_VALUE

        self._display.set_address(self._readwrite_address)
        self._display.set_data(self._get_word(self._readwrite_address))

    def run(self):
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

            # Set Mode on dipslay
            self._display.set_mode("RUN")

            self._panel_mode = RUN

    def set_word_from_user_input(self):
        """
        Set the word at the readwrite address from the current user
        input.
        """

        if self._panel_mode != STOP:
            return

        # Check user input is valid
        if not self._is_valid_word(self._user_input_string):
            return

        # Set word at current readwrite address
        self._set_word(self._readwrite_address, int(self._user_input_string))

        # Read word at readwrite address and set to display
        self._display.set_data(self._get_word(self._readwrite_address))

    def set_word_from_user_input_then_incr_addr(self):
        """
        Set word from user input, then increment readwrite addr.

        The readwrite addr will wrap if necessary
        """

        if self._panel_mode != STOP:
            return

        # Check user input is valid
        if not self._is_valid_word(self._user_input_string):
            return


        # Set word at current readwrite address
        self._set_word(self._readwrite_address, int(self._user_input_string))

        # Increment readwrite, wrapping if necessary
        self._readwrite_address += 1
        if self._readwrite_address > _MAX_VALUE:
            self._readwrite_address = 0

        self._display.set_address(self._readwrite_address)

        # Read word at readwrite address and set to display
        self._display.set_data(self._get_word(self._readwrite_address))

    def next_clock_source(self):
        """
        Cycle the clock source
        """

        # Cycle the clock source
        self._cpu_clock_source_index = (
            (self._cpu_clock_source_index + 1) % len(self._cpu_clock_sources)
        )
        self._cpu_clock_source = self._cpu_clock_sources[self._cpu_clock_source_index]

        self._update_frequency_display()

        # If running, do the switch
        if self._panel_mode == RUN:
            self._set_clock_source()

    def stop(self):
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

            # Set display to show current readwrite address
            self._display.set_address(self._readwrite_address)

            # Read word at readwrite address and set to display
            self._display.set_data(self._get_word(self._readwrite_address))

            # Set Mode on dipslay
            self._display.set_mode("STOP")

            self._panel_mode = STOP

    def next_program(self):
        """
        Cycle between the available programs
        """

        # Increment, wrapping to 0 if necessary
        self._program_index = (self._program_index + 1) % len(PROGRAMS)

        self._display.set_program_name(
            PROGRAMS[self._program_index]["name"][0:5]
        )

    def set_current_program(self):
        """
        Write the current program to memory
        """

        if self._panel_mode != STOP:
            return

        self._set_words(PROGRAMS[self._program_index]["content"])

    def set_frequency_from_user_input(self):
        """
        Set the clock frequency of the CPU (in Hz) from user input.

        Either sets the frequency immediately (when in run mode and with
        clock source set to panel) or saves the value for use later.
        """
        if not self._is_valid_frequency(self._user_input_string):
            return

        self._frequency = float(self._user_input_string)

        self._update_frequency_display()

        if (self._panel_mode == RUN and self._cpu_clock_source == FRONT_PANEL):
            self._interface.set_cpu_clock_input_enabled(False)
            self._interface.set_clock_pin_frequency(
                self._compensate_clock_frequency(self._frequency)
            )
            self._interface.set_cpu_clock_input_enabled(True)

    def set_reset(self, state):
        """
        Set state of the reset line for the CPU
        """
        if state:
            self._interface.set_reset(True)
        else:
            self._interface.set_reset(False)

    def propose_user_input_character(self, character):
        """

        """
        if character not in ".0123456789":
            return

        if len(self._user_input_string) >= 7:
            return

        self._user_input_string += character
        self._display.set_user_input(self._user_input_string)

    def clear_user_input(self):
        """

        """
        self._user_input_string = ""
        self._display.set_user_input(self._user_input_string)

    def delete_last_user_input_char(self):
        """

        """
        if len(self._user_input_string) > 1:
            self._user_input_string = self._user_input_string[:-1]
            self._display.set_user_input(self._user_input_string)

    def _set_clock_source(self):
        """
        Set the clock source for the CPU.

        No safe guards.
        """

        self._interface.set_cpu_clock_input_enabled(False)

        if self._cpu_clock_source == FRONT_PANEL:
            self._interface.set_cpu_clock_source(interface.MICROCONTROLLER)
            self._interface.set_clock_pin_frequency(
                self._compensate_clock_frequency(self._frequency)
            )
        if self._cpu_clock_source == CRYSTAL:
            self._interface.set_cpu_clock_source(interface.CRYSTAL)

        self._interface.set_cpu_clock_input_enabled(True)

    def _set_words(self, addresses_and_words):
        """
        Set a number of addresses and words at once.
        """
        if self._panel_mode == STOP:

            self._interface.set_read_from_mem(False)
            self._interface.set_write_to_mem(True)
            self._interface.set_interface_address_assert(True)
            self._interface.set_interface_data_assert(True)
            
            num_words = len(addresses_and_words)
            word = 1
            spinners = ["-", "\\", "|", "/"]
            spinner_index = 0
            num_spinners = len(spinners)
            
            for address, word in addresses_and_words:
                if word % 50 == 0:
                    self._display.set_user_input(spinners[spinner_index])
                    spinner_index = (spinner_index + 1) % num_spinners
                self._interface.set_address(address)
                self._interface.set_data(word)
                time.sleep_us(1)
                self._send_cpu_like_clock_cycle()
                time.sleep_us(1)

            self._interface.set_read_from_mem(False)
            self._interface.set_write_to_mem(False)
            self._interface.set_interface_address_assert(False)
            self._interface.set_interface_data_assert(False)
            
            self._display.set_user_input(self._user_input_string)

    def _at_beginning_of_clock_cycle(self):
        """
        Test whether the CPU is at the beginning of a clock cycle.

        This happens when the data clock is high (and so the control
        clock is low).

        Note that after a reset the clock is in the opposite state (i.e.
        control clock high). This may need accounting for if reset is
        pressed in stop mode.
        """

        return self._interface.get_data_clock()

    def _send_clock_pulses(self, num_pulses):
        """
        Send the specified number of clock pulses.
        """
        for _ in range(num_pulses):
            self._interface.set_clock_pin_static_state(True)
            time.sleep_us(1)
            self._interface.set_clock_pin_static_state(False)
            time.sleep_us(1)

    def _compensate_clock_frequency(self, frequency):
        """
        Adjust the clock frequency to account for the clock processing
        in the CPU.
        """

        return frequency * 2

    def _send_cpu_like_clock_cycle(self):
        """
        Create a clock cycle comparable to that genertaed by the CPU.
        """
        self._interface.set_control_clock(True)
        self._interface.set_data_clock(False)
        time.sleep_us(1)
        self._interface.set_control_clock(False)
        self._interface.set_data_clock(True)
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


            time.sleep_us(5)
            self._send_cpu_like_clock_cycle()
            time.sleep_us(5)

            self._interface.set_read_from_mem(False)
            self._interface.set_write_to_mem(False)
            self._interface.set_interface_address_assert(False)
            self._interface.set_interface_data_assert(False)

    def _get_word(self, address):
        """
        Get a word from the device on the data bus at the given address.
        """

        word = 0

        if self._panel_mode == STOP:
            self._interface.set_address(address)
            self._interface.set_read_from_mem(True)
            self._interface.set_interface_address_assert(True)

            time.sleep_us(10)
            word = self._interface.get_data()

            self._interface.set_read_from_mem(False)
            self._interface.set_interface_address_assert(False)

        return word

    def _is_valid_address(self, _address):
        """
        Check if the passed in address is valid
        """
        try:
            address = int(_address)
        except:
            return False

        if not (0 <= address <= _MAX_VALUE):
            return False

        return True

    def _is_valid_word(self, _word):
        """
        Check if the passed in word is valid
        """
        try:
            word = int(_word)
        except:
            return False

        if not (0 <= word <= _MAX_VALUE):
            return False

        return True

    def _is_valid_frequency(self, _frequency):
        """
        Check if the passed in frequency is valid
        """
        try:
            frequency = float(_frequency)
        except:
            return False

        if not (0.1 <= frequency <= 4000000.0):
            return False

        return True

    def _update_frequency_display(self):
        if self._cpu_clock_source == FRONT_PANEL:
            self._display.set_frequency_to_value(self._frequency)

        if self._cpu_clock_source == CRYSTAL:
            self._display.set_frequency_to_crystal()
