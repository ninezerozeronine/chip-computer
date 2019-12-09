"""
Generate the data for the decimal display rom.
"""

from .language_defs import (
    SEGMENT_TO_BIT, CHARACTER_TO_SEGMENTS, CHAR_INDEX_TO_DIGIT_INDEX,
    DISPLAY_OPTIONS
    )
from .number_utils import number_to_bitstring
from . import bitdef
from .data_structures import RomData


def gen_display_romdatas():
    """
    Generate the romdatas that make up the display rom

    Returns:
        list(RomData): List of romdatas (unsorted) that make up the
        display rom.
    """

    romdatas = []
    for raw_value in range(256):
        twos_comp_raw_value = to_2s_compliment(raw_value)

        # Generate unsigned decimal
        unsigned_decimal_str = "{number:>4d}".format(number=raw_value)
        romdatas.extend(
            assemble_romdata(
                raw_value,
                unsigned_decimal_str,
                DISPLAY_OPTIONS["DECIMAL"],
                DISPLAY_OPTIONS["UNSIGNED"],
            )
        )

        # Generate twos compliment decimal
        twos_comp_decimal_str = "{number:>4d}".format(
            number=twos_comp_raw_value
        )
        romdatas.extend(
            assemble_romdata(
                raw_value,
                twos_comp_decimal_str,
                DISPLAY_OPTIONS["DECIMAL"],
                DISPLAY_OPTIONS["TWOS_COMP"],
            )
        )

        # Generate unsigned hex
        unsigned_hex_str = "{number:>4X}".format(number=raw_value)
        romdatas.extend(
            assemble_romdata(
                raw_value,
                unsigned_hex_str,
                DISPLAY_OPTIONS["HEX"],
                DISPLAY_OPTIONS["UNSIGNED"],
            )
        )

        # Generate twos compliment decimal
        twos_comp_hex_str = "{number:>4X}".format(
            number=twos_comp_raw_value
        )
        romdatas.extend(
            assemble_romdata(
                raw_value,
                twos_comp_hex_str,
                DISPLAY_OPTIONS["HEX"],
                DISPLAY_OPTIONS["TWOS_COMP"],
            )
        )

        return romdatas


def to_2s_compliment(value):
    """
    Convert an unsigned value to it's 2's compliment equivalent.

    Args:
        value (int): The unsigned 8 bit value (0-255) to convert
    Returns:
        int: The 2's compliment equivalent.
    """

    if value > 127:
        return value - 256
    else:
        return value


def assemble_romdata(raw_value, disp_chars, base_bitdef, binary_mode_bitdef):
    """
    Assemble the romdatas for the given display configuration.

    Args:
        raw_value (int): The unsigned 8 bit value to convert to display
            rom values.
        disp_chars (string): The display characters that will make up
            this value on the seven segment displays
        base_bitdef (str): A bitdef signifying which base the display
            should be in - hex or decimal. Forms part of the address of
            the rom.
        binary_mode_bitdef (str): Whether the raw value should be
            displayed in unsigned or two's compliment interpreted value.
    Returns:
        list(RomData): List of the romdatas that make up this display
        configuration.
    """
    romdatas = []
    for index, character in enumerate(disp_chars):
        address = bitdef.merge([
            value_to_addr_bitdef(raw_value),
            base_bitdef,
            binary_mode_bitdef,
            CHAR_INDEX_TO_DIGIT_INDEX[index]
        ])
        data = character_to_bitdef(character)
        romdatas.append(RomData(address=address, data=data))
    return romdatas


def value_to_addr_bitdef(value):
    """
    Place the bitdef of the value in the address bitdef.

    The address bitdef is 15 bits wide but the value is only 8. Pad this
    to the correct size by forcing the 3 unused bits in the 3 most
    significate places to be zero and leaving 4 bits for the base and
    interpretation (unsigned vs 2's compliment) in the next most
    significant bits. The valye goes in the 8 least significant bits.

    Args:
        value (int): Unsigned 8 bit value (0-255) to place in the
            address bitdef.
    Returns:
        str: Address bitdef with value in place.
    """

    addr_bitdef = "000....{value_bitdef}".format(
        value_bitdef=number_to_bitstring(value)
    )
    return addr_bitdef


def character_to_bitdef(character):
    """
    Generate a bitdef for the given character.

    Bitdefs are mapped to correspond to a 5641AH 7 segment display:

       A
     - - - 
    |     |
   F|     |B
    |  G  |
     - - -
    |     |
   E|     |C
    |     |
     - - - 
       D

    A = 0000 0001
    B = 0000 0010
    C = 0000 0100
    D = 0000 1000
    E = 0001 0000
    F = 0010 0000
    G = 0100 0000

    Args:
        character (str): Character to get the bidef for.
    Returns:
        str: Bitdef that represents the segments to illuminate for that
        character.
    Raises:
        ValueError: If the character to convert isn't supported.
    """

    if character not in CHARACTER_TO_SEGMENTS:
        msg = (
            "Cannot convert {input_char} to a bitdef for seven segment "
            "display. Valid characters are:\n {valid_chars}.".format(
                input_char = character,
                valid_chars = ", ".join(CHARACTER_TO_SEGMENTS) 
                )
        )
        raise ValueError(msg)

    char_bitdef = bitdef.merge(
        [
            SEGMENT_TO_BIT[segment]
            for segment
            in CHARACTER_TO_SEGMENTS[character]
        ]
    )

    char_bitdef = bitdef.fill(char_bitdef, "0")

    return char_bitdef
