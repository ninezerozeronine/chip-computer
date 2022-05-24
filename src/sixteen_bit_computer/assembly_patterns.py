"""
Definition of patterns - arrangements of tokens that have a higher
meaning.
"""

from abc import ABC, abstractmethod

from .assembly_tokens import (
    ALIAS,
    NUMBER,
    ANCHOR,
    LABEL,
    VARIABLE,
    MEMREF,
)
from .instruction_components import CONST
from . import instruction_listings
from .data_structures import Word


def get_all_patterns():
    """
    Get all the defined patterns.

    Returns:
        tuple[Pattern]: A tuple of all the pattern classes (excluding
        the base class)
    """
    return (
        NullPattern,
        Alias,
        Label,
        Variable,
        VariableDefinition,
        Instruction,
    )


class Pattern(ABC):
    """
    Base class for all patterns.

    A pattern is an arrangement of tokens (potentially only tokens with
    specific values) that has a higher level meaning.

    A simple pattern could be a label, it's a single token, the label.
    E.g.::

        &loopstart
            SETZERO A

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


class Alias(Pattern):
    """
    Represents an alias being defined as a specific value.

    An alias is a convenience to allow a string to be used in place of
    a number constant. E.g. instead of having to hardcode ``#10`` in
    many places in the assmebly code to represent (say) the max number of
    enemies in a game, an alias ``MAX_ENEMIES`` can be defined instead.

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


class Anchor(Pattern):
    """
    A way to pin machine code to a specific location in memory.

    The machine code that follows an anchor will start at the address
    defined by the anchor.

    E.g., in::

        // Define an anchor
        @ #67
            NOOP
            SET_ZERO A

        @ #0XFCCE
        &loopstart
            LOAD [#21] B


    The ``NOOP`` instruction will be placed at ``67`` and the
    ``LOAD [#21] B`` instruction will be placed at 0XFCCE.
    """

    @classmethod
    def from_tokens(cls, tokens):
        if (len(tokens) == 2
                and isinstance(tokens[0], ANCHOR)
                and isinstance(tokens[1], NUMBER)):
            return cls(tokens)
        else:
            return None

    @property
    def location(self):
        """
        int: The location this anchor sets.
        """
        return self.tokens[1].value


class Label(Pattern):
    """
    Label a location in assembly so it can be referenced.

    Labels are a convenience that the assembler provides to easily
    point to a certain instruction in the machinecode.

    When declared, the value of the label is set to the index of the
    machinecode that follows it.

    It is typically used as an index to pass to a JUMP or CALL
    instruction.

    For example, in::

        // Define the first label
        &first
            NOOP
            SET_ZERO A

        // Define the second label
        &second
            ADD B
            JUMP &first

    ``$first`` will be assigned a value of ``0``, as the NOOP
    machinecode word is at index 0. If an instruction occupied
    multiple words (i.e. it has some data) the label will be set to
    the value of the first word.

    ``$second`` will be assigned a value of ``2``, as that is the index
    of the ``ADD B`` instruction. Index 1 went to ``SET_ZERO A``.

    The ``JUMP &first`` instruction will be resolved to ``JUMP #0`` by
    the assembler as the ``$first`` label in the instruction is
    replaced with `#0`.
    """


    @classmethod
    def from_tokens(cls, tokens):
        if (len(tokens) == 1 and isinstance(tokens[0], LABEL)):
            return cls(tokens)
        else:
            return None

    @property
    def name(self):
        """
        str: The name of the label.
        """
        return self.tokens[0].value


class Variable(Pattern):
    """
    A way to refer to a location in memory.

    Variables are typically used to reserve a location in memory
    for a piece of data used throughout the program.

    When a line defines a variable, the machinecode index that line
    would have used (were it an instruction) is reserved for the
    variable but no machincecode will actually be generated at that
    address.

    E.g., in::

        // Anchor the machinecode to 0x10
        @ #10

        // Define some variables
        $num_enemies
        $player_hitponts

        // Begin a main loop
        &main_loop
            NOOP
            SETZERO ACC
            // Use the $num_enemies variable
            STORE ACC [$num_enemies]

    ``$num_enemies`` is set to 10 due to the anchor that
    preceeded it (note that 10 refers to the memory location
    10, not what is in memory at 10), and
    ``$player_hitpoints`` is set to 11. The ``NOOP`` instruction
    will be written out as machinecode at 12. The 
    ``STORE ACC [$num_enemies]`` line will resolve to
    ``STORE ACC [#10]``.
    """

    @classmethod
    def from_tokens(cls, tokens):
        if (len(tokens) == 1 and isinstance(tokens[0], VARIABLE)):
            return cls(tokens)
        else:
            return None

    @property
    def name(self):
        """
        str: The name of the variable.
        """
        return self.tokens[0].value


class VariableDefinition(Pattern):
    """
    A variable with data defined and set in machinecode.

    Very much like a :class:`~Variable`, but as well as reserving the
    location in memory, it sets data into machinecode.

    E.g., in::

        // Anchor the machinecode to 0xFF
        @ #20

        // Define some variables
        $num_lives #3
        $wall_heights #30 #15 #18

        // Begin a main loop
        &main_loop
            NOOP

    ``$num_lives`` will be set to 20 and 3 will be set as machinecode
    at that location. ``$wall_heghts`` will be set to 21 and then the
    values 30, 15, and 18 will be set as machinecode at locations
    21, 22 and 23 respectively.

    The ``NOOP`` instruction will be at machinecode index 24.
    """

    @classmethod
    def from_tokens(cls, tokens):
        if len(tokens) < 2:
            return None

        if not isinstance(tokens[0], VARIABLE):
            return None

        for token in tokens[1:]:
            if not isinstance(token, (NUMBER, ALIAS)):
                return None

        return cls(tokens)

    @property
    def name(self):
        """
        str: The name of the variable.
        """
        return self.tokens[0].value


    def _generate_machinecode(self):
        machinecode = []
        for token in self.tokens[1:]:
            machinecode.append(Word(const_token=token))
        return machinecode


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
                token = token.value
            if token.component == CONST:
                constant_tokens.append(token)

        return machinecode_func(self.signature, constant_tokens)
