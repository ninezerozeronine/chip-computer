"""
Constant
"""

from . import core


class Constant(core.Module):
    """

    """

    def __init__(self, name, bitwidth=1):
        """

        """

        channels = []
        for _ in range(bitwidth):
            channels.append(core.Channel(mode=core.MODE["OUTPUT"]))
        self.output = core.Port("output", channels=channels)

        super(Constant, self).__init__(name)

    def update(self):
        """

        """
        pass
