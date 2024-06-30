"""
Create and export roms for the computer
"""

import os

from .operations import get_all_operations, fetch
from .language_defs import (
    EMPTY_ADDRESS, MODULE_CONTROLS_DEFAULT, DECIMAL_ROM_DEFAULT
)
from .data_structures import RomData
from . import bitdef
from . import number_utils
from .rom_utils import (
    romdatas_have_duplicate_addresses,
    populate_empty_addresses
)

def get_rom():
    """
    Get complete representation of the rom.

    Returns:
        list(RomData): All the defined microcode.

    Raises:
        RuntimeError: When the romdata dataset has duplicate addresses.
    """

    language_templates = collect_language_datatemplates()
    romdatas = collapse_datatemplates_to_romdatas(language_templates)
    if romdatas_have_duplicate_addresses(romdatas):
        raise RuntimeError("Romdata set has duplicate addresses")
    all_addresses = bitdef.collapse(EMPTY_ADDRESS)
    default_data = MODULE_CONTROLS_DEFAULT
    full_rom = populate_empty_addresses(romdatas, all_addresses, default_data)
    full_rom.sort(key=lambda romdata: romdata.address)
    return full_rom


def collect_language_datatemplates():
    """
    Get all the datatemplates from all the defined operations.

    Returns:
        list(DataTemplate): All the data templates from the defined
            operations
    """

    operations = get_all_operations()
    operations.append(fetch)

    templates = []
    for operation in operations:
        templates.extend(operation.generate_microcode_templates())
    return templates


def collapse_datatemplates_to_romdatas(datatemplates):
    """
    Collapse any addresses in datatemplates to real values.

    If an address does need collapsing the original data is copied out
    to all the collapsed addresses.

    Args:
        datatemplates list(DataTemplates): A list of templates to
            collapse.
    Returns:
        list(RomData): The expanded datatemplates
    """

    romdatas = []
    for datatemplate in datatemplates:
        addresses = bitdef.collapse(datatemplate.address_range)
        for address in addresses:
            romdatas.append(
                RomData(address=address, data=datatemplate.data)
            )
    return romdatas


def slice_rom(rom):
    """
    Slice a rom into chunks 8 bits wide.

    This is to prepare the data to write into the roms. To take a single
    RomData as an example, if it looked like this (spaces added for
    clarity)::

        RomData(
            address="0000000 0000 000",
            data="10101010 11111111 00000000 11001100"
        )

    We would end up with::

        {
            0: RomData(
                address="0000000 0000 000",
                data="11001100"
            ),
            1: RomData(
                address="0000000 0000 000",
                data="00000000"
            ),
            2: RomData(
                address="0000000 0000 000",
                data="11111111"
            ),
            3: RomData(
                address="0000000 0000 000",
                data="10101010"
            )
        }

    Args:
        rom (list(RomData)): The complete ROM

    Returns:
        dict(int:list(RomData)) Dictionary of ROM slices
    """

    rom_slices = {}
    for rom_index in range(get_num_bytes(rom[0].data)):
        rom_offset = 8 * rom_index
        rom_slice = get_romdata_slice(rom, rom_offset + 7, rom_offset)
        rom_slices[rom_index] = rom_slice
    return rom_slices


def get_num_bytes(bitstring):
    """
    Get the number of bytes needed to store this bitdef.

    Args:
        bitstring (str): Bitstring representing the bits to store.
    Returns:
        int: The number of bytes needed to store the bitstring.
    """

    num_bits = bitdef.length(bitstring)
    num_bytes = num_bits // 8
    if num_bits % 8:
        num_bytes += 1
    return num_bytes


def get_romdata_slice(romdatas, end, start):
    """
    Get a slice of the data in the romdatas.

    Args:
        romdatas (list(RomData)): The romdatas to get a slice from
        end (int): The index for the end of the slice. Starts at zero at
            the rightmost (least significant) bit.
        start (int): The index for the start of the slice. Starts at
            zero at the rightmost (least significant) bit.
    Returns:
        list(RomData): The sliced list of romdatas
    """

    sliced_romdatas = []
    for romdata in romdatas:
        data_slice = bitdef.extract_bits(romdata.data, end, start)
        sliced_romdata = RomData(address=romdata.address, data=data_slice)
        sliced_romdatas.append(sliced_romdata)
    return sliced_romdatas

