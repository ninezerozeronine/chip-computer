"""
The JUMP_IF_ACC_<CMP> comparison operations.

<CMP> can be LT (less than), LTE (less than or equal to), GTE
(greater than or equal to), or GT (greater than).

Jumps to a location in memory based on the result of the 
comparison between the given module or constant and ACC.
"""

from ..instruction_listings import get_instruction_index
from ..data_structures import Word
from ..instruction_components import (
    JUMP_IF_ACC_LT,
    JUMP_IF_ACC_LTE,
    JUMP_IF_ACC_GTE,
    JUMP_IF_ACC_GT,
    A,
    B,
    C,
    CONST,
    M_CONST,
    component_to_assembly,
)
from .. import number_utils
from ..language_defs import (
    MODULE_CONTROL,
    FLAGS,
    ALU_CONTROL_FLAGS,
)
from . import utils

_SUPPORTED_SIGNATURES = (
    (JUMP_IF_ACC_LT, A, CONST),
    (JUMP_IF_ACC_LT, B, CONST),
    (JUMP_IF_ACC_LT, C, CONST),
    (JUMP_IF_ACC_LT, CONST, CONST),
    (JUMP_IF_ACC_LT, M_CONST, CONST),
    (JUMP_IF_ACC_LTE, A, CONST),
    (JUMP_IF_ACC_LTE, B, CONST),
    (JUMP_IF_ACC_LTE, C, CONST),
    (JUMP_IF_ACC_LTE, CONST, CONST),
    (JUMP_IF_ACC_LTE, M_CONST, CONST),
    (JUMP_IF_ACC_GTE, A, CONST),
    (JUMP_IF_ACC_GTE, B, CONST),
    (JUMP_IF_ACC_GTE, C, CONST),
    (JUMP_IF_ACC_GTE, CONST, CONST),
    (JUMP_IF_ACC_GTE, M_CONST, CONST),
    (JUMP_IF_ACC_GT, A, CONST),
    (JUMP_IF_ACC_GT, B, CONST),
    (JUMP_IF_ACC_GT, C, CONST),
    (JUMP_IF_ACC_GT, CONST, CONST),
    (JUMP_IF_ACC_GT, M_CONST, CONST),
)

CONTROLS_MAP = {
    JUMP_IF_ACC_LT : {
        "gen_flags_controls": ALU_CONTROL_FLAGS["COMPARE_LT_GTE"],
        "true_flags": [FLAGS["CARRY_BORROW"]["LOW"]],
        "false_flags": [FLAGS["CARRY_BORROW"]["HIGH"]],
    },
    JUMP_IF_ACC_LTE : {
        "gen_flags_controls": ALU_CONTROL_FLAGS["COMPARE_LTE_GT_EQ"],
        "true_flags": [FLAGS["CARRY_BORROW"]["LOW"]],
        "false_flags": [FLAGS["CARRY_BORROW"]["HIGH"]],
    },
    JUMP_IF_ACC_GTE : {
        "gen_flags_controls": ALU_CONTROL_FLAGS["COMPARE_LT_GTE"],
        "true_flags": [FLAGS["CARRY_BORROW"]["HIGH"]],
        "false_flags": [FLAGS["CARRY_BORROW"]["LOW"]],
    },
    JUMP_IF_ACC_GT : {
        "gen_flags_controls": ALU_CONTROL_FLAGS["COMPARE_LTE_GT_EQ"],
        "true_flags": [FLAGS["CARRY_BORROW"]["HIGH"]],
        "false_flags": [FLAGS["CARRY_BORROW"]["LOW"]],
    },
}


def generate_machinecode(signature, const_tokens):
    """
    Generate machinecode for the JUMP_IF_ACC_<CMP> operations.

    Args:
        signature (Tuple(:mod:`Instruction component<.instruction_components>`)):
            The signature to check.
        const_tokens (list(Token)): The tokens that represent constant
            values in the instruction.
    Returns:
        list(Word): The machinecode for the given signature.
    """
    if signature not in _SUPPORTED_SIGNATURES:
        raise ValueError

    if signature[1] == CONST:
        return [
            Word(value=get_instruction_index(signature)),
            Word(const_token=const_tokens[0]),
            Word(const_token=const_tokens[1]),
        ]
    elif signature[1] == M_CONST:
        return [
            Word(value=get_instruction_index(signature)),
            Word(const_token=const_tokens[1]),
            Word(const_token=const_tokens[0]),
        ]
    else:
        return [
            Word(value=get_instruction_index(signature)),
            Word(const_token=const_tokens[0]),
        ]


