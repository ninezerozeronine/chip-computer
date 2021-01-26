"""
Definition of tokens - the atomic parts of assembly code.
"""

from abc import ABC, abstractmethod
import re

_IDENTIFIER_REGEX = re.compile(r"[a-zA-Z_]+\w*$")


def get_all_tokens():
    """
    Get all the tokens that have been defined.

    Returns:
        tuple(Token): A tuple of all the token classes (excluding the
        base class)
    """
    return (
        ALIAS,
        NUMBER,
    )


class Token(ABC):
    """
    Base class for all tokens.

    A token is an atomic part of some assembly code which can't be
    split further. Examples would be:

     - ``#123`` A number.
     - ``LOAD`` The OpCode for the load instruction.
     - ``[A]`` The location in memory at the value currently in the A
        register
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


class ALIAS(Token):
    """
    Defines an alias.

    An alias is a convenience to allow a string to be used in place of
    a number constant. E.g. instead of having to hardcode ``#10`` in
    many places in the assmebly code to represent (say) the max number of
    enemies in a game, an alias ``MAX_ENEMIES`` can be defined instead.

    An alias is an :func:`identifier <is_identifier>` prepended with the
    ``!`` character. E.g.:

     - ``!MY_ALIAS``
     - ``!NUM_ROWS``
    """

    @classmethod
    def from_string(cls, _string):
        if not _string:
            return None

        if _string[0] != "!":
            return None

        if not is_identifier(_string[1:]):
            return None

        return cls(_string, _string[1:])


class NUMBER(Token):
    """
    Defines a number.

    An number is an interger value. A ``#`` followed by any valid Python
    representation of an interger is considered a number. E.g.:

     - ``#34``
     - ``#0XFFFC``
     - ``#0o271``
     - ``#-23``
     - ``0b1001010``
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






# class DATA(Token):
#     pass



# class CONSTANT(Token):
#     pass

# class ALIAS(CONSTANT):
#     pass

# class NUMBER(CONSTANT):
#     pass

# class LABEL(CONSTANT):
#     pass

# class VARIABLE(CONSTANT):
#     pass



# class ASCII(Token):
#     pass


# class ANCHOR(Token):
#     pass




# class INSTRUCTION(Token):
#     pass

# class LOAD(INSTRUCTION):
#     pass

# class STORE(INSTRUCTION):
#     pass




# class MODULE(Token):
#     pass

# class A(MODULE):
#     pass

# class B(MODULE):
#     pass

# class C(MODULE):
#     pass




# class MEMREF(Token):
#     pass

# class M_A(MEMREF):
#     pass

# class M_B(MEMREF):
#     pass

# class M_ALIAS(MEMREF):
#     pass

# class M_VARIABLE(MEMREF)




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
