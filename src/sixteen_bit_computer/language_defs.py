"""
Defnitions for the machine code and microcode.
"""

from .bitdef import remove_whitespace as rw
from .bitdef import merge


FLAGS = {
    "EQUAL": {
        "HIGH":         rw("........ ...1 ..."),
        "LOW":          rw("........ ...0 ..."),
    },
    "CARRY_BORROW": {
        "HIGH":         rw("........ ..1. ..."),
        "LOW":          rw("........ ..0. ..."),
    },
    "NEGATIVE": {
        "HIGH":         rw("........ .1.. ..."),
        "LOW":          rw("........ .0.. ..."),
    },
    "ZERO": {
        "HIGH":         rw("........ 1... ..."),
        "LOW":          rw("........ 0... ..."),
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
    "SP": {
        "IN":               rw("........ ........ ........ ...001.."),
        "OUT":              rw("........ ........ ........ 001....."),
    },
    "A": {
        "IN":               rw("........ ........ ........ ...010.."),
        "OUT":              rw("........ ........ ........ 010....."),
    },
    "B": {
        "IN":               rw("........ ........ ........ ...011.."),
        "OUT":              rw("........ ........ ........ 011....."),
    },
    "C": {
        "IN":               rw("........ ........ ........ ...100.."),
        "OUT":              rw("........ ........ ........ 100....."),
    },
    "X": {
        "IN":               rw("........ ........ ........ ...101.."),
        "OUT":              rw("........ ........ ........ 101....."),
    },
    "Y": {
        "IN":               rw("........ ........ ........ ...110.."),
        "OUT":              rw("........ ........ ........ 110....."),
    },
    "Z": {
        "IN":               rw("........ ........ ........ ...111.."),
        "OUT":              rw("........ ........ ........ 111....."),
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
    # The bit in index 19 is memory enable
    # The bit in index 20 is ~RFM/WTM
    "MEM": {
        "READ_FROM":        rw("........ ...01... ........ ........"),
        "WRITE_TO":         rw("........ ...11... ........ ........"),
    },
    "MAR": {
        "IN":               rw("........ .01..... ........ ........"),
        "OUT":              rw("........ .10..... ........ ........"),
        "COUNT":            rw("........ .11..... ........ ........"),
    },

    "PC": {
        "IN":               rw("........ 1....... ........ ........"),
        "OUT":              rw(".......1 ........ ........ ........"),
        "COUNT":            rw("......1. ........ ........ ........"),
    },
    "IR": {
        "IN":               rw(".....1.. ........ ........ ........"),
    },
    "CU": {
        "STEP_RESET":       rw("....1... ........ ........ ........"),
    },
    "CLOCK": {
        "HALT":             rw("...1.... ........ ........ ........"),
    },
    "SHR": {
        "IN":               rw("001..... ........ ........ ........"),
        "OUT":              rw("010..... ........ ........ ........"),
        "ROTL_OUT":         rw("011..... ........ ........ ........"),
        "SHL_OUT":          rw("100..... ........ ........ ........"),
        "ROTR_OUT":         rw("101..... ........ ........ ........"),
        "SHR_OUT":          rw("110..... ........ ........ ........"),
        "POP_BIT_OUT":      rw("111..... ........ ........ ........"),
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
        MODULE_CONTROL["ALU"]["M_LOW"],
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
