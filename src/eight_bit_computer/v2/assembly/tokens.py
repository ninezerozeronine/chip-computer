"""
Tokens define the atomic parts of assembly code.

Tokens are of different types, and one type can have varying values. E.g.
A number type can have a value of 34, or 16.



"""


from abc import ABC, abstractmethod
import re


_IDENTIFIER_REGEX = re.compile(r"[a-zA-Z_]+\w*$")


class Token(ABC):
    @abstractmethod
    def value():
        pass

    @abstractmethod
    def from_word(word):
        pass


class ALIAS(Token):
    @classmethod
    def from_word(cls, word):
        if not word:
            return None

        if word[0] != "!":
            return None

        if not is_identifier(word[1:]):
            return None

        return cls(word, word)

    def __init__(self, raw, value):
        self.raw = raw
        self.value = value


class NUMBER(Token):
    @classmethod
    def from_word(cls, word):
        if not word:
            return None

        if word[0] != "#":
            return None

        number_part = word[1:]

        if not number_part:
            return None

        try:
            num = int(number_part, 0)
        except ValueError:
            return None

        return cls(word, num)

    def __init__(self, raw, value):
        self.raw = raw
        self.value = value












class CONSTANT(Token):
    pass

class ALIAS(CONSTANT):
    pass

class NUMBER(CONSTANT):
    pass

class LABEL(CONSTANT):
    pass

class VARIABLE(CONSTANT):
    pass



class ASCII(Token):
    pass


class ANCHOR(Token):
    pass




class INSTRUCTION(Token):
    pass

class LOAD(INSTRUCTION):
    pass

class STORE(INSTRUCTION):
    pass




class MODULE(Token):
    pass

class A(MODULE):
    pass

class B(MODULE):
    pass

class C(MODULE):
    pass




class MEMREF(Token):
    pass

class M_A(MEMREF):
    pass

class M_B(MEMREF):
    pass

class M_ALIAS(MEMREF):
    pass

class M_VARIABLE(MEMREF)




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


def is_number(test_string):
    """
    Test if a string is a valid number.

    Args:
        test_string (str): The string to test
    Returns:
        bool: True if the string is a valid number, false otherwise.
    """
    if not test_string:
        return False

    try:
        num = int(test_string, 0)
    except ValueError:
        return False
    return True