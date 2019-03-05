.. _control_unit:

Control Unit
============

The control unit interprets the instruction byte and flag bits. It issues
control signals in the correct sequence to operate the other modules in the
computer to complete the current instruction. Steps in the sequence are kept in
order with an internal microcode step counter.

Interface and Operation
-----------------------

This is the interface of the Control Unit:

.. image:: images/control_unit/control_unit_block.png

This is how it operates:

Implementation
--------------

Mirror Registers
^^^^^^^^^^^^^^^^

As per :ref:`james_bates` video_, mirror registers are used to store the
instruction byte and flag bits on a rising ``control_clock``. This is so that
the control signals remain constant when the ``data_clock`` rises.

.. _video: https://youtu.be/ticGSEi0OW4?t=1921

As the instruction byte and flags bits determine the control signals, having
these change while the clock is rising could lead to unpredictable results. The
mirror registers mean that the inputs to the EEPROMs remain steady on the rising
``data_clock`` because those values were stored internally on the rising
``control_clock``.


