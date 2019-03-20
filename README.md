# 8 bit Computer

This is a project to make a basic but fully functional 8 bit computer 
using 7400 series ICs.

The full docs can be found on the GitHub Pages pages for this
project: https://ninezerozeronine.github.io/eight-bit-computer/

# License

The content of this project itself is licensed under the [Creative Commons Attribution 3.0 license](http://creativecommons.org/licenses/by/3.0/us/deed.en_US), 
and any code used is licensed under the [MIT license](http://opensource.org/licenses/mit-license.php).

# Docs

To build the docs on mac run:

    sphinx-apidoc --force --separate --no-toc -o software/source/ ../src/python/eight_bit_computer/
    make clean
    make html

in `sphinx_docs`.

To build the docs in windows run:

    sphinx-apidoc --force --separate --no-toc -o software/source/ ../src/python/eight_bit_computer/
    sphinx-build.exe . _build

in `sphinx_docs`.

Then copy `sphinx_docs/_build/html/*` into `docs` so that github pages can see them.

# Tests

To run the tests, run:

    python -m unittest discover -v

in `src/python`