                  // #0b1111_1111_1111_0000
                  // #0b1111_1111_1111_0001
                  // #0b1111_1111_1111_0010
                  // #0b1111_1111_1111_0011
                  // #0b1111_1111_1111_0100
                  // #0b1111_1111_1111_0101
                  // #0b1111_1111_1111_0110
                  // #0b1111_1111_1111_0111
                  // #0b1111_1111_1111_1000
                  // #0b1111_1111_1111_1001
!STATUS_WORD         #0b1111_1111_1111_1010
!VIDEO_STATUS        #0b1111_1111_1111_1011
!VIDEO_CURSOR_ROW    #0b1111_1111_1111_1100
!VIDEO_CURSOR_COL    #0b1111_1111_1111_1101
!VIDEO_DATA          #0b1111_1111_1111_1110
                  // #0b1111_1111_1111_1111


!VIDEO_RES_20x15_OR      #0b0000_0000_0001_1000

!VIDEO_RES_40x30_AND     #0b1111_1111_1111_0111
!VIDEO_RES_40x30_OR      #0b0000_0000_0001_0000

!VIDEO_RES_80x60_AND     #0b1111_1111_1110_1111
!VIDEO_RES_80x60_OR      #0b0000_0000_0000_1000

!VIDEO_RES_160x120_AND   #0b1111_1111_1110_0111

!VID_COL_WHITE #0b0000_0000_0011_1111

    CALL &init
    CALL &main_loop

$NUM_ROWS
$NUM_COLS


////////////////////////////////////////////////////////////
//
// Initialise the program
//
////////////////////////////////////////////////////////////
&init
    CALL &set_res_to_20x15
    // CALL &check_and_set_screen_res
    // CALL &initialise_dot
    CALL &init_playing_field
    CALL &wait_for_frame_end
    RETURN

////////////////////////////////////////////////////////////
//
// Set the video resolutions
//
////////////////////////////////////////////////////////////
&set_res_to_20x15
    SET [$NUM_COLS] #20
    SET [$NUM_ROWS] #15
    LOAD [!VIDEO_STATUS] ACC
    OR !VIDEO_RES_20x15_OR
    STORE ACC [!VIDEO_STATUS]
    RETURN

&set_res_to_40x30
    SET [$NUM_COLS] #40
    SET [$NUM_ROWS] #30
    LOAD [!VIDEO_STATUS] ACC
    AND !VIDEO_RES_40x30_AND
    OR !VIDEO_RES_40x30_OR
    STORE ACC [!VIDEO_STATUS]
    RETURN

&set_res_to_80x60
    SET [$NUM_COLS] #80
    SET [$NUM_ROWS] #60
    LOAD [!VIDEO_STATUS] ACC
    AND !VIDEO_RES_80x60_AND
    OR !VIDEO_RES_80x60_OR
    STORE ACC [!VIDEO_STATUS]
    RETURN

&set_res_to_160x120
    SET [$NUM_COLS] #160
    SET [$NUM_ROWS] #120
    LOAD [!VIDEO_STATUS] ACC
    AND !VIDEO_RES_160x120_AND
    STORE ACC [!VIDEO_STATUS]
    RETURN

////////////////////////////////////////////////////////////
//
// Main execution loop
//
////////////////////////////////////////////////////////////
&main_loop

    // SET [!STATUS_WORD] #0b1000_0000_0000_0000
    // CALL &check_and_set_screen_res
    // CALL &update_dot
    SET C #0
    CALL &fill_screen
    CALL &draw_playing_field
    // CALL &draw_dot
    // SET [!STATUS_WORD] #0b0000_0000_0000_0000
    CALL &wait_for_frame_end
    CALL &flip_draw_buffer
    JUMP &main_loop


