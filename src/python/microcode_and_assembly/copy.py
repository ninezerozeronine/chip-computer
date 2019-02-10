"""The copy operation"""

from base import MicrocodeAssembly

class Copy(MicrocodeAssembly):
    def generate_microcode(self):
        """
        
        """

        sources = ["ACC", "A", "B", "C", "PC", "SP"]
        destinations = ["ACC", "A", "B", "C", "SP"]
        