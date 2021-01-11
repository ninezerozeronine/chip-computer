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

class Pattern(ABC):
    @abstractmethod
    def has_machinecode():
        pass

class AliasDefinition(Pattern):

    @classmethod
    def match(tokens):
        if (len(tokens) == 2
                and isinstance(tokens[0], ALIAS)
                and isinstance(tokens[1], NUMBER)):
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
    def __init__(self, tokens, instruction_components):



    @classmethod
    def attempt_creation(cls, tokens):
        instruction_components = []
        for token in tokens:
            instruction_component = self.token_to_instruction_component(token)
            if instruction_component is None:
                return False
            else:
                instruction_components.append(instruction_component)

        instruction_components = tuple(instruction_components)
        if is_instruction(instruction_components):
            return cls(tokens, instruction_components)
        else:
            return False


    def token_to_instruction_component(token):
        pass