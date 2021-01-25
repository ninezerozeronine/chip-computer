from .assembly import patterns, tokens
from .exceptions import (
    LineProcessingError,
    NoMatchingTokensError,
    MultipleMatchingTokensError,
    NoMatchingPatternsError,
    MultipleMatchingPatternsError,
)

ERROR_TEMPLATE = "Error processing line {line_no} ({line}): {details}"


class AssemblyLine():
    def __init__(self, raw_line=None, pattern=None, line_no=None):
        self.raw_line = raw_line
        self.pattern = pattern
        self.line_no = None


def ingest_raw_assembly_lines(lines):
    assembly_lines = []
    for line_no, line in enumerate(lines, start=1):
        try:
            pattern = pattern_from_line(line)
        except LineProcessingError as err:
            msg = ERROR_TEMPLATE.format(
                line_no=line_no,
                line=raw_line,
                details=err.args[0],
            )
            raise AssemblyError(msg)

        assembly_lines.append(
            AssemblyLine(
                raw_line=line,
                line_no=line_no,
                pattern=pattern
            )
        )

    return assembly_lines


def process_assembly_lines(assembly_lines):

    check_multiple_alias_defs(assembly_lines)
    check_multiple_marker_defs(assembly_lines)
    check_multiple_marker_assignment(assembly_lines)
    check_numbers_in_range(assembly_lines)

    assign_machinecode_indecies(assembly_lines)
    check_for_colliding_indecies(assembly_lines)

    resolve_numbers(assembly_lines)

    alias_map = build_alias_map(assembly_lines)
    resolve_aliases(assembly_lines, alias_map)

    marker_map = build_marker_map(assembly_lines)
    resolve_markers(assembly_lines, marker_map)


def pattern_from_line(line):
    """
    Get the pattern corresponding to a raw line of assembly code.

    A raw line is something like: ``LOAD [$var] A // A comment.``

    Args:
        line (str): Raw line of assembly code.
    Returns:
        Pattern: Pattern that corresponds to the passed in line.
    """

    no_comments = remove_comments(line)
    tokens = get_tokens(line)
    pattern = get_pattern(tokens)
    return pattern


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
        NoMatchingTokensError: When a matching token was not found.
        MultipleMatchingTokensError: When multiple tokens matched.
    """

    if not line:
        return []

    words = get_words_from_line(line)
    final_tokens = []
    for word in words:
        matched_tokens = []
        for token_class in tokens.get_all_tokens():
            token = token_class.from_string(word)
            if token is not None:
                matched_tokens.append(token)

        num_matches = len(matched_tokens)

        if num_matches == 0:
            raise NoMatchingTokensError("No tokens matched")

        if num_matches > 1:
            raise MultipleMatchingTokensError("Multiple tokens matched")

        final_tokens.append(matched_tokens[0])

    return final_tokens


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
        NoMatchingPatternsError: When a matching token was not found.
        MultipleMatchingPatternsError: When multiple tokens matched.
    """
    matched_patterns = []

    for pattern_class in patterns.get_all_patterns():
        pattern = pattern_class.from_tokens(tokens)
        if pattern is not None:
            matched_patterns.append(pattern)

    num_matches = len(matched_patterns)

    if num_matches == 0:
        raise NoMatchingPatternsError("No patterns matched")

    if num_matches > 1:
        raise MultipleMatchingPatternsError("Multiple patterns matched")

    return matched_patterns[0]


def check_multiple_alias_defs(assembly_lines):
    """
    Check if an alias has been defined multiple times.

    E.g. This is allowed::

        !MY_ALIAS #123
        !OTHER_ALIAS #456

    But this is not::

        !MY_ALIAS #123
        !MY_ALIAS #456

    Args:
        assembly_lines (list(:class:`~.AssemblyLine`)): List of
            processed lines of assembly.
    Raises:
        AssemblyError: If the same alias has been defined more than
            once.
    """

    aliases = set()
    alias_lines = {}
    for assembly_line in assembly_lines:
        if isinstance(assembly_line.pattern, AliasDef):
            alias = assembly_line.pattern.alias
            if alias in aliases:
                details = (
                    "The alias: \"{alias}\" has already been defined on "
                    "line {prev_line}.".format(
                        alias=alias,
                        prev_line=alias_lines[alias],
                    )
                )
                msg = ERROR_TEMPLATE.format(
                    line_no=assembly_line.line_no,
                    line=assembly_line.raw_line,
                    details=details,
                )
                raise AssemblyError(msg)
            else:
                aliases.add(alias)
                alias_lines[alias] = assembly_line.line_no


