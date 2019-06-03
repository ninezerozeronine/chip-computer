import sys
import os

sys.path.append(os.path.abspath("../src"))
from eight_bit_computer.cli import assemble


assemble()
