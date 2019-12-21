"""
Defnitions for the machine code and microcode.
"""

from .bitdef import remove_whitespace as rw
from .bitdef import merge

INSTRUCTION_GROUPS = {
    "COPY":             rw("00...... .... ..."),
    "LOAD":             rw("01...... .... ..."),
    "STORE":            rw("10...... .... ..."),
    "ALU":              rw("11...... .... ..."),
}

SRC_REGISTERS = {
    "ACC":              rw("..000... .... ..."),
    "A":                rw("..001... .... ..."),
    "B":                rw("..010... .... ..."),
    "C":                rw("..011... .... ..."),
    "SP":               rw("..100... .... ..."),
    "PC":               rw("..101... .... ..."),
    "SP+/-":            rw("..110... .... ..."),
    "CONST":            rw("..111... .... ..."),
}

DEST_REGISTERS = {
    "ACC":              rw(".....000 .... ..."),
    "A":                rw(".....001 .... ..."),
    "B":                rw(".....010 .... ..."),
    "C":                rw(".....011 .... ..."),
    "SP":               rw(".....100 .... ..."),
    "PC":               rw(".....101 .... ..."),
    "SP+/-":            rw(".....110 .... ..."),
    "CONST":            rw(".....111 .... ..."),
}

ALU_OPERATIONS = {
    "ZERO":             rw("..0000.. .... ..."),
    "INCR":             rw("..0001.. .... ..."),
    "DECR":             rw("..0010.. .... ..."),
    "ADD":              rw("..0011.. .... ..."),
    "ADDC":             rw("..0100.. .... ..."),
    "SUB":              rw("..0101.. .... ..."),
    "SUBB":             rw("..0110.. .... ..."),
    "AND":              rw("..0111.. .... ..."),
    "NAND":             rw("..1000.. .... ..."),
    "OR":               rw("..1001.. .... ..."),
    "NOR":              rw("..1010.. .... ..."),
    "XOR":              rw("..1011.. .... ..."),
    "NXOR":             rw("..1100.. .... ..."),
    "NOT":              rw("..1101.. .... ..."),
    "LSHIFT":           rw("..1110.. .... ..."),
    "LSHIFTC":          rw("..1111.. .... ..."),

}

ALU_OPERANDS = {
    "ACC/CONST":        rw("......00 .... ..."),
    "A":                rw("......01 .... ..."),
    "B":                rw("......10 .... ..."),
    "C":                rw("......11 .... ..."),
}

FLAGS = {
    "EQUAL": {
        "HIGH":         rw("........ 1... ..."),
        "LOW":          rw("........ 0... ..."),
    },
    "CARRY_BORROW": {
        "HIGH":         rw("........ .1.. ..."),
        "LOW":          rw("........ .0.. ..."),
    },
    "NEGATIVE": {
        "HIGH":         rw("........ ..1. ..."),
        "LOW":          rw("........ ..0. ..."),
    },
    "ZERO": {
        "HIGH":         rw("........ ...1 ..."),
        "LOW":          rw("........ ...0 ..."),
    },
    "ANY":              rw("........ .... ..."),
}

STEPS = {
    0:                  rw("........ .... 000"),
    1:                  rw("........ .... 001"),
    2:                  rw("........ .... 010"),
    3:                  rw("........ .... 011"),
    4:                  rw("........ .... 100"),
    5:                  rw("........ .... 101"),
    6:                  rw("........ .... 110"),
    7:                  rw("........ .... 111"),
}


