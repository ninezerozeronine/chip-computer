Development Tools
=================

.. _logisim:

Logisim
-------

For some reason it got very fussy when there was a pulldown on the input
port (i.e. between the input port and the tri state buffer) inside the CPU. Mysteriously propagating errors (red traces) would keep cropping up - even
inside the ALU - which would go away if you moved a logic gate.

The solution was to move the pulldown outside into the main circuit.

For some reason a pulldown on the bus inside the CPU is fine though.

.. _fritzing:

Fritzing
--------

.. _falstad:

Falstad Circuit Simulator
-------------------------