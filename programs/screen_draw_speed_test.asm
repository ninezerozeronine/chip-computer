&init
    SET C #1
    SET A #1
    SET ACC #159
    STORE ACC [$max_c]
    STORE ACC [$cursor_c]
    SET ACC #119
    STORE ACC [$max_r]
    STORE ACC [$cursor_r]

&draw_loop
    // Store pixel in cursor
    STORE ACC [$video_data]

    // Decrement column
    LOAD [$cursor_c] ACC
    DECR ACC
    STORE ACC [$cursor_c]

    // Back to the start if we're not past the end of the row
    JUMP_IF_NOT_NEGATIVE_FLAG &draw_loop

    // Otherwise we've just drawn the last pixel of the row
    // Set column to max
    LOAD [$max_c] ACC
    STORE ACC [$cursor_c]

    // Decrement row
    LOAD [$cursor_r] ACC
    DECR ACC
    STORE ACC [$cursor_r]

    // Back to the start if we're not past the first row
    JUMP_IF_NOT_NEGATIVE_FLAG &draw_loop

    // Otherwise we've just drawn the last pixel on the screen
    LOAD [$max_r] ACC
    STORE ACC [$cursor_r]

    // Flip the indicator bit
    NOT C

    // Check controller
    LOAD [#0xFFFF] ACC

    // Set appropriate res if necessary
    JUMP_IF_ACC_EQ #0b0000_0000_0000_0001 &set_160x120
    JUMP_IF_ACC_EQ #0b0000_0000_0000_0010 &set_80x60
    JUMP_IF_ACC_EQ #0b0000_0000_0000_0100 &set_40x30
    JUMP_IF_ACC_EQ #0b0000_0000_0000_1000 &set_20x15

    // Back to start
    JUMP &draw_loop

&set_160x120
    SET A #1
    SET ACC #159
    STORE ACC [$max_c]
    SET ACC #119
    STORE ACC [$max_r]
    JUMP &draw_loop

&set_80x60
    SET A #2
    SET ACC #79
    STORE ACC [$max_c]
    SET ACC #59
    STORE ACC [$max_r]
    JUMP &draw_loop

&set_40x30
    SET A #4
    SET ACC #39
    STORE ACC [$max_c]
    SET ACC #29
    STORE ACC [$max_r]
    JUMP &draw_loop

&set_20x15
    SET A #8
    SET ACC #19
    STORE ACC [$max_c]
    SET ACC #14
    STORE ACC [$max_r]
    JUMP &draw_loop

$cursor_c
$cursor_r
$max_c
$max_r
$video_data