MODULE_CONTROL = {
    "ACC": {
        "IN":               rw("........ ........ ........ .......1"),
        "OUT":              rw("........ ........ ........ ......1."),
    },
    "A": {
        "IN":               rw("........ ........ ........ .....1.."),
        "OUT":              rw("........ ........ ........ ....1..."),
    },
    "B": {
        "IN":               rw("........ ........ ........ ...1...."),
        "OUT":              rw("........ ........ ........ ..1....."),
    },
    "C": {
        "IN":               rw("........ ........ ........ .1......"),
        "OUT":              rw("........ ........ ........ 1......."),
    },
    "ALU": {
        "STORE_RESULT":     rw("........ ........ .......1 ........"),
        "STORE_FLAGS":      rw("........ ........ ......1. ........"),
        "OUT":              rw("........ ........ .....1.. ........"),
        "A_IS_BUS":         rw("........ ........ ....1... ........"),
        "S0_HIGH":          rw("........ ........ ...1.... ........"),
        "S0_LOW":           rw("........ ........ ...0.... ........"),
        "S1_HIGH":          rw("........ ........ ..1..... ........"),
        "S1_LOW":           rw("........ ........ ..0..... ........"),
        "S2_HIGH":          rw("........ ........ .1...... ........"),
        "S2_LOW":           rw("........ ........ .0...... ........"),
        "S3_HIGH":          rw("........ ........ 1....... ........"),
        "S3_LOW":           rw("........ ........ 0....... ........"),
        "M_HIGH":           rw("........ .......1 ........ ........"),
        "M_LOW":            rw("........ .......0 ........ ........"),
        "WITH_CARRY":       rw("........ ......1. ........ ........"),
        "NO_CARRY":         rw("........ ......0. ........ ........"),

    },
    "MAR": {
        "IN":               rw("........ .....1.. ........ ........"),
    },
    "RAM": {
        "IN":               rw("........ ....1... ........ ........"),
        "OUT":              rw("........ ...1.... ........ ........"),
        "SEL_PROG_MEM":     rw("........ ..0..... ........ ........"),
        "SEL_DATA_MEM":     rw("........ ..1..... ........ ........"),
    },
    "SP": {
        "IN":               rw("........ .1...... ........ ........"),
        "OUT":              rw("........ 1....... ........ ........"),
    },
    "PC": {
        "IN":               rw(".......1 ........ ........ ........"),
        "OUT":              rw("......1. ........ ........ ........"),
        "COUNT":            rw(".....1.. ........ ........ ........"),
    },
    "IR": {
        "IN":               rw("....1... ........ ........ ........"),
    },
    "CU": {
        "STEP_RESET":       rw("...1.... ........ ........ ........"),
    },
    "CLOCK": {
        "HALT":             rw("..1..... ........ ........ ........"),
    },
}


