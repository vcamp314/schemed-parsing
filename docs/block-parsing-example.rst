block parsing example
=================================
A block here is defined as multiline (one or more lines) of text to be parsed as a single string
for a particular pattern

example composition of a list of schemes  covering a single kind of javascript import statements::

    {
        "schemes": [
            {
                "block_schemes": [
                    {
                        "block_start_pattern": {
                            "query": "{"
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
                        "match_conditions": [
                            {
                                "query": "import",
                                "type": "startswith"
                            }
                        ],
                        "extraction_patterns": [
                            {
                                "query": "{(.*)}"
                            },
                            {
                                "query": "(\\w+)"
                            }
                        ]
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

the parsing will extract the names, `longNameA`, `longNameB`, `longNameC` into a list of the below structure::


    [
        {
            "name": "longNameA",
            "from_path": "./sample/path"
        },
        {
            "name": "longNameB",
            "from_path": "./sample/path"
        },
        {
            "name": "longNameC",
            "from_path": "./sample/path"
        }
    ]

++++++++++++++++
How it works
++++++++++++++++
Defining a block_schemes in a scheme element will indicate to the parser to look at the schemes
inside and apply them in order where these schemes are defined as block or non-block schemes.

Block scheme definition
#########################

Defining the block_start_patterns and block_end_patterns indicates to the parser that this
this scheme is a block scheme and will cause the scheme to look for the end patterns for
each line after the start pattern has been opened until it finds a match.

Each subsequent line will be appended into one string until the end pattern is found, and the
resulting string will have the extraction pattern applied.


should it find another open pattern before finding an end, this scheme will be started for
the new block as well and when that finishes, it will resume the search for the previous one.


The structure of these patterns is the same as that for the extraction patterns and work in
the same way. please see parsing-scheme-example.rst for an explanation of how extraction
patterns work.


