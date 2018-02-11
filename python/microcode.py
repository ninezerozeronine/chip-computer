import rom_programmer
from pprint import pprint

def gen_control_signal_dict():
    """
    Generate dictionary of control signal defitions.
    """

    control_signals = [
        "A_IN",
        "A_OUT",
        "B_IN",
        "B_OUT",
        "OUT_IN",
        "ALU_OUT",
        "ALU_SUB",
        "RAM_ADDR_IN",
        "RAM_IN",
        "RAM_OUT",
        "REQUEST_USER_INPUT",
        "USER_INPUT_OUT",
        "PROGRAM_COUNTER_IN",
        "PROGRAM_COUNTER_OUT",
        "PROGRAM_COUNTER_INCREMENT",
        "INSTRUCTION_REGISTER_IN",
        "STEP_COUNTER_RESET",
        "HALT"
        ]

    # Reversing so that the control signals will be in the same order
    # as specified here when looking from most significant to least
    # significant bit
    control_signals.reverse()

    signal_dict = {}
    for index, name in enumerate(control_signals):
        signal_dict[name] = rom_programmer.BitDef(
            start = index,
            end = index,
            value = 1
            )

    return signal_dict


def gen_opcode_addr_component_dict():
    """
    Generate dictionary of opcode address components
    """

    opcodes = [
        "LDA",
        "STA",
        "JMPA",
        "OUTA",
        "AADD",
        "ASUB",
        "AUI",

        "LDB",
        "STB",
        "JMPB",
        "OUTB",
        "BADD",
        "BSUB",
        "BUI",

        "JIC",
        "JIUF",
        "JMP",
        "BUW",
        "NOOP",
        "HALT"
        ]

    component_dict = {}
    for index, name in enumerate(opcodes):
        component_dict[name] = rom_programmer.BitDef(
            start = 5,
            end = 9,
            value = index
            )

    return component_dict


def gen_microcode_step_addr_component_dict():
    """
    Create a dictionary of microcode step address components
    """

    component_dict = {}
    for index in range(8):
        component_dict[index] = rom_programmer.BitDef(
            start = 2,
            end = 4,
            value = index
            )

    return component_dict


def gen_input_signal_addr_component_dict():
    """
    Create dictionary of input signal address components
    """

    input_signals = [
        "USER_INPUT_READY",
        "CARRY"
        ]

    input_signals.reverse()

    component_dict = {}
    for index, name in enumerate(input_signals):
        component_dict[name] = rom_programmer.BitDef(
            start = index,
            end = index,
            value = 1
            )
        not_name = "NOT_{name}".format(name=name)
        component_dict[not_name] = rom_programmer.BitDef(
            start = index,
            end = index,
            value = 0
            )       

    return component_dict


def fetch():
    """

    """
    control_signal = gen_control_signal_dict()
    mc_step_addr = gen_microcode_step_addr_component_dict()
    opcode_addr = gen_opcode_addr_component_dict()

    templates = []

    # opcodes = opcode_addr.values()

    opcodes = [
        opcode_addr["LDA"],
        opcode_addr["LDB"],
        opcode_addr["AADD"],
        opcode_addr["OUTA"],
        opcode_addr["HALT"],
        opcode_addr["NOOP"],
        opcode_addr["JIC"]
    ]

    for opcode in opcodes:
        # Step 0: PC -> RAM Addr
        addresses = rom_programmer.combine_address_components([
            opcode,
            mc_step_addr[0]
            ])
        data = rom_programmer.combine_data_components([
            control_signal["PROGRAM_COUNTER_OUT"],
            control_signal["RAM_ADDR_IN"]
            ])

        templates.append(rom_programmer.DataTemplate(addresses, data))

        # Step 1: RAM -> instruction register and program counter count
        addresses = rom_programmer.combine_address_components([
            opcode,
            mc_step_addr[1]
            ])
        data = rom_programmer.combine_data_components([
            control_signal["PROGRAM_COUNTER_INCREMENT"],
            control_signal["RAM_OUT"],
            control_signal["INSTRUCTION_REGISTER_IN"]
            ])

        templates.append(rom_programmer.DataTemplate(addresses, data))

    return templates


