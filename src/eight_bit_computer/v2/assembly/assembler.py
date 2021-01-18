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
    label_map = build_label_map(assembly_lines)
    alias_map = build_alias_map(assembly_lines)
    variable_map = build_variable_map(assembly_lines)


def assign_machine_code_indecies(assembly_lines):
    next_mc_index = 0
    for line in assembly_lines:
        if isinstance(line.pattern, Anchor):
            next_mc_index = line.pattern.anchor_value()
        next_mc_index = line.assign_machine_code_indecies(next_mc_index)




def process_line(line):
    no_comments = strip_comments(line)
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

def get_pattern(tokens):
    """
    Find a pattern from the tokens.

    If none of the matchers match thats a problem - raise

    """
    pattern = None

    for pattern_class in patterns.get_all_patterns():
        pattern = pattern_class.from_tokens(tokens)
        if pattern is not None:
            break
    else:
        raise NoMatchingPatternError

    return matched_pattern
