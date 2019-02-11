"""Defnitions of named items"""

REGISTERS = {
    "ACC":   "000",
    "A":     "001",
    "B":     "010",
    "C":     "011",
    "SP":    "100",
    "PC":    "101",
    "SP+/-": "110",
    "IMM":   "111"
}

OPCODE_GROUPS = {
    "COPY":  "00",
    "LOAD":  "01",
    "STORE": "10",
    "ALU":   "11"
}

ALU_OPERANDS = {
    "ACC": "00",
    "A":   "01",
    "B":   "10",
    "C":   "11"
}

ALU_OPERATIONS = {
    "INCR":           "0000",
    "DECR":           "0001",
    "ADD":            "0010",
    "SUB":            "0011", 
    "ADDC":           "0100",
    "SUBC":           "0101",
    "AND":            "0110",
    "OR":             "0111",
    "NAND":           "1000",
    "XOR":            "1001",
    "NOT":            "1010",
    "LSHIFT":         "1011", 
    "LSHIFTC":        "1100",
    "TEST_LTE_GT_EQ": "1101",
    "TEST_LT_GTE":    "1110",
    "TEST_ZERO_NEG":  "1111",
}

ALU_OUTPUT_MODES = {
    "A_PLUS_1"                      
    "A_PLUS_B"                      
    "A_MINUS_B"                     
    "A_PLUS_B_PLUS_1"                       
    "A_MINUS_B_MINS_1"                      
    "A_AND_B"                       
    "A_OR_B"                        
    "A_NAND_B"                      
    "A_XOR_B"                       
    "NOT_A"                     
    "A_PLUS_A"                      
    "A_PLUS_A_PLUS_1"                       
    "COMPARE_LTE_GT_EQ"                     
    "COMPARE_LT_GTE"
    "A"                        
    "ZERO"                      

}

MODULE_CONTROL_FLAGS = {
    "ACC": {
        "IN":
        "OUT":
    },
    "A": {
        "IN":
        "OUT":
    },
    "B": {
        "IN":
        "OUT":
    },
    "C": {
        "IN":
        "OUT":
    },
    "ALU": {
        "STORE_RESULT":
        "OUT":
        "STORE_FLAGS":
        "A_IS_BUS":
        "S0":
        "S1":
        "S2":
        "S3":
        "M":
        "C_IN":
    }
    "MAR": {
        "IN":
    },
    "RAM": {
        "IN":
        "OUT":
        "SEL_PROG_MEM"
    },
    "PC": {
        "IN":
        "OUT":
        "COUNT":
    },
    "SP": {
        "IN":
        "OUT":
    },
    "IR": {
        "IN":
    },
    "CU": {
        "MC_STEP_RESET":
    },
    "CLOCK": {
        "HALT":
    }
}

TESTS = {
    "ZERO":   "000",
    "EQ":     "001",
    "NEG":    "010",
    "LTE":    "011",
    "GT":     "100",
    "LT":     "101",
    "GTE"     "110"
}

