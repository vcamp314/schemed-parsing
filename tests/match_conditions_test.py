import os
import json
import pytest
from .context import pyparse

# the below two lines are for pip installing with test option and when
# the tests will open files:
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
os.chdir(CURRENT_DIR)


def test_empty_conditions_returns_true():
    txt = "import { sampleImportName1, sampleImportName2 } from './sample/path'"
    match_conditions = []
    assert pyparse.check_match_conditions(txt, match_conditions)


@pytest.fixture
def startswith_import_match_conditions():
    match_conditions = [
        {
            'query': 'import',
            'type': 'startswith'
        },
    ]
    return match_conditions


def test_empty_text_returns_false(startswith_import_match_conditions):
    txt = ''
    assert not pyparse.check_match_conditions(txt, startswith_import_match_conditions)


# startswith tests ######################


def test_startswith_returns_true_if_str_starts_with_query(startswith_import_match_conditions):
    txt = "import { sampleImportName1, sampleImportName2 } from './sample/path'"
    assert pyparse.check_match_conditions(txt, startswith_import_match_conditions)


def test_startswith_returns_false_if_str_does_not_start_with_query():
    txt = "import { sampleImportName1, sampleImportName2 } from './sample/path'"
    match_conditions = [
        {
            'query': 'const',
            'type': 'startswith'
        },
    ]
    assert not pyparse.check_match_conditions(txt, match_conditions)


# endswith tests ######################


def test_endswith_returns_true_if_str_end_with_query():
    txt = "import { sampleImportName1, sampleImportName2 } from './sample/path'"
    match_conditions = [
        {
            'query': "'./sample/path'",
            'type': 'endswith'
        },
    ]
    assert pyparse.check_match_conditions(txt, match_conditions)


def test_endswith_returns_false_if_str_does_not_end_with_query():
    txt = "import { sampleImportName1, sampleImportName2 } from './sample/path'"
    match_conditions = [
        {
            'query': "'./sample/path2'",
            'type': 'endswith'
        },
    ]
    assert not pyparse.check_match_conditions(txt, match_conditions)


# regex tests ######################


def test_regex_returns_false_if_does_not_match():
    txt = "import { sampleImportName1, sampleImportName2 } from './sample/path'"
    match_conditions = [
        {
            'query': r'import\s*?\(',
            'type': 'regex'
        },
    ]
    assert not pyparse.check_match_conditions(txt, match_conditions)


def test_regex_returns_true_if_matches():
    txt = "import('@middleware/users')"
    match_conditions = [
        {
            'query': r'import\s*?\(',
            'type': 'regex'
        },
    ]
    assert pyparse.check_match_conditions(txt, match_conditions)


# contains tests ######################


def test_contains_returns_false_if_txt_does_not_contains_query():
    txt = "import('@middleware/users')"
    match_conditions = [
        {
            'query': 'sampleImportName1',
            'type': 'contains'
        },
    ]
    assert not pyparse.check_match_conditions(txt, match_conditions)


def test_contains_returns_true_if_txt_contains_query():
    txt = "import { sampleImportName1, sampleImportName2 } from './sample/path'"
    match_conditions = [
        {
            'query': 'sampleImportName1',
            'type': 'contains'
        },
    ]
    assert pyparse.check_match_conditions(txt, match_conditions)
