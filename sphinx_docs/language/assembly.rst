Assembly
========

Some example assembly::

    % This is a comment

        LOAD [15] ACC
        SET B 15

    @label1
        COPY ACC A
        COPY A B
        COPY B C



    % Another comment
    @label2
        SET SP 255
        JUMP @label1


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

Do @label2, 3 and 4 all mean the COPY SP C line? I guess so! Labels can be
accumulated until a real line is hit, then they get attached to that real line.

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

Tests!

- Assembly files with only @labels in
- What happens when you do LOAD [[#123]] A
- Assembly files with only comments
- assembly files with only empty lines