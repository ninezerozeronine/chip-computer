"""
There's work that goes into checking if tokens match a pattern. This work will
vary by pattern, and we want to store the result of the work in the resulting pattern


"""

from abc import ABC, abstractmethod


from .tokens import (
    ALIAS,
    NUMBER,
)


from ..instructions import components
from ..instructions.listings import INSTRUCTION_SIGNATURES

_TOKEN_TO_COMPONENT = {
    ALIAS: components.CONST,
    NUMBER: components.CONST,
}


def get_all_patterns():
    return (
        AliasDefinition,
    )


class Pattern(ABC):

    @abstractmethod
    def generate_machinecode():
        pass

    @abstractmethod
    def from_tokens(cls, tokens):
        pass


class AliasDefinition(Pattern):
    def __init__(self, tokens):
        self.tokens = tokens

    @classmethod
    def from_tokens(cls, tokens):
        if (len(tokens) == 2
                and type(tokens[0]) == ALIAS
                and type(tokens[1]) == NUMBER):
            return cls(tokens)
        else:
            return None

    def generate_machinecode(self):
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
#         self.tokens = tokens
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




#     def generate_machinecode(self):
#         return [Word, Word]



# def token_to_component(token):
#     token_type = type(token)
#     if token_type in _TOKEN_TO_COMPONENT:
#         return _TOKEN_TO_COMPONENT[token_type]
#     else
#         return None
