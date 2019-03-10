"""
Functions to help working with bits
"""

from collections import namedtuple

DataTemplate = namedtuple("DataTemplate", ["address_range", "data"])
"""
Some data and a range of addresses to store that data in

Attributes:
    address_range (str): The range of addresses to store the data in.
        0 and 1 are absolute values, X is either a 0 or 1 and the
        expectation is that the data will expand out to the parts of the
        address marked with an X. and example could be "0010XX001".
    data (int): The data to be stored at the given addresses.
"""


def byte_bitstring_to_hex_string(bitstring):
    """

    """

    return "{0:02X}".format(int(bitstring, 2))


def chunker(seq, chunk_size):
    """

    """
    return (
        seq[pos:pos + chunk_size] for pos in xrange(0, len(seq), chunk_size)
    )
