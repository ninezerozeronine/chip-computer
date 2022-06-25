"""
Definition of tokens - the atomic parts of assembly code.
"""

from abc import ABC, abstractmethod
import re

from .instruction_components import (
    NOOP,
    HALT,
    SET_ZERO,
    JUMP_IF_EQ_ZERO,
    JUMP_IF_NEQ_ZERO,
    COPY,
    ADD,
    SUB,
    AND,
    OR,
    XOR,
    NAND,
    NOR,
    NXOR,
    ACC,
    A,
    B,
    C,
    PC,
    SP,
    CONST,
    M_ACC,
    M_A,
    M_B,
    M_C,
    M_CONST,
)

_IDENTIFIER_REGEX = re.compile(r"[a-zA-Z_]+\w*$")
"""
    Define what constitutes a valid identifier.
    
    Any upper or lower case letter or an underscore followed by zero or
    more alphanumeric characters. Some examples would be:

     - ``my_name``
     - ``helloWorld2``
     - ``_AnoTHer__exampLE``
"""


def get_all_tokens():
    """
    Get all the tokens that have been defined.

    Returns:
        tuple(Token): A tuple of all the token classes (excluding the
        base class)
    """
    return (
        ANCHOR,
        ALIAS,
        LABEL,
        VARIABLE,
        NUMBER,
        OPCODE,
        MODULE,
        MEMREF,
    )


class Token(ABC):
    """
    Base class for all tokens.

    A token is an atomic part of some assembly code which can't be
    split further. Examples would be:

     * ``#123`` - A number.
     * ``LOAD`` - The OpCode for the load instruction.
     * ``[A]`` - The location in memory at the value currently in the A
       module.
    """

    def __init__(self, raw, value):
        """
        Initialise the class.

        Args:
            raw (str): The raw string that this token was generated
                from.
            value: The value that this token contains. The type will
                vary based on the nature of the token.
        """
        self._raw = raw
        self._value = value

    @classmethod
    @abstractmethod
    def from_string(cls, _string):
        """
        Attempt to create an instance of this token from a string.

        If the string does not match what the token should be, None
        should be returned instead of an instance of the class.

        Args:
            _string (str): The string to try and create the token from.

        Returns:
            None or subclass of Token: None if the string doesn't match
            the token, an instance of the token if it does.
        """
        return None

    @property
    def value(self):
        """
        The value that this token contains.

        The type will vary based on the nature of the token.
        """
        return self._value

    @property
    def raw(self):
        """
        str: The raw string that this token was generated from.
        """
        return self._raw

    @property
    def component(self):
        """
        :mod:`Instruction component<.instruction_components>` or None:
        Instruction Component this token represents or None if it has
        no mapping to a component.
        """
        return None

    def is_const(self):
        """
        Whether or not this token represents a constant word.

        A constant value is something like a number or an alias, some
        raw data that will eventually end up in machinecode.

        Returns:
            bool: Whether the token represents a constant word.
        """
        return False


class ANCHOR(Token):
    """
    Defines an anchor.

    Anchors pin machine code that follows them to a specific address.
    See the :class:`~sixteen_bit_computer.assembly_patterns.Anchor`
    pattern for details.

    An anchor token is the ``@`` character.
    """

    @classmethod
    def from_string(cls, _string):
        if _string == "@":
            return cls(_string, None)
        else:
            return None


class ALIAS(Token):
    """
    Defines an alias.

    Aliases provide a convenience to refer to a value. See the
    :class:`~sixteen_bit_computer.assembly_patterns.Alias` pattern for
    details.

    An alias token is an :func:`identifier <is_identifier>` prepended
    with the ``!`` character. E.g.:

     - ``!MY_ALIAS``
     - ``!NUM_ROWS``
    """

    @classmethod
    def from_string(cls, _string):
        if not _string:
            return None

        if _string[0] != "!":
            return None

        identifier = _string[1:]
        if not is_identifier(identifier):
            return None

        return cls(_string, identifier)

    def is_const(self):
        return True

    @property
    def component(self):
        return CONST


class LABEL(Token):
    """
    Defines a label.

    A label is a named index in machine code. See the
    :class:`~sixteen_bit_computer.assembly_patterns.Label` pattern for
    details.

    It is declared as an :func:`identifier <is_identifier>` prepended
    with the ``&`` character. E.g.:

     - ``&MY_LABEL``
     - ``&loop_start``
    """

    @classmethod
    def from_string(cls, _string):
        if not _string:
            return None

        if _string[0] != "&":
            return None

        identifier = _string[1:]
        if not is_identifier(identifier):
            return None

        return cls(_string, identifier)

    def is_const(self):
        return True

    @property
    def component(self):
        return CONST


class VARIABLE(Token):
    """
    Defines a variable.

    A variable is a named location in memory. See the
    :class:`~sixteen_bit_computer.assembly_patterns.Variable`
    pattern for details.

    It is declared as an :func:`identifier <is_identifier>` prepended
    with the ``$`` character. E.g.:

     - ``$MY_VARIABLE``
     - ``$num_lives``
    """

    @classmethod
    def from_string(cls, _string):
        if not _string:
            return None

        if _string[0] != "$":
            return None

        identifier = _string[1:]
        if not is_identifier(identifier):
            return None

        return cls(_string, identifier)

    def is_const(self):
        return True

    @property
    def component(self):
        return CONST


