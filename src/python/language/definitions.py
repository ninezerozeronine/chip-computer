"""Defnitions of named items"""

from utils import BitDef

OPCODE_GROUPS = {
    "COPY":  BitDef(end=14, start=13, value="00"),
    "LOAD":  BitDef(end=14, start=13, value="01"),
    "STORE": BitDef(end=14, start=13, value="10"),
    "ALU":   BitDef(end=14, start=13, value="11"),
}

SRC_REGISTERS = {
    "ACC":   BitDef(end=12, start=10, value="000"),
    "A":     BitDef(end=12, start=10, value="001"),
    "B":     BitDef(end=12, start=10, value="010"),
    "C":     BitDef(end=12, start=10, value="011"),
    "SP":    BitDef(end=12, start=10, value="100"),
    "PC":    BitDef(end=12, start=10, value="101"),
    "SP+/-": BitDef(end=12, start=10, value="110"),
    "IMM":   BitDef(end=12, start=10, value="111"),
}

DST_REGISTERS = {
    "ACC":   BitDef(end=9, start=7, value="000"),
    "A":     BitDef(end=9, start=7, value="001"),
    "B":     BitDef(end=9, start=7, value="010"),
    "C":     BitDef(end=9, start=7, value="011"),
    "SP":    BitDef(end=9, start=7, value="100"),
    "PC":    BitDef(end=9, start=7, value="101"),
    "SP+/-": BitDef(end=9, start=7, value="110"),
    "IMM":   BitDef(end=9, start=7, value="111"),
}

ALU_OPERATIONS = {
    "INCR":           BitDef(end=12, start=9, value="0000"),
    "DECR":           BitDef(end=12, start=9, value="0001"),
    "ADD":            BitDef(end=12, start=9, value="0010"),
    "SUB":            BitDef(end=12, start=9, value="0011"), 
    "ADDC":           BitDef(end=12, start=9, value="0100"),
    "SUBC":           BitDef(end=12, start=9, value="0101"),
    "AND":            BitDef(end=12, start=9, value="0110"),
    "OR":             BitDef(end=12, start=9, value="0111"),
    "NAND":           BitDef(end=12, start=9, value="1000"),
    "XOR":            BitDef(end=12, start=9, value="1001"),
    "NOT":            BitDef(end=12, start=9, value="1010"),
    "LSHIFT":         BitDef(end=12, start=9, value="1011"), 
    "LSHIFTC":        BitDef(end=12, start=9, value="1100"),
    "TEST_LTE_GT_EQ": BitDef(end=12, start=9, value="1101"),
    "TEST_LT_GTE":    BitDef(end=12, start=9, value="1110"),
    "TEST_ZERO_NEG":  BitDef(end=12, start=9, value="1111"),
}

ALU_OPERANDS = {
    "ACC": BitDef(end=8, start=7, value="00"),
    "A":   BitDef(end=8, start=7, value="01"),
    "B":   BitDef(end=8, start=7, value="10"),
    "C":   BitDef(end=8, start=7, value="11"),
}

# ALU_OUTPUT_MODES = {
#     "A_PLUS_1"                      
#     "A_PLUS_B"                      
#     "A_MINUS_B"                     
#     "A_PLUS_B_PLUS_1"                       
#     "A_MINUS_B_MINS_1"                      
#     "A_AND_B"                       
#     "A_OR_B"                        
#     "A_NAND_B"                      
#     "A_XOR_B"                       
#     "NOT_A"                     
#     "A_PLUS_A"                      
#     "A_PLUS_A_PLUS_1"                       
#     "COMPARE_LTE_GT_EQ"                     
#     "COMPARE_LT_GTE"
#     "A"                        
#     "ZERO"                      
# }

