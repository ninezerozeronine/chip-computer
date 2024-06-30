def chunker(seq, chunk_size):
    """
    Take a larger sequence and split it into smaller chunks.

    E.g.::

        chunker([0,1,2,3,4,5], 4) -> [0,1,2,3], [4,5]

    Args:
        seq (list): List of things to chunk up
        chunk_size (int): How big each chunk should be.
    Returns:
        generator: Generator that yields each chunk.
    """
    return (
        seq[pos:pos + chunk_size] for pos in range(0, len(seq), chunk_size)
    )