ALU_CONTROL_FLAGS = {
    "A_PLUS_1": [
        MODULE_CONTROL["ALU"]["S0_LOW"],
        MODULE_CONTROL["ALU"]["S1_LOW"],
        MODULE_CONTROL["ALU"]["S2_LOW"],
        MODULE_CONTROL["ALU"]["S3_LOW"],
        MODULE_CONTROL["ALU"]["M_LOW"],
        MODULE_CONTROL["ALU"]["WITH_CARRY"],
    ],
    "A_MINUS_1": [
        MODULE_CONTROL["ALU"]["S0_HIGH"],
        MODULE_CONTROL["ALU"]["S1_HIGH"],
        MODULE_CONTROL["ALU"]["S2_HIGH"],
        MODULE_CONTROL["ALU"]["S3_HIGH"],
        MODULE_CONTROL["ALU"]["M_LOW"],
        MODULE_CONTROL["ALU"]["NO_CARRY"],
    ],
    "A_PLUS_B": [
        MODULE_CONTROL["ALU"]["S0_HIGH"],
        MODULE_CONTROL["ALU"]["S1_LOW"],
        MODULE_CONTROL["ALU"]["S2_LOW"],
        MODULE_CONTROL["ALU"]["S3_HIGH"],
        MODULE_CONTROL["ALU"]["M_LOW"],
        MODULE_CONTROL["ALU"]["NO_CARRY"],
    ],
    "A_MINUS_B": [
        MODULE_CONTROL["ALU"]["S0_LOW"],
        MODULE_CONTROL["ALU"]["S1_HIGH"],
        MODULE_CONTROL["ALU"]["S2_HIGH"],
        MODULE_CONTROL["ALU"]["S3_LOW"],
        MODULE_CONTROL["ALU"]["M_LOW"],
        MODULE_CONTROL["ALU"]["WITH_CARRY"],
    ],
    "A_PLUS_B_PLUS_1": [
        MODULE_CONTROL["ALU"]["S0_HIGH"],
        MODULE_CONTROL["ALU"]["S1_LOW"],
        MODULE_CONTROL["ALU"]["S2_LOW"],
        MODULE_CONTROL["ALU"]["S3_HIGH"],
        MODULE_CONTROL["ALU"]["M_LOW"],
        MODULE_CONTROL["ALU"]["WITH_CARRY"],
    ],
    "A_MINUS_B_MINUS_1": [
        MODULE_CONTROL["ALU"]["S0_LOW"],
        MODULE_CONTROL["ALU"]["S1_HIGH"],
        MODULE_CONTROL["ALU"]["S2_HIGH"],
        MODULE_CONTROL["ALU"]["S3_LOW"],
        MODULE_CONTROL["ALU"]["M_LOW"],
        MODULE_CONTROL["ALU"]["NO_CARRY"],
    ],
    "A_AND_B": [
        MODULE_CONTROL["ALU"]["S0_HIGH"],
        MODULE_CONTROL["ALU"]["S1_HIGH"],
        MODULE_CONTROL["ALU"]["S2_LOW"],
        MODULE_CONTROL["ALU"]["S3_HIGH"],
        MODULE_CONTROL["ALU"]["M_HIGH"],
        MODULE_CONTROL["ALU"]["NO_CARRY"],
    ],
    "A_OR_B": [
        MODULE_CONTROL["ALU"]["S0_LOW"],
        MODULE_CONTROL["ALU"]["S1_HIGH"],
        MODULE_CONTROL["ALU"]["S2_HIGH"],
        MODULE_CONTROL["ALU"]["S3_HIGH"],
        MODULE_CONTROL["ALU"]["M_HIGH"],
        MODULE_CONTROL["ALU"]["NO_CARRY"],
    ],
    "A_NAND_B": [
        MODULE_CONTROL["ALU"]["S0_LOW"],
        MODULE_CONTROL["ALU"]["S1_LOW"],
        MODULE_CONTROL["ALU"]["S2_HIGH"],
        MODULE_CONTROL["ALU"]["S3_LOW"],
        MODULE_CONTROL["ALU"]["M_HIGH"],
        MODULE_CONTROL["ALU"]["NO_CARRY"],
    ],
    "A_NOR_B": [
        MODULE_CONTROL["ALU"]["S0_HIGH"],
        MODULE_CONTROL["ALU"]["S1_LOW"],
        MODULE_CONTROL["ALU"]["S2_LOW"],
        MODULE_CONTROL["ALU"]["S3_LOW"],
        MODULE_CONTROL["ALU"]["M_HIGH"],
        MODULE_CONTROL["ALU"]["NO_CARRY"],
    ],
    "A_XOR_B": [
        MODULE_CONTROL["ALU"]["S0_LOW"],
        MODULE_CONTROL["ALU"]["S1_HIGH"],
        MODULE_CONTROL["ALU"]["S2_HIGH"],
        MODULE_CONTROL["ALU"]["S3_LOW"],
        MODULE_CONTROL["ALU"]["M_HIGH"],
        MODULE_CONTROL["ALU"]["NO_CARRY"],
    ],
    "A_NXOR_B": [
        MODULE_CONTROL["ALU"]["S0_HIGH"],
        MODULE_CONTROL["ALU"]["S1_LOW"],
        MODULE_CONTROL["ALU"]["S2_LOW"],
        MODULE_CONTROL["ALU"]["S3_HIGH"],
        MODULE_CONTROL["ALU"]["M_HIGH"],
        MODULE_CONTROL["ALU"]["NO_CARRY"],
    ],
    "NOT_A": [
        MODULE_CONTROL["ALU"]["S0_LOW"],
        MODULE_CONTROL["ALU"]["S1_LOW"],
        MODULE_CONTROL["ALU"]["S2_LOW"],
        MODULE_CONTROL["ALU"]["S3_LOW"],
        MODULE_CONTROL["ALU"]["M_HIGH"],
        MODULE_CONTROL["ALU"]["NO_CARRY"],
    ],
    "A_PLUS_A": [
        MODULE_CONTROL["ALU"]["S0_LOW"],
        MODULE_CONTROL["ALU"]["S1_LOW"],
        MODULE_CONTROL["ALU"]["S2_HIGH"],
        MODULE_CONTROL["ALU"]["S3_HIGH"],
        MODULE_CONTROL["ALU"]["M_LOW"],
        MODULE_CONTROL["ALU"]["NO_CARRY"],
    ],
    "A_PLUS_A_PLUS_1": [
        MODULE_CONTROL["ALU"]["S0_LOW"],
        MODULE_CONTROL["ALU"]["S1_LOW"],
        MODULE_CONTROL["ALU"]["S2_HIGH"],
        MODULE_CONTROL["ALU"]["S3_HIGH"],
        MODULE_CONTROL["ALU"]["M_LOW"],
        MODULE_CONTROL["ALU"]["WITH_CARRY"],
    ],
    "COMPARE_LTE_GT_EQ": [
        MODULE_CONTROL["ALU"]["S0_LOW"],
        MODULE_CONTROL["ALU"]["S1_HIGH"],
        MODULE_CONTROL["ALU"]["S2_HIGH"],
        MODULE_CONTROL["ALU"]["S3_LOW"],
        MODULE_CONTROL["ALU"]["M_LOW"],
        MODULE_CONTROL["ALU"]["NO_CARRY"],
    ],
    "COMPARE_LT_GTE": [
        MODULE_CONTROL["ALU"]["S0_LOW"],
        MODULE_CONTROL["ALU"]["S1_HIGH"],
        MODULE_CONTROL["ALU"]["S2_HIGH"],
        MODULE_CONTROL["ALU"]["S3_LOW"],
        MODULE_CONTROL["ALU"]["M_LOW"],
        MODULE_CONTROL["ALU"]["WITH_CARRY"],
    ],
    "A": [
        MODULE_CONTROL["ALU"]["S0_LOW"],
        MODULE_CONTROL["ALU"]["S1_LOW"],
        MODULE_CONTROL["ALU"]["S2_LOW"],
        MODULE_CONTROL["ALU"]["S3_LOW"],
        MODULE_CONTROL["ALU"]["M_HIGH"],
        MODULE_CONTROL["ALU"]["NO_CARRY"],
    ],
    "ZERO": [
        MODULE_CONTROL["ALU"]["S0_HIGH"],
        MODULE_CONTROL["ALU"]["S1_HIGH"],
        MODULE_CONTROL["ALU"]["S2_LOW"],
        MODULE_CONTROL["ALU"]["S3_LOW"],
        MODULE_CONTROL["ALU"]["M_HIGH"],
        MODULE_CONTROL["ALU"]["NO_CARRY"],
    ],
}


