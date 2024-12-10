from setuptools import setup, find_packages

setup(
    name="sixteen-bit-computer",
    version="0.0.2",
    author="Andy Palmer",
    author_email="contactninezerozeronine@gmail.com",
    description="Tools to build a physical sixteen bit computer.",
    url="https://github.com/ninezerozeronine/eight-bit-computer",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        "console_scripts": [
            "sbc-assemble=sixteen_bit_computer.cli:assemble",
            "sbc-assemble-and-send=sixteen_bit_computer.cli:assemble_and_send",
            "sbc-gen-roms=sixteen_bit_computer.cli:gen_roms",
            "sbc-ui=sixteen_bit_computer.ui.main:open_ui"
        ]
    }
)
