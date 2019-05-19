from setuptools import setup, find_packages

setup(
    name="eight_bit_computer_amptest",
    version="0.0.1",
    author="Andy Palmer",
    author_email="contactninezerozeronine@gmail.com",
    description="Tools to build a physical eight bit computer.",
    url="https://github.com/ninezerozeronine/eight_bit_computer",
    packages=find_packages('src'),
    package_dir={'': 'src'},
)
