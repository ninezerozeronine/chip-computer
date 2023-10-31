import argparse
import asyncio

from . import main


def assemble():
    """
    Entry point for the command line assemble script.
    """

    parser = get_assemble_parser()
    args = parser.parse_args()
    main.assemble(
        args.asm_filepath,
        output_filename_base=args.output_filename_base,
        output_dir=args.output_directory,
        output_format=args.output_format
    )


def get_assemble_parser():
    """
    Generate arg parser for the ebc_assemble command line script.

    Returns:
        argparse.ArgumentParser: The argument parser.
    """

    parser = argparse.ArgumentParser(
        description=(
            "Assemble eight bit computer assembly files to machine "
            "code."
        )
    )
    parser.add_argument(
        "asm_filepath", help="Path to the assembly file to assemble."
    )
    parser.add_argument(
        "-o",
        "--output_filename_base",
        help=(
            "Filename base for the assembled file. E.g. "
            "\"myfile\" or \"fibonacci\". Do not include "
            "an extension."
        )
    )
    parser.add_argument(
        "-d",
        "--output_directory",
        help=(
            "Directory for the output filed. Defaults to current "
            "directory."
        )
    )
    parser.add_argument(
        "-f",
        "--output_format",
        choices=["logisim", "arduino", "python"],
        help="Format to write the assembled code in.",
        default="logisim",
    )

    return parser


def gen_roms():
    """
    Entry point for the command line rom generation script.
    """

    parser = get_gen_roms_parser()
    args = parser.parse_args()
    if args.file_prefix:
        main.gen_roms(
            output_dir=args.output_dir,
            file_prefix=args.file_prefix,
            output_format=args.output_format,
        )
    else:
        main.gen_roms(
            output_dir=args.output_dir,
            output_format=args.output_format,
        )


def get_gen_roms_parser():
    """
    Generate arg parser for the gen_roms command line script.

    Returns:
        argparse.ArgumentParser: The argument parser.
    """

    parser = argparse.ArgumentParser(
        description="Generate ROMs that contain the microcode."
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        help="Directory to write the ROMs into.",
        default=".",
    )
    parser.add_argument(
        "-p",
        "--file_prefix",
        help="Prefix for the ROM files.",
    )
    parser.add_argument(
        "-f",
        "--output_format",
        choices=["logisim", "arduino"],
        help="Format to write the ROMs in.",
        default="logisim",
    )

    return parser

def assemble_and_send():
    """
    Entry point for the command line assemble and send script.
    """

    parser = get_assemble_and_send_parser()
    args = parser.parse_args()
    asyncio.run(
        main.assemble_and_send(
            args.asm_filepath,
            args.ip_address,
            args.port
        )
    )


def get_assemble_and_send_parser():
    """
    Generate arg parser for the assemble and send command line script.

    Returns:
        argparse.ArgumentParser: The argument parser.
    """
    
    parser = argparse.ArgumentParser(
        description="Assemble and send some assembly to the Computer."
    )
    parser.add_argument(
        "asm_filepath", help="Path to the assembly file to assemble."
    )
    parser.add_argument(
        "ip_address", help="IP address to send to."
    )
    parser.add_argument(
        "port", help="The port to connect to."
    )

    return parser