def LDA():
    """

    """

    control_signal = gen_control_signal_dict()
    opcode_addr = gen_opcode_addr_component_dict()
    mc_step_addr = gen_microcode_step_addr_component_dict()

    templates = []

    # Step 2: PC -> RAM Addr
    addresses = rom_programmer.combine_address_components([
        mc_step_addr[2],
        opcode_addr["LDA"]
        ])
    data = rom_programmer.combine_data_components([
        control_signal["PROGRAM_COUNTER_OUT"],
        control_signal["RAM_ADDR_IN"]
        ])

    templates.append(rom_programmer.DataTemplate(addresses, data))

    # Step 3: RAM -> A and PC Incr
    addresses = rom_programmer.combine_address_components([
        mc_step_addr[3],
        opcode_addr["LDA"]
        ])
    data = rom_programmer.combine_data_components([
        control_signal["RAM_OUT"],
        control_signal["A_IN"],
        control_signal["PROGRAM_COUNTER_INCREMENT"]
        ])

    templates.append(rom_programmer.DataTemplate(addresses, data))

    # Step 4: Reset microcode step counter
    addresses = rom_programmer.combine_address_components([
        mc_step_addr[4],
        opcode_addr["LDA"]
        ])
    data = rom_programmer.combine_data_components([
        control_signal["STEP_COUNTER_RESET"]
        ])

    templates.append(rom_programmer.DataTemplate(addresses, data))

    return templates


def LDB():
    """

    """

    control_signal = gen_control_signal_dict()
    opcode_addr = gen_opcode_addr_component_dict()
    mc_step_addr = gen_microcode_step_addr_component_dict()

    templates = []

    # Step 2: PC -> RAM Addr
    addresses = rom_programmer.combine_address_components([
        mc_step_addr[2],
        opcode_addr["LDB"]
        ])
    data = rom_programmer.combine_data_components([
        control_signal["PROGRAM_COUNTER_OUT"],
        control_signal["RAM_ADDR_IN"]
        ])

    templates.append(rom_programmer.DataTemplate(addresses, data))

    # Step 3: RAM -> B and PC Incr
    addresses = rom_programmer.combine_address_components([
        mc_step_addr[3],
        opcode_addr["LDB"]
        ])
    data = rom_programmer.combine_data_components([
        control_signal["RAM_OUT"],
        control_signal["B_IN"],
        control_signal["PROGRAM_COUNTER_INCREMENT"]
        ])

    templates.append(rom_programmer.DataTemplate(addresses, data))

    # Step 4: Reset microcode step counter
    addresses = rom_programmer.combine_address_components([
        mc_step_addr[4],
        opcode_addr["LDB"]
        ])
    data = rom_programmer.combine_data_components([
        control_signal["STEP_COUNTER_RESET"]
        ])

    templates.append(rom_programmer.DataTemplate(addresses, data))

    return templates


def AADD():
    """

    """

    control_signal = gen_control_signal_dict()
    opcode_addr = gen_opcode_addr_component_dict()
    mc_step_addr = gen_microcode_step_addr_component_dict()

    templates = []

    # Step 2: ALU -> A
    addresses = rom_programmer.combine_address_components([
        mc_step_addr[2],
        opcode_addr["AADD"]
        ])
    data = rom_programmer.combine_data_components([
        control_signal["ALU_OUT"],
        control_signal["A_IN"]
        ])

    templates.append(rom_programmer.DataTemplate(addresses, data))

    # Step 3: Reset microcode step
    addresses = rom_programmer.combine_address_components([
        mc_step_addr[3],
        opcode_addr["AADD"]
        ])
    data = rom_programmer.combine_data_components([
        control_signal["STEP_COUNTER_RESET"]
        ])

    templates.append(rom_programmer.DataTemplate(addresses, data))

    return templates


def OUTA():
    """
    The OUTA Operation
    """

    control_signal = gen_control_signal_dict()
    opcode_addr = gen_opcode_addr_component_dict()
    mc_step_addr = gen_microcode_step_addr_component_dict()
    input_sig_addr = gen_input_signal_addr_component_dict()

    templates = []

    # Step 2 - A -> OUT
    addresses = rom_programmer.combine_address_components([
        mc_step_addr[2],
        opcode_addr["OUTA"]
        ])
    data = rom_programmer.combine_data_components([
        control_signal["A_OUT"],
        control_signal["OUT_IN"]
        ])

    templates.append(rom_programmer.DataTemplate(addresses, data))

    # Step 3: Reset microcode step
    addresses = rom_programmer.combine_address_components([
        mc_step_addr[3],
        opcode_addr["OUTA"]
        ])
    data = rom_programmer.combine_data_components([
        control_signal["STEP_COUNTER_RESET"]
        ])

    templates.append(rom_programmer.DataTemplate(addresses, data))

    return templates


