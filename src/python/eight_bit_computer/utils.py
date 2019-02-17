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
    data (int): The data to be stored at the given addreses.
"""

def bitdefs_same_length(bitdefs):
    """
    Check if the passed in bitdefs are all the same length
    """

    all_same = True
    first_length = bitdef_length(bitdefs[0])
    for other_bitdef in bitdefs[1:]:
        other_length = bitdef_length(other_bitdef)
        if first_length != other_length:
            all_same = False
            break
    return all_same

def bitdef_length(bitdef):
    """
    Calculate length of bitdef
    """

    return len(bitdef)

def bitdefs_have_overlapping_bits(bitdefs):
    """
    Check if the bitdefs have any bits set in the same position
    """
    if not bitdefs_same_length(bitdefs):
        raise ValueError("Bitdefs are not all the same length.")

    different_bits = False
    for bitdef_index, bitdef in enumerate(bitdefs):
        for bit_index, bit in enumerate(bitdef):
            for test_bitdef in bitdefs[(bitdef_index + 1):]:
                test_bit = test_bitdef[bit_index]
                if bit != "." and test_bit != ".":
                    different_bits = True

    return different_bits

def remove_whitespace(input_string):
    """
    Remove the whitespace from a string
    """
    return "".join(input_string.strip().split())

def merge_bitdefs(bitdefs):
    """
    Merge the bitdefs to a single bitdef

    Bitdefs must
    - All be the same length
    - Not have any bits defined in the same position
    """

    if not bitdefs_same_length(bitdefs):
        raise ValueError("Bitdefs are not all the same length.")
    if bitdefs_have_overlapping_bits(bitdefs):
        raise ValueError("Bitdefs have overlapping bits.")

    output = ""
    for index in range(bitdef_length(bitdefs[0])):
        for bitdef in bitdefs:
            bit = bitdef[index]
            if bit != ".":
                output += bit
                break
        else:
            output += "."

    return output

def collapse_bitdef(bitdef):
    """
    Collapse undefined bits into real bits to make new bitdefs.

    For example, 10.0. becomes:
        10000
        10001
        10100
        10101
    """

    if "." in bitdef:
        res = collapse_bitdef(bitdef.replace(".", "0", 1))
        res.extend(collapse_bitdef(bitdef.replace(".", "1", 1)))
    else:
        res = [bitdef]

    return res

def fill_bitdef(bitdef, value):
    """
    Fill undefined bits with a value

    E.g. 1..0100.1 becomes 111010011 when filled with 1s
    """

    output = ""
    for bit in bitdef:
        if bit == ".":
            output += value
        else:
            output += bit
    return output

def extract_bits(end, start, bitdef):
    """
    Extract a region from the bitdef.

    end and start are indecies starting at the rightmost (least
    significant) bit, starting at 0
    """

    length = bitdef_length(bitdef)
    if end > length:
        raise ValueError("Extraction region is larger than bitdef.")
    if end < start:
        raise ValueError("Extraction end index is before extraction start index.")
    if start < 0:
        raise ValueError("Extraction start index is less than 0.")
    if length == 0:
        return bitdef

    reverse_end = reverse_index(end, length)
    reverse_start = reverse_index(start, length)

    return bitdef[reverse_end:reverse_start + 1]

def reverse_index(index, length):
    return length - index - 1

