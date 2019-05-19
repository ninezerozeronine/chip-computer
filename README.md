# 8 bit Computer

This is a project to make a basic but fully functional 8 bit computer 
using 7400 series ICs.

The full docs can be found on the Read the Docs: https://eight-bit-computer.readthedocs.io/

# License

The content of this project itself is licensed under the [Creative Commons Attribution 3.0 license](http://creativecommons.org/licenses/by/3.0/us/deed.en_US), 
and any code used is licensed under the [MIT license](http://opensource.org/licenses/mit-license.php).

# Docs

To build the docs on mac run:

    make clean
    make html

in `docs`.

To build the docs in windows run:

    sphinx-build.exe . _build

in `docs`.

# Tests

To run the tests, run:

    python -B -m pytest

in `src/python`

To generate a coverage report run:

    python -B -m pytest --cov=eight_bit_computer --cov-report=html:cov_html tests

