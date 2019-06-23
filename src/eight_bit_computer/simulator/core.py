"""

"""

import random

MODE = {
    "INPUT": 0,
    "OUTPUT": 1,
    "NC": 2,
}
"""
Possible modes a channel can be in.
"""

STATE = {
    "LOW": 0,
    "HIGH": 1,
}
"""
Possible states a channel can be in.
"""

class Channel(object):
    """
    A 1 bit wide data channel.
    """

    def __init__(self, mode=MODE["NC"]):
        """
        Initialise the Channel.

        Args:
            mode (int): The mode for the channel.
        """
        self.mode = mode
        self.state = STATE["LOW"]

    @property
    def mode(self):
        """
        int: Mode of the channel.

        The mode describes how the channel will operate.
        """
        return self._mode

    @mode.setter
    def mode(self, mode):
        if mode not in (MODE["INPUT"], MODE["OUTPUT"], MODE["NC"]):
            raise ValueError
        else:
            self._mode = mode

    @property
    def state(self):
        """
        int: State of the channel, or the current value of the data.

        Only has meaning when the mode is INPUT or OUTPUT.
        """
        return self._state

    @state.setter
    def state(self, state):
        if state not in (STATE["HIGH"], STATE["LOW"]):
            raise ValueError
        else:
            self._state = state

    def randomise_state(self):
        """
        Randomise the state of the channel.
        """
        self.state = random.choice([STATE["HIGH"], STATE["LOW"]])


class Port(object):
    """
    An external connection point for a module.
    """

    def __init__(self, name, channels=None):
        """
        Initialise the Port.

        Args:
            name (str): Name of the port.
            channels (list(Channel)) (optional): List of channels for
                this port to communicate over.
        """
        self.name = name
        self._width = 0
        if channels is None:
            self.channels = []
        else:
            self.channels = channels

    @property
    def width(self):
        """
        Number of channels in the port.
        """
        return self._width

    @width.setter
    def width(self, width):
        self._width = width

    @property
    def channels(self):
        """
        The channels in this port.
        """
        return self._channels

    @channels.setter
    def channels(self, channels):
        # Ensure it's a list and all the items are Channels
        self._channels = channels
        self.width = len(channels)

    @property
    def states(self):
        """
        States of the channels in the port.
        """
        return [channel.state for channel in self.channels]

    @states.setter
    def states(self, states):
        if len(states) != self._width:
            raise ValueError

        for state, channel in zip(states, self.channels):
            channel.state = state

    @property
    def modes(self):
        """
        Modes of the channels in the port.
        """
        return [channel.mode for channel in self.channels]

    @modes.setter
    def modes(self, modes):
        if len(modes) != self.width:
            raise ValueError

        for mode, channel in zip(modes, self.channels):
            channel.mode = mode

    def set_all_modes(self, mode):
        """
        Set the modes of all the channels in the port

        Args:
            mode (int): The mode to set all the ports to.
        """
        for channel in self.channels:
            channel.mode = mode

    def randomise_states(self):
        """
        Randomise the state of all the channels in the port.
        """
        for channel in self.channels:
            channel.randomise_state()


class Connection(object):
    """
    A connection between to or more Ports
    """
    def __init__(self, ports=None):
        """
        Create new connection

        Args:
            ports (list(Port)): List of ports to add to this connection
        """
        if ports is None:
            self.ports = []
        else:
            self.ports = ports

    @property
    def width(self):
        """
        The width of all the ports in this connection
        """
        return self._width

    @width.setter
    def width(self, width):
        self._width = width

    @property
    def ports(self):
        """
        The ports this connection connects.
        """
        return self._ports

    @ports.setter
    def ports(self, ports):
        if not ports:
            self._ports = []
            self.width = 0
        elif all_ports_same_width(ports):
            self._ports = ports
            self.width = ports[0].width
        else:
            raise ValueError

    def add_port(self, port):
        """
        Add a single port to this connection.

        Args:
            port (Port): The port to add to the connection
        """

        if port.width == self.width:
            self.ports.append(port)
        else:
            raise ValueError

    def ports_in_contention(self):
        """
        Check if any aligned channels on ports are both in output mode.
        """

        # List of lists of modes
        port_modes = []
        for port in self.ports:
            port_modes.append(port.modes)

        # Check mode of first channel on all ports, mode of second
        # channel on all ports, etc
        for modes in zip(*port_modes):
            num_outputs = 0
            for mode in modes:
                if mode == MODE["OUTPUT"]:
                    num_outputs += 1
                    if num_outputs > 1:
                        return True

        return False

    def propagate(self):
        """
        Update value of any inputs in the connection
        """

        if self.ports_in_contention():
            raise RuntimeError

        # List of lists of channels
        port_channels = []
        for port in self.ports:
            port_channels.append(port.channels)

        # Check first channel on all ports, second channel on all ports,
        # etc
        for channels in zip(*port_channels):
            floating = True
            for channel in channels:
                if channel.mode == MODE["OUTPUT"]:
                    floating = False
                    state = channel.state
                    break
            for channel in channels:
                if channel.mode == MODE["INPUT"]:
                    if not floating:
                        channel.state = state
                    else:
                        channel.randomise_state()


class Module(object):
    """
    Base class for modules in the simulation.
    """

    def __init__(self, name):
        """
        Initialise the class

        Args:
            name (str): The name of this module.
        """
        self.name = name

    def update(self):
        """
        Update the ports/state in accordance to any changes
        """
        raise NotImplementedError


def all_ports_same_width(ports):
    """
    Check if all passed in port are the same width.

    If no ports (empty list) is passed, they are all considered to have
    the same width.

    Args:
        ports (list(Port)): List of port to check.
    Returns:
        bool: Whether or not all the ports had the same width.
    """

    if not ports:
        return True

    common_width = ports[0].width
    for port in ports[1:]:
        if port.width != common_width:
            return False

    return True


def create_port(name, mode=MODE["NC"], width=8):
    """
    Convenience method to create an eight bit port.

    Args:
        name (str) (optional): Name of the port.
        width (int) (optional): Number of channels in the port.
    Returns:
        Port: Created port.
    """

    channels = []
    for _ in range(width):
        channels.append(Channel(mode=mode))
    return Port(name, channels=channels)
























