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
            "ebc-assemble=sixteen_bit_computer.cli:assemble",
            "ebc-gen-roms=sixteen_bit_computer.cli:gen_roms",
        ]
    }
)
