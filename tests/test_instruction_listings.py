import pytest

from sixteen_bit_computer import instruction_listings

def test_not_too_many_instructions():
    assert len(instruction_listings.all_signatures()) < 256