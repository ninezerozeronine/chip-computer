from . import assembly_patterns
from . import assembly_tokens
from . import number_utils
from .exceptions import (
    AssemblyError,
    LineProcessingError,
    NoMatchingTokensError,
    MultipleMatchingTokensError,
    NoMatchingPatternsError,
    MultipleMatchingPatternsError,
)

ERROR_TEMPLATE = "Error processing line {line_no} ({line}): {details}"
"""
    The template for top level error reports during assembly.
"""

class AssemblyLine():
    """
    Representation of a line in the assembly file.
    """
    def __init__(self, raw_line=None, pattern=None, line_no=None):
        """
        Initialise the class

        Args:
            raw_line (str): The line of assembly code as it was in the
                assembly file.
            pattern (Pattern): The pattern this line corresponds to.
            line_no (int): The line of the assembly file this line came
                from.
        """
        self.raw_line = raw_line
        self.pattern = pattern
        self.line_no = line_no


def assemble(lines):
    assembly_lines = ingest_raw_assembly_lines(lines)
    process_assembly_lines(assembly_lines)
    return assembly_lines


def ingest_raw_assembly_lines(lines):
    """
    Take strings and convert to :class:`~sixteen_bit_computer.assembler.AssemblyLine`
    objects.

    All lines are processed in isolation at this point.
    :func:`process_assembly_lines` has a more global view of how lines
    interact with each other.

    Args:
        lines (list(str)): List of assembly lines to ingest
    Returns:
        list(AssemblyLine): List of processed assembly lines.
    Raises:
        LineProcessingError: If there was problem processing a line.
    """
    assembly_lines = []
    for line_no, raw_line in enumerate(lines, start=1):
        try:
            pattern = pattern_from_line(raw_line)
        except LineProcessingError as err:
            msg = ERROR_TEMPLATE.format(
                line_no=line_no,
                line=raw_line,
                details=err.args[0],
            )
            raise AssemblyError(msg)

        assembly_lines.append(
            AssemblyLine(
                raw_line=raw_line,
                pattern=pattern,
                line_no=line_no,
            )
        )

    return assembly_lines


def pattern_from_line(line):
    """
    Get the pattern corresponding to a raw line of assembly code.

    A raw line is something like: ``LOAD [$var] A // My comment.``

    Args:
        line (str): Raw line of assembly code.
    Returns:
        Pattern: Pattern that corresponds to the passed in line.
    """

    no_comments = remove_comments(line)
    tokens = get_tokens(no_comments)
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
        list(Token) or None: List of tokens on this line (could be
            empty).
    Raises:
        NoMatchingTokensError: When no matching tokens were found for
            something on the line.
        MultipleMatchingTokensError: When multiple tokens matched
            something on the line.
    """

    if not line:
        return []

    words = get_words_from_line(line)
    final_tokens = []
    for word in words:
        matched_tokens = []
        for token_class in assembly_tokens.get_all_tokens():
            token = token_class.from_string(word)
            if token is not None:
                matched_tokens.append(token)

        num_matches = len(matched_tokens)

        if num_matches == 0:
            raise NoMatchingTokensError(
                F"No tokens matched the following: \"{word}\""
            )

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
        list(str): The words in the line.
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
        tokens (list(Token)): The tokens to match to a
            pattern. Can be an empty list - returns a
            :class:`~sixteen_bit_computer.assembly_patterns.NullPattern`.
    Returns:
        Pattern or None: The pattern that matches the tokens.
    Raises:
        NoMatchingPatternsError: When a matching token was not found.
        MultipleMatchingPatternsError: When multiple tokens matched.
    """
    matched_patterns = []

    for pattern_class in assembly_patterns.get_all_patterns():
        pattern = pattern_class.from_tokens(tokens)
        if pattern is not None:
            matched_patterns.append(pattern)

    num_matches = len(matched_patterns)

    if num_matches == 0:
        raise NoMatchingPatternsError("No patterns matched")

    if num_matches > 1:
        raise MultipleMatchingPatternsError("Multiple patterns matched")

    return matched_patterns[0]


