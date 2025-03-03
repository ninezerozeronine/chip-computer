def main():

    # E   O.O.O.OO................OO....OOOO
    # D   ..................OOO.......O.....
    # C   O.O.O.OO....OOO.........OO....OOOO
    # A#  ..................OOO.......O.....
    # G#  ............OOO...................

    # Ch1 E.E.E.EE....CCC...DDD...EE..D.EEEE
    # Ch2 C.C.C.CC....ggg...aaa...CC..a.CCCC


    # Sounds better!
    # C4   O.O.O.OO................OO....OOOO
    # A#3  ..................OOO.......O.....
    # G#3  ............OOO...................
    # G3   O.O.O.OO................OO....OOOO
    # F3   ..................OOO.......O.....
    # D#3  ............OOO...................

    # Ch1 C.C.C.CC....ggg...aaa...CC..a.CCCC
    # Ch2 G.G.G.GG....ddd...FFF...GG..F.GGGG

    ch1 = "C.C.C.CC....ggg...aaa...CC..a.CCCC"
    ch2 = "G.G.G.GG....ddd...FFF...GG..F.GGGG"

    notes_to_freqs = {
        "C": 956,
        "a": 1073,
        "g": 1204,
        "G": 1276,
        "F": 1432,
        "d": 1607
    }

    pairs = notes_to_pairs(ch1)
    assembly = notes_pairs_to_assembly(
        pairs,
        "!MUSIC_CHANNEL_1",
        notes_to_freqs,
        4,
        8
    )
    print("\n".join(assembly))


def notes_pairs_to_assembly(note_pairs, channel_address, notes_to_freqs, period_multiplier, volume):
    assembly_lines = []
    for note, duration in note_pairs:
        if note == ".":
            res = 0
        else:
            res = volume << 12
            res |= notes_to_freqs[note]
        assembly_lines.append(f"SET A #0b{res:019_b}")
        assembly_lines.append(f"SET B #0{duration * period_multiplier}")
        assembly_lines.append(f"SET C {channel_address}")
        assembly_lines.append("CALL &add_note")
    return assembly_lines


def notes_to_pairs(notes):
    pairs = []
    last_note = notes[0]
    duration = 1
    for sound in notes[1:]:
        if sound == last_note:
            duration += 1
        else:
            pairs.append((last_note, duration))
            last_note = sound
            duration = 1
    return pairs

if __name__ == "__main__":
    main()