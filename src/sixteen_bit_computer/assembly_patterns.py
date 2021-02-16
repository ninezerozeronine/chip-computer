"""
Definition of patterns - arrangements of tokens that have a higher
meaning.
"""

from abc import ABC, abstractmethod

from .assembly_tokens import (
    ALIAS,
    NUMBER,
    MEMREF,
)
from . import instruction_listings


def get_all_patterns():
    """
    Get all the defined patterns.

    Returns:
        tuple[Pattern]: A tuple of all the pattern classes (excluding
        the base class)
    """
    return (
        NullPattern,
        AliasDefinition,
        Instruction,
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

        The machinecode that the pattern generates (if any) is generated
        on initialisation.

        Args:
            tokens (List[Token]): The list of tokens from the assembler
                that make up this pattern.
        """

        self._tokens = tokens
        self._machinecode = self._generate_machinecode()

    @property
    def tokens(self):
        """
        List[Token]: The tokens that matched this pattern.
        """
        return self._tokens

    @property
    def machinecode(self):
        """
        List[Word]: The machine code this pattern generates.

        If the pattern generates no machine code this is an empty list.
        """
        return self._machinecode

    def _generate_machinecode(self):
        """
        Generate the machinecode for this pattern.

        Returns:
            List[Word]: List of machinecode words or an empty list if
            the pattern generates no machinecode.
        """
        return []

    @classmethod
    @abstractmethod
    def from_tokens(cls, tokens):
        """
        Attempt to create an instance of this pattern from Tokens.

        If the tokens don't match the pattern, None is returned.

        Args:
            tokens (List[Token]): List of tokens from the assembler to
                attempt to match
        Returns:
            None or List[Token]: None if the tokens didn't match, the
            created pattern if they did.
        """
        return None


class NullPattern(Pattern):
    """
    Pattern that represents no tokens.

    Useful for compatability and code streamlining so things ilke empty
    lines and lines that are just comments don't have to be treated
    specially.
    """

    @classmethod
    def from_tokens(cls, tokens):
        if not tokens:
            return cls([])
        else:
            return None


class AliasDefinition(Pattern):
    """
    Represents an alias being defined as a specific value.

    E.g.::

        !my_alias #23
    """

    @classmethod
    def from_tokens(cls, tokens):
        if (len(tokens) == 2
                and isinstance(tokens[0], ALIAS)
                and isinstance(tokens[1], NUMBER)):
            return cls(tokens)
        else:
            return None

    @property
    def name(self):
        """
        str: The name of the defined alias.
        """

        return self.tokens[0].value

    @property
    def value(self):
        """
        int: The value of the defined alias.
        """
        return self.tokens[1].value


class Instruction(Pattern):
    """
    An instruction.
    """

    def __init__(self, tokens, signature):
        self.signature = signature
        super().__init__(tokens)

    @classmethod
    def from_tokens(cls, tokens):
        instruction_components = []
        for token in tokens:
            instruction_component = token.component
            if instruction_component is None:
                return None
            else:
                instruction_components.append(instruction_component)

        signature = tuple(instruction_components)
        if instruction_listings.is_supported_signature(signature):
            return cls(tokens, signature)
        else:
            return None

    def _generate_machinecode(self):
        machinecode_func = instruction_listings.get_machinecode_function(self.signature)
        constant_tokens = []
        for token in self.tokens:
            if isinstance(token, MEMREF):
                token = token.inner_token
            if token.is_const():
                constant_tokens.append(token)

        return machinecode_func(self.signature, constant_tokens)


# class Marker(Pattern):
#     pass
#     pass


# class MarkerDefinition(Pattern):
#     pass
#     pass


# class DataSet(Pattern):
#     def __init__(self, tokens):
#         self.tokens = tokens

#     @classmethod
#     def from_tokens(cls, tokens):
#         for token in tokens:
#             if not isinstance(token, (NUMBER, ALIAS, MARKER, ASCII):
#                 return None
#         return cls(tokens)

#     def generate_machinecode(self):
#         return [Word, Word]
