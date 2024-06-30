import sys
import os

sys.path.append(os.path.abspath("../src"))
from sixteen_bit_computer.cli import gen_roms


gen_roms()
