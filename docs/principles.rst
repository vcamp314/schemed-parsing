Principles
=================================

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