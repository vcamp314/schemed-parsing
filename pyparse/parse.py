"""
This is a module used for config driven parsing.

"""
import re
import typing

# todo: fix up block-parsing-example.rst documentation to match implementation
# todo: rename module to schemed-parsing
# todo: create error handling layer
# todo: evaluate the possibility of creating blocklist class to make functions
#   like get_last_opened_block_that_ends_with more readable


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


def parse_all_lines(line_gen: typing.Generator, schemes: list) -> {list, list}:
    blocklist = []
    names = []
    line_no = 0

    for line in line_gen:
        line_no += 1
        apply_schemes_with_blocks(line, schemes, blocklist, names, line_no)

    return blocklist, names


# todo: add logic in function that calls this function to filter schemes based on match_conditions before passing
#  schemes
def apply_schemes_with_blocks(txt: str, schemes: list, blocklist: list, names: list, line_no: int):
    block_schemes = get_block_schemes(schemes)

    if schemes:
        search_str_pattern_type = {scheme['block_start_pattern']['query']: 'start' for scheme in block_schemes}
        search_str_pattern_type = {**search_str_pattern_type,
                                   **{scheme['block_end_pattern']['query']: 'end' for scheme in block_schemes}}

        search_str = '|'.join(
            [scheme['block_start_pattern']['query'] + '|' + scheme['block_end_pattern']['query'] for scheme in
             block_schemes])
        search_regex = re.compile(search_str)

        find_blocks(txt, schemes, search_regex, blocklist, names, search_str_pattern_type, line_no)


# todo: document this function's biz logic
# small is better than big... so process each individual line separately
# check for opening and closing of blocks, assign parts of the line based on this and apply the
# matching scheme for that part of the line of text

def find_blocks(txt: str, schemes: list, search_regex, blocklist: list, names: list, search_str_pattern_type: dict,
                line_no: int, ending_prop_schemes: list = None, ending_block_index: int = -1):
    match = search_regex.search(txt)
    last_unclosed_block_index = get_last_unclosed_block_index(blocklist)
    next_ending_prop_schemes = None
    next_ending_block_index = -1

    if match:
        first_matching_scheme = next(
            scheme for scheme in schemes if
            get_block_pattern_query(scheme, 'block_start_pattern') == match.group() or get_block_pattern_query(scheme,
                                                                                                               'block_end_pattern') == match.group())

        curr_txt = txt[:match.start()]
        # set all name matches for last unclosed block for text up until new block pattern match
        parse_block_names(curr_txt, last_unclosed_block_index, schemes, names)

        if ending_block_index != -1:
            prev_ending_props = extract_properties(curr_txt, ending_prop_schemes)
            blocklist[ending_block_index] = {**blocklist[ending_block_index], **prev_ending_props}

        # set the next text to search in from the remaining string in txt after the match
        next_txt = txt[match.start() + len(match.group()):]

        if search_str_pattern_type[match.group()] == 'start':
            curr_starting_props = extract_properties(curr_txt, first_matching_scheme['block_start_pattern'].get('properties'))
            curr_block = {
                'block_category': first_matching_scheme['block_category'],
                'starting_line_no': line_no,
                **curr_starting_props
            }
            parent_block_index = last_unclosed_block_index
            if parent_block_index != -1:
                curr_block['parent_id'] = parent_block_index

            blocklist.append(curr_block)

        if search_str_pattern_type[match.group()] == 'end':
            last_unclosed_matched_block_index = get_last_unclosed_block_index(blocklist,
                                                                              first_matching_scheme['block_category'])
            if last_unclosed_matched_block_index != -1:
                blocklist[last_unclosed_block_index]['ending_line_no'] = line_no

            next_ending_prop_schemes = first_matching_scheme['block_end_pattern'].get('properties')
            next_ending_block_index = last_unclosed_matched_block_index

        find_blocks(next_txt, schemes, search_regex, blocklist, names, search_str_pattern_type, line_no, next_ending_prop_schemes, next_ending_block_index)
    else:
        parse_block_names(txt, last_unclosed_block_index, schemes, names)
        if ending_block_index != -1:
            prev_ending_props = extract_properties(txt, ending_prop_schemes)
            blocklist[ending_block_index] = {**blocklist[ending_block_index], **prev_ending_props}


def get_last_unclosed_block_index(blocklist: list, category: str = None) -> int:
    # loop through blocks in reverse to find last using range
    for i in range(len(blocklist) - 1, -1, -1):
        if blocklist[i].get('ending_line_no') is None and (blocklist[i]['block_category'] == category or not category):
            return i
    return -1


def add_block_id_prop_to_schemes(schemes, block_id):
    modified_schemes = []
    block_id_prop = {
        'property_name': 'block_id',
        'value': block_id
    }
    for scheme in schemes:
        scheme_with_block_id = {**scheme}
        if scheme_with_block_id.get('extraction_patterns'):
            if scheme_with_block_id['extraction_patterns'][0].get('properties'):
                scheme_with_block_id['extraction_patterns'][0]['properties'].append(block_id_prop)
            else:
                scheme_with_block_id['extraction_patterns'][0]['properties'] = [block_id_prop, ]
            modified_schemes.append(scheme_with_block_id)

    return modified_schemes


def parse_block_names(txt: str, last_unclosed_block_index: int, schemes: list, names: list):
    if last_unclosed_block_index != -1:
        schemes_with_block_id_prop = add_block_id_prop_to_schemes(schemes, last_unclosed_block_index)

        last_unclosed_block_names = parse(txt, schemes_with_block_id_prop)
        names += last_unclosed_block_names


def get_block_pattern_query(scheme: dict, pattern_type: str):
    pattern = scheme.get(pattern_type)
    if pattern:
        return pattern['query']
    return None


def get_block_schemes(schemes: list) -> list:
    block_schemes = []

    for scheme in schemes:
        block_start_pattern = scheme.get('block_start_pattern')
        if block_start_pattern:
            block_end_pattern = scheme.get('block_end_pattern')
            if not block_end_pattern:
                continue

            block_schemes.append(scheme)

    return block_schemes


def apply_scheme(txt: str, scheme: dict) -> list:
    is_meeting_match_conditions = check_match_conditions(txt, scheme.get('match_conditions'))

    if is_meeting_match_conditions:
        return extract_names(txt, scheme['extraction_patterns'])

    return []


def check_match_conditions(txt: str, match_conditions: list) -> bool:
    if match_conditions is None:
        return True
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


# todo: document this function's biz logic
def set_props(props: dict, prop_props: dict, matches_found: list, field_name: str):
    # don't add props if nothing matched
    if not matches_found:
        return

    # single match should return just the value, not a list
    # multiple matches should be returned as a list
    resulting_match = matches_found
    if len(matches_found) == 1:
        resulting_match = matches_found[0]

    # if the prop has its own props, return it as an object with each of its prop fields
    resulting_prop = {'value': resulting_match, **prop_props} if prop_props != {} else resulting_match

    # in case of multiple props with the same field name, append them to a list
    current_value_in_field = props.get(field_name)
    if current_value_in_field:
        if type(current_value_in_field) is not list:
            props[field_name] = [current_value_in_field]

        props[field_name].append(resulting_prop)

    # only one prop with this field name, set the value directly
    else:
        props[field_name] = resulting_prop


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
                                      extraction_patterns, result_field_name)
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
