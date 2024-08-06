"""
The LOAD and STORE operations.

Load a value from or wtire a value to memory,
"""

import textwrap

from ..instruction_listings import get_instruction_index
from ..data_structures import Word
from ..instruction_components import (
    LOAD,
    STORE,
    ACC,
    A,
    B,
    C,
    M_ACC,
    M_A,
    M_B,
    M_C,
    M_SP,
    M_CONST,
    memory_ref_to_component,
    component_to_assembly,
)
from .. import number_utils
from ..language_defs import (
    MODULE_CONTROL,
    FLAGS,
)
from . import utils

_SUPPORTED_SIGNATURES = (
    (LOAD, M_ACC, A),
    (LOAD, M_ACC, B),
    (LOAD, M_ACC, C),
    (LOAD, M_A, ACC),
    (LOAD, M_A, B),
    (LOAD, M_A, C),
    (LOAD, M_B, ACC),
    (LOAD, M_B, A),
    (LOAD, M_B, C),
    (LOAD, M_C, ACC),
    (LOAD, M_C, A),
    (LOAD, M_C, B),
    (LOAD, M_SP, ACC),
    (LOAD, M_SP, A),
    (LOAD, M_SP, B),
    (LOAD, M_SP, C),
    (LOAD, M_CONST, ACC),
    (LOAD, M_CONST, A),
    (LOAD, M_CONST, B),
    (LOAD, M_CONST, C),
    (STORE, ACC, M_A),
    (STORE, ACC, M_B),
    (STORE, ACC, M_C),
    (STORE, ACC, M_SP),
    (STORE, ACC, M_CONST),
    (STORE, A, M_ACC),
    (STORE, A, M_B),
    (STORE, A, M_C),
    (STORE, A, M_SP),
    (STORE, A, M_CONST),
    (STORE, B, M_ACC),
    (STORE, B, M_A),
    (STORE, B, M_C),
    (STORE, B, M_SP),
    (STORE, B, M_CONST),
    (STORE, C, M_ACC),
    (STORE, C, M_A),
    (STORE, C, M_B),
    (STORE, C, M_SP),
    (STORE, C, M_CONST),
)


