block parsing example
=================================
A block here is defined as multiline (one or more lines) of text to be parsed as a single string
for a particular pattern

example composition of a list of schemes  covering a single kind of javascript import statements::

    {
        "schemes": [
            {
                "match_conditions": [
                    {
                        "query": "import",
                        "type": "startswith"
                    },
                    {
                        "query": "{(.*)}",
                        "type": "regex"
                    }
                ],
                "extraction_patterns": [
                    {
                        "properties": [
                            {
                                "property_name": "from_path",
                                "extraction_patterns":[
                                    {
                                        "query": "from\\s*?(?:\"|\\')(.*)(?:\"|\\')"
                                    }
                                ]
                            }
                        ],
                        "query": "{(.*)}"
                    },
                    {
                        "query": "(\\w+)"
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
        }
        {
            "name": "longNameC",
            "from_path": "./sample/path"
        }
    ]

++++++++++++++++
How it works
++++++++++++++++

Each scheme in the list will be applied if and only if all the conditions in the :code:`match_conditions`
are met::

    ...
    "match_conditions": [
        {
            "query": "import",
            "type": "startswith"
        },
        {
            "query": "{(.*)}",
            "type": "regex"
        }
    ],
    ...

Possible match conditions supported are:

* startwith
* endwith
* contains
* regex

If all the conditions are met, the regex expressions in the :code:`extraction_patterns` will
be applied in order, where the result of one will be used as the text to be parsed for the next::

    ...
    "extraction_patterns": [
        {
            "properties": [
                {
                    "property_name": "from_path",
                    "extraction_patterns":[
                        {
                            "query": "from\\s*?(?:\"|\\')(.*)(?:\"|\\')"
                        }
                    ]
                }
            ],
            "query": "{(.*)}"
        },
        {
            "query": "(\w+)"
        }
    ...

In the first extraction pattern, the expression :code:`{(.*)}` will extract::

    { sampleImportName1, sampleImportName2 }

The :code:`properties` attribute defines any additional properties to be extracted from the
text to be parsed. In this case, that is the path to the package to import from::

    ...
    "properties": [
        {
            "property_name": "from_path",
            "extraction_patterns":[
                {
                    "query": "from\s*?(?:"|\')(.*)(?:"|\')"
                }
            ]
        }
    ],
    ...

This extracts the below::

    'sample/path'

(Reminder: Each element in the :code:`extraction_patterns` receives the text to be parsed for
extraction from the result of the previous one)

This resulting text will then have the next expression applied to it, :code:`(\w+)`, that will
extract just the two resulting names in a list.

Note that properties defined upstream will apply to all matches found downstream.

This means that properties defined on the first element will be added to all matches
while properties defined on subsequent elements will only apply to specific matches

++++++++++++++++
Principles
++++++++++++++++
Ideally, each pattern list should be defined for a keyword for which names need to be extracted, for example::

    import sampleImportName from 'sample/path'
    const paramName = 'paramValue'

keywords are import and const here, names are sampleImportName, and paramName

names can be defined to have a value and a definition location, which we will refer to as scope.

In the above example::


    {
        "name": "sampleImportName",
        "from_path": "sample/path"
    },
    {
        "name": "paramName",
        "value": "paramValue",
        "scope": "./"
    }


having scope as its own object, defining both a file path and an reference to the
block containing the name definition is in consideration.