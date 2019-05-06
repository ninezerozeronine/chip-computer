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
    return int(bitstring, 2)


def number_is_within_bit_limit(number, bits=8):
    """
    Check if a number can be stored in the number of bits given.

    Negative numbers are stored in 2's compliment binary.

    Args:
        number (int): The number to check.
        bits (int, optional): The number of bits available.
    Returns:
        bool: True if within limits, False if not.
    """

    min_val = ((2**bits / 2) - 1) * -1
    max_val = 2**bits - 1

    return min_val <= number <= max_val


def bitstring_to_hex_string(bitstring, zero_pad_width=2):
    """

    """

    return "{num:0{zero_pad_width}X}".format(
        num=int(bitstring, 2), zero_pad_width=zero_pad_width
    )
