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

    """

    operations = [
        copy,
        load,
    ]

    templates = []
    for operation in operations:
        templates.extend(operation.generate_microcode_templates())
    return templates

def datatemplates_to_romdatas(datatemplates):
    """
    Collapse address templates to real values
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
    Check if any of the romdatas have duplicate addresses
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

def get_all_romdata():
    """
    Get a list of the pieces of data to write into the rom
    """

    templates = collect_operation_datatemplates()
    romdatas = datatemplates_to_romdatas(templates)
    if romdatas_have_duplicate_addresses(romdatas):
        raise ValueError("Romdata set has duplicate addresses")
    romdatas.sort(key=lambda romdata: romdata.address)
    return romdatas

def populate_empty_addresses(romdatas):
    """

    """

    all_addresses = utils.collapse_bitdef(EMPTY_ADDRESS)
    filled_addresses = {romdata.address:romdata.data for romdata in romdatas}
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











