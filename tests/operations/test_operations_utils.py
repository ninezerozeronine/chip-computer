import pytest

from sixteen_bit_computer.operations import utils
from sixteen_bit_computer.language_defs import (
    MODULE_CONTROL,
    FLAGS,
    ALU_CONTROL_FLAGS,
    STEPS
)
from sixteen_bit_computer import bitdef
from sixteen_bit_computer.data_structures import DataTemplate

def test_assemble_instruction_steps_raises():
    instr_bitdef = "00001111"
    flags_bitdefs = [
        FLAGS["EQUAL"]["HIGH"]
    ]
    control_steps = [
        [MODULE_CONTROL["ACC"]["IN"]],
        [MODULE_CONTROL["ACC"]["IN"]],
        [MODULE_CONTROL["ACC"]["IN"]],
        [MODULE_CONTROL["ACC"]["IN"]],
        [MODULE_CONTROL["ACC"]["IN"]],
        [MODULE_CONTROL["ACC"]["IN"]],
        [MODULE_CONTROL["ACC"]["IN"]],
        [MODULE_CONTROL["ACC"]["IN"]],
    ]

    with pytest.raises(ValueError):
        utils.assemble_instruction_steps(instr_bitdef, flags_bitdefs, control_steps)


def test_assemble_instruction_steps():
    instr_bitdef = "00001111"
    flags_bitdefs = [
        FLAGS["EQUAL"]["HIGH"],
        FLAGS["NEGATIVE"]["HIGH"],
    ]
    control_steps = [
        [
            MODULE_CONTROL["ACC"]["IN"]
        ],
        [
            MODULE_CONTROL["ACC"]["OUT"]
        ],
    ]

    padded_instruction_bitdef = "{instr}.......".format(
        instr=instr_bitdef
    )

    expected = []
    step_0_addr = bitdef.merge([
        padded_instruction_bitdef,
        FLAGS["EQUAL"]["HIGH"],
        FLAGS["NEGATIVE"]["HIGH"],
        STEPS[2]
    ])
    step_0_data = bitdef.fill(MODULE_CONTROL["ACC"]["IN"], "0")
    expected.append(DataTemplate(address_range=step_0_addr, data=step_0_data))

    step_1_addr = bitdef.merge([
        padded_instruction_bitdef,
        FLAGS["EQUAL"]["HIGH"],
        FLAGS["NEGATIVE"]["HIGH"],
        STEPS[3]
    ])
    step_1_data = bitdef.merge(
        [
            MODULE_CONTROL["ACC"]["OUT"],
            MODULE_CONTROL["CU"]["STEP_RESET"],
        ]
    )
    step_1_data = bitdef.fill(step_1_data, "0")
    expected.append(DataTemplate(address_range=step_1_addr, data=step_1_data))

    res = utils.assemble_instruction_steps(instr_bitdef, flags_bitdefs, control_steps)

    assert res == expected


def test_assemble_explicit_instruction_steps():

    microcode_defs = []

    step_0_flags = [FLAGS["ANY"]]
    step_0_module_controls = [
        MODULE_CONTROL["B"]["OUT"],
        MODULE_CONTROL["ALU"]["A_IS_BUS"],
        MODULE_CONTROL["ALU"]["STORE_FLAGS"],
    ]
    step_0_module_controls.extend(ALU_CONTROL_FLAGS["A"])
    microcode_defs.append({
        "step": 0,
        "flags": step_0_flags,
        "module_controls": step_0_module_controls,
    })

    # If the zero flag was set, perform the jump.
    #
    # PC is currently pointing at the location in memory that holds the
    # location to jump to (this was the second instruction word).
    # Set the MAR with the value of PC so it can then be loaded from memory.
    true_step_1_flags = [FLAGS["ZERO"]["HIGH"]]
    true_step_1_module_controls = [
        MODULE_CONTROL["PC"]["OUT"],
        MODULE_CONTROL["MAR"]["IN"],
    ]
    microcode_defs.append({
        "step": 1,
        "flags": true_step_1_flags,
        "module_controls": true_step_1_module_controls,
    })

    # Next step of the jump.
    #
    # Set PC to the value of the second instruction word and reset the
    # microcode step to fetch the next instruction from that location.
    true_step_2_flags = [FLAGS["ANY"]]
    true_step_2_module_controls = [
        MODULE_CONTROL["MEM"]["READ_FROM"],
        MODULE_CONTROL["PC"]["IN"],
        MODULE_CONTROL["CU"]["STEP_RESET"],
    ]
    microcode_defs.append({
        "step": 2,
        "flags": true_step_2_flags,
        "module_controls": true_step_2_module_controls,
    })

    # If the zero flag wasn't set, increment the program counter to move past
    # the constant that would have been jumped to and reset the step counter.
    # to fetch the next instruction.
    false_step_1_flags = [FLAGS["ZERO"]["LOW"]]
    false_step_1_module_controls = [
        MODULE_CONTROL["PC"]["COUNT"],
        MODULE_CONTROL["CU"]["STEP_RESET"],
    ]
    microcode_defs.append({
        "step": 1,
        "flags": false_step_1_flags,
        "module_controls": false_step_1_module_controls,
    })

    instr_bitdef = "00000101"
    padded_instruction_bitdef = "{instr}.......".format(
        instr=instr_bitdef
    )

    expected = []

    step_0_addr = bitdef.merge([
        padded_instruction_bitdef,
        STEPS[2]
    ])
    step_0_data = bitdef.fill(bitdef.merge(step_0_module_controls), "0")
    expected.append(DataTemplate(address_range=step_0_addr, data=step_0_data))

    true_step_1_addr = bitdef.merge([
        padded_instruction_bitdef,
        FLAGS["ZERO"]["HIGH"],
        STEPS[3],
    ])
    true_step_1_data = bitdef.fill(bitdef.merge(true_step_1_module_controls), "0")
    expected.append(DataTemplate(address_range=true_step_1_addr, data=true_step_1_data))

    true_step_2_addr = bitdef.merge([
        padded_instruction_bitdef,
        STEPS[4],
    ])
    true_step_2_data = bitdef.fill(bitdef.merge(true_step_2_module_controls), "0")
    expected.append(DataTemplate(address_range=true_step_2_addr, data=true_step_2_data))

    false_step_1_addr = bitdef.merge([
        padded_instruction_bitdef,
        FLAGS["ZERO"]["LOW"],
        STEPS[3],
    ])
    false_step_1_data = bitdef.fill(bitdef.merge(false_step_1_module_controls), "0")
    expected.append(DataTemplate(address_range=false_step_1_addr, data=false_step_1_data))

    assert expected == utils.assemble_explicit_instruction_steps(5, microcode_defs)