DISPLAY_OPTIONS = {
    "DECIMAL":   rw("... .0 .. .... ...."),
    "HEX":       rw("... .1 .. .... ...."),
    "UNSIGNED":  rw("... 0. .. .... ...."),
    "TWOS_COMP": rw("... 1. .. .... ...."),
}


# This is reversed due to wiring the seven segment digit index
# activation lines backwards. Oops.
CHAR_INDEX_TO_DIGIT_INDEX = {
    0:           rw("... .. 11 .... ...."),
    1:           rw("... .. 10 .... ...."),
    2:           rw("... .. 01 .... ...."),
    3:           rw("... .. 00 .... ...."),
}


SEGMENT_TO_BIT = {
    "A":           rw(".... ...1"),
    "B":           rw(".... ..1."),
    "C":           rw(".... .1.."),
    "D":           rw(".... 1..."),
    "E":           rw("...1 ...."),
    "F":           rw("..1. ...."),
    "G":           rw(".1.. ...."),
    "NO_SEGMENTS": rw(".... ....")
}


CHARACTER_TO_SEGMENTS = {
    " ": ["NO_SEGMENTS"],
    "-": ["G"],
    "0": ["A", "B", "C", "D", "E", "F"],
    "1": ["B", "C"],
    "2": ["A", "B", "G", "E", "D"],
    "3": ["A", "B", "G", "C", "D"],
    "4": ["F", "G", "B", "C"],
    "5": ["A", "F", "G", "C", "D"],
    "6": ["A", "F", "G", "C", "D", "E"],
    "7": ["A", "B", "C"],
    "8": ["A", "B", "C", "D", "E", "F", "G"],
    "9": ["A", "B", "C", "D", "F", "G"],
    "A": ["E", "F", "A", "B", "C", "G"],
    "B": ["F", "E", "D", "C", "G"],
    "C": ["A", "F", "E", "D"],
    "D": ["B", "C", "D", "E", "G"],
    "E": ["A", "F", "G", "E", "D"],
    "F": ["A", "F", "G", "E"],
}


EMPTY_ADDRESS = rw("........ .... ...")
MODULE_CONTROLS_DEFAULT = rw("00000000 00000000 00000000 00000000")
MODULE_CONTROLS_NONE = rw("........ ........ ........ ........")
DECIMAL_ROM_DEFAULT = rw("00000000")


def instruction_byte_from_bitdefs(bitdefs):
    """
    Extract an instruction byte from the bitdefs that make it up.

    If more than one bitdef is passed it will be merged with the others
    prior to extraction.

    Args:
        bitdefs list(str): List of bitdefs to potentially merge and
            extract
    Returns:
        str: Bitstring of the instruction byte
    """

    merged_bitdefs = merge(bitdefs)
    return merged_bitdefs[0:8]
