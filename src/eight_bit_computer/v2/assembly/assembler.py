from . import patterns


class AssemblyLine():
    def __init__(self):
        self.raw_line = None
        self.pattern = None
        self.line_no = None
        self.machinecode = None

    def assign_machine_code_indecies(next_mc_index):
        if self.machinecode is None:
            return next_mc_index
        else:
            for word in machinecode:
                word.index = next_mc_index
                next_mc_index = next_mc_index + 1

        return next_mc_index

def process_raw_assembly_lines(lines):
    assembly_lines = []
    for line_no, line in enumerate(lines, start=1):
        try:
            assembly_line = process_line(line)
        except LineProcessingError as inst:
            msg = (
                "Error processing line {line_no} ({line}): "
                "{reason}".format(
                    line_no=line_no,
                    line=line,
                    reason=inst.args[0])
            )
            raise AssemblyError(msg)
        assembly_line.line_no = line_no
        assembly_lines.append(assembly_line)

    check_structure_validity(assembly_lines)
    assign_machine_code_indecies(assembly_lines)
    check_for_overlapping_indecies(assembly_lines)

    alias_map = build_alias_map(assembly_lines)
    resolve_aliases(assembly_lines, alias_map)

    label_map = build_label_map(assembly_lines)
    resolve_labels(assembly_lines, label_map)

    variable_map = build_variable_map(assembly_lines)
    resolve_variables(assembly_lines, variable_map)


def assign_machine_code_indecies(assembly_lines):
    next_mc_index = 0
    for line in assembly_lines:
        if isinstance(line.pattern, Anchor):
            next_mc_index = line.pattern.anchor_value()
        next_mc_index = line.assign_machine_code_indecies(next_mc_index)




def process_line(line):
    no_comments = remove_comments(line)
    try
        tokens = get_tokens(line)
    except InvalidTokenError:
        raise

    try
        pattern = get_pattern(tokens)
    except NoMatchingPatternError
        raise

    machinecode = pattern.generate_machinecode()

    return AssemblyLine(
        raw_line=line,
        pattern=pattern,
        machinecode=machinecode
    )


def remove_comments(line):
    """
    Remove comments from a line.

    A comment is anything on the line after and including an occurrence
    of ``//``.

    Args:
        line (str): line to remove comments from.
    Returns:
        str: The line with comments removed.
    """
    comment_index = line.find("//")
    comments_removed = line
    if comment_index >= 0:
        comments_removed = line[:comment_index]
    return comments_removed


def get_tokens(line):
    """
    Get the tokens this line contains.

    Expects the line to have had it's comments removed.

    Args:
        line (str): Line to get tokens from.
    Returns:
        list(Token): List of tokens on this line
    Raises:
        NoMatchingTokenError: When a matching token was not found
        MultipleTokensMatchedError: When a string in the line matched
            multiple tokens.
    """

    if not line:
        return []

    words = get_words_from_line(line)
    tokens = []
    for word in words:
        matched_tokens = []
        for token_class in tokens.get_all_tokens():
            token = token_class.from_string(word)
            if token is not None:
                matched_tokens.append(token)

        num_matches = len(matched_tokens)

        if num_matches == 0:
            raise NoMatchingTokenError

        if num_matches > 1:
            raise MultipleTokensMatchedError

        tokens.append(matched_tokens[0])
        
    return tokens


def get_words_from_line(line):
    """
    Given a line split it into words and return them.

    Words are runs of characters separated by spaces. If there are no
    words return an empty list.

    Args:
        line (str): Line to convert to tokens.
    Returns:
        list(str): The words.
    """

    # Does line have any content
    if not line:
        return []

    # Does the line have any content after splitting it
    words = line.split()
    if not words:
        return []

    return words


def get_pattern(tokens):
    """
    Find the pattern that the tokens match.

    Args:
        tokens list(Token): The tokens to match to a pattern.
    Returns:
        Pattern: The pattern that matches the tokens.
    Raises:
        NoMatchingPatternError: When not pattern could be found that
            matches the tokens.
        MultipleTokensMatchedError: When multiple patterns matched the
            tokens.
    """
    matched_patterns = []

    for pattern_class in patterns.get_all_patterns():
        pattern = pattern_class.from_tokens(tokens)
        if pattern is not None:
            matched_patterns.append(pattern)

    num_matches = len(matched_patterns)

    if num_matches == 0:
        raise NoMatchingPatternError

    if num_matches > 1:
        raise MultiplePatternsMatchedError

    return matched_patterns[0]
