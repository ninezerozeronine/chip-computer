"""
Helps programming EEPROMS for my 74 series computer project
"""

from collections import namedtuple
from pprint import pprint

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

BitDef = namedtuple("BitDef", ["start", "end", "value"])
"""
Define a range of bits with a given value

Attributes:
    start (int): The index of the bit that this definition starts at.
        The first index is 0 and is the at the rightmost (least
        significant) bit.
    end (int): The index of the bit that this definition ends at. The 
        first index is 0 and is the at the rightmost (least significant)
        bit.
    value (int): The unsigned integer value of the value in that bit range
"""

def value_to_binary_string(value, width=-1):
    """

    """
    binary_string = None

    if width < 0:
        binary_string = bin(value)[2:]
    elif width == 0:
        binary_string = ""
    else:
        binary_string = "{0:0{width}b}".format(value, width=width)

    return binary_string


def binary_string_to_value(binary_string):
    """
    Convert a binary string representing an unsigned int to a value

    Args:
        binary_string (str): The string to convert. e.g. "001010010"
    Returns:
        (int): the value of the binary string
    """

    return int(binary_string, 2)


def bit_width(value):
    """
    Determine how many bits are needed to store this vaule

    Args:
        value (int): The value to see how many bits we need to store it
    Returns:
        (int): The number of bits needed to store this value
    """

    return len(bin(value)) - 2


def num_bytes_for_value(value):
    """
    Calculate how many bytes "wide" this value is

    Args:
        value (int): The value to be stored as an unsinged int
    Returns:
        (int): The number of bytes "wide" this value is
    """

    num_bits = bit_width(value)
    whole_bytes = num_bits / 8
    partial_bytes = 1 if (num_bits % 8 != 0) else 0
    return whole_bytes + partial_bytes


def get_data_byte_at_index(data, byte_index):
    """
    Get the data at a given byte position.

    Given a data value that may require more than 8 bits to represent in
    unsigned binary, return the value of the data in the byte at the 
    given index. If the data doesn't extend into the byte index
    requested, the space is filled with zeroes. The index starts at 0
    and increases from right to left (or least to most signifcant bit).

    Args:
        data (int): The bit pattern of data (as an int) to get 8 bits
            (a byte) from
        byte_index (int): The index of the byte you want to retrieve.
    Returns:
        int: The bit pattern (as an 8 bit unsigned int) of the byte of
        data at the given byte index.

    """

    # Shift by desired amount and extract least significant byte
    shifted = data >> (byte_index * 8)
    res = shifted & 0b11111111

    return res


def get_value_from_bit_range(value, end, start):
    """
    Extract a value from a range of bits in another value

    Lets say the value is 001001010011 and we start at 2 and end at 5.
    the bit mask we want is 111100. One we and the value and the mask we
    get 010000. Next we shift that value over so its as if the least 
    significant bit was where start was. 010000 >> 2 = 0100 = 4

    End and start arguments are in "reverse" order to match the
    "reverse" indexing of bits from least to most significant bit.

    Args:
        value (int): The value to extract information from
        end (int): The index of the bit that ends the extraction range.
            The index starts at 0 from the rightmost (least significant)
            bit.
        start (int): The index of the bit that begins the extraction
            range. The index starts at 0 from the rightmost (least
            significant) bit

    Returns:
        (int): The extracted value
    """

    bit_mask = "1" * ((end - start) + 1) + "0" * start
    extraction = value & binary_string_to_value(bit_mask)
    shifted_extraction = extraction >> start
    return shifted_extraction


def width_from_bitdefs(bitdefs):
    """
    Determine how wide an binary value needs to be based on bitdefs used
    to define it.

    Args:
        bitdefs (list(BitDef)): List of bitdefs to find max width of
    Returns:
        (int): Maximum width
    """

    max_index = max([bitdef.end for bitdef in bitdefs])
    width = max_index + 1
    return width