class NUMBER(Token):
    """
    Defines a number.

    An number is an interger value. A ``#`` followed by any valid Python
    representation of an interger is considered a number. E.g.:

     - ``#34``
     - ``#0XFFFC``
     - ``#0o271``
     - ``#-23``
     - ``#0b1001010``
    """

    @classmethod
    def from_string(cls, _string):
        if not _string:
            return None

        if _string[0] != "#":
            return None

        number_part = _string[1:]

        if not number_part:
            return None

        try:
            num = int(number_part, 0)
        except ValueError:
            return None

        return cls(_string, num)

    def is_const(self):
        return True

    @property
    def component(self):
        return CONST


class OPCODE(Token):
    """
    Defines an Opcode.

    An opcode is the part of an instruction that defines the type of
    behaviour. E.g., in:

    .. code-block:: none

        LOAD [A] B
        LOAD [#123] ACC

    ``LOAD`` is the opcode. Regardless of where in memory the value is
    being fetched from, or what module the value is being loaded into,
    it's still a load.
    """

    _OPCODE_TO_COMPONENT = {
        "NOOP": NOOP,
        "SET_ZERO": SET_ZERO,
        "JUMP_IF_EQ_ZERO": JUMP_IF_EQ_ZERO,
        "JUMP_IF_NEQ_ZERO": JUMP_IF_NEQ_ZERO,
        "COPY": COPY,
        "ADD": ADD,
        "SUB": SUB,
        "AND": AND,
        "OR": OR,
        "XOR": XOR,
        "NAND": NAND,
        "NOR": NOR,
        "NXOR": NXOR,
        "HALT": HALT,
    }
    """
    dict[str, :mod:`Instruction component<.instruction_components>`]:
    A mapping of opcode strings to thier :mod:`instruction component
    <components>` equivalents.
    """

    @classmethod
    def from_string(cls, _string):
        if _string in cls._OPCODE_TO_COMPONENT:
            return cls(_string, _string)
        else:
            return None

    @property
    def component(self):
        return self._OPCODE_TO_COMPONENT[self.value]


class MODULE(Token):
    """
    Defines a Module.

    A module is a part of the CPU that can be interacted with in an in
    instruction. E.g., in:

    .. code-block:: none

        LOAD [A] B
        LOAD [123] ACC

    ``A``, ``B``, and ``ACC`` are modules.

    ..
        Add these here as using private-members in
        autodoc_default_options means all sort of private nonsense
        gets documented.

    .. autoattribute:: _MODULE_TO_COMPONENT
    """

    _MODULE_TO_COMPONENT = {
        "ACC": ACC,
        "A": A,
        "B": B,
        "C": C,
        "SP": SP,
        "PC": PC,
    }
    """
    Dict[str, :mod:`instruction component<.instruction_components>`]:
    A mapping of module strings to thier :mod:`instruction
    component<.instruction_components>` equivalents.
    """

    @classmethod
    def from_string(cls, _string):
        if _string in cls._MODULE_TO_COMPONENT:
            return cls(_string, _string)
        else:
            return None

    @property
    def component(self):
        return self._MODULE_TO_COMPONENT[self.value]


class MEMREF(Token):
    """
    A way to represent a location in memory.

    If the token starts with ``[`` and ends with ``]`` it is considered
    to be a memory reference.

    The location in memory (i.e.) the thing between the brackets needs
    to be one of the following:

     - ``ALIAS``
     - ``LABEL``
     - ``VARIABLE``
     - ``NUMBER``
     - ``MODULE``
    """

    _COMPONENT_TO_MEMREF_COMPONENT = {
        ACC: M_ACC,
        A: M_A,
        B: M_B,
        C: M_C,
        CONST: M_CONST,
    }

    _VALID_TOKENS = (
        ALIAS,
        LABEL,
        VARIABLE,
        NUMBER,
        MODULE,
    )

    @classmethod
    def from_string(cls, _string):
        if len(_string) < 3:
            return None

        if not (_string.startswith("[") and _string.endswith("]")):
            return None

        matched_token = None
        for valid_token in cls._VALID_TOKENS:
            matched_token = valid_token.from_string(_string[1:-1])
            if matched_token is not None:
                break

        if matched_token is None:
            return None

        return cls(_string, matched_token)

    @property
    def component(self):
        return self._COMPONENT_TO_MEMREF_COMPONENT[self.value.component]


def is_identifier(test_string):
    """
    Test if a string is a valid identifier.

    An identifier is a string that's used to refer to a named constant
    like a label or a variable.

    Args:
        test_string (str): The string to test
    Returns:
        bool: True if the string is a valid identifier, false otherwise.
    """
    if not test_string:
        return False

    match = _IDENTIFIER_REGEX.match(test_string)
    if match:
        return True
    else:
        return False
