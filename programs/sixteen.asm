// A comment

!five #5

@ #5
&label1
    NOOP
    ADD A

@ #50
&pointless
$var #1 #2

    AND [!five]
    NOOP
    ADD &label1
    ADD [&label2]
    NOOP
    AND A

&label2
@ #20
    AND A
    AND B
    AND C
    SET_ZERO ACC
    ADD $var
    ADD &label2
    ADD [&pointless]
    ADD &pointless
    AND A
    AND B
    AND C
    // AND ACC
    ADD A
    ADD B
    ADD C
    // ADD ACC
    SET_ZERO A
    // SET_ZERO #10