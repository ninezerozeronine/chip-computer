L.E.D.s and 74LS Chips
======================

It's very useful to be able to quickly see the if the input or output to or from a gate is high or low. With the 74LS chips L.E.D.s are a convenient option for this. It's possible to run into problems using L.E.D.s though so lets walk through the steps to see when the problems arise and how we can avoid them.

We'll use a very basic circuit with a ``74LSXXXX`` chip to demonstrate:

I'll be using the terms high and low to mean logical true, or 1, and logical 0 or false.

No L.E.D.s
----------
With no L.E.D.s in the picture we have to read voltages to see whats going on.

Single gate
^^^^^^^^^^^

The voltages for high or low inputs coming directly from 5V or ground are...:


5V or 0V as we would expect :).


The output voltages are a little different but not unexpected as the datasheet gives us and idea what to expect:


XV for high and YV for low.


Connected Gates
^^^^^^^^^^^^^^^

The output of the first gate is connected to the input of the second so we have one voltage for our connected input and output. When high and low we get:


XV for high and YV for low. Hmm, not quite the same as with no gate connected. Let's keep that in mind and move on to testing some L.E.D.s.


With L.E.D.s
------------

Single Gate
^^^^^^^^^^^

We can add an L.E.D. in parallel with the input to see what's going into the input (we'll need a protective resistor. This doesn's affect out input voltages and they stay at:


5V for high and 0V for low. But now we get an L.E.D. to quickly see what the input is - great!

With 74LS output pins we can put an L.E.D. in series with the output to ground with no protective resistor. I believe this is because the 74LS series outputs have internal resistors that limit the output current:

L.E.D.s and series resistors






