def generate_microcode_templates():
    """
    Generate microcode for the JUMP_IF_ACC_<CMP> operations.

    Returns:
        list(DataTemplate): DataTemplates for all the JUMP_IF_ACC_<CMP> microcode.
    """

    data_templates = []

    for signature in _SUPPORTED_SIGNATURES:
        data_templates.extend(generate_templates_for_signature(signature))

    return data_templates


def generate_templates_for_signature(signature):
    """

    Args:
        signature (Tuple(:mod:`Instruction component<.instruction_components>`)):
            The signature to generate templates for.
    Returns:
        list(DataTemplate): DataTemplates for the given signature.

    """
    microcode_defs = []

    # Comparing to a value in memory, e.g.
    # JUMP_IF_ACC_<CMP> [#22] &label
    if signature[1] == M_CONST:
        # First unconditional step to store the value to jump to 
        step_0_flags = [FLAGS["ANY"]]
        step_0_module_controls = [
            MODULE_CONTROL["MEM"]["READ_FROM"],
            MODULE_CONTROL["SHR"]["IN"],
            MODULE_CONTROL["PC"]["COUNT"],
            MODULE_CONTROL["MAR"]["COUNT"],
        ]
        microcode_defs.append({
            "step": 0,
            "flags": step_0_flags,
            "module_controls": step_0_module_controls,
        })

        # Second unconditional step to address the value to compare
        step_1_flags = [FLAGS["ANY"]]
        step_1_module_controls = [
            MODULE_CONTROL["MEM"]["READ_FROM"],
            MODULE_CONTROL["MAR"]["IN"],
            MODULE_CONTROL["PC"]["COUNT"],
        ]
        microcode_defs.append({
            "step": 1,
            "flags": step_1_flags,
            "module_controls": step_1_module_controls,
        })

        # Third unconditional step to generate the flags comparing the
        # value from memory
        step_2_flags = [FLAGS["ANY"]]
        step_2_module_controls = [
            MODULE_CONTROL["MEM"]["READ_FROM"],
            MODULE_CONTROL["ALU"]["STORE_FLAGS"],
        ]
        step_2_module_controls.extend(CONTROLS_MAP[signature[0]]["gen_flags_controls"])
        microcode_defs.append({
            "step": 2,
            "flags": step_2_flags,
            "module_controls": step_2_module_controls,
        })

        # If flag is the true condition, comparison is true, do the jump
        true_step_3_flags = CONTROLS_MAP[signature[0]]["true_flags"]
        true_step_3_module_controls = [
            MODULE_CONTROL["SHR"]["OUT"],
            MODULE_CONTROL["PC"]["IN"],
            MODULE_CONTROL["CU"]["STEP_RESET"],
        ]
        microcode_defs.append({
            "step": 3,
            "flags": true_step_3_flags,
            "module_controls": true_step_3_module_controls,
        })

        # If flag is the false condition, comparison is false, do not do the jump
        false_step_3_flags = CONTROLS_MAP[signature[0]]["false_flags"]
        false_step_3_module_controls = [
            MODULE_CONTROL["CU"]["STEP_RESET"],
        ]
        microcode_defs.append({
            "step": 3,
            "flags": false_step_3_flags,
            "module_controls": false_step_3_module_controls,
        })

    # Comparing to a constant value, e.g.
    # JUMP_IF_ACC_<CMP> #34 &label
    elif signature[1] == CONST:
        # First unconditional step to actually generate the flags,
        # comparing the value from memory
        step_0_flags = [FLAGS["ANY"]]
        step_0_module_controls = [
            MODULE_CONTROL["MEM"]["READ_FROM"],
            MODULE_CONTROL["ALU"]["STORE_FLAGS"],
            MODULE_CONTROL["PC"]["COUNT"],
            MODULE_CONTROL["MAR"]["COUNT"]
        ]
        step_0_module_controls.extend(CONTROLS_MAP[signature[0]]["gen_flags_controls"])
        microcode_defs.append({
            "step": 0,
            "flags": step_0_flags,
            "module_controls": step_0_module_controls,
        })

        # If flag is the true condition, comparison is true, do the jump
        true_step_1_flags = CONTROLS_MAP[signature[0]]["true_flags"]
        true_step_1_module_controls = [
            MODULE_CONTROL["MEM"]["READ_FROM"],
            MODULE_CONTROL["PC"]["IN"],
            MODULE_CONTROL["CU"]["STEP_RESET"],
        ]
        microcode_defs.append({
            "step": 1,
            "flags": true_step_1_flags,
            "module_controls": true_step_1_module_controls,
        })

        # If flag is the false condition, comparison is false, do not do the jump
        false_step_1_flags = CONTROLS_MAP[signature[0]]["false_flags"]
        false_step_1_module_controls = [
            MODULE_CONTROL["PC"]["COUNT"],
            MODULE_CONTROL["CU"]["STEP_RESET"],
        ]
        microcode_defs.append({
            "step": 1,
            "flags": false_step_1_flags,
            "module_controls": false_step_1_module_controls,
        })

    # Comparing to a module, e.g.
    # JUMP_IF_ACC_<CMP> B &label
    elif signature[1] in (A, B, C):
        # Unconditional step to generate the flags.
        step_0_flags = [FLAGS["ANY"]]
        step_0_module_controls = [
            MODULE_CONTROL[utils.component_to_module_name(signature[1])]["OUT"],
            MODULE_CONTROL["ALU"]["STORE_FLAGS"],
        ]
        step_0_module_controls.extend(CONTROLS_MAP[signature[0]]["gen_flags_controls"])
        microcode_defs.append({
            "step": 0,
            "flags": step_0_flags,
            "module_controls": step_0_module_controls,
        })

        # If flag is the true condition, comparison is true, do the jump
        true_step_1_flags = CONTROLS_MAP[signature[0]]["true_flags"]
        true_step_1_module_controls = [
            MODULE_CONTROL["MEM"]["READ_FROM"],
            MODULE_CONTROL["PC"]["IN"],
            MODULE_CONTROL["CU"]["STEP_RESET"],
        ]
        microcode_defs.append({
            "step": 1,
            "flags": true_step_1_flags,
            "module_controls": true_step_1_module_controls,
        })

        # If flag is the false condition, comparison is fasle, do not do the jump
        false_step_1_flags = CONTROLS_MAP[signature[0]]["false_flags"]
        false_step_1_module_controls = [
            MODULE_CONTROL["PC"]["COUNT"],
            MODULE_CONTROL["CU"]["STEP_RESET"],
        ]
        microcode_defs.append({
            "step": 1,
            "flags": false_step_1_flags,
            "module_controls": false_step_1_module_controls,
        })
    
    else:
        raise ValueError("Unexpected signature")

    instr_index = get_instruction_index(signature)
    data_templates = utils.assemble_explicit_instruction_steps(
        instr_index, microcode_defs
    )

    return data_templates


