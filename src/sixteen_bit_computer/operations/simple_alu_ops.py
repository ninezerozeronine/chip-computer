"""
The simple ALU Ops
"""

pass


"""
_SUPPORTED_SIGNATURES = frozenset(
    (ADD, A),
    (ADD, B),
    (ADD, C),
    (ADD, CONST),
    (ADD, M_CONST),
)

# ADD
# SUB
# AND
# OR
# XOR
# NAND
# NOR
# NXOR


def generate_machinecode(signature, const_tokens):
    if signature not in _SUPPORTED_SIGNATURES:
        raise ValueError

    if signature[1] in set(A, B, C):
        return _add_module_machinecode(signature)

    if signature[1] == CONST:
        return _add_const_machinecode(signature, const_tokens)

    if signature[1] == M_CONST:
        return _add_memref_const_machinecode(signature, const_tokens)


def _add_module_machinecode(signature):
    return [
        Word(value=get_instruction_index(signature))
    ]


def _add_const_machinecode(signature, const_tokens):
    return [
        Word(value=get_instruction_index(signature)),
        Word(const_token=const_tokens[0]),
    ]


def _add_memref_const_machinecode(signature, const_tokens):
    return [
        Word(value=get_instruction_index(signature)),
        Word(const_token=const_tokens[0]),
    ]



def generate_microcode(signature):
    if signature not in _SUPPORTED_SIGNATURES:
        raise ValueError

    instruction_index_bitdef = int_to_bitdef(get_instruction_index(signature))
    flags_bitdefs = flags_bitdefs = [FLAGS["ANY"]]


def alu_opcode_to_alu_mode(component):
    mapping = {
        ADD: "A_PLUS_B",
        AND: "A_AND_B",
    }

    return mapping[component]


def generate_control_steps(signature):
    if signature[1] in set(A, B, C):
        step_0 = [
            MODULE_CONTROL[component_to_module_name(signature[1])]["OUT"],
            MODULE_CONTROL["ALU"]["STORE_RESULT"],
            MODULE_CONTROL["ALU"]["STORE_FLAGS"],
        ]
        step_0.extend(ALU_CONTROL_FLAGS[alu_opcode_to_alu_mode(signature[0])])

        step_1 = [
            MODULE_CONTROL["ALU"]["OUT"],
            MODULE_CONTROL["ACC"]["IN"],
        ]

        control_steps = [step_0, step_1]

    elif signature[0] == CONST:
        step_0 = [
            MODULE_CONTROL["PC"]["OUT"],
            MODULE_CONTROL["MAR"]["IN"],
        ]

        step_1 = [
            MODULE_CONTROL["RAM"]["OUT"],
            MODULE_CONTROL["ALU"]["STORE_RESULT"],
            MODULE_CONTROL["ALU"]["STORE_FLAGS"],
            MODULE_CONTROL["PC"]["COUNT"],
        ]
        step_1.extend(ALU_CONTROL_FLAGS[alu_opcode_to_alu_mode(signature[0])])

        step_2 = [
            MODULE_CONTROL["ALU"]["OUT"],
            MODULE_CONTROL["ACC"]["IN"],
        ]

        control_steps = [step_0, step_1, step_2]

    elif signature[0] == M_CONST:
        step_0 = [
            MODULE_CONTROL["PC"]["OUT"],
            MODULE_CONTROL["MAR"]["IN"],
        ]

        step_1 = [
            MODULE_CONTROL["RAM"]["OUT"],
            MODULE_CONTROL["MAR"]["IN"],
            MODULE_CONTROL["PC"]["COUNT"],
        ]

        step_2 = [
            MODULE_CONTROL["RAM"]["OUT"],
            MODULE_CONTROL["ALU"]["STORE_RESULT"],
            MODULE_CONTROL["ALU"]["STORE_FLAGS"],
        ]
        step_2.extend(ALU_CONTROL_FLAGS[alu_opcode_to_alu_mode(signature[0])])

        step_3 = [
            MODULE_CONTROL["ALU"]["OUT"],
            MODULE_CONTROL["ACC"]["IN"],
        ]

        control_steps = [step_0, step_1, step_2, step_3]

    return control_steps
"""