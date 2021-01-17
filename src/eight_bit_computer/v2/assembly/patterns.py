"""
There's work that goes into checking if tokens match a pattern. This work will
vary by pattern, and we want to store the result of the work in the resulting pattern


"""

from abc import ABC, abstractmethod


from .tokens import (
    ALIAS
    NUMBER
    CONSTANT
)


from ..instruction_set import components
from ..instruction_set.listings import INSTRUCTION_SIGNATURES

_TOKEN_TO_COMPONENT = {
    A : components.A,
    B : components.B,
    LOAD : components.LOAD,
    STORE : components.STORE,
    NUMBER : components.CONST,
    LABEL : components.CONST,
    M_NUMBER : components.M_CONST
    M_LABEL : components.M_CONST
}



class Pattern(ABC):
    @abstractmethod
    def has_machinecode():
        pass

    @abstractmethod
    def from_tokens(tokens):
        pass

class AliasDefinition(Pattern):

    @classmethod
    def match(tokens):
        if (len(tokens) == 2
                and tokens[0] == ALIAS
                and tokens[1] == NUMBER):
            return True
        else:
            return False

class DataSet(Pattern):

    @classmethod
    def match(tokens):
        for token in tokens:
            if not isinstance(token, CONSTANT):
                return False
        return True

class Instruction(Pattern):
    def __init__(self, tokens, signature):
        self.tokens = tokens
        self.signature = signature


    @classmethod
    def from_tokens(cls, tokens):
        instruction_components = []
        for token in tokens:
            instruction_component = token_to_component(token)
            if instruction_component is None:
                return False
            else:
                instruction_components.append(instruction_component)

        signature = tuple(instruction_components)
        if signature in INSTRUCTION_SIGNATURES:
            return cls(tokens, signature)
        else:
            return False




    def has_machinecode(self):
        return True

    def get_machinecode_template(self):



def token_to_component(token):
    token_type = type(token)
    if token_type in _TOKEN_TO_COMPONENT:
        return _TOKEN_TO_COMPONENT[token_type]
    else
        return None
