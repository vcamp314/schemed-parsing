import os
import pytest
from .context import schemedparsing

# the below two lines are for pip installing with test option and when
# the tests will open files:
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
os.chdir(CURRENT_DIR)


def test_block_extraction_empty_patterns_returns_empty_list():
    txt_gen = (txt for txt in ["import { sampleImportName1, sampleImportName2 } from './sample/path'"])
    schemes = []
    expected = []
    result_blocklist, result_names = schemedparsing.parse_all_lines(txt_gen, schemes)
    assert result_blocklist == expected
    assert result_names == expected


@pytest.fixture
def single_extraction_pattern():
    return [{'query': r'import (\w+)', }, ]


def test_extraction_empty_text_returns_empty_list(single_extraction_pattern):
    txt_gen = (txt for txt in [])
    expected = []
    result_blocklist, result_names = schemedparsing.parse_all_lines(txt_gen, single_extraction_pattern)
    assert result_blocklist == expected
    assert result_names == expected


def test_find_flat_blocks():
    txt = 'if(isTest == true){ doSomething() }; if(isSpecialTest == true) { doSomethingElse() };'
    block_schemes = [
        {
            'block_start_pattern': {'query': '{'},
            'block_end_pattern': {'query': '}'},
            'block_category': 'test_cat',
        }
    ]
    expected = [
        {
            'block_category': 'test_cat',
            'starting_line_no': 1,
            'ending_line_no': 1,
        },
        {
            'block_category': 'test_cat',
            'starting_line_no': 1,
            'ending_line_no': 1,
        }
    ]

    result = []
    names = []
    line_no = 1
    schemedparsing.apply_schemes_with_blocks(txt, block_schemes, result, names, line_no)

    assert result == expected
    assert names == []


def test_find_nested_blocks():
    txt = 'if(isTest == true){ if(isSpecialTest == true;) { doSomethingElse(); } }'
    block_schemes = [
        {
            'block_start_pattern': {'query': '{'},
            'block_end_pattern': {'query': '}'},
            'block_category': 'test_cat',
        }
    ]
    expected = [
        {
            'block_category': 'test_cat',
            'starting_line_no': 1,
            'ending_line_no': 1,
        },
        {
            'block_category': 'test_cat',
            'starting_line_no': 1,
            'ending_line_no': 1,
            'parent_id': 0,
        }
    ]

    result = []
    names = []
    line_no = 1
    schemedparsing.apply_schemes_with_blocks(txt, block_schemes, result, names, line_no)

    assert result == expected
    assert names == []


def test_find_flat_blocks_and_their_params():
    txt = "import { sampleImportName1, sampleImportName2 } from './sample/path'; import { sampleImportName3, " \
          "sampleImportName4 } from './sample/path'; "
    block_schemes = [
        {
            'block_start_pattern': {'query': '{'},
            'block_end_pattern': {'query': '}'},
            'block_category': 'test_cat',
            'extraction_patterns': [
                {
                    'query': r'(\w+)'
                }
            ]
        }
    ]
    expected_blocks = [
        {
            'block_category': 'test_cat',
            'starting_line_no': 1,
            'ending_line_no': 1,
        },
        {
            'block_category': 'test_cat',
            'starting_line_no': 1,
            'ending_line_no': 1,
        }
    ]
    expected_names = [
        {
            'name': 'sampleImportName1',
            'block_id': 0,
        },
        {
            'name': 'sampleImportName2',
            'block_id': 0,
        },
        {
            'name': 'sampleImportName3',
            'block_id': 1,
        },
        {
            'name': 'sampleImportName4',
            'block_id': 1,
        },
    ]

    result_blocks = []
    result_names = []
    line_no = 1
    schemedparsing.apply_schemes_with_blocks(txt, block_schemes, result_blocks, result_names, line_no)

    assert result_blocks == expected_blocks
    assert result_names == expected_names


def test_find_flat_blocks_with_ending_props_and_params():
    txt = "import { sampleImportName1, sampleImportName2 } from './sample/path1'; import { sampleImportName3, " \
          "sampleImportName4 } from './sample/path2'; "
    block_schemes = [
        {
            'block_start_pattern': {'query': '{'},
            'block_end_pattern': {
                'query': '}',
                'properties': [
                    {
                        'property_name': 'from_path',
                        'extraction_patterns': [
                            {
                                'query': r'from\s*?(?:"|\')(.*)(?:"|\')'
                            }
                        ]
                    }
                ]
            },
            'block_category': 'test_cat',
            'extraction_patterns': [
                {
                    'query': r'(\w+)'
                }
            ]
        }
    ]
    expected_blocks = [
        {
            'block_category': 'test_cat',
            'starting_line_no': 1,
            'ending_line_no': 1,
            'from_path': './sample/path1',
        },
        {
            'block_category': 'test_cat',
            'starting_line_no': 1,
            'ending_line_no': 1,
            'from_path': './sample/path2',
        }
    ]
    expected_names = [
        {
            'name': 'sampleImportName1',
            'block_id': 0,
        },
        {
            'name': 'sampleImportName2',
            'block_id': 0,
        },
        {
            'name': 'sampleImportName3',
            'block_id': 1,
        },
        {
            'name': 'sampleImportName4',
            'block_id': 1,
        },
    ]

    result_blocks = []
    result_names = []
    line_no = 1
    schemedparsing.apply_schemes_with_blocks(txt, block_schemes, result_blocks, result_names, line_no)

    assert result_blocks == expected_blocks
    assert result_names == expected_names


def test_find_flat_blocks_with_starting_props_and_params():
    txt = "; import { sampleImportName1, sampleImportName2 } from './sample/path1'; import { sampleImportName3, " \
          "sampleImportName4 } from './sample/path2'; "
    block_schemes = [
        {
            'block_start_pattern': {
                'query': '{',
                'properties': [
                    {
                        'property_name': 'block_type',
                        'extraction_patterns': [
                            {
                                'query': r'; (\w+)'
                            }
                        ]
                    }
                ]
            },
            'block_end_pattern': {'query': '}'},
            'block_category': 'test_cat',
            'extraction_patterns': [
                {
                    'query': r'(\w+)'
                }
            ]
        }
    ]
    expected_blocks = [
        {
            'block_category': 'test_cat',
            'starting_line_no': 1,
            'ending_line_no': 1,
            'block_type': 'import',
        },
        {
            'block_category': 'test_cat',
            'starting_line_no': 1,
            'ending_line_no': 1,
            'block_type': 'import',
        }
    ]
    expected_names = [
        {
            'name': 'sampleImportName1',
            'block_id': 0,
        },
        {
            'name': 'sampleImportName2',
            'block_id': 0,
        },
        {
            'name': 'sampleImportName3',
            'block_id': 1,
        },
        {
            'name': 'sampleImportName4',
            'block_id': 1,
        },
    ]

    result_blocks = []
    result_names = []
    line_no = 1
    schemedparsing.apply_schemes_with_blocks(txt, block_schemes, result_blocks, result_names, line_no)

    assert result_blocks == expected_blocks
    assert result_names == expected_names