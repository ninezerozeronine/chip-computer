class AssemblyLine():
    def __init__(self):
        self.raw_line = None
        self.pattern = None
        self.line_no = None

def process_line(line, line_no):
    no_comments = strip_comments(line)
    tokens = get_tokens(line)
    pattern = get_pattern(tokens)
    return AssemblyLine(
        line_no=line_no,
        raw_line=line,
        pattern=pattern
    )