def expand_address_range(address_range):
    """
    Expand an address if bits are marked as optional

    Args:
        address_range (str): The address to expand

    Returns:
        list(str): A list of addresses this address has been expanded to
    """

    if "X" in address_range:
        res = expand_address_range(address_range.replace("X", "0", 1))
        res.extend(expand_address_range(address_range.replace("X", "1", 1)))
    else:
        res = [address_range]

    return res


def string_addresses_to_ints(addresses):
    """
    Convert string addresses to int addresses

    Args:
        addresses (list(str)): List of string addresses in binary. e.g:
            ["00100100", "001010"]
    Returns:
        list(int): Converted addresses
    """

    return [binary_string_to_value(address) for address in addresses]


def data_template_to_dict(template):
    """
    Convert a DataTemplate to address-data pairs

    Args:
        template (`DataTemplate`): The template to convert to real
            address-data pairs.
    Returns:
        dict(int:int): dictionary of address keys and data values (both
            as ints).

    """

    string_addresses = expand_address_range(template.address_range)
    addresses = string_addresses_to_ints(string_addresses)
    ret = {}
    for address in addresses:
        ret[address] = template.data
    return ret


def data_templates_to_dict(templates):
    """
    Convert a list of templates to a single dictionary

    For each template, expand it and add it to a dictionary. Check for
    address clashes with each expanded step of each template.

    Args:
        templates list(`DataTemplate`)): A list of data templates
    Returns:
        dict(int:int): A dictionary of addresses and data values
    Raises:
        RuntimeError: If there's a clash of addresses once they've been 
            expanded.
    """

    resolved = {}
    for template in templates:
        template_dict = data_template_to_dict(template)
        for address, data in template_dict.items():
            if address in resolved:
                msg = "Address {0} ({1}) already has data".format(
                    bin(address), address)
                raise RuntimeError(msg)
            else:
                resolved[address] = data

    return resolved


def num_bytes_needed_for_data(rom_dict):
    """
    Get the number of bytes to store the largest data in the rom.

    Args:
        rom_dict (dict(int:int)): Dictionary of address and data values
    Returns:
        (int): Number of bytes needed for largest piece of data
    """
    largest_data = max(rom_dict.itervalues())
    num_bytes = num_bytes_for_value(largest_data)
    return num_bytes


def rom_to_parallel_byte_roms(rom):
    """
    Convert a rom dictionary to parallel byte romss

    The data in the rom is split into 8 bit wide chunks - hence the
    parallel roms.
    The returned roms are in order from least signficant byte to most.

    Args:
        rom (dict(int:int)): The rom dictionary of addresses and data
    Returns:
        (list(dict(int:int))): Parallel roms
    """

    num_data_bytes = num_bytes_needed_for_data(rom)

    byte_roms = []
    for byte_index in range(num_data_bytes):
        byte_rom = {}
        for address in rom:
            data = get_data_byte_at_index(rom[address], byte_index)
            byte_rom[address] = data
        byte_roms.append(byte_rom)

    return byte_roms


def rom_to_list(rom):
    """
    Convert a rom dictionary to a list

    The address of the data in the rom is converted to the index of that
    piece of data in the list.
    If nothing is specified for the rom at a given address, 0 is used
    as the data value.

    Args:
        rom (dict(int:int)): The rom dictionary of addresses and data
    Returns:
        (list(int)): Rom data converted to list
    """

    num_address_bits = bit_width(max(rom.keys()))
    byte_list = []
    for address in range(2 ** num_address_bits):
        data = rom.get(address, 0)
        byte_list.append(data)
    return byte_list


def rom_to_parallel_byte_lists(rom):
    """
    Convert a rom dictionary to parallel byte lists

    Converts a rom to parallel lists of bytes. The address of the data 
    in the rom is converted to the index of that piece of data in the
    list.
    The data is split into 8 bit wide chunks - hence the parallel lists.
    The returned lists are in order from least signficant byte to most.
    If nothing is specified for the rom at a given address, 0 is used
    as the data value.

    Args:
        rom (dict(int:int)): The rom dictionary of addresses and data
    Returns:
        (list(list(int))): Parallel lists of the data split into bytes
    """


    parallel_roms = rom_to_parallel_byte_roms(rom)
    byte_lists = []
    for parallel_rom in parallel_roms:
        byte_lists.append(rom_to_list(parallel_rom))
    return byte_lists


