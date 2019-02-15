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


def concatenate_bitdefs(bitdefs):
    """
    Join the values of the passed in bitdefs
    """

    if bitdefs_have_gaps(bitdefs):
        raise ValueError("Bitdefs have gaps.")
    if bitdefs_overlap(bitdefs):
        raise ValueError("Bitdefs overlap.")

    new_end, new_start = bitdef_limits(bitdefs)
    sorted_bitdefs = sorted(
        bitdefs, key=lambda bitdef: bitdef.end, reverse=True
    )
    new_value = "".join([bitdef.value for bitdef in sorted_bitdefs])

    return BitDef(end=new_end, start=new_start, value=new_value)


def merge_bitdefs(bitdefs):
    """
    Merge the bitdefs into a single bitdef.

    The bitdefs must:
        Be the same length and position
        Not have any absolute values in common indexes
    """
    pass


def stack_bitdefs(bitdefs, fill_value="0"):
    """

    """
    pass

def resize_bitdef(bitdef, new_end, new_start, fill_value="0"):
    """
    Change the size and or position of a bitdef.

    Can be thought of as a trim/extend operation
    """

    new_value = ""
    for new_index in reversed(range(new_start, new_end + 1)):
        if (new_index >= bitdef.start) and (new_index <= bitdef.end):
            old_value_index = new_index - bitdef.start
            reversed_old_value_index = (bitdef.end - bitdef.start) - old_value_index
            new_value += bitdef.value[reversed_old_value_index]
        else:
            new_value += fill_value
    
    return BitDef(end=new_end, start=new_start, value=new_value)


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

def bitdefs_in_same_position(bitdefs):
    """
    Check if the bitdefs are all in the same position
    """

    ends = set([bitdef.end for bitdef in bitdefs])
    starts = set([bitdef.start for start in bitdefs])

    same_position = False
    if len(ends) == 0 and len(starts) == 0:
        same_position = True
    return same_position

def bitdefs_have_different_absolutes(bitdefs):
    """
    Check if the bitdefs have any different absolute (non X) values.
    """

    # This is a slow, brute force approach...
    max_end, max_start = bitdef_limits(bitdefs)
    padded_values = []
    for bitdef in bitdefs:
        padded = resize_bitdef(bitdef, max_end, max_start, fill_value="X")
        padded_values.append(padded.value)

    different_absolutes = False
    for index, padded_value in enumerate(padded_values):
        for bit_index, bit in enumerate(padded_value):
            for test_value in padded_values[(index + 1):]:
                test_bit = test_value[bit_index]
                if bit != "X" and test_bit != "X" and bit != test_bit:
                    different_absolutes = True

    return different_absolutes

def collapse_bitdef_possibilities(bitdefs):
    pass