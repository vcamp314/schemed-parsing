Parsing scheme example
=================================
example composition of a list of schemes covering a single kind of javascript import statements::

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
                        "properties": {
                            "property_name": "from_path",
                            "extraction_patterns":[
                                {
                                    "query": "from\\s*?(?:\"|\\')(.*)(?:\"|\\')"
                                }
                            ]
                        },
                        "query": "{(.*)}"
                    },
                    {
                        "type": "findall",
                        "query": "(\\w+)"
                    }
                ]
            }
        ]
    }


the above example would apply to the below example import statement structure::

     import { sampleImportName1, sampleImportName2 } from './sample/path'

the parsing will extract the names, `sampleImportName1`, `sampleImportName2` into a dict of the below structure::


    "sampleImportName1": {
        "from_path": "./sample/path"
    }
    "sampleImportName2": {
        "from_path": "./sample/path"
    }

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
                "property_name": "from_path",
                "extraction_patterns":[
                    {
                        "query": "from\s*?(?:"|\')(.*)(?:"|\')"
                    }
                ]
            ],
            "query": "{(.*)}",
        },
        {
            "type": "findall",
            "query": "(\w+)"
        }
    ...

In the first extraction pattern, the expression :code:`{(.*)}` will extract::

    { sampleImportName1, sampleImportName2 }

The :code:`properties` attribute defines any additional properties to be extracted from the
text to be parsed. In this case, that is the path to the package to import from::

    ...
    "properties": [
        "property_name": "from_path",
        "extraction_patterns":[
            {
                "query": "from\s*?(?:"|\')(.*)(?:"|\')"
            }
        ]
    ],
    ...

This extracts the below::

    'sample/path'

(Reminder: Each element in the :code:`extraction_patterns` receives the text to be parsed for
extraction from the result of the previous one)

This resulting text will then have the next expression applied to it, :code:`(\w+)`, that will
extract just the two resulting names in a list.

Note that if properties are defined downstream from an element in :code:`extraction_patterns`
that has a :code:`type` defined as :code:`findall` the properties found on a single match will
only be added as attributes to the names found on that single match.

Otherwise it will be added to all names found in this scheme.

++++++++++++++++
Principles
++++++++++++++++
Ideally, each pattern list should be defined for a keyword for which names need to be extracted, for example::

    import sampleImportName from 'sample/path'
    const paramName = 'paramValue'

keywords are import and const here, names are sampleImportName, and paramName

names can be defined to have a value and a definition location, which we will refer to as scope.

In the above example::


    "sampleImportName": {
        "value": undefined
        "from_path": "sample/path"
    }
    "sampleImportName": {
        "value": "paramValue"
        "scope": "./"
    }


having scope as its own object, defining both a file path and an reference to the
block containing the name definition is in consideration.