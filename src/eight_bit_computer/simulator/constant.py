"""
Constant
"""

from . import core


class Constant(core.Module):
    """
    A module that outputs a constant value.
    """

    def __init__(self, name, bitwidth=1):
        """
        Initialise the object.

        Args:
            name (str): Name of the constant.
            bitwidth (int): How many bit the output port should have.
        """
        channels = []
        for _ in range(bitwidth):
            channels.append(core.Channel(mode=core.MODE["OUTPUT"]))
        self.output = core.Port("output", channels=channels)

        super(Constant, self).__init__(name)

    def update(self):
        """
        Update the module to react to changes in inputs.
        """
        pass

    def set_high(self):
        """
        Set all the channels in the output port high.
        """
        highs = [core.STATE["HIGH"] for _ in range(self.output.width)]
        self.output.states = highs

    def set_low(self):
        """
        Set all the channels in the output port low.
        """
        lows = [core.STATE["LOW"] for _ in range(self.output.width)]
        self.output.states = highs
