"""
The low level hardware interface to the computer.
"""

from machine import Pin, PWM, Timer
import time

from gpiodefs import (
    INPUT_STORAGE_CLOCK_GPIO_NO,
    INPUT_PARALLEL_LOAD_GPIO_NO,
    INPUT_SHIFT_CLOCK_GPIO_NO,
    INPUT_SERIAL_READ_GPIO_NO,
    OUTPUT_SERIAL_OUT_GPIO_NO,
    OUTPUT_SHIFT_CLOCK_GPIO_NO,
    OUTPUT_OUTPUT_CLOCK_GPIO_NO,
    CPU_CLOCK_GPIO_NO,
)

# CPU_Clock sources
CPU_CLK_SRC_PANEL = 100
CPU_CLK_SRC_CRYSTAL = 101

# Clock pin modes
_STATIC = 200
_TIMER = 201
_PWM = 202

# Pieces of data that can be read from the computer
_DATA = 300
_ADDRESS = 301
_CONTROL_CLOCK = 302
_DATA_CLOCK = 303
_MEM_ACTIVE = 304
_RFM_WTM = 305

# Sources for the data and control clocks, and memory control
# signals fed to the peripherals 
PERIPH_CLK_SRC_PANEL = 400
PERIPH_CLK_SRC_CPU = 401
PERIPH_MEM_CTL_SRC_PANEL = 402
PERIPH_MEM_CTL_SRC_CPU = 403


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

        self._memory_active = False
        self._rfm_wtm = False
        self._mem_ctl_source = PERIPH_MEM_CTL_SRC_PANEL

        self._data_clock = False
        self._control_clock = False
        self._control_data_clock_source = PERIPH_CLK_SRC_PANEL

        self._cpu_clock_input_enabled = False

        self._clock_mode = _STATIC
        self._clock_pin = Pin(CPU_CLOCK_GPIO_NO, mode=Pin.OUT, value=False)
        self._pwm = PWM(self._clock_pin)
        self._pwm.deinit()
        self._clock_pin = Pin(CPU_CLOCK_GPIO_NO, mode=Pin.OUT, value=False)
        self._timer = Timer()

        # Pins to control shift registers that read the state of the
        # buses
        # Clocks in all 8 bits to an intermediate storage register (not
        #the shift register).
        self._input_storage_reg_clock_pin = Pin(
            INPUT_STORAGE_CLOCK_GPIO_NO, mode=Pin.OUT, value=False
        )
        # Loads the data from the intermediate storage register to the
        # shift register. Pin is active low.
        self._input_parallel_load_pin = Pin(
            INPUT_PARALLEL_LOAD_GPIO_NO, mode=Pin.OUT, value=True
        )
        # Moves each bit along one position in the shift register.
        self._input_shift_reg_clock_pin = Pin(
            INPUT_SHIFT_CLOCK_GPIO_NO, mode=Pin.OUT, value=False
        )
        # Used to read the shifted out bit from the last 74HC597.
        self._input_serial_read_pin = Pin(
            INPUT_SERIAL_READ_GPIO_NO, mode=Pin.IN, pull=Pin.PULL_DOWN
        )

        # Pins to control shift registers that assert onto the buses
        # Outputs a bit to be shifted into the shift registers.
        self._output_serial_out_pin = Pin(
            OUTPUT_SERIAL_OUT_GPIO_NO, mode=Pin.OUT, value=False
        )
        # Shifts all the bits in the shift registers along one place.
        self._output_shift_clock_pin = Pin(
            OUTPUT_SHIFT_CLOCK_GPIO_NO, mode=Pin.OUT, value=False
        )
        # Transfers all the bits in the shift registers to the output
        # register.
        self._output_output_clock_pin = Pin(
            OUTPUT_OUTPUT_CLOCK_GPIO_NO, mode=Pin.OUT, value=False
        )

        self._cpu_clock_source = CPU_CLK_SRC_PANEL

        self._reset_to_cpu = False
        self._reset_to_peripherals = False

        self._shift_out()

    def set_data(self, data):
        """
        Set the data to be output to the data bus.
        """

        # Clamp data to 16 bit value
        if data < 0:
            data = 0
        if data > 65535:
            data = 65535

        self._data = data
        self._shift_out()

    def get_data(self):
        """
        Get the data currently on the data bus.
        """
        bus_states = self._shift_in()
        return bus_states[_DATA]

    def set_interface_data_assert(self, state):
        """
        Set whether the interface should assert onto the data bus.
        """

        # Protect from CPU and interface  asserting onto the bus
        if not (self._cpu_data_assert and state):
            self._interface_data_assert = bool(state)
            self._shift_out()

    def set_cpu_data_assert(self, state):
        """
        Set whether the CPU should assert onto the data bus.
        """

        # Protect from CPU and interface  asserting onto the bus
        if not (self._interface_data_assert and state):
            self._cpu_data_assert = bool(state)
            self._shift_out()

    def set_address(self, address):
        """
        Set the address to put on the address bus.
        """

        # Clamp address to 16 bit value
        if address < 0:
            address = 0
        if address > 65535:
            address = 65535

        self._address = address
        self._shift_out()

    def get_address(self):
        """
        Get the address currently on the address bus.
        """
        bus_states = self._shift_in()
        return bus_states[_ADDRESS]

    def set_interface_address_assert(self, state):
        """
        Set whether the interface should assert onto the address bus.
        """

        # Protect from CPU and interface asserting onto the bus
        if not (self._cpu_address_assert and state):
            self._interface_address_assert = bool(state)
            self._shift_out()

    def set_cpu_address_assert(self, state):
        """
        Set whether the CPU should assert onto the address bus.
        """

        # Protect from CPU and interface  asserting onto the bus
        if not (self._interface_address_assert and state):
            self._cpu_address_assert = bool(state)
            self._shift_out()

    def get_memory_active(self):
        """
        Get the state of the memory active line.

        Returns:
            bool: The state of the memory active line.
        """
        bus_states = self._shift_in()
        return bus_states[_MEM_ACTIVE]

    def set_memory_active(self, state):
        """
        Set the state of the memory active line.

        Args:
            state (bool): The logic value to set the line to.
        """

        self._memory_active = bool(state)
        self._shift_out()

    def get_rfm_wtm(self):
        """
        Get the state of the RFM/WTM line.

        A low level on the line is reading from memory, a high is
        writing to it.

        Returns:
            bool: The state of the RFM/WTM line.
        """
        bus_states = self._shift_in()
        return bus_states[_RFM_WTM]

    def set_rfm_wtm(self, state):
        """
        Set the state of the RFM/WTM line.

        A low level on the line is reading from memory, a high is
        writing to it.

        Args:
            state (bool): The logic value to set the line to.
        """

        self._rfm_wtm = bool(state)
        self._shift_out()

    def set_peripheral_mem_ctl_source(self, source):
        """
        Set the source of the read and write memory lines fed to the
        peripherals.
        """
        if source in (PERIPH_MEM_CTL_SRC_PANEL, PERIPH_MEM_CTL_SRC_CPU):
            self._mem_ctl_source = source
            self._shift_out()

    def get_data_clock(self):
        """
        Get the state of the data clock from the CPU.
        """
        bus_states = self._shift_in()
        return bus_states[_DATA_CLOCK]

    def set_data_clock(self, state):
        """
        Set the state of the data clock to send to the peripherals.

        This will only reach the peripherals if the clock source is set
        to the front panel.
        """
        self._data_clock = bool(state)
        self._shift_out()

    def get_control_clock(self):
        """
        Get the state of the control clock from the CPU.
        """
        bus_states = self._shift_in()
        return bus_states[_CONTROL_CLOCK]

    def set_control_clock(self, state):
        """
        Set the state of the control clock to send to the peripherals.

        This will only reach the peripherals if the clock source is set
        to the front panel.
        """
        self._control_clock = bool(state)
        self._shift_out()

    def set_data_and_control_clocks(self, data_state, control_state):
        """
        Set the state of the control and data clocks to send to the
        peripherals.

        This will only reach the peripherals if the clock source is set
        to the front panel.
        """
        self._data_clock = bool(data_state)
        self._control_clock = bool(control_state)
        self._shift_out()

    def set_peripheral_clock_source(self, source):
        """
        Set the source of the control and data clocks for the
        peripherals.
        """
        if source in (PERIPH_CLK_SRC_PANEL, PERIPH_CLK_SRC_CPU):
            self._control_data_clock_source = source
            self._shift_out()

    def set_cpu_clock_input_enabled(self, state):
        """
        Set whether the CPU clock input is enabled or not.
        """
        self._cpu_clock_input_enabled = bool(state)
        self._shift_out()

    def set_cpu_clock_source(self, source):
        """
        Set the source for the clock.
        """
        if source in (CPU_CLK_SRC_PANEL, CPU_CLK_SRC_CRYSTAL):
            self._cpu_clock_source = source
            self._shift_out()

    def set_reset_to_cpu(self, state):
        """
        Set the state of the reset line going to the CPU.
        """
        self._reset_to_cpu = bool(state)
        self._shift_out()

    def set_reset_to_peripherals(self, state):
        """
        Set the state of the reset line going to the peripherals.
        """
        self._reset_to_peripherals = bool(state)
        self._shift_out()

    def set_clock_pin_static_state(self, state):
        """
        Set the clock pin to a static state
        """

        # Disable the timer if is't currently active
        if self._clock_mode == _TIMER:
            self._timer.deinit()

        # Disable the PWM if it's currently active and reset the pin
        # object
        if self._clock_mode == _PWM:
            self._pwm.deinit()
            self._clock_pin = Pin(
                CPU_CLOCK_GPIO_NO, mode=Pin.OUT, value=False
            )

        # Set the pin to the desired state
        self._clock_pin.value(state)
        self._clock_mode = _STATIC

    def set_clock_pin_frequency(self, frequency):
        """
        Set the clock pin to a certain frequency.
        """

        # If the frequency is low
        if frequency < 10:
            # Disable the PWM if it's active and reset the clock pin.
            if self._clock_mode == _PWM:
                self._pwm.deinit()
                self._clock_pin = Pin(
                    CPU_CLOCK_GPIO_NO, mode=Pin.OUT, value=False
                )

            # We were either in static or timer mode so just
            # re-init the timer.
            self._timer.init(
                # Need to double the frequency as the callback only
                # toogles the state
                freq=frequency * 2,
                mode=Timer.PERIODIC,
                callback=self._timer_callback
            )

            self._clock_mode = _TIMER

        # Otherwise the frequency is high
        else:
            if self._clock_mode == _TIMER:
                self._timer.deinit()
                self._pwm = PWM(self._clock_pin)

            if self._clock_mode == _STATIC:
                self._pwm = PWM(self._clock_pin)

            self._pwm.duty_u16(32768)
            self._pwm.freq(int(frequency))

            self._clock_mode = _PWM

    def _shift_in(self):
        """
        Shift in the state of the buses

        The data for each shift register is:

         - SR0: Address 15-8

         - SR1: Address 7-0

         - SR2: Data 15-8

         - SR3: Data 7-0

         - SR4-0: Control clock
         - SR4-1: Data clock
         - SR4-2: Read from memory
         - SR4-3: Write to memory
         - SR4-4: <blank>
         - SR4-5: <blank>
         - SR4-6: <blank>
         - SR4-7: <blank>
        """

        # Capture the state of the pins
        self._input_storage_reg_clock_pin.value(True)
        time.sleep_us(1)
        self._input_storage_reg_clock_pin.value(False)
        time.sleep_us(1)

        # Load it into the shift register (pin is active low)
        self._input_parallel_load_pin.value(False)
        time.sleep_us(1)
        self._input_parallel_load_pin.value(True)
        time.sleep_us(1)

        ret = {}

        # Shift past the last 4 bits in SR4
        self._shift_in_bit()
        self._shift_in_bit()
        self._shift_in_bit()
        self._shift_in_bit()

        # Get the first 4 bits of SR4
        ret[_RFM_WTM] = self._shift_in_bit()
        ret[_MEM_ACTIVE] = self._shift_in_bit()
        ret[_DATA_CLOCK] = self._shift_in_bit()
        ret[_CONTROL_CLOCK] = self._shift_in_bit()

        # Get SR3 then SR2 which make up the data bus
        data = 0 
        for i in range(16):
            data |= self._shift_in_bit() << i
        ret[_DATA] = data

        # Get SR1 then SR0 which make up the address bus
        address = 0 
        for i in range(16):
            address |= self._shift_in_bit() << i
        ret[_ADDRESS] = address

        return ret

    def _shift_in_bit(self):
        """
        Shift in a single bit.
        """

        ret = self._input_serial_read_pin.value()
        time.sleep_us(1)
        self._input_shift_reg_clock_pin.value(True)
        time.sleep_us(1)
        self._input_shift_reg_clock_pin.value(False)
        time.sleep_us(1)

        return bool(ret)

    def _shift_out(self):
        """
        Shift out the control signals.

        The data for each shift register is:

         - SR0: Address 15-8

         - SR1: Address 7-0

         - SR2: Data 15-8

         - SR3: Data 7-0

         - SR4-0: Control clock
         - SR4-1: Data clock
         - SR4-2: Memory active
         - SR4-3: RFM/WTM
         - SR4-4: Control/data clock source
         - SR4-5: Memory control source
         - SR4-6: Interface address bus assert
         - SR4-7: Interface data bus assert

         - SR5-0: Reset to CPU
         - SR5-1: CPU clock input enable
         - SR5-2: CPU clock source (Panel/crystal)
         - SR5-3: CPU address bus assert
         - SR5-4: CPU data bus assert
         - SR5-5: Reset to peripherals
         - SR5-6: <blank>
         - SR5-7: <blank>
        """

        # Shift Register 5
        self._shift_bit_out(self._reset_to_peripherals)
        self._shift_bit_out(self._cpu_data_assert)
        self._shift_bit_out(self._cpu_address_assert)
        if self._cpu_clock_source == CPU_CLK_SRC_PANEL:
            self._shift_bit_out(False)
        else:
            self._shift_bit_out(True)
        self._shift_bit_out(self._cpu_clock_input_enabled)
        self._shift_bit_out(self._reset_to_cpu)
        
        # Shift Register 4
        self._shift_bit_out(not self._interface_data_assert)
        self._shift_bit_out(not self._interface_address_assert)
        if self._mem_ctl_source == PERIPH_MEM_CTL_SRC_PANEL:
            self._shift_bit_out(False)
        else:
            self._shift_bit_out(True)
        if self._control_data_clock_source == PERIPH_CLK_SRC_PANEL:
            self._shift_bit_out(False)
        else:
            self._shift_bit_out(True)
        self._shift_bit_out(self._rfm_wtm)
        self._shift_bit_out(self._memory_active)
        self._shift_bit_out(self._data_clock)
        self._shift_bit_out(self._control_clock)

        # Shift Register 3
        for i in range(8):
            self._shift_bit_out(1 & self._data >> i)

        # Shift Register 2
        for i in range(8, 16):
            self._shift_bit_out(1 & self._data >> i)

        # Shift Register 1
        for i in range(8):
            self._shift_bit_out(1 & self._address >> i)

        # Shift Register 0
        for i in range(8, 16):
            self._shift_bit_out(1 & self._address >> i)
        
        # Output all the shifted in bits.
        self._output_output_clock_pin.value(True)
        time.sleep_us(1)
        self._output_output_clock_pin.value(False)
        time.sleep_us(1)

    def _shift_bit_out(self, bit):
        """
        Shift out a single bit.

        This doesn't latch it into the output register though.
        """
        self._output_serial_out_pin.value(bit)
        # time.sleep_us(1)
        self._output_shift_clock_pin.value(True)
        # time.sleep_us(1)
        self._output_shift_clock_pin.value(False)
        # time.sleep_us(1)

    def _timer_callback(self, timer):
        """
        Timer callback for low frequency clocks
        """
        self._clock_pin.toggle()
