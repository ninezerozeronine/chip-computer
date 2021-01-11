class AssemblyLine():
    def __init__(self):
        self.raw_line = None
        self.pattern = None
        self.line_no = None

def process_line(line, line_no):
    no_comments = strip_comments(line)
    try
        tokens = get_tokens(line)
    except InvalidTokenError:
        raise

    try
        pattern = get_pattern(tokens)
    except NoMatchingPatternError
        raise

    return AssemblyLine(
        line_no=line_no,
        raw_line=line,
        pattern=pattern
    )

def get_pattern(tokens):
    """
    Find a pattern from the tokens.

    If none of the matchers match thats a problem - raise

    """
    matched_pattern = True

    for pattern_matcher in pattern_matchers:
        pattern = pattern_matcher(tokens)
        if pattern is None:
            continue
        else
            matched_pattern = pattern
            break

    if matched_pattern is None:
        raise NoMatchingPatternError

    return matched_pattern

    pattern = pattern_matcher(tokens):
    if 