def HALT():
    """

    """

    control_signal = gen_control_signal_dict()
    opcode_addr = gen_opcode_addr_component_dict()
    mc_step_addr = gen_microcode_step_addr_component_dict()

    templates = []

    # Step 2: Set halt flag
    addresses = rom_programmer.combine_address_components([
        mc_step_addr[2],
        opcode_addr["HALT"]
        ])
    data = rom_programmer.combine_data_components([
        control_signal["HALT"]
        ])

    return [rom_programmer.DataTemplate(addresses, data)]


def NOOP():
    """
    The NOOP Operation
    """

    opcode_addr = gen_opcode_addr_component_dict()
    mc_step_addr = gen_microcode_step_addr_component_dict()
    control_signal = gen_control_signal_dict()


    # Step 2: Reset microcode step
    addresses = rom_programmer.combine_address_components([
        mc_step_addr[2],
        opcode_addr["NOOP"]
        ])
    data = rom_programmer.combine_data_components([
        control_signal["STEP_COUNTER_RESET"]
        ])

    return [rom_programmer.DataTemplate(addresses, data)]


def JIC():
    """

    """

    control_signal = gen_control_signal_dict()
    opcode_addr = gen_opcode_addr_component_dict()
    mc_step_addr = gen_microcode_step_addr_component_dict()
    input_signals = gen_input_signal_addr_component_dict()

    templates = []

    ############
    # IF CARRY #
    ############
    # Step 2: PC -> RAM Addr
    addresses = rom_programmer.combine_address_components([
        mc_step_addr[2],
        opcode_addr["JIC"],
        input_signals["CARRY"]
        ])
    data = rom_programmer.combine_data_components([
        control_signal["PROGRAM_COUNTER_OUT"],
        control_signal["RAM_ADDR_IN"]
        ])
    templates.append(rom_programmer.DataTemplate(addresses, data))

    # Step 3: RAM -> PC
    addresses = rom_programmer.combine_address_components([
        mc_step_addr[3],
        opcode_addr["JIC"],
        input_signals["CARRY"]
        ])
    data = rom_programmer.combine_data_components([
        control_signal["RAM_OUT"],
        control_signal["PROGRAM_COUNTER_IN"],
        ])
    templates.append(rom_programmer.DataTemplate(addresses, data))

    # Step 4: Reset microcode step counter
    addresses = rom_programmer.combine_address_components([
        mc_step_addr[4],
        opcode_addr["JIC"],
        input_signals["CARRY"]
        ])
    data = rom_programmer.combine_data_components([
        control_signal["STEP_COUNTER_RESET"]
        ])
    templates.append(rom_programmer.DataTemplate(addresses, data))

    ################
    # IF NOT CARRY #
    ################
    # Step 2: PC increment (Skip past the address we would have jumped 
    # to)
    addresses = rom_programmer.combine_address_components([
        mc_step_addr[2],
        opcode_addr["JIC"],
        input_signals["NOT_CARRY"]
        ])
    data = rom_programmer.combine_data_components([
        control_signal["PROGRAM_COUNTER_INCREMENT"],
        ])
    templates.append(rom_programmer.DataTemplate(addresses, data))

    # Step 3: Reset microcode step counter
    addresses = rom_programmer.combine_address_components([
        mc_step_addr[3],
        opcode_addr["JIC"],
        input_signals["NOT_CARRY"]
        ])
    data = rom_programmer.combine_data_components([
        control_signal["STEP_COUNTER_RESET"]
        ])
    templates.append(rom_programmer.DataTemplate(addresses, data))

    return templates


def create_microcode_rom():
    """

    """

    data_templates = []

    data_templates.extend(fetch())
    data_templates.extend(LDA())
    data_templates.extend(LDB())
    data_templates.extend(AADD())
    data_templates.extend(OUTA())    
    data_templates.extend(HALT())
    data_templates.extend(NOOP())
    data_templates.extend(JIC())


    rom_dict = rom_programmer.data_templates_to_dict(data_templates)

    return rom_dict


