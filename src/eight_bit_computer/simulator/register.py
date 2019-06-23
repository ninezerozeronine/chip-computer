"""
Register
"""

import random

from . import core


class Register(core.Module):
    """
    Storage for 8 bits of data.
    """

    def __init__(self, name):
        """
        Initialise the class.

        Args:
            name (str): Name of the register.
        """

        self.data = core.create_port("data", mode=core.MODE["INPUT"], width=8)
        self.contents = core.create_port(
            "contents", mode=core.MODE["OUTPUT"], width=8
        )
        self.input_enable = core.create_port(
            "input_enable", mode=core.MODE["INPUT"], width=1
        )
        self.output_enable = core.create_port(
            "output_enable", mode=core.MODE["INPUT"], width=1
        )
        self.clock = core.create_port(
            "clock", mode=core.MODE["INPUT"], width=1
        )

        self._last_clock = core.STATE["LOW"]
        self.contents.randomise_states()

        super(Register, self).__init__(name)

    def update(self):
        """
        Update the register to react to changes in the inputs.
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
        Determine whether the output enable input is high.

        Returns:
            bool: Whether or not the input is high.
        """
        return self.output_enable.states[0] == core.STATE["HIGH"]

    def _copy_contents_to_data(self):
        """
        Copy the state of the contents port to the data port.
        """

        for data, content in zip(self.data.channels, self.contents.channels):
            data.state = content.state

    def _copy_data_to_contents(self):
        """
        Copy the state of the data port to the contents port.
        """

        for content, data in zip(self.contents.channels, self.data.channels):
            content.state = data.state

    def _rising_clock(self):
        """
        Determine if the clock has just risen.

        Returns:
            bool: Whether or not the clock has just risen.
        """

        return (
            self._last_clock == core.STATE["LOW"]
            and self.clock.states[0] == core.STATE["HIGH"]
        )

    def _input_enabled(self):
        """
        Determine whether the input enable input is high.

        Returns:
            bool: Whether or not the input is high.
        """
        return self.input_enable.states[0] == core.STATE["HIGH"]
