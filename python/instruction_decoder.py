import rom_programmer

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
        "SET_USER_WAIT",
        "PROGRAM_COUNTER_IN",
        "PROGRAM_COUNTER_OUT",
        "PROGRAM_COUNTER_COUNT",
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

        "JC",
        "JUF",
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
        "WAIT_FOR_USER",
        "CARRY"
        ]

    input_signals.reverse()

    component_dict = {}
    for index, name in enumerate(input_signals):
        component_dict[name] = rom_programmer.BitDef(
            start = 0,
            end = 1,
            value = 1 << index
            )

    return component_dict