def supports(signature):
    """
    Whether this operation provides a definition for the given signature.

    Args:
        signature (Tuple(:mod:`Instruction component<.instruction_components>`)):
            The signature to check.
    Returns:
        bool: Whether it's supported or not.
    """
    return signature in _SUPPORTED_SIGNATURES

def gen_test_assembly():
    """
    Generate assembly code that verifies the instructions work as expected.
    """
    test_assembly = """\
        ////////////////////////////////////////////////////////////////
        // JUMP_IF_ACC_LT
        ////////////////////////////////////////////////////////////////

    // Test true cases
    &jialt_0
        SET A #12
        SET ACC #2
        JUMP_IF_ACC_LT A &jialt_1
        HALT

    &jialt_1
        SET B #123
        SET ACC #0
        JUMP_IF_ACC_LT B &jialt_2
        HALT

    &jialt_2
        SET C #12345
        SET ACC #1234
        JUMP_IF_ACC_LT C &jialt_3
        HALT

    &jialt_3
        SET SP #6000
        SET ACC #4242
        JUMP_IF_ACC_LT SP &jialt_4
        HALT

    &jialt_4
        SET ACC #1000
        JUMP_IF_ACC_LT #1001 &jialt_5
        HALT

    // Test false cases
    &jialt_5
        SET A #2
        SET ACC #2
        JUMP_IF_ACC_LT A &jialt_halt_0

        SET B #1
        SET ACC #123
        JUMP_IF_ACC_LT B &jialt_halt_1

        SET C #123
        SET ACC #12345
        JUMP_IF_ACC_LT C &jialt_halt_2

        SET SP #3545
        SET ACC #3545
        JUMP_IF_ACC_LT SP &jialt_halt_3

        SET ACC #1001
        JUMP_IF_ACC_LT #1000 &jialt_halt_4
        JUMP &jialte_0

    &jialt_halt_0
        HALT
    &jialt_halt_1
        HALT
    &jialt_halt_2
        HALT
    &jialt_halt_3
        HALT
    &jialt_halt_4
        HALT

        ////////////////////////////////////////////////////////////////
        // JUMP_IF_ACC_LTE
        ////////////////////////////////////////////////////////////////

    // Test true cases
    &jialte_0
        SET A #12
        SET ACC #2
        JUMP_IF_ACC_LTE A &jialte_1
        HALT

    &jialte_1
        SET A #123
        SET ACC #123
        JUMP_IF_ACC_LTE A &jialte_2
        HALT

    &jialte_2
        SET B #12345
        SET ACC #1234
        JUMP_IF_ACC_LTE B &jialte_3
        HALT

    &jialte_3
        SET B #6000
        SET ACC #6000
        JUMP_IF_ACC_LTE B &jialte_4
        HALT

    &jialte_4
        SET C #12345
        SET ACC #1234
        JUMP_IF_ACC_LTE C &jialte_5
        HALT

    &jialte_5
        SET C #4321
        SET ACC #4321
        JUMP_IF_ACC_LTE C &jialte_6
        HALT

    &jialte_6
        SET SP #12345
        SET ACC #1234
        JUMP_IF_ACC_LTE SP &jialte_7
        HALT

    &jialte_7
        SET SP #6000
        SET ACC #6000
        JUMP_IF_ACC_LTE SP &jialte_8
        HALT

    &jialte_8
        SET ACC #1000
        JUMP_IF_ACC_LTE #1001 &jialte_9
        HALT

    &jialte_9
        SET ACC #1111
        JUMP_IF_ACC_LTE #1111 &jialte_10
        HALT


    // Test false cases
    &jialte_10
        SET A #2
        SET ACC #12
        JUMP_IF_ACC_LTE A &jialte_halt_0

        SET B #1
        SET ACC #123
        JUMP_IF_ACC_LTE B &jialte_halt_1

        SET C #123
        SET ACC #12345
        JUMP_IF_ACC_LTE C &jialte_halt_2

        SET SP #3545
        SET ACC #50000
        JUMP_IF_ACC_LTE SP &jialte_halt_3

        SET ACC #1001
        JUMP_IF_ACC_LTE #1000 &jialte_halt_4
        JUMP &jiagte_0

    &jialte_halt_0
        HALT
    &jialte_halt_1
        HALT
    &jialte_halt_2
        HALT
    &jialte_halt_3
        HALT
    &jialte_halt_4
        HALT

        ////////////////////////////////////////////////////////////////
        // JUMP_IF_ACC_GTE
        ////////////////////////////////////////////////////////////////

    // Test true cases
    &jiagte_0
        SET A #12
        SET ACC #20
        JUMP_IF_ACC_GTE A &jiagte_1
        HALT

    &jiagte_1
        SET A #123
        SET ACC #123
        JUMP_IF_ACC_GTE A &jiagte_2
        HALT

    &jiagte_2
        SET B #1234
        SET ACC #12341
        JUMP_IF_ACC_GTE B &jiagte_3
        HALT

    &jiagte_3
        SET B #6000
        SET ACC #6000
        JUMP_IF_ACC_GTE B &jiagte_4
        HALT

    &jiagte_4
        SET C #123
        SET ACC #1234
        JUMP_IF_ACC_GTE C &jiagte_5
        HALT

    &jiagte_5
        SET C #555
        SET ACC #555
        JUMP_IF_ACC_GTE C &jiagte_6
        HALT

    &jiagte_6
        SET SP #500
        SET ACC #1000
        JUMP_IF_ACC_GTE SP &jiagte_7
        HALT

    &jiagte_7
        SET SP #999
        SET ACC #999
        JUMP_IF_ACC_GTE SP &jiagte_8
        HALT

    &jiagte_8
        SET ACC #1000
        JUMP_IF_ACC_GTE #3 &jiagte_9
        HALT

    &jiagte_9
        SET ACC #1111
        JUMP_IF_ACC_GTE #1111 &jiagte_10
        HALT


    // Test false cases
    &jiagte_10
        SET A #24
        SET ACC #12
        JUMP_IF_ACC_GTE A &jiagte_halt_0

        SET B #1
        SET ACC #0
        JUMP_IF_ACC_GTE B &jiagte_halt_1

        SET C #987
        SET ACC #654
        JUMP_IF_ACC_GTE C &jiagte_halt_2

        SET SP #50000
        SET ACC #352
        JUMP_IF_ACC_GTE SP &jiagte_halt_3

        SET ACC #10001
        JUMP_IF_ACC_GTE #12000 &jiagte_halt_4
        JUMP &jiagt_0

    &jiagte_halt_0
        HALT
    &jiagte_halt_1
        HALT
    &jiagte_halt_2
        HALT
    &jiagte_halt_3
        HALT
    &jiagte_halt_4
        HALT

        ////////////////////////////////////////////////////////////////
        // JUMP_IF_ACC_GT
        ////////////////////////////////////////////////////////////////

    // Test true cases
    &jiagt_0
        SET A #12
        SET ACC #200
        JUMP_IF_ACC_GT A &jiagt_1
        HALT

    &jiagt_1
        SET B #123
        SET ACC #9999
        JUMP_IF_ACC_GT B &jiagt_2
        HALT

    &jiagt_2
        SET C #100
        SET ACC #10000
        JUMP_IF_ACC_GT C &jiagt_3
        HALT

    &jiagt_3
        SET SP #6000
        SET ACC #7000
        JUMP_IF_ACC_GT SP &jiagt_4
        HALT

    &jiagt_4
        SET ACC #1111
        JUMP_IF_ACC_GT #1110 &jiagt_5
        HALT

    // Test false cases
    &jiagt_5
        SET A #2
        SET ACC #2
        JUMP_IF_ACC_GT A &jiagt_halt_0

        SET B #1112
        SET ACC #12
        JUMP_IF_ACC_GT B &jiagt_halt_1

        SET C #9987
        SET ACC #345
        JUMP_IF_ACC_GT C &jiagt_halt_2

        SET SP #748
        SET ACC #333
        JUMP_IF_ACC_GT SP &jiagt_halt_3

        SET ACC #10
        JUMP_IF_ACC_GT #15 &jiagt_halt_4
        JUMP &jiagt_done

    &jiagt_halt_0
        HALT
    &jiagt_halt_1
        HALT
    &jiagt_halt_2
        HALT
    &jiagt_halt_3
        HALT
    &jiagt_halt_4
        HALT

    &jiagt_done
        NOOP
    """

    return textwrap.dedent(test_assembly)

def gen_all_assembly():
    """
    Generate assembly lines for all the instructions this module supports.

    Returns:
        list(str): The assembly lines.
    """
    ret = []
    for signature in _SUPPORTED_SIGNATURES:
        ret.append(" ".join(
            [component_to_assembly(component) for component in signature]
        ))
    return ret