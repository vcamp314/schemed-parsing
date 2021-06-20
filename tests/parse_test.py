import os
import json
import pytest
from .context import pyparse

# the below two lines are for pip installing with test option and when
# the tests will open files:
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
os.chdir(CURRENT_DIR)

# todo: create extraction patterns simple test ? findall needed?
# todo: create extraction patterns multiple test
# todo: create extraction patterns simple findall test
# todo: create extraction patterns multiple with starting findall test
# todo: create extraction patterns multiple with ending findall test
# todo: create extraction patterns multiple with middle findall test
# todo: create extraction patterns properties test
# todo: create extraction patterns properties upstream test
# todo: create extraction patterns properties downstream test


def load(file_path: str):
    with open(file_path, 'r') as file:
        return json.load(file)


def test_empty_schemes_returns_empty_dict():
    schemes = []
    txt = "import { sampleImportName1, sampleImportName2 } from './sample/path'"
    expected = {}
    assert pyparse.parse(txt, schemes) == expected


@pytest.fixture
def load_schemes():
    return load('../docs/sample-schemes.json')['schemes']


def test_empty_str_returns_empty_dict(load_schemes):
    txt = ''
    expected = {}
    assert pyparse.parse(txt, load_schemes) == expected


def test_js_import_sample_returns_import_names_dict(load_schemes):
    txt = "import { sampleImportName1, sampleImportName2 } from './sample/path'"
    expected = {
        "sampleImportName1": {
            "from_path": "./sample/path"
        },
        "sampleImportName2": {
            "from_path": "./sample/path"
        }
    }
    assert pyparse.parse(txt, load_schemes) == expected
