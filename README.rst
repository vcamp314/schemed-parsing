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
The Schemed Parsing library parse function::

    schemedparsing.parse



example usage::

    import schemedparsing
    schemedparsing.parse('sample text', parsing_schemes)


For the structure of the above :code:`parsing_scheme` parameter, please see the parsing scheme example document in the docs folder <./docs/parsing-scheme-example.rst>`

The result will be a tuple of lists, the first element of which will contain the names extracted by the parsing.
The second element of the tuple will contain any blocks found, or an empty list if none are found.

For examples of how to set up the :code:`parsing_scheme` parameter to include blocks, please see the block parsing example document in the docs folder <./docs/block-parsing-example.rst>`

++++++++
Testing
++++++++
how to run unit tests including doctests::

    $ py.test


