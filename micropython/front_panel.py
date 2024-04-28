import time
import asyncio

import interface
from outcome import Outcome
from programs import PROGRAMS
from constants import PANEL_MODE_STEP as STEP
from constants import PANEL_MODE_RUN as RUN
from constants import PANEL_MODE_STOP as STOP
from constants import PANEL_MODE_READ_MEMORY as READ_MEMORY
from constants import (
    CPU_CLK_SRC_CRYSTAL,
    CPU_CLK_SRC_PANEL,
    PERIPH_CLK_SRC_PANEL,
    PERIPH_CLK_SRC_CPU,
    PERIPH_MEM_CTL_SRC_PANEL,
    PERIPH_MEM_CTL_SRC_CPU,
)

# # The current mode the panel is in
# # Allows single stepping of the CPU. The CPU is in full control
# # of the peripherals.
# STEP = 100

# # Running at a given frequency. The CPU is in full control of the
# # peripherals.
# RUN = 101

# # The CPU is stopped. Control of peripherals is given to the panel.
# STOP = 102

# # The memory can be read manually
# READ_MEMORY = 103


# # The clock source for the CPU 
# CPU_CLK_SRC_PANEL = 200
# CPU_CLK_SRC_CRYSTAL = 201

# Maximum 16 bit value
_MAX_VALUE = 2**16 - 1

