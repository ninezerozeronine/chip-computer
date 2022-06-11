from .data_structures import RomData

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