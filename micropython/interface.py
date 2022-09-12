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

# Clock sources
MICROCONTROLLER = 100
CRYSTAL = 101

# Clock pin modes
_STATIC = 200
_TIMER = 201
_PWM = 202

# Pieces of data that can be read from the computer
_DATA = 300
_ADDRESS = 301
_CONTROL_CLOCK = 302
_DATA_CLOCK = 303
_WTM = 304
_RFM = 305

# Sources for the data and control clocks, and read from/write to memory
# signals fed to the peripherals 
FRONT_PANEL = 400
CPU = 401


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
        self._write_to_mem = False
        self._read_write_mem_source = _FRONT_PANEL

        self._data_clock = False
        self._control_clock = False
        self._data_control_clock_source = _FRONT_PANEL

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
        self.  = Pin(
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

        self._clock_source = MICROCONTROLLER

        self._reset = False

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
            self._interface_data_assert = state
            self._shift_out()

    def set_cpu_data_assert(self, state):
        """
        Set whether the CPU should assert onto the data bus.
        """

        # Protect from CPU and interface  asserting onto the bus
        if not (self._interface_data_assert and state):
            self._cpu_data_assert = state
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

        # Protect from CPU and interface  asserting onto the bus
        if not (self._cpu_address_assert and state):
            self._interface_address_assert = state
            self._shift_out()

    def set_cpu_address_assert(self, state):
        """
        Set whether the CPU should assert onto the address bus.
        """

        # Protect from CPU and interface  asserting onto the bus
        if not (self._interface_address_assert and state):
            self._cpu_address_assert = state
            self._shift_out()

    def set_read_from_mem(self, state):
        """
        Set the state of the read from memory line.
        """
        self._read_from_mem = state
        self._shift_out()

    def set_write_to_mem(self, state):
        """
        Set the state of the write to memory line.
        """
        self._write_to_mem = state
        self._shift_out()

    def get_read_from_mem(self):
        """
        Get the state of the read from memory bus.
        """
        bus_states = self._shift_in()
        return bus_states[_RFM]

    def get_write_to_mem(self):
        """
        Get the state of the write to memory bus.
        """
        bus_states = self._shift_in()
        return bus_states[_WTM]

    def set_read_write_mem_source(self, source):
        """
        Set the source of the read and write memory lines fed to the
        peripherals.
        """

        self._read_write_mem_source = source
        self._shift_out()

    def get_data_clock(self):
        """
        Get the state of the data clock bus.
        """
        bus_states = self._shift_in()
        return bus_states[_DATA_CLOCK]

    def set_data_clock(self, state):
        """
        Set the state to assert onto the data clock bus.
        """
        self._data_clock = state
        self._shift_out()

    def get_control_clock(self):
        """
        Get the state of the control clock bus.
        """
        bus_states = self._shift_in()
        return bus_states[_CONTROL_CLOCK]

    def set_control_clock(self, state):
        """
        Set the state to assert onto the control clock bus.
        """
        self._control_clock = state
        self._shift_out()

    def set_control_data_clock_source(self, source):
        """
        Set the source of the control and data clocks.
        """
        self._control_data_clock_source = source
        self._shift_out()

    def set_cpu_clock_input_enabled(self, state):
        """
        Set whether the CPU clock input is enabled or not.
        """
        self._cpu_clock_input_enabled = state
        self._shift_out()

    def set_clock_source(self, source):
        """
        Set the source for the clock.
        """
        if source in (MICROCONTROLLER, CRYSTAL):
            self._source = source
        self._shift_out()

    def set_reset(self, state):
        """
        Set the state of the reset line.
        """
        self._reset = state
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
            self._pwm.freq(frequency)

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
         - SR4-2: Write to memory
         - SR4-3: Read from memory
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
        ret[_RFM] = self._shift_in_bit()
        ret[_WTM] = self._shift_in_bit()
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
         - SR4-2: Read from memory
         - SR4-3: Write to memory
         - SR4-4: Reset
         - SR4-5: CPU Clock source (Panel/crystal)
         - SR4-6: Data/control clock source
         - SR4-7: RFM/WTM source

         - SR5-0: Interface address bus assert
         - SR5-1: Interface data bus assert
         - SR5-2: CPU address bus assert
         - SR5-3: CPU data bus assert
         - SR5-4: <blank>
         - SR5-5: <blank>
         - SR5-6: <blank>
         - SR5-7: <blank>
        """

        # Convert the logical values here to the hardware values i.e.,
        # account for active low inputs on some of the chips.

        # Shift Register 5
        self._shift_bit_out(self._cpu_data_assert)
        self._shift_bit_out(self._cpu_address_assert)
        self._shift_bit_out(not self._interface_data_assert)
        self._shift_bit_out(not self._interface_address_assert)

        # Shift Register 4
        if self._read_write_mem_source == _FRONT_PANEL:
            self._shift_bit_out(False)
        else:
            self._shift_bit_out(True)
        if self._data_control_clock_source == _FRONT_PANEL:
            self._shift_bit_out(False)
        else:
            self._shift_bit_out(True)
        if self._clock_source == MICROCONTROLLER:
            self._shift_bit_out(False)
        else:
            self._shift_bit_out(True)
        self._shift_bit_out(self._reset)
        self._shift_bit_out(self._write_to_mem)
        self._shift_bit_out(self._read_from_mem)
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
        time.sleep_us(1)
        self._output_shift_clock_pin.value(True)
        time.sleep_us(1)
        self._output_shift_clock_pin.value(False)
        time.sleep_us(1)

    def _timer_callback(self, timer):
        """
        Timer callback for low frequency clocks
        """
        self._clock_pin.toggle()