MODULE_CONTROL = {
    "ACC": {
        "IN":               BitDef(end=0,   start=0,   value="1"),
        "OUT":              BitDef(end=1,   start=1,   value="1"),
    },
    "A": {
        "IN":               BitDef(end=2,   start=2,   value="1"),
        "OUT":              BitDef(end=3,   start=3,   value="1"),
    },
    "B": {
        "IN":               BitDef(end=4,   start=4,   value="1"),
        "OUT":              BitDef(end=5,   start=5,   value="1"),
    },
    "C": {
        "IN":               BitDef(end=6,   start=6,   value="1"),
        "OUT":              BitDef(end=7,   start=7,   value="1"),
    },
    "ALU": {
        "STORE_RESULT":     BitDef(end=8,   start=8,   value="1"),
        "OUT":              BitDef(end=9,   start=9,   value="1"),
        "STORE_FLAGS":      BitDef(end=10,  start=10,  value="1"),
        "A_IS_BUS":         BitDef(end=11,  start=11,  value="1"),
        "S0":               BitDef(end=12,  start=12,  value="1"),
        "S1":               BitDef(end=13,  start=13,  value="1"),
        "S2":               BitDef(end=14,  start=14,  value="1"),
        "S3":               BitDef(end=15,  start=15,  value="1"),
        "M":                BitDef(end=16,  start=16,  value="1"),
        "C_IN":             BitDef(end=17,  start=17,  value="1"),
    }
    "MAR": {
        "IN":               BitDef(end=18,  start=18,  value="1"),
    },
    "RAM": {
        "IN":               BitDef(end=19,  start=19,  value="1"),
        "OUT":              BitDef(end=20,  start=20,  value="1"),
        "SEL_PROG_MEM"      BitDef(end=21,  start=21,  value="1"),
    },
    "PC": {
        "IN":               BitDef(end=22,  start=22,  value="1"),
        "OUT":              BitDef(end=23,  start=23,  value="1"),
        "COUNT":            BitDef(end=24,  start=24,  value="1"),
    },
    "SP": {
        "IN":               BitDef(end=25,  start=25,  value="1"),
        "OUT":              BitDef(end=26,  start=26,  value="1"),
    },
    "IR": {
        "IN":               BitDef(end=27,  start=27,  value="1"),
    },
    "CU": {
        "STEP_RESET":       BitDef(end=28,  start=28,  value="1"),
    },
    "CLOCK": {
        "HALT":             BitDef(end=29,  start=29,  value="1"),
    }
}

MODULE_CONTROL_START = 0
MODULE_CONTROL_END = 29

# TESTS = {
#     "ZERO":   "000",
#     "EQ":     "001",
#     "NEG":    "010",
#     "LTE":    "011",
#     "GT":     "100",
#     "LT":     "101",
#     "GTE"     "110"
# }

FLAGS = {
    "ZERO": {
        "HIGH":         BitDef(end=6, start=3, value="1XXX"),
        "LOW":          BitDef(end=6, start=3, value="0XXX"),
    },
    "NEGATIVE": {
        "HIGH":         BitDef(end=6, start=3, value="X1XX"),
        "LOW":          BitDef(end=6, start=3, value="X0XX"),
    },
    "CARRY_BORROW": {
        "HIGH":         BitDef(end=6, start=3, value="XX1X"),
        "LOW":          BitDef(end=6, start=3, value="XX0X"),
    },
    "EQUAL": {
        "HIGH":         BitDef(end=6, start=3, value="XXX1"),
        "LOW":          BitDef(end=6, start=3, value="XXX0"),
    },
    "ALL" :             BitDef(end=6, start=3, value="XXXX"),
}

STEPS = {
    0: BitDef(end=2,  start=0,  value="000"),
    1: BitDef(end=2,  start=0,  value="001"),
    2: BitDef(end=2,  start=0,  value="010"),
    3: BitDef(end=2,  start=0,  value="011"),
    4: BitDef(end=2,  start=0,  value="100"),
    5: BitDef(end=2,  start=0,  value="101"),
    6: BitDef(end=2,  start=0,  value="110"),
    7: BitDef(end=2,  start=0,  value="111"),
}