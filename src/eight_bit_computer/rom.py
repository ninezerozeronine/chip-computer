"""
Create and export roms for the computer
"""

import os

from .operations import get_all_operations, fetch
from .language_defs import EMPTY_ADDRESS, MODULE_CONTROLS_DEFAULT
from .data_structures import RomData
from . import bitdef
from . import number_utils


def get_rom():
    """
    Get complete representation of the rom.

    Returns:
        list(RomData): All the defined microcode.
    """

    language_templates = collect_language_datatemplates()
    romdatas = collapse_datatemplates_to_romdatas(language_templates)
    if romdatas_have_duplicate_addresses(romdatas):
        raise ValueError("Romdata set has duplicate addresses")
    all_addresses = bitdef.collapse(EMPTY_ADDRESS)
    default_data = MODULE_CONTROLS_DEFAULT
    empties_filled = populate_empty_addresses(
        romdatas, all_addresses, default_data
    )
    full_rom = rom_to_bitdef_list(empties_filled)
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


def romdatas_have_duplicate_addresses(romdatas):
    """
    Check if any of the romdatas have duplicate addresses.

    Args:
        romdatas list(RomData): List of romdatas to check.
    Returns:
        Bool: Whether or not there were any duplicated addresses.
    """

    duplicates = False
    addresses = []
    for romdata in romdatas:
        if romdata.address in addresses:
            duplicates = True
            break
        else:
            addresses.append(romdata.address)
    return duplicates


def populate_empty_addresses(romdatas, all_addresses, default_data):
    """
    Form a complete set of rom data by filling any undefined addresses.

    Args:
        romdatas list(RomData): The romdatas defined by the
            instructions.
        all_addresses (list(str)): List of bitdefs representing every
            address in the rom
        default_data (str): The value to set for any address that isn't
            in romdatas.
    Returns:
        list(RomData): List of RomDatas representing a completely full
            rom
    """

    filled_addresses = {romdata.address: romdata.data for romdata in romdatas}
    complete_rom = []
    for address in all_addresses:
        if address in filled_addresses:
            complete_rom.append(
                RomData(address=address, data=filled_addresses[address])
            )
        else:
            complete_rom.append(
                RomData(address=address, data=default_data)
            )
    return complete_rom


def rom_to_bitdef_list(rom):
    """
    Convert a rom to a list of bitdefs.

    Args:
        rom (list(RomData)): The complete ROM
    Returns:
        list(str): Bitdefs that make up the rom in order.
    Raises:
        ValueError: If the addresses don't start at 0, or the addresses
            aren't continuous.
    """

    bitdefs = []
    rom.sort(key=lambda romdata: romdata.address)

    next_address = 0
    for romdata in rom:
        address = number_utils.bitstring_to_number(romdata.address)
        if address != next_address:
            if next_address == 0:
                raise ValueError(
                    "Romdata set does not start at zero. It starts at "
                    "{address}".format(address=address)
                )
            else:
                raise ValueError(
                    "Romdata set is not continuous. The last good "
                    "address is {address}".format(address=address)
                )
        else:
            bitdefs.append(romdata.data)
            next_address += 1

    return bitdefs


def slice_rom(rom):
    """
    Slice a rom into chunks 8 bits wide.

    This is to prepare the data to write into the roms. To take a single
    RomData as an example, if it looked like this (spaces added for
    clarity)::

        [
            "10101010 11111111 00000000 11001100"
            "00000000 11000011 00111100 11110000",
        ]

    We would end up with::

        {
            0: [
                "11001100",
                "11110000",
            1: [
                "00000000",
                "00111100",
            ]
            2: [
                "11111111",
                "11000011",
            ]
            3: [
                "10101010",
                "00000000",
            ]
        }

    Args:
        rom (list(str)): The complete ROM

    Returns:
        dict(int:list(str)) Dictionary of ROM slices
    """

    rom_slices = {}
    for rom_index in range(get_num_bytes(rom[0])):
        rom_offset = 8 * rom_index
        rom_slice = get_rom_slice(rom, rom_offset + 7, rom_offset)
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


def get_rom_slice(bitdefs, end, start):
    """
    Get a slice of the data in the rom.

    Args:
        bitdefs (list(str)): The bitdefs to get a slice from
        end (int): The index for the end of the slice. Index starts at
            zero at the rightmost (least significant) bit.
        start (int): The index for the start of the slice. Index starts
            at zero at the rightmost (least significant) bit.
    Returns:
        list(str): The sliced list of bitdefs
    """

    sliced_bitdefs = []
    for each_bitdef in bitdefs:
        bitdef_slice = bitdef.extract_bits(each_bitdef, end, start)
        sliced_bitdefs.append(bitdef_slice)
    return sliced_bitdefs
