!video_status #65531
!cursor_row #65532
!cursor_col #65533
!video_data #65534

// Set video res to 80x60
SET ACC #0b0000_0000_0000_1000
STORE ACC [!video_status]

// Set Screen size variables
SET ACC #79
STORE ACC [$screen_cols_minus_1]
SET ACC #59
STORE ACC [$screen_rows_minus_1]

// Set player pos
SET_ZERO ACC
STORE ACC [$p1_col]

// Set the stack pointer
SET SP #256

$p1_col
&main_loop
    // Flip the draw buffer
    LOAD [!video_status] ACC
    XOR #0b_0000_0000_0010_0000
    STORE ACC [!video_status]

    // Draw black BG
    SET_ZERO B
    CALL &fill_screen

    // Increment player pos
    LOAD [$p1_col] ACC
    INCR ACC
    
    // Reset to zero if past edge
    LOAD [$screen_cols_minus_1] A
    JUMP_IF_ACC_LTE A &draw_player
    SET_ZERO ACC

&draw_player
    // Draw the player
    STORE ACC [$p1_col]
    SET_ZERO A
    STORE A [!cursor_row]
    STORE ACC [!cursor_col]
    SET ACC #0b11_00_00
    STORE ACC [!video_data]

    // Wait for the frame to end
    CALL &wait_for_frame_end

    // Back to the top
    JUMP &main_loop


$last_vblank
&wait_for_frame_end
    // Set A to point at the video status
    SET A !video_status

    // Store current vblank
    LOAD [A] ACC
    AND #0b0000_0000_1000_0000
    STORE ACC [$last_vblank]
    
&wait_for_frame_end_inner
    // Get current vblank
    LOAD [A] ACC
    AND #0b0000_0000_1000_0000

    // Back to top of loop if lask vblank was not low
    LOAD [$last_vblank] B
    JUMP_IF_NEQ_ZERO B &wait_for_frame_end_next_iter
    
    // Back to top of loop if current vblank is not high
    JUMP_IF_EQ_ZERO ACC &wait_for_frame_end_next_iter

    // As last vblank was low and current is high, we
    // just transitioned from low to high - return
    RETURN

&wait_for_frame_end_next_iter
    // Put current in last
    STORE ACC [$last_vblank]

    // Back to top
    JUMP &wait_for_frame_end_inner


$screen_cols_minus_1
$screen_rows_minus_1
&fill_screen
    // Fill the screen with the colour in B

    // Set cursor column to max col index
    LOAD [$screen_cols_minus_1] ACC
    STORE ACC [!cursor_col]
    
    // Set cursor row to max row index
    LOAD [$screen_rows_minus_1] ACC
    STORE ACC [!cursor_row]

    SET C !video_data
    SET A !cursor_col


&draw_next_pixel_in_row

    // Store the colour (B) into video data (pointed to by C)
    STORE B [C]

    // Decrement the column (pointed to by A)
    DECR [A]

    // If we didn't go below zero
        // Draw the next pixel
        JUMP_IF_CARRYBORROW_FLAG &draw_next_pixel_in_row

    // Else
        // Run through to go to the next row

&next_row
    // Set column to max col index
    LOAD [$screen_cols_minus_1] ACC
    STORE ACC [!cursor_col]

    // Decrement the row
    LOAD [!cursor_row] ACC
    DECR ACC
    STORE ACC [!cursor_row]
    
    // If we didn't go below zero
        // Draw the next pixel
        JUMP_IF_CARRYBORROW_FLAG &draw_next_pixel_in_row
    
    // Else
        // We're done!
        RETURN