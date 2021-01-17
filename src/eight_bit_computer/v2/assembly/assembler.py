class AssemblyLine():
    def __init__(self):
        self.raw_line = None
        self.pattern = None
        self.line_no = None
        self.machinecode = None

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
    pattern = None

    for pattern_class in all_pattern_classes:
        pattern = pattern_class.from_tokens(tokens)
        if pattern is not None:
            break
    else:
        raise NoMatchingPatternError

    return matched_pattern
