"""
Custom exceptions used in this project.
"""


class EightBitComputerError(Exception):
    """
    Base class for exceptions in the computer
    """
    pass


class OperationParsingError(EightBitComputerError):
    """
    Raised when parsing an operation fails.

    E.g. An incorrect argument is used with the LOAD operation.
    """
    pass


class LineProcessingError(EightBitComputerError):
    """
    Raised when processing a line fails.

    E.g. The line was not a constant declaration and no operations
    matched.
    """
    pass


class AssemblyError(EightBitComputerError):
    """
    Raised when the assembly could not be converted to machine code.
    """
    pass





class SixteentBitComputerError(Exception):
    """
    Base class for exceptions in the computer
    """
    pass


class LineProcessingError(SixteentBitComputerError):
    """
    Raised when processing a line of assembly fails.
    """
    pass


class NoMatchingTokensError(LineProcessingError):
    """
    Raised when a word matches no tokens.
    """
    pass


class MultipleMatchingTokensError(LineProcessingError):
    """
    Raised when a word matches multiple tokens.
    """
    pass


class NoMatchingPatternsError(LineProcessingError):
    """
    Raised when tokens match no patterns.
    """
    pass


class MultipleMatchingPatternsError(LineProcessingError):
    """
    Raised when tokens match multiple patterns.
    """
    pass


class AssemblyError(SixteentBitComputerError):
    """
    Raised when the assembly could not be converted to machine code.
    """
    pass
