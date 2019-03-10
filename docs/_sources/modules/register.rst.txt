Register
========

A register stores an 8 bit number. In the computer registers are
connected to the bus and can read a value from the bus or assert a value
onto the bus. They also provide an output which is the currently stored
value.

As well as the data oriented ACC, A, B and C registers, the control oriented
instruction register, stack pointer and memory address register are all just
registers. The memory address register only needs to read from the bus and not
assert values onto it so it's slightly simpler.

Interface and Operation
-----------------------

This is the interface of a register:

.. image:: images/register/register_block.png

This is how it operates:

+---------------+-----------+--------------------------------------------------------------------------+
| Name          | Bit width | Description                                                              |
+===============+===========+==========================================================================+
| data          | 8         | Reads bits from, or asserts bits onto this connection                    |
+---------------+-----------+--------------------------------------------------------------------------+
| contents      | 8         | Always outputs the current value held in the register                    |
+---------------+-----------+--------------------------------------------------------------------------+
| clock         | 1         | Clock signal from the clock module                                       |
+---------------+-----------+--------------------------------------------------------------------------+
| input_enable  | 1         | While high, the register stores the value on data on a rising clock edge |
+---------------+-----------+--------------------------------------------------------------------------+
| output_enable | 1         | While high, the register asserts it's content onto data                  |
+---------------+-----------+--------------------------------------------------------------------------+

Implementation
--------------

- A 74HCT377 is used to store the contents of the register.
- A 74HCT245 is used to provide a tri-state output to allow asserting
  values onto the bus, or not.
- LEDs with current limiting resistors are used to display the current
  contents.
- A 74HCT04 is used to invert the incoming input_enable and output_enable
  signals to drive the active low inputs on the 74HCT377 and 74HCT245.

The electronics are laid out on the breadboard like so:

.. image:: images/register/register_bus_left_bb.png
    :width: 100%

Due to the central bus in the layout of the computer it's convenient to
also have a version where the connection to the bus is on the right:

.. image:: images/register/register_bus_right_bb.png
    :width: 100%

An input only register like the memory address register is simpler:

.. image:: images/register/register_input_only_right_bb.png
    :width: 100%