def process_assembly_lines(assembly_lines):
    """
    
    """

    check_numbers_in_range(assembly_lines)
    check_anchors_are_in_range(assembly_lines)
    check_for_duplicate_alias_names(assembly_lines)
    check_for_duplicate_label_names(assembly_lines)
    check_for_multiple_label_assignment(assembly_lines)
    check_for_duplicate_variable_names(assembly_lines)

    assign_machinecode_indecies(assembly_lines)
    check_for_colliding_indecies(assembly_lines)
    check_for_out_of_range_indecies(assembly_lines)

    resolve_numbers(assembly_lines)

    alias_map = build_alias_map(assembly_lines)
    resolve_aliases(assembly_lines, alias_map)

    label_map = build_label_map(assembly_lines)
    resolve_labels(assembly_lines, label_map)

    variable_map = build_variable_map(assembly_lines)
    resolve_variables(assembly_lines, variable_map)


def check_numbers_in_range(assembly_lines):
    """
    Check that any number tokens have a value that is within the range
    the computer can handle.

    It's a sixteen bit computer so numbers from -32767 to 65535 are
    supported.
    """

    for line in assembly_lines:
        for token in line.pattern.tokens:
            # Extract the token in the memref if it's a memref
            if (isinstance(token, assembly_tokens.MEMREF)):
                token = token.value

            if (isinstance(token, assembly_tokens.NUMBER)
                    and not number_utils.number_is_within_bit_limit(
                        token.value, bit_width=16)):
                details = (
                    "Number token: \"{token}\" with a value of {value} "
                    "is outside the supported range of -32767 to 65535 "
                    "(inclusive).".format(
                        token=token.raw, value=token.value
                    )
                )
                msg = ERROR_TEMPLATE.format(
                    line_no=line.line_no,
                    line=line.raw_line,
                    details=details,
                )
                raise AssemblyError(msg)


def check_anchors_are_in_range(assembly_lines):
    """
    Check that the values used for any anchors are in range.

    The value has to be between 0 and 65535 to fit into memory.

    Args:
        assembly_lines (List(AssemblyLine)): List of
            processed lines of assembly.
    Raises:
        AssemblyError: If an achor sets a location outside the specified
            range.
    """
    for line in assembly_lines:
        if isinstance(line.pattern, assembly_patterns.Anchor):
            if not 0 <= line.pattern.location < 65536:
                details = (
                    "The anchor specifies a value of {value} which is "
                    "outside the supported range of 0 to 65535 "
                    "(inclusive).".format(value=line.pattern.location)
                )
                msg = ERROR_TEMPLATE.format(
                    line_no=line.line_no,
                    line=line.raw_line,
                    details=details,
                )
                raise AssemblyError(msg)


def check_for_duplicate_alias_names(assembly_lines):
    """
    Check if an alias has been defined multiple times.

    E.g. This is allowed:

    .. code-block:: none

        !MY_ALIAS #123
        !OTHER_ALIAS #456

    But this is not::

    .. code-block:: none

        !MY_ALIAS #123
        !MY_ALIAS #456

    Args:
        assembly_lines (List(AssemblyLine)): List of
            processed lines of assembly.
    Raises:
        AssemblyError: If the same alias has been defined more than
            once.
    """

    aliases = set()
    alias_lines = {}
    for assembly_line in assembly_lines:
        if isinstance(assembly_line.pattern, assembly_patterns.AliasDef):
            alias = assembly_line.pattern.name
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