def generate_machinecode(signature, const_tokens):
    """
    Generate machinecode for the LOAD and STORE instructions.

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

    machinecode = [
        Word(value=get_instruction_index(signature))
    ]

    for const_token in const_tokens:
        machinecode.append(Word(const_token=const_token))

    return machinecode


def generate_microcode_templates():
    """
    Generate microcode for the LOAD and STORE operations.

    Returns:
        list(DataTemplate): DataTemplates for all the LOAD and STORE
        microcode.
    """
    data_templates = []

    for signature in _SUPPORTED_SIGNATURES:
        instr_index = get_instruction_index(signature)
        instr_index_bitdef = number_utils.number_to_bitstring(
            instr_index, bit_width=8
        )
        flags_bitdefs = [FLAGS["ANY"]]

        if signature[0] == LOAD:
            if signature[1] == M_CONST:
                # E.g. LOAD [#123] ACC/A/B/C
                # MAR is already pointing at the mem location holding 
                # the address to read from thanks to the fetch.
                # Read from memory into module, increment PC
                control_steps = [
                    [
                        MODULE_CONTROL["MEM"]["READ_FROM"],
                        MODULE_CONTROL["MAR"]["IN"],
                        MODULE_CONTROL["PC"]["COUNT"],
                    ],
                    [
                        MODULE_CONTROL["MEM"]["READ_FROM"],
                        MODULE_CONTROL[
                            utils.component_to_module_name(signature[2])
                        ]["IN"],
                    ]
                ]
            else:
                # E.g. LOAD [ACC/A/B/C/SP] ACC/A/B/C 
                control_steps = [
                    [
                        MODULE_CONTROL[
                            utils.component_to_module_name(
                                memory_ref_to_component(
                                    signature[1]
                                )
                            )
                        ]["OUT"],
                        MODULE_CONTROL["MAR"]["IN"],
                    ],
                    [
                        MODULE_CONTROL["MEM"]["READ_FROM"],
                        MODULE_CONTROL[
                            utils.component_to_module_name(signature[2])
                        ]["IN"],
                    ],
                ]
        elif signature[0] == STORE:
            if signature[2] == M_CONST:
                # E.g. STORE ACC/A/B/C/SP [#123]
                # MAR is already pointing at the mem location holding 
                # the address to read from thanks to the fetch.
                control_steps = [
                    [
                        MODULE_CONTROL["MEM"]["READ_FROM"],
                        MODULE_CONTROL["MAR"]["IN"],
                        MODULE_CONTROL["PC"]["COUNT"],
                    ],
                    [
                        MODULE_CONTROL["MEM"]["WRITE_TO"],
                        MODULE_CONTROL[
                            utils.component_to_module_name(signature[1])
                        ]["OUT"],
                    ]
                ]
            else:
                # E.g. STORE ACC/A/B/C [ACC/A/B/C/SP]
                control_steps = [
                    [
                        MODULE_CONTROL[
                            utils.component_to_module_name(
                                memory_ref_to_component(
                                    signature[2]
                                )
                            )
                        ]["OUT"],
                        MODULE_CONTROL["MAR"]["IN"],
                    ],
                    [
                        MODULE_CONTROL["MEM"]["WRITE_TO"],
                        MODULE_CONTROL[
                            utils.component_to_module_name(signature[1])
                        ]["OUT"],
                    ],
                ]
        else:
            raise RuntimeError(
                "Unexpected signature {sig} in load/store "
                "microcode generation".format(sig=signature)
            )

        templates = utils.assemble_instruction_steps(
            instr_index_bitdef, flags_bitdefs, control_steps
        )
        data_templates.extend(templates)

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
    return signature in _SUPPORTED_SIGNATURES\


def gen_test_assembly():
    """
    Generate assembly code that verifies the instructions work as expected.
    """

    test_assembly = """\
        ////////////////////////////////////////////////////////////////
        // LOAD
        ////////////////////////////////////////////////////////////////

    $v_load_0 #24004
    &load_0
        SET ACC $v_load_0
        LOAD [ACC] ACC
        JUMP_IF_ACC_EQ #24004 &load_1
        HALT

    $v_load_1 #11709
    &load_1
        SET ACC $v_load_1
        LOAD [ACC] A
        SET ACC #11709
        JUMP_IF_ACC_EQ A &load_2
        HALT

    $v_load_2 #59692
    &load_2
        SET ACC $v_load_2
        LOAD [ACC] B
        SET ACC #59692
        JUMP_IF_ACC_EQ B &load_3
        HALT

    $v_load_3 #12087
    &load_3
        SET ACC $v_load_3
        LOAD [ACC] C
        SET ACC #12087
        JUMP_IF_ACC_EQ C &load_4
        HALT

    $v_load_4 #20982
    &load_4
        SET A $v_load_4
        LOAD [A] ACC
        JUMP_IF_ACC_EQ #20982 &load_5
        HALT

    $v_load_5 #51597
    &load_5
        SET A $v_load_5
        LOAD [A] A
        SET ACC #51597
        JUMP_IF_ACC_EQ A &load_6
        HALT

    $v_load_6 #22009
    &load_6
        SET A $v_load_6
        LOAD [A] B
        SET ACC #22009
        JUMP_IF_ACC_EQ B &load_7
        HALT

    $v_load_7 #11703
    &load_7
        SET A $v_load_7
        LOAD [A] C
        SET ACC #11703
        JUMP_IF_ACC_EQ C &load_8
        HALT

    $v_load_8 #57854
    &load_8
        SET B $v_load_8
        LOAD [B] ACC
        JUMP_IF_ACC_EQ #57854 &load_9
        HALT

    $v_load_9 #37360
    &load_9
        SET B $v_load_9
        LOAD [B] A
        SET ACC #37360
        JUMP_IF_ACC_EQ A &load_10
        HALT

    $v_load_10 #57819
    &load_10
        SET B $v_load_10
        LOAD [B] B
        SET ACC #57819
        JUMP_IF_ACC_EQ B &load_11
        HALT

    $v_load_11 #60912
    &load_11
        SET B $v_load_11
        LOAD [B] C
        SET ACC #60912
        JUMP_IF_ACC_EQ C &load_12
        HALT

    $v_load_12 #38245
    &load_12
        SET C $v_load_12
        LOAD [C] ACC
        JUMP_IF_ACC_EQ #38245 &load_13
        HALT

    $v_load_13 #25454
    &load_13
        SET C $v_load_13
        LOAD [C] A
        SET ACC #25454
        JUMP_IF_ACC_EQ A &load_14
        HALT

    $v_load_14 #25444
    &load_14
        SET C $v_load_14
        LOAD [C] B
        SET ACC #25444
        JUMP_IF_ACC_EQ B &load_15
        HALT

    $v_load_15 #20527
    &load_15
        SET C $v_load_15
        LOAD [C] C
        SET ACC #20527
        JUMP_IF_ACC_EQ C &load_16
        HALT

    $v_load_16 #60336
    &load_16
        SET SP $v_load_16
        LOAD [SP] ACC
        JUMP_IF_ACC_EQ #60336 &load_17
        HALT

    $v_load_17 #56769
    &load_17
        SET SP $v_load_17
        LOAD [SP] A
        SET ACC #56769
        JUMP_IF_ACC_EQ A &load_18
        HALT

    $v_load_18 #49044
    &load_18
        SET SP $v_load_18
        LOAD [SP] B
        SET ACC #49044
        JUMP_IF_ACC_EQ B &load_19
        HALT

    $v_load_19 #34177
    &load_19
        SET SP $v_load_19
        LOAD [SP] C
        SET ACC #34177
        JUMP_IF_ACC_EQ C &load_20
        HALT

    $v_load_20 #56580
    &load_20
        LOAD [$v_load_20] ACC
        JUMP_IF_ACC_EQ #56580 &load_21
        HALT

    $v_load_21 #47253
    &load_21
        LOAD [$v_load_21] A
        SET ACC #47253
        JUMP_IF_ACC_EQ A &load_22
        HALT

    $v_load_22 #55439
    &load_22
        LOAD [$v_load_22] B
        SET ACC #55439
        JUMP_IF_ACC_EQ B &load_23
        HALT

    $v_load_23 #7661
    &load_23
        LOAD [$v_load_23] C
        SET ACC #7661
        JUMP_IF_ACC_EQ C &store_0
        HALT

        ////////////////////////////////////////////////////////////////
        // STORE
        ////////////////////////////////////////////////////////////////

    $v_store_0
    &store_0
        SET ACC $v_store_0
        STORE ACC [ACC]
        LOAD [ACC] ACC
        JUMP_IF_ACC_EQ $v_store_0 &store_1
        HALT

    $v_store_1
    &store_1
        SET ACC #31763
        SET A $v_store_1
        STORE ACC [A]
        LOAD [A] ACC
        JUMP_IF_ACC_EQ #31763 &store_2
        HALT

    $v_store_2
    &store_2
        SET ACC #35606
        SET B $v_store_2
        STORE ACC [B]
        LOAD [B] ACC
        JUMP_IF_ACC_EQ #35606 &store_3
        HALT

    $v_store_3
    &store_3
        SET ACC #27292
        SET C $v_store_3
        STORE ACC [C]
        LOAD [C] ACC
        JUMP_IF_ACC_EQ #27292 &store_4
        HALT

    $v_store_4
    &store_4
        SET ACC #13156
        SET SP $v_store_4
        STORE ACC [SP]
        LOAD [SP] ACC
        JUMP_IF_ACC_EQ #13156 &store_5
        HALT

    $v_store_5
    &store_5
        SET ACC #36181
        STORE ACC [$v_store_5]
        LOAD [$v_store_5] ACC
        JUMP_IF_ACC_EQ #36181 &store_6
        HALT

    $v_store_6
    &store_6
        SET A #11935
        SET ACC $v_store_6
        STORE A [ACC]
        LOAD [ACC] ACC
        JUMP_IF_ACC_EQ #11935 &store_7
        HALT

    $v_store_7
    &store_7
        SET A $v_store_7
        STORE A [A]
        LOAD [A] ACC
        JUMP_IF_ACC_EQ $v_store_7 &store_8
        HALT

    $v_store_8
    &store_8
        SET A #27215
        SET B $v_store_8
        STORE A [B]
        LOAD [B] ACC
        JUMP_IF_ACC_EQ #27215 &store_9
        HALT

    $v_store_9
    &store_9
        SET A #31533
        SET C $v_store_9
        STORE A [C]
        LOAD [C] ACC
        JUMP_IF_ACC_EQ #31533 &store_10
        HALT

    $v_store_10
    &store_10
        SET A #65214
        SET SP $v_store_10
        STORE A [SP]
        LOAD [SP] ACC
        JUMP_IF_ACC_EQ #65214 &store_11
        HALT

    $v_store_11
    &store_11
        SET A #25149
        STORE A [$v_store_11]
        LOAD [$v_store_11] ACC
        JUMP_IF_ACC_EQ #25149 &store_12
        HALT

    $v_store_12
    &store_12
        SET B #61844
        SET ACC $v_store_12
        STORE B [ACC]
        LOAD [ACC] ACC
        JUMP_IF_ACC_EQ #61844 &store_13
        HALT

    $v_store_13
    &store_13
        SET B #22749
        SET A $v_store_13
        STORE B [A]
        LOAD [A] ACC
        JUMP_IF_ACC_EQ #22749 &store_14
        HALT

    $v_store_14
    &store_14
        SET B $v_store_14
        STORE B [B]
        LOAD [B] ACC
        JUMP_IF_ACC_EQ $v_store_14 &store_15
        HALT

    $v_store_15
    &store_15
        SET B #21277
        SET C $v_store_15
        STORE B [C]
        LOAD [C] ACC
        JUMP_IF_ACC_EQ #21277 &store_16
        HALT

    $v_store_16
    &store_16
        SET B #64660
        SET SP $v_store_16
        STORE B [SP]
        LOAD [SP] ACC
        JUMP_IF_ACC_EQ #64660 &store_17
        HALT

    $v_store_17
    &store_17
        SET B #54157
        STORE B [$v_store_17]
        LOAD [$v_store_17] ACC
        JUMP_IF_ACC_EQ #54157 &store_18
        HALT

    $v_store_18
    &store_18
        SET C #46522
        SET ACC $v_store_18
        STORE C [ACC]
        LOAD [ACC] ACC
        JUMP_IF_ACC_EQ #46522 &store_19
        HALT

    $v_store_19
    &store_19
        SET C #7117
        SET A $v_store_19
        STORE C [A]
        LOAD [A] ACC
        JUMP_IF_ACC_EQ #7117 &store_20
        HALT

    $v_store_20
    &store_20
        SET C #49497
        SET B $v_store_20
        STORE C [B]
        LOAD [B] ACC
        JUMP_IF_ACC_EQ #49497 &store_21
        HALT

    $v_store_21
    &store_21
        SET C $v_store_21
        STORE C [C]
        LOAD [C] ACC
        JUMP_IF_ACC_EQ $v_store_21 &store_22
        HALT

    $v_store_22
    &store_22
        SET C #12486
        SET SP $v_store_22
        STORE C [SP]
        LOAD [SP] ACC
        JUMP_IF_ACC_EQ #12486 &store_23
        HALT

    $v_store_23
    &store_23
        SET C #63220
        STORE C [$v_store_23]
        LOAD [$v_store_23] ACC
        JUMP_IF_ACC_EQ #63220 &store_done
        HALT

    &store_done
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
