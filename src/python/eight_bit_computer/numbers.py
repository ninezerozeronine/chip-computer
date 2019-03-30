"""
Functions for working with, checking and converting numbers.
"""


def number_to_bitstring(number, bit_width=8):
    """

    Raises:
        ValueError: If a negative number doesn't fit in the bit width.
    """
    return "{number:0{bit_width}b}".format(number=number, bit_width=bit_width)


def bitstring_to_number(bitstring, twos_compliment=False):
    """

    """
    pass


def number_is_within_bit_limit(number, bits=8):
    """
    Check if a number can be stored in the number of bits given.

    Negative numbers are stored in 2's compliment binary.

    Args:
        number (int): The number to check.
    Returns:
        bool: True if within limits, False if not.
    """

    return -127 <= number <= 255