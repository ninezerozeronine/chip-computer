from .tokens import (
    ALIAS
    NUMBER
    CONSTANT
)

class Pattern():
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
    @classmethod
    def match(tokens):
        pass