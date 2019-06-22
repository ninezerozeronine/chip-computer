"""
Register
"""

import random

from . import core


class Register(core.Module):
    """

    """

    def __init__(self, name):
        """

        """

        self.data = core.eight_bit_port("data", mode=core.MODE["INPUT"])
        self.contents = core.eight_bit_port(
            "contents", mode=core.MODE["OUTPUT"]
        )
        self.input_enable = core.one_bit_port(
            "input_enable", mode=core.MODE["INPUT"]
        )
        self.output_enable = core.one_bit_port(
            "output_enable", mode=core.MODE["INPUT"]
        )
        self.clock = core.one_bit_port(
            "clock", mode=core.MODE["INPUT"]
        )

        self._last_clock = core.STATE["LOW"]
        self.contents.randomise_states()

        super(Register, self).__init__(name)

    def update(self):
        """

        """

        if self._output_enabled():
            self.data.set_all_modes(core.MODE["OUTPUT"])
            self._copy_contents_to_data()
        else:
            self.data.set_all_modes(core.MODE["INPUT"])

        if self._rising_clock() and self._input_enabled():
            self._copy_data_to_contents()

        self._last_clock = self.clock.states[0]

    def _output_enabled(self):
        """

        """
        return self.output_enable.states[0] == core.STATE["HIGH"]

    def _copy_contents_to_data(self):
        """

        """

        for data, content in zip(self.data.channels, self.contents.channels):
            data.state = content.state

    def _copy_data_to_contents(self):
        """

        """

        for content, data in zip(self.contents.channels, self.data.channels):
            content.state = data.state

    def _rising_clock(self):
        """

        """

        return (
            self._last_clock == core.STATE["LOW"]
            and self.clock.states[0] == core.STATE["HIGH"]
        )

    def _input_enabled(self):
        """

        """
        return self.input_enable.states[0] == core.STATE["HIGH"]
