class FrontPanel():
    """
    The user facing interface to the computer.

    Almost all the methods are async because they update the display,
    which needs to send data over the network if a client is connected.
    """

    def __init__(self):
        """
        Initialise the class.
        """

        self._cpu_clock_sources = [
            CPU_CLK_SRC_PANEL,
            CPU_CLK_SRC_CRYSTAL,
        ]
        self._cpu_clock_source_index = 0
        self._cpu_clock_source = self._cpu_clock_sources[self._cpu_clock_source_index]
        self._program_index = 0
        self._frequency = 10
        self._readwrite_address = 0
        self._user_input_string = ""
        self._interface = interface.Interface()
        self._display_ref = None
        self._panel_mode = RUN

    async def initialise(self):
        """
        Initialise the Panel.

        Can't be done in __init__ because calling async in there is ...
        problematic.

        https://stackoverflow.com/questions/33128325/how-to-set-class-attribute-with-await-in-init
        """
        await self._display_ref.set_frequency(self._frequency)
        await self._display_ref.set_cpu_clock_source(
            self._cpu_clock_sources[self._cpu_clock_source_index]
        )
        await self._display_ref.set_program(self._program_index)
        await self.set_mode_to_stop()
        await self.set_reset(True)
        await asyncio.sleep(1)
        await self.set_reset(False)

    def set_display_ref(self, display):
        """
        Set the panels reference to the display

        Args:
            display (Display): Reference to the display held by the
                manager.
        """
        self._display_ref=display

    async def half_steps(self, num_steps=1):
        """
        Advance the CPU by the given number of half steps.

        Keyword Args:
            num_steps (int): The number of half steps to advance by.
        """
        if self._panel_mode != STEP:
            return Outcome(
                False,
                msg="Cannot step when not in step mode."
            )

        self._send_clock_pulses(num_steps)

        # Read and display the address and data
        await self._display_ref.set_address(self._interface.get_address())
        await self._display_ref.set_data(self._interface.get_data())

        return Outcome(True)

    async def full_steps(self, num_steps=1):
        """
        Advance the CPU by the given number of full steps.

        Keyword Args:
            num_steps (int): The number of full steps to advance by.
        """

        if self._panel_mode != STEP:
            return Outcome(
                False,
                msg="Cannot step when not in step mode."
            )

        self._send_clock_pulses(num_steps * 2)

        # Read and display the address and data
        await self._display_ref.set_address(self._interface.get_address())
        await self._display_ref.set_data(self._interface.get_data())

        return Outcome(True)

    async def set_mode_to_step(self):
        """
        Puts the panel into step mode.
        """

        if self._panel_mode != STEP:
            # Disable any output onto the address and data buses from
            # the interface
            self._interface.set_interface_data_assert(False)
            self._interface.set_interface_address_assert(False)

            # Set the source of the control and data clocks, and the
            # memory control lines for the peripherals to the CPU
            self._interface.set_peripheral_clock_source(PERIPH_CLK_SRC_CPU)
            self._interface.set_peripheral_mem_ctl_source(PERIPH_MEM_CTL_SRC_CPU)

            # Allow CPU to assert onto the buses.
            self._interface.set_cpu_data_assert(True)
            self._interface.set_cpu_address_assert(True)

            # Disable the clock on the CPU
            self._interface.set_cpu_clock_input_enabled(False)

            # Make sure the CPU gets clock pulses from the
            # microcontroller
            self._interface.set_cpu_clock_source(CPU_CLK_SRC_PANEL)

            # Set the interface clock pin to a static state, ready for
            # stepping.
            self._interface.set_clock_pin_static_state(False)

            # Enable the clock on the CPU
            self._interface.set_cpu_clock_input_enabled(True)

            # Read and display the address and data
            await self._display_ref.set_address(self._interface.get_address())
            await self._display_ref.set_data(self._interface.get_data())

            # Set Mode on dipslay
            await self._display_ref.set_run_mode(STEP)

            self._panel_mode = STEP
            return Outcome(True)

        else:
            return Outcome(False, msg="Panel is already in step mode")

    async def set_readwrite_address_from_user_input(self):
        """
        Attempt to set the readwrite address from the user input.

        Nothing happens if the user input is invalid.

        If the user input is valid, that new address is set, and the
        word at the new address read and displayed.
        """

        if self._panel_mode != STOP:
            return Outcome(False)

        if not self._is_valid_address(self._user_input_string):
            return Outcome(False)

        self._readwrite_address = int(self._user_input_string)
        await self._display_ref.set_address(self._readwrite_address)
        await self._display_ref.set_data(self._get_word(self._readwrite_address))
        return Outcome(True)

    async def incr_readwrite_address(self):
        """
        Increment the current readwrite address by one.

        If the value is at the max, wrap back to zero.
        """
        
        if self._panel_mode != STOP:
            return Outcome(False, msg="Can only increment head in stop mode.")

        # Increment, wrapping if necessary
        self._readwrite_address += 1
        if self._readwrite_address > _MAX_VALUE:
            self._readwrite_address = 0

        await self._display_ref.set_address(self._readwrite_address)
        await self._display_ref.set_data(self._get_word(self._readwrite_address))
        return Outcome(True)

    async def decr_readwrite_address(self):
        """
        Decrement the current readwrite address by one.

        If the value goes below zero, wrap back to the max
        """
        
        if self._panel_mode != STOP:
            return Outcome(False, msg="Can only decrement head in stop mode.")

        # Decrement, wrapping if necessary
        self._readwrite_address -= 1
        if self._readwrite_address < 0:
            self._readwrite_address = _MAX_VALUE

        await self._display_ref.set_address(self._readwrite_address)
        await self._display_ref.set_data(self._get_word(self._readwrite_address))
        return Outcome(True)

    async def set_mode_to_run(self):
        """
        Put the panel into run mode.
        """
        if self._panel_mode != RUN:
            # Disable any output onto the address and data buses from
            # the interface
            self._interface.set_interface_data_assert(False)
            self._interface.set_interface_address_assert(False)

            # Set the source of the control and data clocks, and the
            # memory control lines for the peripherals to the CPU
            self._interface.set_peripheral_clock_source(PERIPH_CLK_SRC_CPU)
            self._interface.set_peripheral_mem_ctl_source(PERIPH_MEM_CTL_SRC_CPU)

            # Allow CPU to assert onto the buses.
            self._interface.set_cpu_data_assert(True)
            self._interface.set_cpu_address_assert(True)

            # Disable the clock on the CPU
            self._interface.set_cpu_clock_input_enabled(False)

            # Set the clock source for the CPU
            self._set_clock_source()

            # Enable the clock on the CPU
            self._interface.set_cpu_clock_input_enabled(True)

            # Set Mode on dipslay
            await self._display_ref.set_run_mode(RUN)

            self._panel_mode = RUN
            return Outcome(True)
        else:
            return Outcome(False, msg="Panel already in run mode.")

    async def set_word_from_user_input(self):
        """
        Set the word at the readwrite address from the current user
        input.
        """

        if self._panel_mode != STOP:
            return Outcome(False)

        # Check user input is valid
        if not self._is_valid_word(self._user_input_string):
            return Outcome(False)

        # Set word at current readwrite address
        self._set_word(self._readwrite_address, int(self._user_input_string))

        # Read word at readwrite address and set to display
        await self._display_ref.set_data(self._get_word(self._readwrite_address))

    async def set_word_from_user_input_then_incr_addr(self):
        """
        Set word from user input, then increment readwrite addr.

        The readwrite addr will wrap if necessary
        """

        if self._panel_mode != STOP:
            return Outcome(False)

        # Check user input is valid
        if not self._is_valid_word(self._user_input_string):
            return Outcome(False)

        # Set word at current readwrite address
        self._set_word(self._readwrite_address, int(self._user_input_string))

        # Increment readwrite, wrapping if necessary
        self._readwrite_address += 1
        if self._readwrite_address > _MAX_VALUE:
            self._readwrite_address = 0

        await self._display_ref.set_address(self._readwrite_address)

        # Read word at readwrite address and set to display
        await self._display_ref.set_data(self._get_word(self._readwrite_address))

        return Outcome(True)

    async def next_clock_source(self):
        """
        Cycle to the next clock source
        """

        # Cycle the clock source
        self._cpu_clock_source_index = (
            (self._cpu_clock_source_index + 1) % len(self._cpu_clock_sources)
        )
        self._cpu_clock_source = self._cpu_clock_sources[self._cpu_clock_source_index]

        await self._display_ref.set_cpu_clock_source(self._cpu_clock_source)

        # If running, do the switch
        if self._panel_mode == RUN:
            self._interface.set_cpu_clock_input_enabled(False)
            self._set_clock_source()
            self._interface.set_cpu_clock_input_enabled(True)

        return Outcome(True)

    async def set_mode_to_stop(self):
        """
        Put the panel into stop mode.
        """
        if self._panel_mode != STOP:
            # Disable the clock on the CPU
            self._interface.set_cpu_clock_input_enabled(False)

            # Set the CPU to get clock pulses from the microcontroller
            self._interface.set_cpu_clock_source(CPU_CLK_SRC_PANEL)

            # Set the interface clock pin to a static state, ready for
            # stepping.
            self._interface.set_clock_pin_static_state(False)

            # Enable the clock on the CPU
            self._interface.set_cpu_clock_input_enabled(True)

            # Advance the clock so control clock is high
            while not self._at_beginning_of_clock_cycle():
                self._send_clock_pulses(1)

            # Disable the clock on the CPU
            self._interface.set_cpu_clock_input_enabled(False)

            # Disable the CPU from asserting onto the buses.
            self._interface.set_cpu_data_assert(False)
            self._interface.set_cpu_address_assert(False)

            # Disable interface from asserting onto the data or address bus
            self._interface.set_interface_data_assert(False)
            self._interface.set_interface_address_assert(False)

            # Set the control clock high, data clock low, memory active low,
            # and memory direction to read.
            self._interface.set_control_clock(True)
            self._interface.set_data_clock(False)
            self._interface.set_memory_active(False)
            self._interface.set_rfm_wtm(False)

            # Set the source of the control and data clocks, and the
            # memory control lines for the peripherals to the Panel
            self._interface.set_peripheral_mem_ctl_source(
                PERIPH_MEM_CTL_SRC_PANEL
            )
            self._interface.set_peripheral_clock_source(
                PERIPH_CLK_SRC_PANEL
            )

            # Set display to show current readwrite address
            await self._display_ref.set_address(self._readwrite_address)

            # Read word at readwrite address and set to display
            await self._display_ref.set_data(self._get_word(self._readwrite_address))

            # Set Mode on dipslay
            await self._display_ref.set_run_mode(STOP)

            self._panel_mode = STOP
            return Outcome(True)
        else:
            return Outcome(False, msg="Panel is already in stop mode.")

    async def next_program(self):
        """
        Cycle between the available programs
        """

        # Increment, wrapping to 0 if necessary
        self._program_index = (self._program_index + 1) % len(PROGRAMS)

        await self._display_ref.set_program(self._program_index)
        return Outcome(True)

    async def load_current_program(self):
        """
        Write the current program to memory
        """

        if self._panel_mode != STOP:
            return Outcome(False, msg="Can only load program in stop mode")

        await self.set_words(PROGRAMS[self._program_index]["data"])
        return Outcome(True)

    async def set_frequency_from_user_input(self):
        """
        Set the clock frequency of the CPU (in Hz) from user input.

        Either sets the frequency immediately (when in run mode and with
        clock source set to panel) or saves the value for use later.
        """
        if not self._is_valid_frequency(self._user_input_string):
            return Outcome(False)

        self._frequency = float(self._user_input_string)

        await self._display_ref.set_frequency(self._frequency)

        if (self._panel_mode == RUN and self._cpu_clock_source == CPU_CLK_SRC_PANEL):
            self._interface.set_cpu_clock_input_enabled(False)
            self._interface.set_clock_pin_frequency(
                self._compensate_clock_frequency(self._frequency)
            )
            self._interface.set_cpu_clock_input_enabled(True)

        return Outcome(True)

    async def set_reset(self, state):
        """
        Set state of the reset lines for the CPU and peripherals.
        """
        self._interface.set_reset_to_cpu(state)
        self._interface.set_reset_to_peripherals(state)

    async def propose_user_input_character(self, character):
        """
        Propose a character to add to the user input.
        """
        if character not in ".0123456789":
            return Outcome(False)

        if len(self._user_input_string) >= 7:
            return Outcome(False)

        self._user_input_string += character
        await self._display_ref.set_user_input(self._user_input_string)
        return Outcome(True)

    async def clear_user_input(self):
        """
        Clear the user input.
        """
        self._user_input_string = ""
        await self._display_ref.set_user_input(self._user_input_string)
        return Outcome(True)

    async def delete_last_user_input_char(self):
        """
        Delete the last character of the user input.
        """
        if len(self._user_input_string) >= 1:
            self._user_input_string = self._user_input_string[:-1]
            await self._display_ref.set_user_input(self._user_input_string)
            return Outcome(True)
        else:
            return Outcome(False)

    async def set_words(self, addresses_and_words):
        """
        Set a number of addresses and words at once.

        Args:
            addresses_and_words (tuple(tuple(int, int))): List of pairs
                of addresses and words.
        """
        if self._panel_mode != STOP:
            return Outcome(
                False,
                msg="Can only set words when panel is in stop mode"
            )

        self._interface.set_memory_active(True)
        self._interface.set_rfm_wtm(True)
        self._interface.set_interface_address_assert(True)
        self._interface.set_interface_data_assert(True)
        
        num_words = len(addresses_and_words)
        word = 1
        spinners = ["-", "\\", "|", "/"]
        spinner_index = 0
        num_spinners = len(spinners)
        
        current_word = 1
        last_percentage = 0
        for address, word in addresses_and_words:
            if word % 50 == 0:
                percentage = int((current_word / num_words) * 100)
                if percentage > last_percentage + 10:
                    last_percentage += 10
                status_update = "{spinner} - {last_percentage}%".format(
                    spinner=spinners[spinner_index],
                    last_percentage=last_percentage
                )
                await self._display_ref.set_user_input(status_update)
                spinner_index = (spinner_index + 1) % num_spinners
            current_word += 1
            self._interface.set_address(address)
            self._interface.set_data(word)
            time.sleep_us(1)
            self._send_cpu_like_clock_cycle()
            time.sleep_us(1)

        self._interface.set_memory_active(False)
        self._interface.set_interface_address_assert(False)
        self._interface.set_interface_data_assert(False)
        
        await self._display_ref.set_user_input(self._user_input_string)
        await self._display_ref.set_data(self._get_word(self._readwrite_address))

        return Outcome(True)

    async def set_mode_to_read_memory(self):
        """
        Put the computer into a state where memory can be read manually.

        Expects something to be setting values on the address bus, data
        will be presented on the data bus.
        """

        if self._panel_mode != READ_MEMORY:
            # Stop computer first
            await self.set_mode_to_stop()

            # Set memory control lines so mem is active and we're reading
            self._interface.set_memory_active(True)
            self._interface.set_rfm_wtm(False)

            # Set Mode on dipslay
            await self._display_ref.set_run_mode(READ_MEMORY)

            # Set the panel mode
            self._panel_mode = READ_MEMORY
            return True
        else:
            return Outcome(False, msg="Panel is already in Read Memory mode")

    def _set_clock_source(self):
        """
        Set the clock source for the CPU.

        No safe guards.
        """

        if self._cpu_clock_source == CPU_CLK_SRC_PANEL:
            self._interface.set_cpu_clock_source(CPU_CLK_SRC_PANEL)
            self._interface.set_clock_pin_frequency(
                self._compensate_clock_frequency(self._frequency)
            )
        if self._cpu_clock_source == CPU_CLK_SRC_CRYSTAL:
            self._interface.set_cpu_clock_source(CPU_CLK_SRC_CRYSTAL)

    def _at_beginning_of_clock_cycle(self):
        """
        Test whether the CPU is at the beginning of a clock cycle.

        This happens when the data clock is low and the control
        clock is high.
        """

        print("Dont forget to revert _at_beginning_of_clock_cycle!")
        return True
        # return self._interface.get_control_clock()

    def _send_clock_pulses(self, num_pulses):
        """
        Send the specified number of clock pulses to the CPU.
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
        Create a clock cycle comparable to that generated by the CPU.
        """
        
        self._interface.set_data_and_control_clocks(True, False)
        time.sleep_us(1)
        self._interface.set_data_and_control_clocks(False, True)
        time.sleep_us(1)

    def _set_word(self, address, word):
        """
        Set a word on the device on the data bus at the given address.
        """
        if self._panel_mode == STOP:
            self._interface.set_address(address)
            self._interface.set_data(word)
            self._interface.set_memory_active(True)
            self._interface.set_rfm_wtm(True)
            self._interface.set_interface_address_assert(True)
            self._interface.set_interface_data_assert(True)

            time.sleep_us(1)
            self._send_cpu_like_clock_cycle()
            time.sleep_us(1)

            self._interface.set_memory_active(False)
            self._interface.set_interface_address_assert(False)
            self._interface.set_interface_data_assert(False)

    def _get_word(self, address):
        """
        Get a word from the device on the data bus at the given address.
        """

        word = 0

        if self._panel_mode == STOP:
            self._interface.set_address(address)
            self._interface.set_memory_active(True)
            self._interface.set_rfm_wtm(False)
            self._interface.set_interface_address_assert(True)

            time.sleep_us(1)
            word = self._interface.get_data()

            self._interface.set_memory_active(False)
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