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

// Set p1 positions
SET_ZERO ACC
STORE ACC [$p1_row]
STORE ACC [$p1_col]

// Set p2 position
SET ACC #1
STORE ACC [$p2_row]
SET_ZERO ACC
STORE ACC [$p2_col]

// Set p3 position
SET ACC #2
STORE ACC [$p3_row]
SET_ZERO ACC
STORE ACC [$p3_col]

// Set the stack pointer
SET SP #500

SET ACC #1
STORE ACC [$frame_2_counter]

SET ACC #2
STORE ACC [$frame_3_counter]

$p1_row
$p1_col
$p2_row
$p2_col
$p3_row
$p3_col
&main_loop
    // Flip the draw buffer
    LOAD [!video_status] ACC
    XOR #0b_0000_0000_0010_0000
    STORE ACC [!video_status]

    CALL &update_frame_counters

    // Do things that need to be done every frame
    CALL &every_frame

    // Do things that need to be done every 2nd frame
    LOAD [$frame_2_counter] ACC
    JUMP_IF_NEQ_ZERO ACC &main_check_3_frame
    CALL &every_2_frame

    // Do things that need to be done every 3rd frame
&main_check_3_frame
    LOAD [$frame_3_counter] ACC
    JUMP_IF_NEQ_ZERO ACC &main_past_check_3_frame
    CALL &every_3_frame

&main_past_check_3_frame
    // Draw the result to the framebuffer ready to be shown next frame
    CALL &draw

    // Wait for the frame to end
    CALL &wait_for_frame_end

    JUMP &main_loop


&every_frame
    // Increment player 1 pos
    LOAD [$p1_col] ACC
    INCR ACC
    
    // Reset to zero if past edge
    LOAD [$screen_cols_minus_1] A
    JUMP_IF_ACC_LTE A &every_frame_end
    SET_ZERO ACC
    
&every_frame_end
    STORE ACC [$p1_col]
    RETURN


&every_2_frame
    // Increment player 2 pos
    LOAD [$p2_col] ACC
    INCR ACC
    
    // Reset to zero if past edge
    LOAD [$screen_cols_minus_1] A
    JUMP_IF_ACC_LTE A &every_2_frame_end
    SET_ZERO ACC
    
&every_2_frame_end
    STORE ACC [$p2_col]
    RETURN


&every_3_frame
    // Increment player 3 pos
    LOAD [$p3_col] ACC
    INCR ACC
    
    // Reset to zero if past edge
    LOAD [$screen_cols_minus_1] A
    JUMP_IF_ACC_LTE A &every_3_frame_end
    SET_ZERO ACC
    
&every_3_frame_end
    STORE ACC [$p3_col]
    RETURN


&draw
    // Draw black BG
    SET_ZERO B
    CALL &fill_screen

    // Draw p1
    LOAD [$p1_row] ACC
    STORE ACC [!cursor_row]
    LOAD [$p1_col] ACC
    STORE ACC [!cursor_col]
    SET ACC #0b11_00_00
    STORE ACC [!video_data]

    // Draw p2
    LOAD [$p2_row] ACC
    STORE ACC [!cursor_row]
    LOAD [$p2_col] ACC
    STORE ACC [!cursor_col]
    SET ACC #0b00_11_00
    STORE ACC [!video_data]

    // Draw p3
    LOAD [$p3_row] ACC
    STORE ACC [!cursor_row]
    LOAD [$p3_col] ACC
    STORE ACC [!cursor_col]
    SET ACC #0b00_00_11
    STORE ACC [!video_data]

    RETURN


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

$frame_2_counter
$frame_3_counter
&update_frame_counters
    SET A $frame_2_counter
    DECR [A]

    // If we didn't go below zero, move to next counter
    JUMP_IF_CARRYBORROW_FLAG &update_fc_3
    // Otherwise reset counter back to 1
    SET ACC #1
    STORE ACC [A]

&update_fc_3
    SET A $frame_3_counter
    DECR [A]

    // If we didn't go below zero, move to next counter
    JUMP_IF_CARRYBORROW_FLAG &update_fc3_end
    // Otherwise reset counter back to 3
    SET ACC #2
    STORE ACC [A]

&update_fc3_end
    RETURN




























