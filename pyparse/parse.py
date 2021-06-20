"""
This is a module used for config driven parsing.

"""
import re

def parse(txt: str, schemes: list) -> dict:
    """Parse text based on provided list of parsing schemes"
    >>> parse('some text', [])
    {}

    :return: dict
    """
    all_extracted_names = {}

    for scheme in schemes:
        current_scheme_names = apply_scheme(txt, scheme)
        all_extracted_names = {**all_extracted_names, **current_scheme_names}

    return all_extracted_names


def apply_scheme(txt: str, scheme: dict) -> dict:

    is_meeting_match_conditions = check_match_conditions(txt, scheme['match_conditions'])

    if is_meeting_match_conditions:
        return extract_names(txt, scheme['extraction_patterns'])

    return {}


def check_match_conditions(txt: str, match_conditions: list) -> bool:

    for match_condition in match_conditions:
        is_matched_condition = check_match_condition(txt, match_condition)
        if not is_matched_condition:
            return False
    return True


def check_match_condition(txt: str, match_condition: dict) -> bool:

    if match_condition['type'] == 'regex':
        return re.search(match_condition['query'], txt) is not None

    if match_condition['type'] == 'contains':
        return match_condition['query'] in txt

    # startswith and endswith case, utilize built in str class methods via getattr
    pattern_func = getattr(txt, match_condition['type'])
    return pattern_func(match_condition['query'])


def extract_names(txt: str, extraction_patterns: list) -> dict:

    return {}