def check_for_duplicate_label_names(assembly_lines):
    """
    Check if a label name has been used more than once.

    E.g. This is allowed:

    .. code-block:: none

        &label_1
            NOOP
        &label_2
            ADD #3

    But this is not:

    .. code-block:: none

        &label_0
            NOOP
        &label_1
            ADD A
        &label_0
            NOT ACC

    As ``&label_0`` is already assigned to the index holding the
    ``NOOP`` instruction, so cannot also be assigned the index of the
    ``NOT ACC`` instruction.

    Args:
        assembly_lines (List[AssemblyLine]): List of
            processed lines of assembly.
    Raises:
        AssemblyError: If the same label name has been used more than
            once.
    """

    labels = set()
    label_lines = {}
    for assembly_line in assembly_lines:
        if isinstance(assembly_line.pattern, assembly_patterns.Label):
            label = assembly_line.pattern.name
            if label in labels:
                details = (
                    "The label: \"{label}\" has already been defined on "
                    "line {prev_line}.".format(
                        label=label,
                        prev_line=label_lines[label],
                    )
                )
                msg = ERROR_TEMPLATE.format(
                    line_no=assembly_line.line_no,
                    line=assembly_line.raw_line,
                    details=details,
                )
                raise AssemblyError(msg)
            else:
                labels.add(label)
                label_lines[label] = assembly_line.line_no


def check_for_multiple_label_assignment(assembly_lines):
    """
    Check if a single line will be assigned more than one label.

    E.g. This is allowed:

    .. code-block:: none

        &label_1
            NOOP
        &label_2
            AND A

    But this is not:

    .. code-block:: none

        &label_0
        &label_1
            ADD A
        &label_2
            NOT ACC

    Args:
        assembly_lines (List[AssemblyLine]): List of
            processed lines of assembly.
    Raises:
        AssemblyError: If a single line been assigned more than one
            label.
    """
    label_queued = False
    last_label = "INVALID"
    last_line = -1
    for line in assembly_lines:
        if isinstance(line.pattern, assembly_patterns.Label):
            if label_queued:
                details = (
                    "There is already a label ({label}) from line "
                    "{last_line} queued for assignment to the next "
                    "machinecode word.".format(
                        label=last_label,
                        last_line=last_line
                    )
                )
                msg = ERROR_TEMPLATE.format(
                    line_no=line.line_no,
                    line=line.raw_line,
                    details=details,
                )
                raise AssemblyError(msg)
            else:
                label_queued = True
                last_label = line.pattern.name
                last_line = line.line_no
                continue

        if line.pattern.machinecode:
            label_queued = False


def check_for_duplicate_variable_names(assembly_lines):
    """
    Check if a variable name has been used more than once.

    E.g. This is allowed:

    .. code-block:: none

        $variable1
        $variable2 #23 #300

    But this is not:

    .. code-block:: none

        $variable_0
        $variable_1
        $variable_0

    Because is creates ambiguity over which memory address
    ``$variable_0`` should be.

    Args:
        assembly_lines (List[AssemblyLine]): List of
            processed lines of assembly.
    Raises:
        AssemblyError: If the same variable name has been used more than
            once.
    """

    variables = set()
    variable_lines = {}
    for assembly_line in assembly_lines:
        line_is_variable = isinstance(
            assembly_line.pattern,
            (
                assembly_patterns.Variable,
                assembly_patterns.VariableDef,
            )
        )
        if line_is_variable:
            variable = assembly_line.pattern.name
            if variable in variables:
                details = (
                    "The variable: \"{variable}\" has already been defined on "
                    "line {prev_line}.".format(
                        variable=variable,
                        prev_line=variable_lines[variable],
                    )
                )
                msg = ERROR_TEMPLATE.format(
                    line_no=assembly_line.line_no,
                    line=assembly_line.raw_line,
                    details=details,
                )
                raise AssemblyError(msg)
            else:
                variables.add(variable)
                variable_lines[variable] = assembly_line.line_no