def byte_list_to_hex_string_list(byte_list):
    """
    
    """

    hex_list = []
    for byte_value in byte_list:
        if byte_value > 255:
            raise RuntimeError("Invalid byte value: {0}".format(byte_val))
        else:
            hex_list.append("{0:02X}".format(byte_value))

    return hex_list


def rom_to_logisim(
        rom,
        directory=None,
        name="rom",
        bytes_per_line=8,
        bytes_per_chunk=4
        ):
    """

    """

    byte_lists = rom_to_parallel_byte_lists(rom)
    rom_strings = []
    for byte_list in byte_lists:
        hex_lines = []
        hex_bytes = byte_list_to_hex_string_list(byte_list)
        for index_start in xrange(0, len(byte_list), bytes_per_line):
            hex_line_vals = hex_bytes[index_start : index_start + bytes_per_line]
            hex_chunks = []
            for chunk_index_start in range(0, bytes_per_line, bytes_per_chunk):
                hex_chunk_vals = hex_line_vals[chunk_index_start : chunk_index_start + bytes_per_chunk]
                hex_chunks.append(" ".join(hex_chunk_vals))
            hex_lines.append("  ".join(hex_chunks))
        rom_strings.append("\n".join(hex_lines))

    for index, rom_string in enumerate(rom_strings):
        print "ROM {0} - Length: {1}, Address bit width: {2}\n{3}".format(
            index, 
            len(rom),
            bit_width(max(rom.keys())),
            rom_string)

        if directory is not None:
            pass



def prune_zero_values(rom):
    """

    """

    addresses = rom.keys()
    for address in addresses:
        if rom[address] == 0:
            del rom[address]


def rom_to_arduino(rom):
    """

    """

    parallel_roms = rom_to_parallel_byte_roms(rom)
    for parallel_rom in parallel_roms:
        prune_zero_values(parallel_rom)

    for index, parallel_rom in enumerate(parallel_roms):
        print "ROM {0} (length {1})".format(index, len(parallel_rom))
        pprint(parallel_rom)


def combine_address_components(components):
    """
    Create address template from address components

    Args:
        components (list(BitDef)): The components that will make up the
        address
    Returns:
        (str): The address template
    """

    if bitdefs_overlap(components):
        raise RuntimeError("Overlapping address components passed")

    address_width = width_from_bitdefs(components)

    template = ""
    # Iterate over indexes backwards due to string construction direction
    for index in reversed(range(address_width)):
        bit = "X"
        for component in components:
            if component.end >= index >= component.start:
                component_width = (component.end - component.start) + 1
                value_in_position = component.value << component.start
                binary_string = value_to_binary_string(value_in_position, address_width)
                bit_index = address_width - (index + 1)
                bit = binary_string[bit_index]
        template += bit

    return template


def combine_data_components(components):
    """

    """

    if bitdefs_overlap(components):
        raise RuntimeError("Overlapping data components passed")

    ret = 0
    for component in components:
        ret = ret | component.value << component.start

    return ret


def bitdefs_overlap(bitdefs):
    """
    Check if bitdefs overlap

    Args:
        bitdefs (list(BitDef)): List of BitDefs to check for overlaps.
    Returns:
        (bool): Whether or not the BitDefs overlap
    """

    address_width = width_from_bitdefs(bitdefs)

    overlap = False

    # This is a very brute force approach...
    for index in range(address_width):
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


def decompose_address(address, component_dicts):
    """
    Decompose an address into named components.

    Args:
        adddress (int): The address to decode
        component_dicts (dict(str:(dict(str:BitDef)))): A dictionary of
            names of component groups to the component groups
            themselves.
    Returns:
        (dict(str:str)): Dictionary of names of component groups to 
            matches of named components.
    """

    ret = {}
    for name, component_dict in component_dicts.items():
        ret[name] = extract_bitdefs(address, component_dict)

    return ret


