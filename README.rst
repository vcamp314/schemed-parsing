Schemed Parsing Package
=================================
Schemed Parsing is a python package developed with the intent of allowing for config driven text parsing.
The premise is that a parsing configuration in the form of a dictionary which we will call a "scheme" can
be used to define the matching criteria and text to extract at runtime.

This library admittedly has a narrow use case scope; in most cases it would be better to use regex directly if you can.
This library was created to be part of a larger project for which the use cases it covers is essential.

If you find a use for it in whatever you may be working on, feel free to give it a try.


+++++++++++++
Installation
+++++++++++++
Installing package with dependencies::

    $ python3 -m pip install git+https://github.com/user/parse

++++++
Usage
++++++
How to use this library.

The Schemed Parsing library parse function::

    schemedparsing.parse



example usage::

    import schemedparsing
    names, blocklist = schemedparsing.parse('sample text', parsing_schemes)


For the structure of the above :code:`parsing_scheme` parameter, please see the  `parsing scheme example <https://github.com/vcamp314/schemed-parsing/blob/master/docs/parsing-scheme-example.rst>`_ document in the
docs folder

The result will be a tuple of lists, the first element of which will contain the names extracted by the parsing.
The second element of the tuple will contain any blocks found, or an empty list if none are found.

As shown above, this result can be destructured into names and blocklist parameters for use.
Each element of the names list will contain the index of the block in which it was found, if any blocks are present

For examples of how to set up the :code:`parsing_scheme` parameter to include blocks, and how the parsing results look
like please see the `block parsing example <https://github.com/vcamp314/schemed-parsing/blob/master/docs/block-parsing-example.rst>`_ document in the docs folder <./docs/block-parsing-example.rst>`

++++++++
Testing
++++++++
how to run unit tests including doctests::

    $ py.test