////////////////////////////////////////////////////////////
//
// Check and set screen res
// 
// Check the status word to see what the screen res should
// be and sets it
//
// xx.._...._...._....
// 
// Rotate left 5 times gives
//
// ...._...._...x_x...
// 
////////////////////////////////////////////////////////////
&check_and_set_screen_res
    LOAD [!STATUS_WORD] ACC
    AND #0b1100_0000_0000_0000
    ROT_LEFT ACC
    ROT_LEFT ACC
    ROT_LEFT ACC
    ROT_LEFT ACC
    ROT_LEFT ACC
    COPY ACC B
    LOAD [!VIDEO_STATUS] ACC
    AND #0b0000_0000_0001_1000
    COPY ACC A
    COPY B ACC

    // If the res is the same, no change needed
    JUMP_IF_ACC_EQ A &check_and_set_screen_res_done

    // Overwise, update
    CALL &initialise_dot
    JUMP_IF_ACC_EQ #0b0000_0000_0001_1000 &check_and_set_screen_res_20x15
    JUMP_IF_ACC_EQ #0b0000_0000_0001_0000 &check_and_set_screen_res_40x30
    JUMP_IF_ACC_EQ #0b0000_0000_0000_1000 &check_and_set_screen_res_80x60
    JUMP_IF_ACC_EQ #0b0000_0000_0000_0000 &check_and_set_screen_res_160x120


&check_and_set_screen_res_20x15
    CALL &set_res_to_20x15
    RETURN

&check_and_set_screen_res_40x30
    CALL &set_res_to_40x30
    RETURN

&check_and_set_screen_res_80x60
    CALL &set_res_to_80x60
    RETURN

&check_and_set_screen_res_160x120
    CALL &set_res_to_160x120
    RETURN

&check_and_set_screen_res_done
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
    // Set cursor column to zero
    SET [!VIDEO_CURSOR_COL] #0
    
    // Set cursor row to max row index
    // LOAD [$NUM_ROWS] ACC
    // DECR ACC
    // STORE ACC [!VIDEO_CURSOR_ROW]

    SET [!VIDEO_CURSOR_ROW] #1

    SET A !VIDEO_DATA
    SET B !VIDEO_CURSOR_COL

&fill_screen_draw_row
    LOAD [!VIDEO_STATUS] ACC
    AND #0b0000_0000_0001_1000
    JUMP_IF_ACC_EQ #0b0000_0000_0001_1000 &fill_screen_draw_row_20
    JUMP_IF_ACC_EQ #0b0000_0000_0001_0000 &fill_screen_draw_row_40
    JUMP_IF_ACC_EQ #0b0000_0000_0000_1000 &fill_screen_draw_row_80
    JUMP_IF_ACC_EQ #0b0000_0000_0000_0000 &fill_screen_draw_row_160
    HALT

&fill_screen_draw_row_20
    // Put the colour in ACC
    COPY C ACC

    // 0 -> 9
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]

    // 10 -> 19
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]

    JUMP &fill_screen_move_to_next_row

&fill_screen_draw_row_40
    // Put the colour in ACC
    COPY C ACC

    // 0 -> 9
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]

    // 10 -> 19
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]

    // 20 -> 29
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]

    // 30 -> 39
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]

    JUMP &fill_screen_move_to_next_row

&fill_screen_draw_row_80

    // Put the colour in ACC
    COPY C ACC

    // 0 -> 9
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]

    // 10 -> 19
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]

    // 20 -> 29
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]

    // 30 -> 39
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]

    // 40 -> 49
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]

    // 50 -> 59
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]

    // 60 -> 69
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]

    // 70 -> 79
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]

    JUMP &fill_screen_move_to_next_row

&fill_screen_draw_row_160
    // Put the colour in ACC
    COPY C ACC

    // 0 -> 9
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]

    // 10 -> 19
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]

    // 20 -> 29
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]

    // 30 -> 39
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]

    // 40 -> 49
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]

    // 50 -> 59
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]

    // 60 -> 69
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]

    // 70 -> 79
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]

    // 80 -> 89
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]

    // 90 -> 99
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]

    // 100 -> 109
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]

    // 110 -> 119
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]

    // 120 -> 129
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]

    // 130 -> 139
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]

    // 140 -> 149
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]

    // 150 -> 159
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]
    STORE_INCR ACC [A] [B]

    JUMP &fill_screen_move_to_next_row

&fill_screen_move_to_next_row
    // Decrement the row
    DECR [!VIDEO_CURSOR_ROW]

    // If the row went below zero we're done
    JUMP_IF_BORROW &fill_screen_done

    // Otherwise setup the next row
    // Set cursor column to zero
    SET [!VIDEO_CURSOR_COL] #0
    
    JUMP &fill_screen_draw_row      
    
