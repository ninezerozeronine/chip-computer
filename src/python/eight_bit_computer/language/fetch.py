"""
The fetch steps
"""

from .definitions import MODULE_CONTROL, STEPS, EMPTY_ADDRESS
from .. import utils as language_utils
from .. import utils as common_utils


def generate_microcode_templates():
    """
    Generate datatemplates for all the fetch steps.
    """

    return [fetch_step_0(), fetch_step_1()]


def fetch_step_0():
    """
    Create template for the first fetch step
    """

    address_bitdef = common_utils.merge_bitdefs(
        [
            EMPTY_ADDRESS,
            STEPS[0],
        ]
    )

    control_bitdef = common_utils.merge_bitdefs(
        [
            MODULE_CONTROL["PC"]["OUT"],
            MODULE_CONTROL["MAR"]["IN"],
        ]
    )
    control_bitdef = common_utils.fill_bitdef(control_bitdef, "0")

    return language_utils.DataTemplate(
        address_range=address_bitdef, data=control_bitdef
    )


def fetch_step_1():
    """
    Create template for the second fetch step
    """
    address_bitdef = common_utils.merge_bitdefs(
        [
            EMPTY_ADDRESS,
            STEPS[1],
        ]
    )

    control_bitdef = common_utils.merge_bitdefs(
        [
            MODULE_CONTROL["PC"]["COUNT"],
            MODULE_CONTROL["RAM"]["OUT"],
            MODULE_CONTROL["RAM"]["SEL_PROG_MEM"],
            MODULE_CONTROL["IR"]["IN"],
        ]
    )
    control_bitdef = common_utils.fill_bitdef(control_bitdef, "0")
    return language_utils.DataTemplate(
        address_range=address_bitdef, data=control_bitdef
    )
