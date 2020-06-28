    SET A #1
@loop
    ROT_LEFT A
    // STORE A [#255]
    COPY A C
    JUMP @loop