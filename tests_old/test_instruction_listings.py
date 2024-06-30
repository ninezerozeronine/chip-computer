from sixteen_bit_computer import instruction_listings


def test_all_sigs_have_index():
    assert instruction_listings._INSTRUCTION_SIGNATURES == set(instruction_listings._INSTRUCTION_INDECIES.keys())


def test_all_indexes_are_unique():
    assert len(instruction_listings._INSTRUCTION_INDECIES) == len(set(instruction_listings._INSTRUCTION_INDECIES.values()))
