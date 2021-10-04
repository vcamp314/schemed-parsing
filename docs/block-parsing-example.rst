block parsing example
=================================
A block here is defined as multiline (one or more lines) of text bounded by a particular starting and ending pattern
from which a particular text pattern is to be extracted

example composition of a list of schemes covering a single kind of javascript import statements::

    {
        "schemes": [
            {
                "block_start_pattern": {
                    "query": "import {"
                },
                "block_end_pattern": {
                    "query": "}",
                    "properties": [
                        {
                            "property_name": "from_path",
                            "extraction_patterns":[
                                {
                                    "query": "from\\s*?(?:\"|\\')(.*)(?:\"|\\')"
                                }
                            ]
                        }
                    ]
                },
                "block_category": "block_import",
                "extraction_patterns": [
                    {
                        "query": "{(.*)}"
                    }
                ]
            }
        ]
    }

the above example would apply to the below example multiline import statement structure::

      import {
          longNameA,
          longNameB,
          longNameC,
      } from '/some/pretty/long/path/'

The parsing will return a list of all the blocks found, and a list of all the names containing their parent block ids
as well as any properties defined in the scheme.

In this case the parsing will extract the below blocks::

    [
        {
            'block_category': 'block_import',
            "from_path": "/some/pretty/long/path/",
            'starting_line_no': 1,
            'ending_line_no': 5,
        }
    ]


and the below names, `longNameA`, `longNameB`, `longNameC` into a list of the below structure::


    [
        {
            "name": "longNameA",
            'block_id': 0,
        },
        {
            "name": "longNameB",
            'block_id': 0,
        },
        {
            "name": "longNameC",
            'block_id': 0,
        }
    ]

++++++++++++++++
How it works
++++++++++++++++

Block scheme definition
#########################

Defining the `block_start_patterns` and `block_end_patterns` indicates to the parser that this
this scheme is a block scheme and will cause the scheme to look for the end patterns for
each line after the start pattern has been opened until it finds a match.


should it find another open pattern before finding an end, this scheme will be started for
the new block as well and when that finishes, it will resume the search for the previous one.


The structure of these patterns is the same as that for the extraction patterns and work in
the same way. please see parsing-scheme-example.rst for an explanation of how extraction
patterns work.


