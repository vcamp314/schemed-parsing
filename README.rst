Schemed Parsing Package
=================================
This is a template package structure for future packages.
Replace this text with your project's description.

Note: All  below commands should be executed from root (directory of this readme)

+++++++++++++
Installation
+++++++++++++
Installing package with dependencies (update accordingly for actual github link/PyPI)::

    $ python3 -m pip install git+https://github.com/user/parse

++++++
Usage
++++++
How to use this library.
The Schemed Parsing library has two main methods of parsing:
1. schemedparsing.parse
2. schemedparsing.parse_all_lines

Simple parsing
***************

example usage::

    import schemedparsing
    schemedparsing.parse('sample text', parsing_schemes)


For the structure of the above :code:`parsing_scheme` parameter, please see the parsing scheme example document in the docs folder <./docs/sample-parsing-scheme-example.rst>`

Block parsing
***************

++++++++
Testing
++++++++
how to run unit tests including doctests::

    $ py.test


