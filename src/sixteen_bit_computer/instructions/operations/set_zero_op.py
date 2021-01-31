from .. import listings
from ..machinecode import Word
from ..components import SET_ZERO, ACC, A, B, C

_SUPPORTED_SIGNATURES = frozenset([
    (SET_ZERO, ACC),
    (SET_ZERO, A),
    (SET_ZERO, B),
    (SET_ZERO, C),
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
