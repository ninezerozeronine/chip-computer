"""
Helps programming EEPROMS for my 74 series computer project
"""

from collections import namedtuple, defaultdict
from pprint import pprint

DataTemplate = namedtuple("DataTemplate", ["address_template", "data"])
AddressComponent = namedtuple("AddressComponent", ["start", "end", "value"])

def expand_address(address):
    """
    Expand an address if bits are marked as optional

    Args:
        address (str): The address to expand

    Returns:
        list(str): A list of addresses this address has been expanded to
    """

    if "X" in address:
        res = expand_address(address.replace("X", "0", 1))
        res.extend(expand_address(address.replace("X", "1", 1)))
    else:
        res = [address]

    return res


def get_data_byte_at(data, byte_index):
    """
    Get the data bits at a given byte position.

    Given some data bits, return the value of the data in the byte at
    the given index. If the data doesn't extend into the byte index
    requested, the space is filled with zeroes.

    Args:
        data (int): The bit pattern of data (as an int) to get 8 bits
            (a byte) from
        byte_index (int): The index of the byte you want to retrieve.
            The index starts at 0 being the least significant
            (rightmost) side 
    Returns:
        int: the bit pattern (as an int) of the byte of data at the
        given byte index

    """

    # Shift by desired amount and extract least significant byte
    shifted = data >> (index * 8)
    res = shifted & 0b11111111

    return res


def template_to_dict(template):
    """
    Convert a DataTemplate to address-data pairs

    Args:
        template (`DataTemplate`): The template to convert to real
            address-data pairs.
    Returns:
        dict(int:int): dictionary of address keys and data values (both
            as ints).

    """

    addresses = expand_address(template["address_template"])
    ret = {}
    for address in addresses:
        ret[address] = template["data"]
    return ret


def templates_to_dict(templates):
    """
    Convert a list of templates to a single dictionary

    For each template, expand it and add it to a dictionary. Check for
    address clashes with each expanded step of each template.

    Args:
        templates list(`ROMTemplate`)): A list of ROM templates
    Returns:
        dict(int:int): A dictionary of addresses and data values
    Raises:
        RuntimeError: If there's a clash of addresses once they've been 
            expanded.
    """

    resolved = {}
    for template in templates:
        template_dict = template_to_dict(
            template["address_template"], template["data"])
        for address, data in template_dict.iteritems():
            if address in resolved:
                msg = "Address {0} ({1}) already has data".format(
                    address, bin(address))
                raise RuntimeError(msg)
            else:
                resolved[address] = data

    return resolved


def create_rom_dict(templates):
    """
    Create a ROM default dict of all the templates passed in

    Args:
        templates (list(`ROMTemplate`)): The templates to convert
    Returns:
        defaultdict: The address-data paris to write into the ROM
    """

    data = templates_to_dict(templates)
    rom_dict = defaultdict(int)
    rom_dict.update(data)

    return rom_dict


def num_bytes_needed(rom_dict):
    """
    Get the number of bytes needed to store the largest piece of data.
    """
    largest_data = max(rom_dict.itervalues())


def ROM_to_logisim():
    """
    Convert a microcode dictionary to a logisim ready string
    """

    pass


def ROM_to_arduino():
    """
    Convert a microcode dictionary to an arduino ready string
    """

    pass


def gen_control_signal_dict():
    """
    Generate dictionary of control signal defitions.
    """

    control_signals = [
        "A_IN",
        "A_OUT",
        "B_IN",
        "B_OUT",
        "ALU_OUT",
        "ALU_SUB",
        "RAM_ADDR_IN",
        "RAM_IN",
        "RAM_OUT",
        "SET_USER_WAIT",
        "PROGRAM_COUNTER_IN",
        "PROGRAM_COUNTER_OUT",
        "PROGRAM_COUNTER_COUNT",
        "INSTRUCTION_REGISTER_IN",
        "ZEROCHECK_IN",
        "STEP_COUNTER_RESET"
        ]

    signal_dict = {}
    for index, name in enumerate(control_signals):
        signal_dict[name] = 1 << index

    return signal_dict


def gen_opcode_addr_component_dict():
    """
    Generate dictionary of opcode address components
    """

    opcodes = [
        "LDA",
        "STA",
        "JMPA",
        "JIAZ",
        "OUTA",
        "AADD",
        "ASUB",
        "AUI",

        "LDB",
        "STB",
        "JMPB",
        "JIBZ",
        "OUTB",
        "BADD",
        "BSUB",
        "BUI",

        "JCA",
        "JCS",
        "JUF",
        "JMP",
        "BUW",
        "NOOP",
        "HALT"
        ]

    component_dict = {}
    for index, name in enumerate(opcodes):
        component_dict[name] = AddressComponent(
            start = 0,
            end = 4,
            value = index
            )

    return component_dict


