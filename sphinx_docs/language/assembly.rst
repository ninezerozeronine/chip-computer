Assembly
========

Some example assembly::

    % This is a comment

        LOAD [#15] ACC
        SET B 15

    @label1
        COPY ACC A
        COPY A B
        COPY B C



    % Another comment
    @label2
        SET SP #255
        JUMP @label1


Handling Constants
-------------------

If the assembler finds an @label, $variable or #number within an instruction
then when looking for a match in all the instructions it informs it that an
constant value has been passed, and what the value is. e.g.::

    LOAD [$variable] A

    called as:
    for instruction in instructions:
        instruction.parse_line(line, constants=["$variable"])

If there's no constant it's just a normal parse::

    LOAD [ACC] A

    called as:
    for instruction in instructions:
        instruction.parse_line(line)

Good Constants
^^^^^^^^^^^^^^

$$X_POS = [#14, #13]

$$BALL_Y_VALUES[10]

LOAD [$X_POS] A
SET A #14
STORE A [$y_pos]

LOAD [$xpos] A

JUMP @LOOP_START
JUMP $STRANGE_USE

Bad Constants
^^^^^^^^^^^^^

$$$BLAH

LOAD [#@$WORLD] B
JUMP




Validating numbers
------------------

#numbers in the assembly are first attempted to be cast to ints. Thay can be
specified in the same way integers are specified in python, e.g.:

- 123
- 0xff
- 0b100101
- 0o77
  
If a number is greater than 255 or less than 128 it's an assembly error.

Assembly errors
---------------

The user needs to know which line of the assembly file an error occurred on.

Should these be execptions?

Assembly steps
--------------

Can raise assembly errors and parsing errors?

Go through every line and extract the following info::

    {
        "line_no": 34,
        "raw_line": "  COPY   ACC   A",
        "cleaned_line": "COPY ACC A",
        "is_label": True
        "label": "@label1",
        "assigned_labels": [],
        
        "variables": [],
        "numbers": [],
        "constants": [],
    }         

Get machine code for the line from the instruction, add it to the dict. Parser
is passed list of constants. Catch Parsing error and re raise as assembly error.

Check numbers are valid - Raise assembly error if there's a bad number

Check for references to labels that haven't been declared. Raise assembly error
if something goes wrong.

Warn about unused labels

Aggregate labels onto real instructions

Warn about multiple labels on single instruction


Exceptions
----------

Could raise exceptions to handle assembly errors?

These get raised by the language parsers:

- InstructionParsingError

  - ConstantsError
  - ArgumentsError

These get raised during assembly:

- AssemblyError

  - InstructionBytesError
  - UndeclaredLabelError
  - GlobalVariablesError
  - IncorrectNumberError
  - IncorrectLabelNameError
  - IncorrectVariableNameError
  - ParsingError
  - UnmatchedInstructionError














.. code-block:: python
    try:
        machine_code = assemble(filepath)
    except AssemblyError:
        print AssemblyError

    def assemble(file):
        lines = [line for line in file]


        assembly_lines = []
        for line_no, line in enumerate(lines):
            line_info = {}
            line_info["line_number"] = line_no
            line_info["raw_line"] = line

            


        aggre
        check_undelcared_labels(assembly_lines)
        check_num_global_variables(assembly_lines)

        for assembly_line in assembly_lines:
            machine_code = machine_code_from_line(assembly_line["clean"])
            assembly_line["machine_code"].extend(machine_code)

        check_num_instruction_bytes(assembly_lines)


    def preprocess_line(line):
            cleaned_line = clean_line(line)
            line_info["cleaned_line"] = cleaned_line
            line_info["defined_label"] = get_defined_label(cleaned_line)


    def machine_code_from_line(line):
        if not line:
            return []
        machine_code = None
        for instruction in instructions:
            try:
                machine_code = instruction.parse_line(line)
            except InstructionParsingError as e:
                raise ParsingError(e)
        if machine_code is None:
            raise UnmatchedInstructionError()
        return machine_code

    def assembly_lines_to_machine_code(assembly_lines):
        variables = index_variables(assembly_lines)
        labels = index_labels(assembly_lines)













.. code-block:: python
    assembly_lines = []
    labels = []
    for line in file:
        cleaned = clean_line(line)

        label = get_label_def(cleaned)
        used_label = get_used_label()
        assembly_lines.append({
            "input_line_no": 34,
            "input_line": "  COPY   ACC   A",
            "cleaned_input_line": "COPY ACC A",
            "labels": None,
            "label_ref"
            "number"
            "variable"
        })


    def 




Have a layer of indirection between the assembly and the instructions.
All the instructions need to know is that they've been passed an
immediate value. It's up to the assembler to eventually resolve that immediate
value into:

- An actual number (43)
- A reference to a label (e.g for a jump instruction)

It's the assemblers job to resolve references to @labels (and eventually
$variables). The instructions will need to pass back some kind of placeholder.

Does the assembler just need to say: "You were passed a constant" to the
instruction? And the instruction will pass say: "Here's where to insert that
constant in the machine code"? It needs to be able to pass back some kind of
identifier so that an @label or $variable can later be resolved once it's buried
in the machine code.

What happens if there's some assembly like this::

        %My comment

    @label1
        COPY ACC A
        COPY A B
        COPY B C

    @label2
    @label3
    @label4
        COPY SP C
        COPY A B
        COPY B C

Do @label2, 3 and 4 all mean the COPY SP C line? No, this is invalid. the
assembly will fail

Here's some example data structures::

    assembly_line = {
        "input_line_no": 34,
        "input_line": "  COPY   ACC   A",
        "cleaned_input_line": "COPY ACC A",
        "labels": None,
    }

    machine_code_line {
        "data": "00101010",
    }

    machine_code_line {
        "data": "@label1",
    }

    machine_code_line {
        "data": "11010110",
        "label": "@label2"
    }

I quite like the idea of the machine_code_line structure. If the data is an
@label or $variable then the assembler will know to replace it.

Instructions can keep things simple and return a list of program bytes,
including anything immediate. eg::

    [
        "00101010",
        "IMM",
    ]

Then it's up to the assembler to replace the immediate values with the @label or
$variable in the original assembly line.

As some point the assembler will need to resolve the labels to actual lines in
the machine code.

The assembler needs to be able to cope with:

- LOAD [$variable] A
- LOAD [#123] A
- LOAD [@label] A <- weird, but whatever
- LOAD [ACC] B
- STORE A [$variable]
- STORE A [@label] <- weird, but whatever
- STORE A [#123]
- SET A #123
- JUMP @label
- JUMP B
- JUMP $variable  <- weird, but whatever
- JUMP_IF_FLAG ZERO #123
- JUMP_IF_FLAG ZERO @label
  
Perhaps $variables, @labels and #numbers get converted to IMM by the assembler?
The brackets can just be in the assembly side as a reminder when programming?

Instructions only need to be able to deal with ACC, A, B, C, SP, PC, IMM?

Given ``LOAD [$variable] A`` the assembler should only replace $variable to
arrive at: ``LOAD [IMM] A``.

A user shouldn't be able to write things like:

- ``LOAD [IMM] A``
- ``LOAD [SP+/-] A``
- ``LOAD [SP+/-] IMM``
- ``JUMP SP+/-``
  
The assembler won't end up being able to replace that with a real value later.
It would also trick the instruction matcher as the assembler is meant to pass
IMM to designate an immediate value.

An instruction should be responsible for determining if the line is valid.

Should the assembler inform the instruction if it's being passed a
placeholder/immediate value?

 Could do:

- A list of allowed tokens in assembly files
- A special function that the assembler calls if it's passing through a
  placeholder

We need to be able to point the user back at at line in the assembly file to:

- Warn if a line has multiple labels
- Warn if a label is unused
- Error if you try to jump to an undefined label
  
Does this mean resole @labels while parsing the raw lines?

Constants start with a # but could be int, binary or hex. #i #b #h and it
defaults to int? Use python notation and then ``int(value_string, 0)`` e.g.

- #123
- #0x4f
- #0o77
- #0b1001010

Tests!

- Assembly files with only @labels in
- What happens when you do LOAD [[#123]] A
- Assembly files with only comments
- assembly files with only empty lines