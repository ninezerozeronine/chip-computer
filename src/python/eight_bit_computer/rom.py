"""
Create and export roms for the computer
"""

from .language import copy, load
from .language.definitions import EMPTY_ADDRESS, MODULE_CONTROLS_DEFAULT
from . import utils

from collections import namedtuple


RomData = namedtuple("RomData", ["address", "data"])
"""
Some data and an address to store it in

Attributes:
    address (str): The address to store the data in.
    data (int): The data to be stored at the given address.
"""


def collect_operation_datatemplates():
    """
    Get all the datatemplates from all the defined operations.

    Returns:
        list(DataTemplate): All the data templates from the defined
            operations
    """

    operations = [
        copy,
        load,
    ]

    templates = []
    for operation in operations:
        templates.extend(operation.generate_microcode_templates())
    return templates


def collapse_datatemplates_to_romdatas(datatemplates):
    """
    Collapse any addresses in datatemplates to real values.

    If an address does need collapsing the data is copied out to all the
    collapsed addresses.

    Args:
        datatemplates list(DataTemplates): A list of templates to
            collapse.
    Returns:
        list(RomData): The expanded datatemplates
    """

    romdatas = []
    for datatemplate in datatemplates:
        addresses = utils.collapse_bitdef(datatemplate.address_range)
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


def get_defined_romdata():
    """
    Get all the microcode data that the instructions have defined.

    Returns:
        list(RomData): All the defined microcode.
    """

    templates = collect_operation_datatemplates()
    romdatas = collapse_datatemplates_to_romdatas(templates)
    if romdatas_have_duplicate_addresses(romdatas):
        raise ValueError("Romdata set has duplicate addresses")
    romdatas.sort(key=lambda romdata: romdata.address)
    return romdatas


def populate_empty_addresses(romdatas):
    """
    Form a complete set of rom data by filling any blanks

    Args:
        romdatas list(RomData): The romdata defined by the instructions.
    Returns:
        list(RomData): List of RomDatas representing a completely full
            rom
    """

    all_addresses = utils.collapse_bitdef(EMPTY_ADDRESS)
    filled_addresses = {romdata.address: romdata.data for romdata in romdatas}
    complete_rom = []
    for address in all_addresses:
        if address in filled_addresses:
            complete_rom.append(
                RomData(address=address, data=filled_addresses[address])
            )
        else:
            complete_rom.append(
                RomData(address=address, data=MODULE_CONTROLS_DEFAULT)
            )
    return complete_rom


def get_rom_data_slice(romdatas, end, start):
    """

    """

    pass
