from .. import listings
from ..machinecode import Word
from ..components import NOOP

_SUPPORTED_SIGNATURES = frozenset([
    (NOOP,),
])


def generate_machinecode(signature, const_tokens):
    """

    """
    if signature not in _SUPPORTED_SIGNATURES:
        raise ValueError

    return [
        Word(value=listings.get_instruction_index(signature))
    ]


def generate_microcode(signature):
    """

    """
    pass


def supports(signature):
    return signature in _SUPPORTED_SIGNATURES
