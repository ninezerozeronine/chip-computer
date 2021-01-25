"""
Definition of patterns - arrangements of tokens that have a higher
meaning.
"""

from abc import ABC, abstractmethod

from .tokens import (
    ALIAS,
    NUMBER,
)
from ..instructions import components
from ..instructions.listings import INSTRUCTION_SIGNATURES


def get_all_patterns():
    """
    Get all the defined patterns.

    Returns:
        tuple(Pattern): A tuple of all the pattern classes (excluding
        the base class)
    """
    return (
        AliasDefinition,
    )


class Pattern(ABC):
    """
    Base class for all patterns.

    A pattern is an arrangement of tokens (potentially only tokens with
    specific values) that has a higher level meaning.

    A simple pattern could be a Marker, it's a single token, the marker.
    E.g.::

        $mymarker

    A more complex pattern could be a definition of an alias, it's two
    tokens, an alias, and then a number. E.g.::

        !my_alias #123
    """

    def __init__(self, tokens):
        """
        Initialise the class.

        Args:
            tokens (list(Token)): The list of tokens from the assembler
                that make up this pattern.
        """

        self._tokens = tokens
        self._machinecode = self._generate_machinecode()

    @property
    def tokens(self):
        return self._tokens

    @property
    def machinecode(self):
        return self._machinecode

    def _generate_machinecode(self):
        return []

    @classmethod
    @abstractmethod
    def from_tokens(cls, tokens):
        return None


class AliasDefinition(Pattern):
    """
    Represents an alias being defined as a specific value.
    """

    @classmethod
    def from_tokens(cls, tokens):
        if (len(tokens) == 2
                and isinstance(tokens[0], ALIAS)
                and isinstance(tokens[1], NUMBER)):
            return cls(tokens)
        else:
            return None


# class DataSet(Pattern):
#     def __init__(self, tokens):
#         self.tokens = tokens

#     @classmethod
#     def from_tokens(cls, tokens):
#         for token in tokens:
#             if not isinstance(token, CONSTANT):
#                 return None
#         return cls(tokens)

#     def generate_machinecode(self):
#         return [Word, Word]

# class Instruction(Pattern):
#     def __init__(self, tokens, signature):
#         super().__init__(tokens)
#         self.signature = signature

#     @classmethod
#     def from_tokens(cls, tokens):
#         instruction_components = []
#         for token in tokens:
#             instruction_component = token_to_component(token)
#             if instruction_component is None:
#                 return None
#             else:
#                 instruction_components.append(instruction_component)

#         signature = tuple(instruction_components)
#         if signature in INSTRUCTION_SIGNATURES:
#             return cls(tokens, signature)
#         else:
#             return None


#     def _generate_machinecode(self):
#         return [Word, Word]


# def token_to_component(token):
#     token_type = type(token)
#     if token_type in _TOKEN_TO_COMPONENT:
#         return _TOKEN_TO_COMPONENT[token_type]
#     else
#         return None


# _TOKEN_TO_COMPONENT = {
#     ALIAS: components.CONST,
#     NUMBER: components.CONST,
# }
