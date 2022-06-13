// A comment

!five #5

@ #5
&label
    NOOP
    ADD A

$var #1 #2

    AND [!five]
    NOOP
    ADD &label
    ADD [&label]
    NOOP
    AND A

@ #20
    AND A