def assign_machinecode_indecies(assembly_lines):
    """
    Assign indecies to all the machinecode words.

    Instructions can resolve to more than one word, and sections of
    assembly can be placed with a anchor so the machine code index has
    no correlation to the assembly line index.

    Edits the assembly lines in place.

    Args:
        assembly_lines (List(AssemblyLine)): List of
            processed lines of assembly.
    """
    next_mc_index = 0
    for line in assembly_lines:
        # Place the machinecode words that follow at the position
        # specified by the anchor.
        if isinstance(line.pattern, assembly_patterns.Anchor):
            next_mc_index = line.pattern.location

        # Reserve a word in memory for the variable (but don't generate
        # machinecode for it)
        if isinstance(line.pattern, assembly_patterns.Variable):
            next_mc_index += 1

        # Increment index for each machinecode word
        for word in line.pattern.machinecode:
            word.index = next_mc_index
            next_mc_index += 1


def check_for_colliding_indecies(assembly_lines):
    """
    Check that all machinecode words have a unique index.

    Args:
        assembly_lines (List[AssemblyLine]): List of
            processed lines of assembly.
    Raises:
        AssemblyError: If a machine code word collides with another.
    """

    indecies_to_lines = {}
    for line in assembly_lines:
        for word in line.pattern.machinecode:
            index = word.index
            if index in indecies_to_lines:
                details = (
                    "The machinecode word at index {index} collides "
                    "with the machinecode word already defined "
                    "there from assembly line {prior_line} ({prior_line_content})".format(
                        index=index,
                        prior_line=indecies_to_lines[index].line_no,
                        prior_line_content=indecies_to_lines[index].raw_line
                    )
                )
                msg = ERROR_TEMPLATE.format(
                    line_no=line.line_no,
                    line=line.raw_line,
                    details=details,
                )
                raise AssemblyError(msg)
            else:
                indecies_to_lines[index] = line


def check_for_out_of_range_indecies(assembly_lines):
    """
    Check that all machinecode words have a valid index.

    Args:
        assembly_lines (List[AssemblyLine]): List of
            processed lines of assembly.
    Raises:
        AssemblyError: If a machine code word collides with another.
    """
    for line in assembly_lines:
        for word in line.pattern.machinecode:
            if (word.index < 0) or (word.index > ((2**16) - 1)):
                details = (
                    "The machinecode word(s) would be placed at the "
                    " index {index} which is not within the range "
                    "0-65535 inclusive.".format(index=word.index)
                )
                msg = ERROR_TEMPLATE.format(
                    line_no=line.line_no,
                    line=line.raw_line,
                    details=details,
                )
                raise AssemblyError(msg)


def resolve_numbers(assembly_lines):
    """
    Resolve any number tokens used in machine code.

    Modifies the assmebly lines in place.

    Args:
        assembly_lines (List[AssemblyLine]): List of
            processed lines of assembly.
    """
    for line in assembly_lines:
        for word in line.pattern.machinecode:
            token = word.const_token
            if isinstance(token, assembly_tokens.NUMBER):
                word.value = token.value


def build_alias_map(assembly_lines):
    """
    Build a mapping of aliases to thier values.

    Args:
        assembly_lines (List[AssemblyLine]): List of
            processed lines of assembly.
    Returns:
        Dict[str, int]: Dictionary of alias
        name keys to thier values.
    """
    alias_map = {}
    for line in assembly_lines:
        if isinstance(line.pattern, assembly_patterns.AliasDef):
            alias_map[line.pattern.name] = line.pattern.value
    return alias_map


def resolve_aliases(assembly_lines, alias_map):
    """
    Resolve any references to aliases in machinecode words.

    Edits the assembly lines in place.

    Args:
        assembly_lines (List[AssemblyLine]): List of
            processed lines of assembly.
    Raises:
        AssemblyError: If an alias has been referenced but not defined.
    """
    for line in assembly_lines:
        for word in line.pattern.machinecode:
            token = word.const_token
            if isinstance(token, assembly_tokens.ALIAS):
                try:
                    word.value = alias_map[token.value]
                except KeyError:
                    details = (
                        "The alias: {alias} has not been defined.".format(
                            alias=token.value
                        )
                    )
                    msg = ERROR_TEMPLATE.format(
                        line_no=line.line_no,
                        line=line.raw_line,
                        details=details,
                    )
                    raise AssemblyError(msg)


