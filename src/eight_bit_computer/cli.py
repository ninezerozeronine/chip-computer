import argparse

from . import assembler


def assemble():
    """

    """
    parser = get_assemble_parser()
    args = parser.parse_args()
    print "finish"


def get_assemble_parser():
    """

    """

    parser = argparse.ArgumentParser()
    return parser


if __name__ == "__main__":
    assemble()