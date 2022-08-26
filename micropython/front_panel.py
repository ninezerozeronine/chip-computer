RUN = 100
STOP = 101

STEP = 200
VARIABLE = 201
CRYSTAL = 202

class FrontPanel():
    """
    The user facing interface to the computer.
    """

    def __init__(self):
        """
        Initialise the class.
        """

        self._mode = STOP
        self._clock_mode = STEP

    def run():
        """
        Put the computer into run mode.
        """
        pass

    def stop():
        """
        Put the computer into stop mode.
        """
        pass

    def toggle_run_stop():
        """
        Toggle the computer between run and stop mode.
        """
        pass

    def reset():
        """
        Reset the computer.
        """
        pass

    def quarter_step(self):
        """
        Advance the CPU by a quarter step.
        """
        pass

    def half_step(self):
        """
        Advance the CPU by a half step.
        """
        pass

    def full_step(self):
        """
        Advance the CPU by a full step.
        """
        pass

    def set_clock_frequency(self, frequency):
        """
        Set the clock frequency of the CPU (in Hz)
        """
        pass

    def set_clock_mode(self, mode):
        """
        Set the clock mode.

        The available modes are STEP, VARIABLE, and CRYSTAL:

         - STEP: The clock is advanced 1, 2, or 4 steps at a time.
         - VARIABLE: The clock can be set to a desired frequency in Hz.
         - CRYSTAL: The speed of the clock is determined by the crystal
           in the front panel.
        """
        pass

    def get_word(self, address):
        """
        Get a word from the device on the data bus at the given address.
        """
        pass

    def set_word(self, address, word):
        """
        Set a word on the device on the data bus at the given address.
        """
        pass

    def set_words(self, addresses_and_words):
        """
        Set a number of addresses and words at once.
        """
        pass