def build_label_map(assembly_lines):
    """
    Build a mapping of labels to thier machinecode indecies.

    Args:
        assembly_lines (List[AssemblyLine]): List of
            processed lines of assembly.
    Returns:
        dict of str to int: Dictionary of string label name keys to thier 
        int machinecode indecies.
    """
    labels_needing_values = []
    label_map = {}
    for line in assembly_lines:
        if isinstance(line.pattern, assembly_patterns.Label):
            labels_needing_values.append(line.pattern.name)
            continue

        if line.pattern.machinecode:
            for label in labels_needing_values:
                label_map[label] = line.pattern.machinecode[0].index
            labels_needing_values = []
    return label_map


def resolve_labels(assembly_lines, label_map):
    """
    Resolve any references to labels in machinecode words.

    Edits the assembly lines in place.

    Args:
        assembly_lines (List[AssemblyLine]): List of
            processed lines of assembly.
    Raises:
        AssemblyError: If a label has been referenced but not defined.
    """
    for line in assembly_lines:
        for word in line.pattern.machinecode:
            token = word.const_token
            if isinstance(token, assembly_tokens.LABEL):
                try:
                    word.value = label_map[token.value]
                except KeyError:
                    details = (
                        "The label: {label} has not been defined.".format(
                            label=token.value
                        )
                    )
                    msg = ERROR_TEMPLATE.format(
                        line_no=line.line_no,
                        line=line.raw_line,
                        details=details,
                    )
                    raise AssemblyError(msg)


def build_variable_map(assembly_lines):
    """
    Build a mapping of variables to thier values.

    Args:
        assembly_lines (List[AssemblyLine]): List of
            processed lines of assembly.
    Returns:
        dict of str to int: Dictionary of variable name keys to thier
        values.
    """
    variable_map = {}

    # Determine positions of Variables.
    # Not a huge fan of how this duplicates what's going on in
    # assign_machinecode_indecies
    next_mc_index = 0
    for line in assembly_lines:
        # Place the machinecode words that follow at the position
        # specified by the anchor.
        if isinstance(line.pattern, assembly_patterns.Anchor):
            next_mc_index = line.pattern.location

        # Reserve a word in memory for the variable (but don't generate
        # machinecode for it)
        if isinstance(line.pattern, assembly_patterns.Variable):
            variable_map[line.pattern.name] = next_mc_index
            next_mc_index += 1

        # Increment index for each machinecode word
        next_mc_index += len(line.pattern.machinecode)

    # Determine posisions of Variable Defs
    for line in assembly_lines:
        if isinstance(line.pattern, assembly_patterns.VariableDef):
            variable_map[line.pattern.name] = line.pattern.machinecode[0].index

    return variable_map


def resolve_variables(assembly_lines, variable_map):
    """
    Resolve any references to variables in machinecode words.

    Edits the assembly lines in place.

    Args:
        assembly_lines (List[AssemblyLine]): List of
            processed lines of assembly.
    Raises:
        AssemblyError: If a variable has been referenced but not defined.
    """
    for line in assembly_lines:
        for word in line.pattern.machinecode:
            token = word.const_token
            if isinstance(token, assembly_tokens.VARIABLE):
                try:
                    word.value = variable_map[token.value]
                except KeyError:
                    details = (
                        "The variable: {variable} has not been defined.".format(
                            variable=token.value
                        )
                    )
                    msg = ERROR_TEMPLATE.format(
                        line_no=line.line_no,
                        line=line.raw_line,
                        details=details,
                    )
                    raise AssemblyError(msg)
