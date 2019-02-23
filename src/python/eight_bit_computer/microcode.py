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

    opcodes = opcode_addr.values()

    # opcodes = [
    #     opcode_addr["LDA"],
    #     opcode_addr["LDB"],
    #     opcode_addr["AADD"],
    #     opcode_addr["OUTA"],
    #     opcode_addr["HALT"],
    #     opcode_addr["NOOP"],
    #     opcode_addr["JIC"]
    # ]

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

    # Step 3: RAM -> RAM Addr and PC Incr
    addresses = rom_programmer.combine_address_components([
        mc_step_addr[3],
        opcode_addr["LDA"]
        ])
    data = rom_programmer.combine_data_components([
        control_signal["RAM_OUT"],
        control_signal["RAM_ADDR_IN"],
        control_signal["PROGRAM_COUNTER_INCREMENT"]
        ])
    templates.append(rom_programmer.DataTemplate(addresses, data))

    # Step 4: RAM -> A and PC Incr
    addresses = rom_programmer.combine_address_components([
        mc_step_addr[4],
        opcode_addr["LDA"]
        ])
    data = rom_programmer.combine_data_components([
        control_signal["RAM_OUT"],
        control_signal["A_IN"]
        ])
    templates.append(rom_programmer.DataTemplate(addresses, data))

    # Step 5: Reset microcode step counter
    addresses = rom_programmer.combine_address_components([
        mc_step_addr[5],
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

    # Step 3: RAM -> RAM Addr and PC Incr
    addresses = rom_programmer.combine_address_components([
        mc_step_addr[3],
        opcode_addr["LDB"]
        ])
    data = rom_programmer.combine_data_components([
        control_signal["RAM_OUT"],
        control_signal["RAM_ADDR_IN"],
        control_signal["PROGRAM_COUNTER_INCREMENT"]
        ])
    templates.append(rom_programmer.DataTemplate(addresses, data))

    # Step 3: RAM -> B
    addresses = rom_programmer.combine_address_components([
        mc_step_addr[4],
        opcode_addr["LDB"]
        ])
    data = rom_programmer.combine_data_components([
        control_signal["RAM_OUT"],
        control_signal["B_IN"]
        ])
    templates.append(rom_programmer.DataTemplate(addresses, data))

    # Step 5: Reset microcode step counter
    addresses = rom_programmer.combine_address_components([
        mc_step_addr[5],
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

# rom = create_microcode_rom()
# print len(rom)
# pprint(rom)
# # print_microcode_rom(rom)

# rom_programmer.rom_to_logisim(
#     rom, 
#     directory="/Users/andy/Documents/74_series_computer/logisim_roms",
#     filename_base="microcode",
#     bytes_per_line=16)
# rom_programmer.rom_to_arduino(rom)


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

-----

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

----


Memory mapped and proper ALU planning


Opcodes
-------
LDMX
LDIX
STOX
ADDX
SUBX
ANDX
ORX
NOTX
XORX
BSLX
BSRX
JMPX
PCX

JMP
JMPIC
JMPIBSL
JMPIBSR
JMPZ
NOOP
HALT

MOVXY (12)

0XXXXXXX - Register speciific instructions
000XXXXX - Register A speciific instructions
001XXXXX - Register B speciific instructions
010XXXXX - Register C speciific instructions
011XXXXX - Register D speciific instructions

11XXXXXX - General instructions

10XXXXXX - Move instructions
1000YYZZ - Move YY to ZZ



Control Sigs
------------
A_IN
A_OUT
B_IN
B_OUT
C_IN
C_OUT
D_IN
D_OUT

ALU_OUT
ALUOP_0
ALUOP_1
ALUOP_2
ZERO_CHECK_ENABLE
RAM_ADDR_IN
RAM_IN
RAM_OUT

PROGRAM_COUNTER_IN
PROGRAM_COUNTER_OUT
PROGRAM_COUNTER_INCREMENT
INSTRUCTION_REGISTER_IN
HALT
STEP_COUNTER_RESET

Input sigs
----------
IS_ZERO
OVERFLOW





















############################################################
Using 74LS181 for ALU, stack pointer and Havard architecture
############################################################





Op codes
COPY - SRC:[A, B, C, D, PC, SP], DEST:[A, B, C, D, PC, SP]
    Copies SRC to DEST
ADD - REG:[A, B, C, D, PC, SP]
    Adds REG to B and stores the result in REG
ADD_CARRY - REG:[A, B, C, D, PC, SP]
    Adds REG to B, adding 1 if the last add had a carry and stores the result in REG
SUB - REG:[A, B, C, D, PC, SP]
    Subtracts B from REG and stores the result in REG
SUB_BORROW - REG:[A, B, C, D, PC, SP]
    Subtracts B from REG, sutracting 1 if the last subtracton had a borrow, stores the result in REG
LOAD - SRC:[A, B, C, D, PC, SP], DEST:[A, B, C, D, PC, SP]
    Copies the value in memory at the location in SRC to DEST
LOAD_IMMEDIATE - CONSTANT, DEST:[A, B, C, D, PC, SP]
    Sets DEST to CONSTANT
STORE - SRC:[A, B, C, D, PC, SP] DEST:[A, B, C, D, PC, SP]
    Copies the value in the register SRC into memory at the location in DEST
STORE_IMMEDIATE - CONSTANT, DEST:[A, B, C, D, PC, SP]
    Sets the memory at the location in DEST to CONSTANT



PUSH - DEST:[A, B, C, D]
    Copy the value in DEST to memory at the location in SP and then decrement SP by 1
POP - DEST:[A, B, C, D]
    Increment SP by 1 and copy the value in memory at the location in SP to DEST
AND

OR

NOT

XOR

HALT

JUMP

INCR

DECR

CALL

RET

JUMP

JUMP_IF_ZERO

JUMP_IF_EQUAL

JUMP_IF_LESS_THAN

JUMP_IF_LESS_THAN_OR_EQUAL

JUMP_IF_GREATER_THAN

JUMP_IF_GREATER_THAN_OR_EQUAL

JUMP_IF_CARRY

JUMP_IF_BORROW




Input Sigs
----------
Opcode (8 bits)
Microcode Step (3 bits)
ALU ZERO
ALU CARRY/COMPARE
ALU EQUALITY

Control Sigs
------------
A_IN
A_OUT
B_IN
B_OUT
C_IN
C_OUT
D_IN
D_OUT

ALU_IN
ALU_OUT
ALU_S0
ALU_S1
ALU_S2
ALU_S3
ALU_CIN
ALU_M

RAM_ADDR_IN
RAM_IN
RAM_OUT
PROGRAM_COUNTER_IN
PROGRAM_COUNTER_OUT
PROGRAM_COUNTER_COUNT
SP_IN
SP_OUT

INSTRUCTION_REGISTER_IN
PROGRAM_MEMORY_SELECT
STEP_COUNTER_RESET
HALT
















#########################
Op Codes from James Bates
#########################

00 DDD SSS - Copy instructions - Copy SSS to DDD
01 DDD [SSS] - Load instructions - Load memory contents at SSS into DDD
10 [DDD] SSS - Store instructions - Store SSS into memory at DDD
11 WWWW ZZ - ALU instructions - Do WWWW using ZZ (and sometimes B), and store the result in ZZ
00 110 CCC - Jump to an immediate value based on the result of the last test using the ALU (Pushes, Pops, Calls, Returns and other ALU operations will clobber the test results (Unless I AND bits 3, 4 and 5 (index starting at the right) of the op code and the alu write signal to enable a write to the flags register. But that will mean checking of other routine operations won't be possible))
00 111 CCC - Jump to an immediate value based on a test and check CCC between A and B register

Copy, Load and Store
====================
SSS = Source
DDD = Destination
WWWW = Operation
ZZ = Source/Dest

SSS/DDD - Source / Destination
000 = A
001 = B
010 = C
011 = D
100 = SP
101 = PC
110 = SP+/-
111 = Immediate

ALU
===
ZZ - Source / Destination
00 = A
01 = B
10 = C
11 = D

WWWW - ALU Operation
0000: ZZ = 0 
0001: ZZ = ZZ + 1
0010: ZZ = ZZ - 1
0011: ZZ = A + B
0100: ZZ = A - B
0101: ZZ = A + B with carry
0110: ZZ = A - B with borrow
0111: ZZ = A AND B
1000: ZZ = A OR B 
1001: ZZ = A NAND B
1010: ZZ = A XOR B 
1011: ZZ = NOT A 
1100: ZZ = A < 1
1101: ZZ = A < 1 with carry 
1110: Test ZZ and B (Greater than or equal to or less than and all other non size comparison tests) 
1111: Test ZZ and B (Less than or equal to or greater than and all other non size comparison tests)

Checks
======
000: Check for equality to zero of the first value or last operation
001: Check for equality between the two values
010: Check if an addition resulted in a carry 
011: Check if subtraction resulted in a borrow 
100: Check if the first value is greater than the second value  
101: Check if the first value is greater than or equal to the second value 
110: Check if the first value is less than the second value
111: Check if the first value is less than or equal to the second value

Op Codes
========
COPY - Copy SSS into DDD
    00 DDD SSS
LOAD - Copy the value in memory at SSS to DDD
    01 DDD [SSS]
STORE - Copy the value in SSS to memory at DDD
    10 [DDD] SSS
POP - Decrement SP and copy the memory at SP into DDD
    Actually a load with the source set to [SP+/-]
    01 DDD 110
PUSH - Copy DDD into memory at SP and increment SP
    Actually a store with the destination set to [SP+/-]
    10 110 DDD
DATA - Set a DDD to a specific value
    Actually a copy from an immediate value to DDD
    00 DDD 111
JUMP - Set the program counter to a value. JJJ has the same meaning as SSS/DDD
    Actually a copy where the desination is PC
    00 101 JJJ
CONDITIONAL_JUMP - Conditionally jump to an immediate value based on a check (CCC) of the result of the last test using the ALU
    Uses the unused move instruction with the destination as SP+/-
    00 110 CCC
TEST_AND_CONDITONAL_JUMP - Conditionally jump to an immediate value based on a check (CCC) of a test between A and B register
    Uses the unused move instruction with the destination as Immediate
    00 111 CCC
ALU - Perform the WWWW operation with the ALU where ZZ is a source, destination or both
    11 WWWW ZZ
CALL - Push the program counter, then set the program counter to a value. LLL has the same meaning as SSS/DDD
    Actually a load where the destination is PC+/-
    01 110 LLL
RETURN - Set the program counter to the value pointed at by the stack pointer, then increment the stack pointer
    Actually a POP into the PC which is actually a load from [SP+/-] to PC
    10 101 110
PROGRAM_LOAD - Load the contents of program memory at PPP into the D register. PPP has the same meaning as SSS/DDD
    01 111 PPP
PROGRAM_STORE - Store the D register into program memory at PPP
    10 PPP 110
NOOP - Do nothing
    00 000 000
HALT - Halt the computer
    00 111 111

Opcode Gaps
===========
Copying a register to itelf is meaningless
00 000 000 - NOOP
00 001 001
00 010 010
00 011 011
00 100 100
00 101 101
00 110 110
00 111 111 - HALT

A copy to or from SP+/- doesn't make sense, it only has a meaning when doing load or stores
00 110 XXX - Used by conditional check and jump
00 XXX 110

A copy to an immediate value doesnt make sense, you can't write to an immediate value
00 111 XXX - Used by conditional test, check and jump

Loading into SP+/- doesn't make sense, do you want to increment or decrement?
01 110 XXX - Used by CALL

Loading into an immediate doeasn't make sense, you cant write to immediate values
01 111 XXX - Used by PROGRAM_LOAD

Storing SP+/- isn't very useful
10 XXX 110 - Used by PROGRAM_STORE


Call microcode steps
store pc into mem at sp
sp -> alu - 1
alu -> sp
constant -> pc





SET_ZERO

INCR

DECR

ADD

ADD_WITH_CARRY

SUBTRACT

SUBTRACT_WITH_BORROW

AND

OR

NAND

XOR

NOT

SHIFT_LEFT

SHIFT_LEFT_WITH_CARRY

CHECK_IF_ZERO

CHECK_IF_EQUAL

CHECK_IF_CARRY

CHECK_IF_BORROW

CHECK_IF_GREATER_THAN

CHECK_IF_GREATER_THAN_OR_EQUAL

CHECK_IF_LESS_THAN

CHECK_IF_LESS_THAN_OR_EQUAL



Microcode II breakdown
======================
32:09
38:54
1:06:09

Call an immediate
-----------------
T0: _PCE | _MAW
T1: _ME | PGM | _IRW | PCC
T2: _SPE | _ALW | ALS(A_MINUS_B)
T3: _ALE | _MAW | _SPW | PCC
T4: _PCE | _MW | _ALW | ALS(A_MINUS_B)
T5: _ALE | _MAW
T6: _ME | PGM | _PCW | _TR

T0: PC -> MAR
T1: PROGRAM_MEM -> IR, PCC
T2: SP -> ALU, ALU:SUB1
T3: ALU -> (MAR, SP), PCC
T4: PC -> (DATA_MEM, ALU), ALU:SUB1
T5: ALU -> MAR
T6: PROGRAM_MEM -> PC, TR

0  0000 0000 
1  0000 0001 ---- CALL #6
2  0000 0010 ---- 0000 0110
3  0000 0011
4  0000 0100
5  0000 0101
6  0000 0110
7  0000 0111

End of T0: SP = 255  PC = 1  MAR = ?    
End of T1: SP = 255  PC = 2  MAR = ?    
End of T2: SP = 255  PC = 2  MAR = ?    
End of T3: SP = 254  PC = 3  MAR = 254  
End of T4: SP = 254  PC = 3  MAR = 254  D[254] = 3
End of T5: SP = 254  PC = 3  MAR = 2    D[254] = 3
End of T6: SP = 254  PC = 6  MAR = 2    D[254] = 3


Call a register
---------------
T0: PC -> MAR
T1: PROGRAM_MEM -> IR, PCC
T2: SP -> ALU, ALU:SUB1
T3: ALU -> (SP, MAR)
T4: PC -> DATA_MEM
T5: REG_X -> PC, TR

0  0000 0000 
1  0000 0001 ---- CALL REG_X
2  0000 0010
3  0000 0011
4  0000 0100
5  0000 0101
6  0000 0110
7  0000 0111

End of T0: SP = 255  PC = 1      MAR = ?    
End of T1: SP = 255  PC = 2      MAR = ?    
End of T2: SP = 255  PC = 2      MAR = ?    
End of T3: SP = 254  PC = 2      MAR = 254  
End of T4: SP = 254  PC = 2      MAR = 254  D[254] = 2
End of T5: SP = 254  PC = REG_X  MAR = 2    D[254] = 2




We can't connect the output of the instruction register directly to the address lines of the EEPROMS.
This is because it takes time for the EEPROMS to settle after an address change.
This means that we need to buffer the inputs to the EEPROMS with a "mirror" register that's clocked on the faling edge of the clock instead.
It's the same trick that we use to increment the microcode step on the falling edge.
https://www.youtube.com/watch?v=ticGSEi0OW4&t=2282s










"""





























