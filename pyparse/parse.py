"""
This is a module used for config driven parsing.

"""
import re
import typing


def parse(txt: str, schemes: list) -> list:
    """Parse text based on provided list of parsing schemes"
    >>> parse('some text', [])
    []

    :return: dict
    """
    all_extracted_names = []

    for scheme in schemes:
        current_scheme_names = apply_scheme(txt, scheme)
        all_extracted_names += current_scheme_names

    return all_extracted_names


def apply_scheme(txt: str, scheme: dict) -> list:
    is_meeting_match_conditions = check_match_conditions(txt, scheme['match_conditions'])

    if is_meeting_match_conditions:
        return extract_names(txt, scheme['extraction_patterns'])

    return []


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


def extract_names(txt: str, extraction_patterns: list) -> list:
    if not extraction_patterns:
        return []
    extracted_names = []
    matches = [txt]
    props = {}
    current_index = 0

    apply_extraction_patterns(set_names, extracted_names, matches, props, current_index, extraction_patterns)
    return extracted_names


def set_names(names: list, props: dict, matches_found: list, field_name: str = 'name'):
    names += [{field_name: match, **props} for match in matches_found]


def set_props(props: dict, prop_props: dict, matches_found: list, field_name: str):
    resulting_match = matches_found
    if len(matches_found) == 1:
        resulting_match = matches_found[0]

        props[field_name] = resulting_match

    if prop_props != {}:
        props[field_name] = {'value': resulting_match, **prop_props}


# iterative function for going through each level of extraction patterns
# for each set of previously found matches
def apply_extraction_patterns(set_results_func: typing.Callable, names: typing.Union[list, dict], prev_matches: list,
                              prev_props: dict, current_index: int, extraction_patterns: list,
                              result_field_name: str = 'name'):
    next_index = current_index + 1
    current_extraction_pattern = extraction_patterns[current_index]

    for prev_match in prev_matches:

        # apply extraction pattern regex
        next_matches = re.findall(current_extraction_pattern['query'], prev_match)

        # extract properties
        matched_props = extract_properties(prev_match, current_extraction_pattern.get('properties'))
        props = {**prev_props, **matched_props}

        if next_index < len(extraction_patterns):

            # if there are more extraction patterns,
            # apply them to the next set of matches
            apply_extraction_patterns(set_results_func, names, next_matches, props, next_index,
                                      extraction_patterns)
        else:
            # if there are no more extraction patterns,
            # set final results using passed function call
            # to allow handling either names or props
            set_results_func(names, props, next_matches, result_field_name)


def extract_properties(txt: str, prop_patterns: list) -> dict:
    extracted_props = {}
    if not prop_patterns:
        return extracted_props

    for pattern in prop_patterns:
        value_to_set = pattern.get('value')

        if value_to_set is not None:
            extracted_props[pattern['property_name']] = value_to_set
            continue

        matches = [txt]
        props = {}
        current_index = 0

        apply_extraction_patterns(set_props, extracted_props, matches, props, current_index,
                                  pattern['extraction_patterns'], pattern['property_name'])

    return extracted_props
