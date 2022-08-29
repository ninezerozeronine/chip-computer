"""
The low level hardware interface to the computer.
"""

from machine import Pin, PWM, Timer

MICROCONTROLLER = 100
CRYSTAL = 101

_STATIC = 200
_TIMER = 201
_PWM = 202

_DATA_BUS = 300
_ADDRESS_BUS = 301
_CONTROL_CLOCK_BUS = 302
_DATA_CLOCK_BUS = 303
_WTM_BUS = 304
_RFM_BUS = 305

_CPU_CLOCK_PIN_NO = 25

_BUS_IN_INPUT_REG_CLOCK_PIN_NO = 1
_BUS_IN_PARALLEL_LOAD_PIN_NO = 2
_BUS_IN_SHIFT_CLOCK_PIN_NO = 4
_BUS_IN_SERIAL_READ_PIN_NO = 5

_BUS_OUT_SERIAL_IN_PIN_NO = 6
_BUS_OUT_SHIFT_CLOCK_PIN_N0 = 7
_BUS_OUT_OUTPUT_REG_CLOCK_PIN_NO = 9


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
        self._interface_read_write_mem_assert = False
        self._cpu_read_write_mem_assert = False

        self._data_clock = False
        self._control_clock = False
        self._interface_clock_bus_assert = False
        self._cpu_clock_bus_assert = False

        self._cpu_clock_input_enabled = False

        self._clock_mode = _STATIC
        self._clock_pin = Pin(_CPU_CLOCK_PIN_NO, mode=Pin.OUT, value=False)
        self._pwm = PWM(self._clock_pin)
        self._pwm.deinit()
        self._clock_pin = Pin(_CPU_CLOCK_PIN_NO, mode=Pin.OUT, value=False)
        self._timer = Timer()

        # Pins to control shift registers that read the state of the buses
        self._bus_in_input_reg_clock_pin = Pin(
            _BUS_IN_INPUT_REG_CLOCK_PIN_NO, mode=Pin.OUT, value=False
        )
        self._bus_in_parallel_load_pin = Pin(
            _BUS_IN_PARALLEL_LOAD_PIN_NO, mode=Pin.OUT, value=True
        )
        self._bus_in_shift_clock_pin = Pin(
            _BUS_IN_SHIFT_CLOCK_PIN_NO, mode=Pin.OUT, value=False
        )
        self._bus_in_serial_read_pin = Pin(
            _BUS_IN_SERIAL_READ_PIN_NO, mode=Pin.IN, pull=Pin.PULL_DOWN
        )

        # Pins to control shift registers that assert onto the buses
        self._bus_out_serial_in_pin = Pin(
            _BUS_OUT_SERIAL_IN_PIN_NO, mode=Pin.OUT, value=False
        )
        self._bus_out_shift_clock_pin = Pin(
            _BUS_OUT_SHIFT_CLOCK_PIN_N0, mode=Pin.OUT, value=False
        )
        self._bus_out_output_reg_clock_pin = Pin(
            _BUS_OUT_OUTPUT_REG_CLOCK_PIN_NO, mode=Pin.OUT, value=False
        )

        self._clock_source = MICROCONTROLLER

        self._reset = False

        self._address_assert = False
        self._data_assert = False
        self._ctl_data_clks_assert = False
        self._wtm_rfm_assert = False

        self._shift_out()

    def set_data(self, data):
        """
        Set the data to be output to the data bus.
        """

        # Clamp data to 16 bit value
        if address < 0:
            address = 0
        if address > 65536:
            address = 65536

        self._data = data
        self._shift_out()

    def get_data(self):
        """
        Get the data currently on the data bus.
        """
        bus_states = self._shift_in()
        return bus_states[_DATA_BUS]

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
        if address > 65536:
            address = 65536

        self._address = address
        self._shift_out()

    def get_address(self):
        """
        Get the address currently on the address bus.
        """
        bus_states = self._shift_in()
        return bus_states[_ADDRESS_BUS]

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

    def get_read_from_mem(self):
        """
        Get the state of the read from memory bus.
        """
        bus_states = self._shift_in()
        return bus_states[_RFM_BUS]

    def get_write_to_mem(self):
        """
        Get the state of the write to memory bus.
        """
        bus_states = self._shift_in()
        return bus_states[_WTM_BUS]

    def set_interface_read_write_mem_assert(self, state):
        """
        Set whether the interface should assert onto the write to and
        read from memory buses.
        """

        # Protect from CPU and interface  asserting onto the bus
        if not (self._cpu_read_write_mem_assert and state):
            self._interface_read_write_mem_assert = state
            self._shift_out()

    def set_cpu_read_write_mem_assert(self, state):
        """
        Set whether the CPU should assert onto the write to and read
        from memory buses.
        """

        # Protect from CPU and interface  asserting onto the bus
        if not (self._interface_read_write_mem_assert and state):
            self._cpu_read_write_mem_assert = state
            self._shift_out()

    def get_data_clock(self):
        """
        Get the state of the data clock bus.
        """
        bus_states = self._shift_in()
        return bus_states[_DATA_CLOCK_BUS]

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
        return bus_states[_CONTROL_CLOCK_BUS]

    def set_control_clock(self, state):
        """
        Set the state to assert onto the control clock bus.
        """
        self._control_clock = state
        self._shift_out()

    def set_interface_clock_bus_assert(self, state):
        """
        Set whether the interface should assert onto the clock buses.
        """

        # Protect from CPU and interface  asserting onto the bus
        if not (self._cpu_clock_bus_assert and state):
            self._interface_clock_bus_assert = state
            self._shift_out()

    def set_cpu_clock_bus_assert(self, state):
        """
        Set whether the CPU should assert onto the clock buses.
        """

        # Protect from CPU and interface  asserting onto the bus
        if not (self._interface_clock_bus_assert and state):
            self._cpu_clock_bus_assert = state
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
                _CPU_CLOCK_PIN_NO, mode=Pin.OUT, value=False
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
                    _CPU_CLOCK_PIN_NO, mode=Pin.OUT, value=False
                )

            # We were either in static or timer mode so just
            # re-init the timer.
            self._timer.init(
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
        """

        return {}

    def _shift_out(self):
        """
        Shift out the control signals.

        The control signals on each shift register are:

         - SR0: Address 0-7
         - SR1: Address 8-15
         - SR2: Data 0-7
         - SR3: Data 8-15
         - SR4-0: Control clock
         - SR4-1: Data clock
         - SR4-2: Write to memory
         - SR4-3: Read from memory
         - SR4-4: Clock source
         - SR4-5: Reset
         - SR4-6: <blank>
         - SR4-7: <blank>
         - SR5-0: Interface address bus assert
         - SR5-1: Interface data bus assert
         - SR5-2: Interface clock bus asset
         - SR5-3: Interface RFM/WTM bus assert
         - SR5-4: CPU address bus assert
         - SR5-5: CPU data bus assert
         - SR5-6: CPU clock bus asset
         - SR5-7: CPU RFM/WTM bus assert
        """

        # Convert the logical values here to the hardware values i.e.,
        # account for active low inputs on some of the chips.

        # Shift Register 5
        self._shift_bit_out(self._cpu_read_write_mem_assert)
        self._shift_bit_out(self._cpu_clock_bus_assert)
        self._shift_bit_out(self._cpu_data_assert)
        self._shift_bit_out(self._cpu_address_assert)
        self._shift_bit_out(self._interface_read_write_mem_assert)
        self._shift_bit_out(self._interface_clock_bus_assert)
        self._shift_bit_out(not self._interface_data_assert)
        self._shift_bit_out(not self._interface_address_assert)

        # Shift Register 4
        self._shift_bit_out(False)
        self._shift_bit_out(False)
        self._shift_bit_out(self._reset)
        if self._clock_source == MICROCONTROLLER:
            self._shift_bit_out(False)
        else:
            self._shift_bit_out(True)
        self._shift_bit_out(self._read_from_mem)
        self._shift_bit_out(self._write_to_mem)
        self._shift_bit_out(self._data_clock)
        self._shift_bit_out(self._control_clock)


    def _shift_bit_out(self, bit):
        """
        Shift out a single bit.

        This doesn't latch it into the output register though.
        """
        self._bus_out_serial_in_pin.value(bit)
        self._bus_out_shift_clock_pin.value(True)
        self._bus_out_shift_clock_pin.value(False)

    def _timer_callback(self, timer):
        """
        Timer callback for low frequency clocks
        """
        self._clock_pin.toggle()