def print_microcode_rom(rom):
    """

    """

    address_width = rom_programmer.bit_width(max(rom.keys()))
    data_width = rom_programmer.bit_width(max(rom.values()))

    opcode_components = gen_opcode_addr_component_dict()
    step_components = gen_microcode_step_addr_component_dict()
    input_signal_components = gen_input_signal_addr_component_dict()
    control_signal_components = gen_control_signal_dict()

    address_reports = []
    address_report_template = ("Address: {address_string}\nAddress: {addr_info_string}\n\n"
        "Data: {data_string}\nData: {data_info_string}")

    for address in sorted(rom.keys()):
        address_string = "{binary_address:} ({address})".format(
            binary_address=rom_programmer.value_to_binary_string(
                address, width=address_width),
            address=address
            )

        address_info = rom_programmer.decompose_address(
            address,
            {
                "opcode":opcode_components,
                "step":step_components,
                "input_signals":input_signal_components
            })

        addr_info_string = ("opcode: {opcode:<7} "
            "step: {step:<7} input signal(s): {input_signals}".format(
                opcode=address_info["opcode"],
                step=address_info["step"],
                input_signals=address_info["input_signals"]
            ))

        data_string = "{binary_data} ({data})".format(
            binary_data=rom_programmer.value_to_binary_string(
                rom[address], width=data_width
                ),
            data=rom[address]
            )

        data_info = rom_programmer.extract_bitdefs(
            rom[address],
            control_signal_components
            )

        data_info_string = "control singal(s): {control_signals}".format(
            control_signals=data_info
            )

        address_reports.append(address_report_template.format(
            address_string=address_string,
            addr_info_string=addr_info_string,
            data_string=data_string,
            data_info_string=data_info_string
            ))

    print "\n=========================================\n".join(address_reports)


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

# mc_steps = gen_microcode_step_addr_component_dict()
# pprint(mc_steps)

# pprint(fetch())
# pprint(LDA())
# pprint(LDB())
# pprint(AADD())
# pprint(OUTA())    
# pprint(HALT())
# pprint(NOOP())

rom = create_microcode_rom()
print len(rom)
pprint(rom)
# print_microcode_rom(rom)

rom_programmer.rom_to_logisim(
    rom, 
    directory="/Users/andy/Documents/74_series_computer/logisim_roms",
    filename_base="microcode",
    bytes_per_line=16)
rom_programmer.rom_to_arduino(rom)


# steps = gen_microcode_step_addr_component_dict()
# pprint(steps)

# print steps[0]

# step0 = combine_address_components([steps[0]])
# print step0




# control_sigs = gen_control_signal_dict()
# pprint(control_sigs)

# fetch_def = fetch()
# print fetch_def

# print get_value_from_bit_range(528, 4, 4)


# print rom_programmer.extract_bitdefs(0, gen_control_signal_dict())
# print rom_programmer.extract_bitdefs(1, gen_control_signal_dict())
# print rom_programmer.extract_bitdefs(2, gen_control_signal_dict())
# print rom_programmer.extract_bitdefs(4, gen_control_signal_dict())
# print rom_programmer.extract_bitdefs(8, gen_control_signal_dict())
# print rom_programmer.extract_bitdefs(16, gen_control_signal_dict())
# print rom_programmer.extract_bitdefs(2**16, gen_control_signal_dict())




# pprint(gen_control_signal_dict())

# first = BitDef(0,0,0)
# second = BitDef(1,3,7)
# bad = BitDef(2,2,0)

# print first.start

# print combine_address_components(5, second, first)
# print combine_address_components(5, first, second)
# print combine_address_components(5, first)
# print combine_address_components(5, second)
# print combine_address_components(5, first, bad)
# print combine_address_components(5, first, second, bad)

# pprint(fetch(11))
# LDA = data_templates_to_dict(LDA(10))
# pprint(LDA)
# rom_info(LDA)
# rom_to_logisim(LDA)
# rom = create_microcode_rom()



# aadd, step 3 and no signal
# pprint(decompose_address("0010000000"))
# pprint(decompose_data(4224))

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
bitDef

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





