"""
Custom exceptions used in this project.
"""


class EightBitComputerError(Exception):
    pass


class InstructionParsingError(EightBitComputerError):
    pass


class LineProcessingError(EightBitComputerError):
    pass


class AssemblyError(EightBitComputerError):
    pass
