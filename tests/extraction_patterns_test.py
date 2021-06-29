import os
import json
import pytest
from .context import pyparse

# the below two lines are for pip installing with test option and when
# the tests will open files:
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
os.chdir(CURRENT_DIR)


# todo: create extraction patterns properties upstream test
# todo: create extraction patterns properties downstream test


def test_extraction_empty_patterns_returns_empty_dict():
    txt = "import { sampleImportName1, sampleImportName2 } from './sample/path'"
    extraction_patterns = []
    expected = []
    assert pyparse.extract_names(txt, extraction_patterns) == expected


@pytest.fixture
def single_extraction_pattern():
    return [{'query': r'import (\w+)', }, ]


def test_extraction_empty_text_returns_false(single_extraction_pattern):
    txt = ''
    expected = []
    assert pyparse.extract_names(txt, single_extraction_pattern) == expected


# startswith tests ######################


def test_single_extraction_pattern_that_returns_single_item(single_extraction_pattern):
    txt = "import sampleImportName from './sample/path'"
    expected = [{'name': 'sampleImportName'}]
    assert pyparse.extract_names(txt, single_extraction_pattern) == expected


def test_multiple_extraction_pattern_that_returns_multiple_items():
    txt = "import { sampleImportName1, sampleImportName2 } from './sample/path'"
    multiple_extraction_pattern = [{'query': '{(.*)}', }, {'query': r'(\w+)', }]
    expected = [
        {'name': 'sampleImportName1'},
        {'name': 'sampleImportName2'}
    ]
    assert pyparse.extract_names(txt, multiple_extraction_pattern) == expected


def test_single_extraction_pattern_with_properties():
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
    assert pyparse.extract_names(txt, extraction_pattern_with_props) == expected
