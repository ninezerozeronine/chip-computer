"""

"""

from .instruction_components import (
    ACC,
    A,
    B,
    C,
)

_COMPONENT_TO_MODULE_NAME = {
    ACC: "ACC",
    A: "A",
    B: "B",
    C: "C",
}


def component_to_module_name(component):
    """

    """
    module_name = _COMPONENT_TO_MODULE_NAME.get(component)
    if module_name is None:
        raise ValueError("Component has no mapping to a module")
    else:
        return module_name


def rw(input_string):
    """
    Remove the whitespace from a string.

    Args:
        input_string (str): The string to remove whitespace from.
    Returns:
        str: The string with the whitespace removed.
    """
    return "".join(input_string.strip().split())


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

EMPTY_ADDRESS = rw("........ .... ...")

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
    "MEM": {
        "WRITE_TO":         rw("........ ....1... ........ ........"),
        "READ_FROM":        rw("........ ...1.... ........ ........"),
    },
    "SP": {
        "IN":               rw("........ ..1..... ........ ........"),
        "OUT":              rw("........ .1...... ........ ........"),
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
}

MODULE_CONTROLS_NONE =      rw("........ ........ ........ ........")
MODULE_CONTROLS_DEFAULT =   rw("00000000 00000000 00000000 00000000")


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