def check_multiple_marker_defs(assembly_lines):
    """
    Check if a marker been defined more than once.

    E.g. This is allowed::

        $marker_0 #123

        $marker_1
            NOOP
        $marker_2
            "hello"

    But this is not::

        $marker_0 #123
        $marker_0 #456

        $marker_1
            NOOP
        $marker_1
            "hello"

    As ``$marker_0`` is defined twice, and ``$marker_1`` is already
    assigned to the index holding the ``NOOP`` instruction.

    Args:
        assembly_lines (list(:class:`~.AssemblyLine`)): List of
            processed lines of assembly.
    Raises:
        AssemblyError: If the same marker has been defined more than
            once.
    """

    markers = set()
    marker_lines = {}
    for assembly_line in assembly_lines:
        if isinstance(assembly_line.pattern, (Marker, MarkerDef)):
            marker = assembly_line.pattern.marker
            if marker in markers:
                details = (
                    "The marker: \"{marker}\" has already been defined on "
                    "line {prev_line}.".format(
                        marker=marker,
                        prev_line=marker_lines[marker],
                    )
                )
                msg = ERROR_TEMPLATE.format(
                    line_no=assembly_line.line_no,
                    line=assembly_line.raw_line,
                    details=details,
                )
                raise AssemblyError(msg)
            else:
                markers.add(marker)
                marker_lines[marker] = assembly_line.line_no


def check_multiple_marker_assignment(assembly_lines):
    """
    Check if a line would be assigned more than one marker.

    E.g. This is allowed::

        &marker_1
            NOOP
        &marker_2
            SET_ZERO A

    But this is not::

        &marker_1
        &marker_2
            SET_ZERO A

    As the ``SET_ZERO A`` instruction would have both ``&marker_1`` and
    ``&marker_2`` assgned to it.

    Args:
        assembly_lines (list(:class:`~.AssemblyLine`)): List of
            processed lines of assembly.
    Raises:
        AssemblyError: If a line been assigned more than one marker.
    """

    marker_queued = False
    last_marker = ""
    for assembly_line in assembly_lines:
        if marker_queued and isinstance(assembly_line.pattern, Marker):
            details = (
                "There is already a marker ({marker}) queued for "
                "assignment to the next machinecode word.".format(
                    marker=last_marker
                )
            )
            msg = ERROR_TEMPLATE.format(
                line_no=assembly_line.line_no,
                line=assembly_line.raw_line,
                details=details,
            )
            raise AssemblyError(msg)

        if isinstance(assembly_line.pattern, Marker):
            marker_queued = True
            last_marker = assembly_line.pattern.marker

        if assembly_line.has_machine_code() and marker_queued:
            marker_queued = False


def assign_machinecode_indecies(assembly_lines):
    """
    Assign indecies to all the machinecode words.

    Instructions can resolve to more than one word, and sections of
    assembly can be anchored so the machine code index has no
    correlation to the assembly line index.

    Edits the assembly lines in place.

    Args:
        assembly_lines (list(:class:`~.AssemblyLine`)): List of
            processed lines of assembly.
    """
    next_mc_index = 0
    for line in assembly_lines:
        if isinstance(line.pattern, Anchor):
            next_mc_index = line.pattern.anchor_value()

        if line.machinecode:
            for word in line.machinecode:
                word.index = next_mc_index
                next_mc_index = next_mc_index + 1


def check_for_colliding_indecies(assembly_lines):
    """
    Check that all machinecode words have a unique index.

    Args:
        assembly_lines (list(:class:`~.AssemblyLine`)): List of
            processed lines of assembly.
    Raises:
        AssemblyError: If a machine code word collides with another.
    """

    indecies_to_lines = {}
    for assembly_line in assembly_lines:
        if assembly_line.has_machinecode():
            for machinecode_word in assembly_line.machinecode:
                index = machinecode_word.index
                if index in indecies_to_lines:
                    details = (
                        "The machinecode word at index {index} "
                        "from assembly line {curr_line} ({curr_line_content}) collides "
                        "with the machinecode word already defined "
                        "there from assembly line {prior_line} ({prior_line_content})".format(
                            index=index,
                            curr_line=assembly_line.line_no,
                            curr_line_content=assembly_line.raw_line,
                            prior_line=indecies_to_lines[index].line_no,
                            prior_line_content=indecies_to_lines[index].raw_line
                        )
                    )
                    msg = ERROR_TEMPLATE.format(
                        line_no=assembly_line.line_no,
                        line=assembly_line.raw_line,
                        details=details,
                    )
                    raise AssemblyError(msg)
                else:
                    indecies_to_lines[index] = assembly_line
