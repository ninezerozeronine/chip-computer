.. _safe_clock_enable:

Safe Clock Enable
=================

Makes sure that when reset is released, only the next rising clock edge
is passed on. If only an AND gate was used, a rising edge would pass
through if the clock was already high, and (an inverted) reset signal
went low.
