import os
import pytest
from .context import schemedparsing

# the below two lines are for pip installing with test option and when
# the tests will open files:
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
os.chdir(CURRENT_DIR)


def test_extraction_empty_patterns_returns_empty_dict():
    txt = "import { sampleImportName1, sampleImportName2 } from './sample/path'"
    extraction_patterns = []
    expected = []
    assert schemedparsing.extract_names(txt, extraction_patterns) == expected


@pytest.fixture
def single_extraction_pattern():
    return [{'query': r'import (\w+)', }, ]


def test_extraction_empty_text_returns_false(single_extraction_pattern):
    txt = ''
    expected = []
    assert schemedparsing.extract_names(txt, single_extraction_pattern) == expected


def test_single_extraction_pattern_that_returns_single_item(single_extraction_pattern):
    txt = "import sampleImportName from './sample/path'"
    expected = [{'name': 'sampleImportName'}]
    assert schemedparsing.extract_names(txt, single_extraction_pattern) == expected


def test_multiple_extraction_pattern_that_returns_multiple_items():
    txt = "import { sampleImportName1, sampleImportName2 } from './sample/path'"
    multiple_extraction_pattern = [{'query': '{(.*)}', }, {'query': r'(\w+)', }]
    expected = [
        {'name': 'sampleImportName1'},
        {'name': 'sampleImportName2'}
    ]
    assert schemedparsing.extract_names(txt, multiple_extraction_pattern) == expected


def test_single_extraction_pattern_with_property():
    txt = "import sampleImportName from './sample/path'"
    extraction_pattern_with_props = [
        {
            'query': r'import (\w+)',
            'properties': [
                {
                    'property_name': 'from_path',
                    'extraction_patterns': [
                        {
                            'query': r'from\s*?(?:"|\')(.*)(?:"|\')'
                        }
                    ]
                }
            ],
        },
    ]
    expected = [{'name': 'sampleImportName', 'from_path': './sample/path'}]
    assert schemedparsing.extract_names(txt, extraction_pattern_with_props) == expected


def test_single_extraction_pattern_with_multiple_properties():
    txt = "@Prop({ required: false, type: String, default: 'default' })readonly sampleParam!: string"
    extraction_pattern_with_props = [
        {
            'query': r'\)readonly (.*)!',
            'properties': [
                {
                    'property_name': 'required',
                    'extraction_patterns': [
                        {
                            'query': r'required: (.*?),'
                        }
                    ]
                },
                {
                    'property_name': 'type',
                    'extraction_patterns': [
                        {
                            'query': r'type: (.*?),'
                        }
                    ]
                },
                {
                    'property_name': 'default',
                    'extraction_patterns': [
                        {
                            'query': r'default: (.*?) }'
                        }
                    ]
                }
            ],
        },
    ]
    expected = [{'name': 'sampleParam', 'required': 'false', 'type': 'String', 'default': "'default'"}]
    assert schemedparsing.extract_names(txt, extraction_pattern_with_props) == expected


def test_single_extraction_pattern_with_deep_properties():
    txt = "@Prop({ required: false, type: String, default: 'default' })readonly sampleParam!: string"
    extraction_pattern_with_props = [
        {
            'query': r'\)readonly (.*)!',
            'properties': [
                {
                    'property_name': 'required',
                    'extraction_patterns': [
                        {
                            'query': r'\((.*)\)'
                        },
                        {
                            'query': r'required: (.*?),'
                        }
                    ]
                },
            ],
        },
    ]
    expected = [{'name': 'sampleParam', 'required': 'false'}]
    assert schemedparsing.extract_names(txt, extraction_pattern_with_props) == expected


def test_single_extraction_pattern_with_multiple_matches_and_props():
    txt = "def set_props(props: dict, prop_props: dict, matches_found: list, field_name: str):"
    extraction_pattern_with_props = [
        {
            'query': r'\((.*)\)',
        },
        {
            'query': r'(.*?)(?:,|$)',
        },
        {
            'query': r'(\w+):',
            'properties': [
                {
                    'property_name': 'type',
                    'extraction_patterns': [
                        {
                            'query': r': (.*)\s*?'
                        }
                    ]
                },
            ],
        }
    ]
    expected = [
        {'name': 'props', 'type': 'dict'},
        {'name': 'prop_props', 'type': 'dict'},
        {'name': 'matches_found', 'type': 'list'},
        {'name': 'field_name', 'type': 'str'},
    ]
    assert schemedparsing.extract_names(txt, extraction_pattern_with_props) == expected


def test_single_extraction_pattern_that_has_prop_with_object_value():
    txt = "def set_props(props: dict, prop_props: dict, matches_found: list, field_name: str):"
    extraction_pattern_with_props = [
        {
            'query': r'def (.*)\(',
            'properties': [
                {
                    'property_name': 'args',
                    'extraction_patterns': [
                        {
                            'query': r'\((.*)\)',
                        },
                        {
                            'query': r'(.*?)(?:,|$)',
                        },
                        {
                            'query': r'(\w+):',
                            'properties': [
                                {
                                    'property_name': 'type',
                                    'extraction_patterns': [
                                        {
                                            'query': r': (.*)\s*?'
                                        }
                                    ]
                                },
                            ],
                        }
                    ]
                },
            ],
        },
    ]
    expected = [
        {
            'name': 'set_props',
            'args': [
                {
                    'value': 'props',
                    'type': 'dict'
                },
                {
                    'value': 'prop_props',
                    'type': 'dict'
                },
                {
                    'value': 'matches_found',
                    'type': 'list'
                },
                {
                    'value': 'field_name',
                    'type': 'str'
                }
            ]
        },
    ]
    assert schemedparsing.extract_names(txt, extraction_pattern_with_props) == expected


def test_single_extraction_pattern_that_has_prop_with_preset_value():
    txt = "def set_props(props: dict, prop_props: dict, matches_found: list, field_name: str):"
    extraction_pattern_with_props = [
        {
            'query': r'def (.*)\(',
            'properties': [
                {
                    'property_name': 'args',
                    'extraction_patterns': [
                        {
                            'query': r'\((.*)\)',
                        },
                        {
                            'query': r'(.*?)(?:,|$)',
                        },
                        {
                            'query': r'(\w+):',
                            'properties': [
                                {
                                    'property_name': 'type',
                                    'value': 'function_input_param',
                                },
                            ],
                        }
                    ]
                },
            ],
        },
    ]
    expected = [
        {
            'name': 'set_props',
            'args': [
                {
                    'value': 'props',
                    'type': 'function_input_param'
                },
                {
                    'value': 'prop_props',
                    'type': 'function_input_param'
                },
                {
                    'value': 'matches_found',
                    'type': 'function_input_param'
                },
                {
                    'value': 'field_name',
                    'type': 'function_input_param'
                }
            ]
        },
    ]
    assert schemedparsing.extract_names(txt, extraction_pattern_with_props) == expected