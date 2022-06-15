// A comment

!five #5

@ #5
&label1
    NOOP
    ADD A

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