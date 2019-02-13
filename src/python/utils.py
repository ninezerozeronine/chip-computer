"""
Functions to help working with bits
"""

from collections import namedtuple

BitDef = namedtuple("BitDef", ["end", "start", "value"])
"""
Define a range of bits with optional bi state values

The end and start components are ordered to reflect the index ordering 
from right to left - or least to most signifcant bit.

The value is stored as a string of 0's, 1's and X's.

Bi state values are defined with an X.

A bistate value means that this definition expands to multiple values.
For example, 10X0X becomes:
    10000
    10001
    10100
    10101

Attributes:
    end (int): The index of the bit that this definition ends at. 
    start (int): The index of the bit that this definition starts at.
    value (str): String representation of this value or values
"""


def join_bitdefs(bitdefs):
    """
    Join the values of the passed in bitdefs
    """

    if bitdefs_have_gaps(bitdefs):
        raise RuntimeError("Bitdefs have gaps.")
    if bitdefs_overlap(bitdefs):
        raise RuntimeError("Bitdefs overlap.")

    new_end, new_start = bitdef_limits(bitdefs)
    sorted_bitdefs = sorted(
        bitdefs, key=lambda bitdef: bitdef.end, reverse=True
    )
    new_value = "".join([bitdef.value for bitdef in sorted_bitdefs])

    return BitDef(end=new_end, start=new_start, value=new_value)


def merge_bitdefs(bitdefs):
    """

    """
    pass


def stack_bitdefs(end, start, bitdefs, base_value=0):
    """

    """
    pass


def bitdefs_overlap(bitdefs):
    """
    Check if bitdefs overlap

    Args:
        bitdefs (list(BitDef)): List of BitDefs to check for overlaps.
    Returns:
        (bool): Whether or not the BitDefs overlap
    """

    max_end, min_start = bitdef_limits(bitdefs)

    overlap = False

    # This is a very brute force approach...
    for index in range(min_start, max_end + 1):
        index_match = False
        if overlap:
            break
        for bitdef in bitdefs:
            if bitdef.end >= index >= bitdef.start:
                if index_match:
                    overlap = True
                    break
                else:
                    index_match = True

    return overlap


def bitdefs_have_gaps(bitdefs):
    """
    Determine if the bitdefs have any gaps between them
    """

    max_end, min_start = bitdef_limits(bitdefs)
    indexes_to_cover = set(range(min_start, max_end + 1))
    for bitdef in bitdefs:
        indexes_covered = set(range(bitdef.start, bitdef.end + 1))
        indexes_to_cover.difference_update(indexes_covered)

    have_gaps = False
    if len(indexes_to_cover) > 0:
        have_gaps = True
    
    return have_gaps


def bitdef_limits(bitdefs):
    """
    Find the highest ends and lowest starts of the bitdefs.
    """
    
    max_end = max([bitdef.end for bitdef in bitdefs])
    min_start = min([bitdef.start for bitdef in bitdefs])
    return (max_end, min_start)