def gen_microcode_step_addr_component_dict():
    """
    Create a dictionary of microcode step address components
    """

    component_dict = {}
    for index in range(8):
        component_dict[index] = AddressComponent(
            start = 5,
            end = 7,
            value = index
            )

    return component_dict


def gen_input_signal_addr_component_dict():
    """
    Create dictionary of input signal address components
    """

    input_signals = [
        "IS_ZERO",
        "WAIT_FOR_USER",
        "CARRY"
        ]

    component_dict = {}
    for index, name in enumerate(input_signals):
        component_dict[name] = AddressComponent(
            start = 8,
            end = 10,
            value = 1 << index
            )


def combine_address_components(length, *components):
    """
    Create address template from components

    Args:
        length (int): How many bits should be in the address
        *components (AddressComponent): The components that will make up
            the address
    Returns:
        (str): The address template
    """

    template = ""
    for index in range(length):
        bit = "X"
        for component in components:
            if component.start <= index <= component.end:
                if bit != "X":
                    raise RuntimeError("Overlapping address components passed")
                width = (component.end - component.start) + 1
                binary_string = "{0:0{width}b}".format(component.value, width=width)
                bit = binary_string[index - component.start]
                
        template += bit

    return template


def create_microcode_rom():
    """

    """

    data_templates = []
    address_width = 11

    data_templates.extend(fetch(address_width))
    data_templates.extend(LDA(address_width))


def fetch(address_width):
    """

    """
    control_signal = gen_control_signal_dict()
    mc_step_addr = gen_microcode_step_addr_component_dict()
    templates = []

    # Step 0: PC -> RAM Addr
    addresses = combine_address_components(
        address_width,
        mc_step_addr[0]
        )
    data = (
        control_signal["PROGRAM_COUNTER_OUT"] |
        control_signal["RAM_ADDR_IN"]
        )

    templates.append(DataTemplate(addresses, data))

    # Step 1: RAM -> Instriction register
    addresses = combine_address_components(
        address_width,
        mc_step_addr[1]
        )
    data = (
        control_signal["PROGRAM_COUNTER_COUNT"] |
        control_signal["RAM_OUT"] |
        control_signal["INSTRUCTION_REGISTER_IN"]
        )

    templates.append(DataTemplate(addresses, data))

    return templates


def LDA(address_width):
    """

    """

    control_signal = gen_control_signal_dict()
    opcode_addr = gen_opcode_addr_component_dict()
    mc_step_addr = gen_microcode_step_addr_component_dict()

    templates = []

    # Step 2: PC -> RAM Addr
    addresses = combine_address_components(
        address_width,
        mc_step_addr[2],
        opcode_addr["LDA"]
        )
    data = (
        control_signal["PROGRAM_COUNTER_OUT"] |
        control_signal["RAM_ADDR_IN"]
        )

    templates.append(DataTemplate(addresses, data))

    # Step 3: RAM -> A and PC Incr
    addresses = combine_address_components(
        address_width,
        mc_step_addr[3],
        opcode_addr["LDA"]
        )
    data = (
        control_signal["RAM_OUT"] |
        control_signal["A_IN"] |
        control_signal["PROGRAM_COUNTER_COUNT"]
        )

    templates.append(DataTemplate(addresses, data))

    # Step 4: Reset microcode step counter
    addresses = combine_address_components(
        address_width,
        mc_step_addr[4],
        opcode_addr["LDA"]
        )
    data = (
        control_signal["STEP_COUNTER_RESET"]
        )

    templates.append(DataTemplate(addresses, data))

    return templates


def LDB(address_width):
    """

    """

    control_signal = gen_control_signal_dict()
    opcode_addr = gen_opcode_addr_component_dict()
    mc_step_addr = gen_microcode_step_addr_component_dict()

    templates = []

    # Step 2: PC -> RAM Addr
    addresses = combine_address_components(
        address_width,
        mc_step_addr[2],
        opcode_addr["LDB"]
        )
    data = (
        control_signal["PROGRAM_COUNTER_OUT"] |
        control_signal["RAM_ADDR_IN"]
        )

    templates.append(DataTemplate(addresses, data))

    # Step 3: RAM -> A and PC Incr
    addresses = combine_address_components(
        address_width,
        mc_step_addr[3],
        opcode_addr["LDB"]
        )
    data = (
        control_signal["RAM_OUT"] |
        control_signal["B_IN"] |
        control_signal["PROGRAM_COUNTER_COUNT"]
        )

    templates.append(DataTemplate(addresses, data))

    # Step 4: Reset microcode step counter
    addresses = combine_address_components(
        address_width,
        mc_step_addr[4],
        opcode_addr["LDB"]
        )
    data = (
        control_signal["STEP_COUNTER_RESET"]
        )

    templates.append(DataTemplate(addresses, data))

    return templates