&fill_screen_done
    RETURN

////////////////////////////////////////////////////////////
//
// Flip the draw buffer
//
////////////////////////////////////////////////////////////
&flip_draw_buffer
    LOAD [!VIDEO_STATUS] ACC
    XOR #0b_0000_0000_0010_0000
    STORE ACC [!VIDEO_STATUS]
    RETURN

$DOT_COLUMN
////////////////////////////////////////////////////////////
//
// Initialise dot
//
////////////////////////////////////////////////////////////
&initialise_dot
    SET [$DOT_COLUMN] #0
    RETURN

////////////////////////////////////////////////////////////
//
// Update dot
//
////////////////////////////////////////////////////////////
&update_dot
    LOAD [$DOT_COLUMN] ACC
    INCR ACC
    LOAD [$NUM_COLS] A
    JUMP_IF_ACC_LT A &update_dot_done
    SET_ZERO ACC
&update_dot_done
    STORE ACC [$DOT_COLUMN]
    RETURN
    

////////////////////////////////////////////////////////////
//
// Draw dot
//
////////////////////////////////////////////////////////////
&draw_dot
    SET [!VIDEO_CURSOR_ROW] #0    
    LOAD [$DOT_COLUMN] ACC
    STORE ACC [!VIDEO_CURSOR_COL]
    SET [!VIDEO_DATA] !VID_COL_WHITE
    RETURN


$PF_TOP_LEFT_COL
$PF_TOP_RIGHT_COL
$PF_TOP_ROW
$PF_TOP_COL

$PF_BOTTOM_LEFT_COL
$PF_BOTTOM_RIGHT_COL
$PF_BOTTOM_ROW
$PF_BOTTOM_COL


////////////////////////////////////////////////////////////
//
// Initialise playing field
//
////////////////////////////////////////////////////////////
&init_playing_field
    SET [$PF_TOP_LEFT_COL] #4
    SET [$PF_TOP_RIGHT_COL] #16
    SET [$PF_TOP_ROW] #5
    SET [$PF_TOP_COL] #0b0000_0000_0000_0011

    SET [$PF_BOTTOM_LEFT_COL] #4
    SET [$PF_BOTTOM_RIGHT_COL] #16
    SET [$PF_BOTTOM_ROW] #14
    SET [$PF_BOTTOM_COL] #0b0000_0000_0000_0011

    RETURN

////////////////////////////////////////////////////////////
//
// Draw playing field
//
////////////////////////////////////////////////////////////
&draw_playing_field
    LOAD [$PF_TOP_ROW] ACC
    STORE ACC [!VIDEO_CURSOR_ROW]
    LOAD [$PF_TOP_LEFT_COL] ACC
    STORE ACC [!VIDEO_CURSOR_COL]
    LOAD [$PF_TOP_RIGHT_COL] B
    STORE ACC [!VIDEO_CURSOR_COL]
    LOAD [$PF_TOP_COL] C
    
&draw_playing_field_top_line_loop
    STORE C [!VIDEO_DATA]
    INCR ACC
    JUMP_IF_ACC_GT B &draw_playing_field_bottom_line
    STORE ACC [!VIDEO_CURSOR_COL]
    JUMP &draw_playing_field_top_line_loop

&draw_playing_field_bottom_line
    LOAD [$PF_BOTTOM_ROW] ACC
    STORE ACC [!VIDEO_CURSOR_ROW]
    LOAD [$PF_BOTTOM_LEFT_COL] ACC
    STORE ACC [!VIDEO_CURSOR_COL]
    LOAD [$PF_BOTTOM_RIGHT_COL] B
    STORE ACC [!VIDEO_CURSOR_COL]
    LOAD [$PF_BOTTOM_COL] C
    
&draw_playing_field_bottom_line_loop
    STORE C [!VIDEO_DATA]
    INCR ACC
    JUMP_IF_ACC_GT B &draw_playing_field_done
    STORE ACC [!VIDEO_CURSOR_COL]
    JUMP &draw_playing_field_bottom_line_loop

&draw_playing_field_done
    RETURN





























