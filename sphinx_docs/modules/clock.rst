Clock
=====

The clock produces signals that synchronise the operation of all the
other modules in the computer.

It can drive the operation of the computer step by step for debugging or
at an arbitrary speed.

Interface and Operation
-----------------------
  
This is the interface to the clock:

.. image:: images/clock_block.png

And this is how it operates:

+---------------+-----------+---------------------------------------------------------------------------------------------------------------------------+
| Name          | Bit width | Description                                                                                                               |
+===============+===========+===========================================================================================================================+
| auto/manual   | 1         | When low, the clock signals are advanced manually with manual_input. When high, clock singals are advanced automatically. |
+---------------+-----------+---------------------------------------------------------------------------------------------------------------------------+
| manual_input  | 1         | High/low transitions here will advance the clock signals.                                                                 |
+---------------+-----------+---------------------------------------------------------------------------------------------------------------------------+
| halt          | 1         | While high, bring both of the clock signals low and stop them advancing.                                                  |
+---------------+-----------+---------------------------------------------------------------------------------------------------------------------------+
| reset         | 1         | While high, bring both of the clock signals low and stop them advancing.                                                  |
+---------------+-----------+---------------------------------------------------------------------------------------------------------------------------+
| data_clock    | 1         | Alternates between high and low, driving the data transitions in the computer.                                            |
+---------------+-----------+---------------------------------------------------------------------------------------------------------------------------+
| control_clock | 1         | Alternates between high and low, driving the control signal transitions in the computer.                                  |
+---------------+-----------+---------------------------------------------------------------------------------------------------------------------------+

Control and Data Clocks
^^^^^^^^^^^^^^^^^^^^^^^

Typically the clocks in other computers invert the data_clock to create
the control_clock, like this:

.. image:: images/inverted_data_clock.png

This is not suitable for this computer due to a couple of notes in the
74HCT161 datasheet::

    2. The High-to-Low transition of PE or TE on the ’HC/HCT161 and the ’HC/HCT163 should only occur while CP is HIGH for conventional operation.
    3. The Low-to-High transition of SPE on the ’HC/HCT161 and SPE or MR on the ’HC/HCT163 should only occur while CP is HIGH for conventional operation.

Control signal changes must happen while data_clock is high. The
inverted clock method doesn't satisfy this constraint as control signal
changes (which happen a short delay after the rising edge of
control_clock) would occur after data_clock had gone low. The delay is
introduced by the EEPROMS settling after a new instruction/flag/micro-step 
value goes onto thier address lines. This demonstares the problem:

.. image:: images/inverted_clock_problem.png

The clock signals change in the following cycle:

+---------------+-------------+
| Clock         | Transition  |
+===============+=============+
| data_clock    | low -> high |
+---------------+-------------+
| control_clock | low -> high |
+---------------+-------------+
| data_clock    | high -> low |
+---------------+-------------+
| control_clock | high -> low |
+---------------+-------------+

Or like this:

.. image:: images/clock_signal_waveforms.png

Once halt and reset go low again after either becomes high, data clock should
be the first to go high and the then sequence continues. Like this:

.. image:: images/clock_halt_reset_behaviour.png

Even duty cycle
^^^^^^^^^^^^^^^

blah