def AADD(address_width):
    """

    """

    control_signal = gen_control_signal_dict()
    opcode_addr = gen_opcode_addr_component_dict()
    mc_step_addr = gen_microcode_step_addr_component_dict()

    templates = []

    # Step 2: ALU -> A
    addresses = combine_address_components(
        address_width,
        mc_step_addr[2],
        opcode_addr["AADD"]
        )
    data = (
        control_signal["ALU_OUT"] |
        control_signal["A_IN"]
        )

    templates.append(DataTemplate(addresses, data))

    # Step 3: Reset microcode step
    addresses = combine_address_components(
        address_width,
        mc_step_addr[3],
        opcode_addr["AADD"]
        )
    data = (
        control_signal["STEP_COUNTER_RESET"]
        )

    templates.append(DataTemplate(addresses, data))

    return templates


def HALT(address_width):
    """

    """

    control_signal = gen_control_signal_dict()
    opcode_addr = gen_opcode_addr_component_dict()
    mc_step_addr = gen_microcode_step_addr_component_dict()

    templates = []

    # Step 2: Set halt flag
    addresses = combine_address_components(
        address_width,
        mc_step_addr[2],
        opcode_addr["HALT"]
        )
    data = (
        control_signal["HALT"]
        )

    return [DataTemplate(addresses, data)]



# def OPCODE(address_width):
#     """

#     """

#     control_signal = gen_control_signal_dict()
#     opcode_addr = gen_opcode_addr_component_dict()
#     mc_step_addr = gen_microcode_step_addr_component_dict()
#     input_sig_addr = gen_input_signal_addr_component_dict()

#     templates = []

#     # Step 2
#     addresses = combine_address_components(
#         address_width,
#         mc_step_addr[2],
#         opcode_addr[ ]
#         )
#     data = (
#         control_signal[""]
#         )

#     templates.append(DataTemplate(addresses, data))

#     # Step N - 1: Reset microcode step
#     addresses = combine_address_components(
#         address_width,
#         mc_step_addr[ ],
#         opcode_addr[ ]
#         )
#     data = (
#         control_signal["STEP_COUNTER_RESET"]
#         )

#     templates.append(DataTemplate(addresses, data))

#     return templates


# pprint(gen_control_signal_dict())

# first = AddressComponent(0,0,0)
# second = AddressComponent(1,3,7)
# bad = AddressComponent(2,2,0)

# print first.start

# print combine_address_components(5, second, first)
# print combine_address_components(5, first, second)
# print combine_address_components(5, first)
# print combine_address_components(5, second)
# print combine_address_components(5, first, bad)
# print combine_address_components(5, first, second, bad)

pprint(fetch(11))
pprint(LDA(11))


"""
An address but some bits need to be expanded to all thier combinations
e.g. 11010XX00100
address template
address range
address combo
address seed
address base
address blueprint
address breakdown
address group
address collection
compressed address
folded address
stacked address


The addresses to be expanded have this data:
data canvas
data blanket
data range
data cover
data group
data set
data collection
rom section
rom slice
rom fill(er)
storage
data template
data plan



This part of the address has this value
addressComponent


Opcode planning
LOAD A
STORE A
JUMP IF A == 0
OUTPUT A
A = A + B
A = A - B
A = USER_INPUT

LOAD B
STORE B
JUMP IF B == 0
OUTPUT B
B = A + B
B = A - B
B = USER_INPUT

JUMP IF CARRY ADD
JUMP IF CARRY SUB
JUMP IF USER FINISHED
JUMP
BEGIN USER WAIT
NOOP
HALT
















LOAD A
SAVE A
JUMP IF A == 0
JUMP TO ADDRESS IN A
JUMP TO ADDRESS IN A IF CARRY ADD
JUMP TO ADDRESS IN A IF CARRY SUB
JUMP TO ADDRESS IN A IF USER FINISHED
OUTPUT A
A = A + B
A = A - B
A = USER_INPUT

LOAD B
SAVE B
JUMP IF B == 0
JUMP TO ADDRESS IN B
JUMP TO ADDRESS IN B IF CARRY ADD
JUMP TO ADDRESS IN B IF CARRY SUB
JUMP TO ADDRESS IN B IF USER FINISHED
OUTPUT B
B = A + B
B = A - B
B = USER_INPUT

JUMP TO ADDRESS IN Y IF Z == 0
LOAD Y FROM ADDRESS IN Z
STORE Y TO ADDRESS IN Z
MOVE Y TO Z

JUMP IF CARRY ADD
JUMP IF CARRY SUB
JUMP IF USER FINISHED
JUMP
BEGIN USER WAIT
NOOP
HALT
"""







