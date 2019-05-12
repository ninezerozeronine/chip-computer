"""

"""

from . import number_utils


def bitstrings_to_cpp(bitstrings):
    """

    """
    pass


def bitstrings_to_logisim(bitstrings):
    """

    """
    logisim_lines = ["v2.0 raw"]
    for line_bytes in chunker(bitstrings, 16):
        line_parts = []
        for line_chunk_bytes in chunker(line_bytes, 4):
            hex_strings = [
                number_utils.bitstring_to_hex_string(bit_string)
                for bit_string
                in line_chunk_bytes
            ]
            four_hex_bytes = " ".join(hex_strings)
            line_parts.append(four_hex_bytes)
        line = "  ".join(line_parts)
        logisim_lines.append(line)
    logisim_string = "\n".join(logisim_lines)
    return logisim_string


def chunker(seq, chunk_size):
    """

    """
    return (
        seq[pos:pos + chunk_size] for pos in xrange(0, len(seq), chunk_size)
    )