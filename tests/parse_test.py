import os
import json
import pytest
from .context import schemedparsing

# the below two lines are for pip installing with test option and when
# the tests will open files:
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
os.chdir(CURRENT_DIR)


def load(file_path: str):
    with open(file_path, 'r') as file:
        for line in file:
            yield line


def load_json(file_path: str):
    with open(file_path, 'r') as file:
        return json.load(file)


def test_empty_schemes_returns_empty_list():
    schemes = []
    txt = "import { sampleImportName1, sampleImportName2 } from './sample/path'"
    expected = []
    assert schemedparsing.parse(txt, schemes) == expected


@pytest.fixture
def load_schemes():
    return load_json('../docs/sample-schemes.json')['schemes']


@pytest.fixture
def load_block_schemes():
    return load_json('../docs/sample-block-schemes.json')['schemes']


@pytest.fixture
def load_block_text():
    return load('sample-flat-blocks-text.txt')


def test_empty_str_returns_empty_list(load_schemes):
    txt = ''
    expected = []
    assert schemedparsing.parse(txt, load_schemes) == expected


def test_js_import_sample_returns_import_names_dict(load_schemes):
    txt = "import { sampleImportName1, sampleImportName2 } from './sample/path'"
    expected = [
        {
            "name": "sampleImportName1",
            "from_path": "./sample/path"
        },
        {
            "name": "sampleImportName2",
            "from_path": "./sample/path"
        }
    ]
    assert schemedparsing.parse(txt, load_schemes) == expected


def test_js_import_block_sample_returns_import_names_dict(load_block_schemes, load_block_text):
    txt = load_block_text

    expected_blocks = [
        {
            'block_category': 'block_import',
            "from_path": "/some/pretty/long/path/",
            'starting_line_no': 1,
            'ending_line_no': 5,
        },
    ]
    expected_names = [
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
    result_blocks, result_names = schemedparsing.parse_all_lines(txt, load_block_schemes)

    assert result_blocks == expected_blocks
    assert result_names == expected_names