def extract_bitdefs(value, bitdef_dict):
    """

    """

    bitdef_names = []
    for name, bitdef in bitdef_dict.items():
        extraction = get_value_from_bit_range(
            value,
            bitdef.end,
            bitdef.start)
        if extraction == bitdef.value:
            bitdef_names.append(name)

    ret = "----"
    if bitdef_names:
        ret = " | ".join([str(bitdef_name) for bitdef_name in bitdef_names])

    return ret


def address_width_from_data_templates(templates):
    """
    Find the number of bits needed to address all the templates.

    Args:
        templates (list(DataTemplate)): The data templates to be
            addressed.
    Returns:
        (int): The width in bits of the largest address
    """

    return max([len(template.address_range) for template in templates])


# 547 = 1000100011
# pprint (extract_bitdefs(
#     547,
#     {
#         "ONES":BitDef(start=0, end=0, value=1),
#         "TWOS":BitDef(start=1, end=1, value=1),
#         "FOURS":BitDef(start=2, end=2, value=1)
#     }
#     ))


# pprint(
#     combine_address_components([
#         BitDef(start=5, end=9, value=1),
#         BitDef(start=2, end=4, value=7)
#         ])
#     )

# pprint(
#     width_from_bitdefs([
#         BitDef(start=5, end=9, value=1),
#         BitDef(start=2, end=4, value=0)
#         ])
#     )


# pprint(
#     bitdefs_overlap([
#         BitDef(start=5, end=9, value=1),
#         BitDef(start=2, end=4, value=0)
#         ])
#     )

# def decompose_address_old(address):
#     """

#     """
#     opcode_defs = gen_opcode_addr_component_dict()
#     mc_step_defs = gen_microcode_step_addr_component_dict()
#     input_sig_defs = gen_input_signal_addr_component_dict()

#     opcode = extract_bitdefs(address, opcode_defs)
#     step = extract_bitdefs(address, mc_step_defs)
#     input_sig = extract_bitdefs(address, input_sig_defs)

#     return {
#         "opcode":opcode,
#         "step":step,
#         "input_signal":input_sig
#     }


# def extract_unique_component(address, component_dict):
#     """

#     """
#     component_name = None
#     for name, component in component_dict.items():
#         bits = address[component.start : component.end + 1]
#         if int(bits, 2) == component.value:
#             component_name = name
#             break

#     return component_name



# def decompose_data(value):
#     """

#     """

#     signals = []
#     control_signals = gen_control_signal_dict()
#     for name, active_bit in control_signals.items():
#         if value & active_bit:
#             signals.append(name)

#     ret = "----"
#     if signals:
#         ret = " | ".join(signals)

#     return ret

# def rom_to_parallel_byte_lists(rom):
#     """
#     Convert a rom dictionary to parallel byte lists

#     Converts a rom to parallel lists of bytes. The address of the data 
#     in the rom is converted to the index of that piece of data in the
#     list.
#     The data is split into 8 bit wide chunks - hence the parallel lists.
#     The returned lists are in order from least signficant byte to most.
#     If nothing is specified for the rom at a given address, 0 is used
#     as the data value.

#     Args:
#         rom (dict(int:int)): The rom dictionary of addresses and data
#     Returns:
#         (list(list(int))): Parallel lists of the data split into bytes
#     """

#     num_data_bytes = num_bytes_needed_for_data(rom)
#     num_address_bits = bit_width(max(rom.keys()))

#     byte_lists = []
#     for byte_index in range(num_data_bytes):
#         byte_list = []
#         for address in range(2 ** num_address_bits):
#             data = get_data_byte_at_index(rom.get(address, 0), byte_index)
#             byte_list.append(data)
#         byte_lists.append(byte_list)

#     return byte_lists
