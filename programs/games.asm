!VIDEO_STATUS #0b0000_0000_0000_0000
!VIDEO_DATA #0b0000_0000_0000_0000
!VIDEO_CURSOR_ROW #0b0000_0000_0000_0000
!VIDEO_CURSOR_COL #0b0000_0000_0000_0000

!CONTROLLER_1 #0b0000_0000_0000_0000

    CALL &init
    // CALL &main_loop

$NUM_ROWS
$NUM_COLS

&init
    CALL &set_res_to_80x60

////////////////////////////////////////////////////////////
//
// Set the video res to 80x60
//
////////////////////////////////////////////////////////////
&set_res_to_80x60
    SET ACC #80
    STORE ACC [$NUM_COLS]
    SET ACC #60
    STORE ACC [$NUM_ROWS]
    SET ACC #0b0000_0000_0000_1000
    STORE ACC [!VIDEO_STATUS]
    RETURN


////////////////////////////////////////////////////////////
//
// Calls itself in a loop until the current frame ends, when
// it does - it returns. The frame ends when vblank goes
// from low to high.
//
////////////////////////////////////////////////////////////
&wait_for_frame_end
    // Store current vblank in A
    LOAD [!VIDEO_STATUS] ACC
    AND #0b0000_0000_1000_0000
    COPY ACC A
    
&wait_for_frame_end_inner
    // Get current vblank
    LOAD [!VIDEO_STATUS] ACC
    AND #0b0000_0000_1000_0000

    // Back to top of loop if lask vblank was not low
    JUMP_IF_NEQ_ZERO A &wait_for_frame_end_next_iter
    
    // Back to top of loop if current vblank is not high
    JUMP_IF_EQ_ZERO ACC &wait_for_frame_end_next_iter

    // As last vblank was low and current is high, we
    // just transitioned from low to high - return
    RETURN

&wait_for_frame_end_next_iter
    // Put current vblank in last
    COPY ACC A

    // Back to top
    JUMP &wait_for_frame_end_inner


////////////////////////////////////////////////////////////
//
// Fill the screen with the colour in C
//
////////////////////////////////////////////////////////////
&fill_screen
    // Set cursor column to max column index
    LOAD [$NUM_COLS] ACC
    DECR ACC
    STORE ACC [!VIDEO_CURSOR_COL]
    
    // Set cursor row to max row index
    LOAD [$NUM_ROWS] ACC
    DECR ACC
    STORE ACC [!VIDEO_CURSOR_ROW]

    SET A !VIDEO_DATA
    SET B !VIDEO_CURSOR_COL

    // Put the colour in ACC
    COPY C ACC

&fill_screen_draw_next_pixel_in_row

    // Store the colour (ACC) into video data (pointed to by A)
    // then decrement the cursor column (pointed to by B)
    STORE_DECR ACC [A] [B]

    // If we didn't go below zero draw the next pixel
    JUMP_IF_NOT_BORROW &fill_screen_draw_next_pixel_in_row

    // Otherwise run through to go to the next row

&fill_screen_move_to_next_row
    // Decrement the row
    DECR [!VIDEO_CURSOR_ROW]

    // If the row went below zero we're done
    JUMP_IF_BORROW &fill_screen_done

    // Otherwise setup the next row
    // Set cursor column to max column index
    LOAD [$NUM_COLS] ACC
    DECR ACC
    STORE ACC [!VIDEO_CURSOR_COL]
    
    // Put the colour in ACC
    COPY C ACC
    
    JUMP &fill_screen_draw_next_pixel_in_row      
    
&fill_screen_done
    RETURN






