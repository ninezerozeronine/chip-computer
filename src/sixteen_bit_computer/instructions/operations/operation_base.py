from abc import ABC, abstractmethod


class Operation(ABC):
    """

    """
    @abstractmethod
    def get_machinecode_function 


    @abstractmethod
    def generate_machinecode(self, signature, const_tokens):
        """

        """
        pass

    @abstractmethod
    def generate_microcode(self, signature):
        """

        """
        pass

    @property
    @abstractmethod
    def supported_signatures(self):
        """

        """
        pass
