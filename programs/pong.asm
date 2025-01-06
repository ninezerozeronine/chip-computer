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

    SET SP #0b0001_1111_1111_0000

    CALL &init
    CALL &main_loop

$NUM_SCREEN_ROWS
$NUM_SCREEN_COLUMNS


////////////////////////////////////////////////////////////
//
// Initialise the program
//
////////////////////////////////////////////////////////////
&init
    CALL &set_res_to_20x15
    CALL &init_playing_field
    CALL &init_ball
    CALL &init_left_paddle
    CALL &init_right_paddle
    CALL &wait_for_frame_end
    RETURN

////////////////////////////////////////////////////////////
//
// Main execution loop
//
////////////////////////////////////////////////////////////
&main_loop

    SET [!STATUS_WORD] #0b1000_0000_0000_0000
    CALL &update_ball
    SET C #0
    CALL &fill_screen
    CALL &draw_playing_field
    CALL &draw_left_paddle
    CALL &draw_right_paddle
    CALL &draw_ball
    SET [!STATUS_WORD] #0b0000_0000_0000_0000
    CALL &wait_for_frame_end
    CALL &flip_draw_buffer
    JUMP &main_loop


////////////////////////////////////////////////////////////
//
// Set the video resolutions
//
////////////////////////////////////////////////////////////
&set_res_to_20x15
    SET [$NUM_SCREEN_ROWS] #15
    SET [$NUM_SCREEN_COLUMNS] #20
    LOAD [!VIDEO_STATUS] ACC
    OR !VIDEO_RES_20x15_OR
    STORE ACC [!VIDEO_STATUS]
    RETURN

////////////////////////////////////////////////////////////
//
// Wait for frame end
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
    LOAD [$NUM_SCREEN_ROWS] ACC
    DECR ACC
    STORE ACC [!VIDEO_CURSOR_ROW]

    SET A !VIDEO_DATA
    SET B !VIDEO_CURSOR_COL

&fill_screen_draw_row
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

$PF_TOP_LEFT_COLUMN
$PF_TOP_RIGHT_COLUMN
$PF_TOP_ROW_FP
$PF_TOP_COLOUR

$PF_BOTTOM_LEFT_COLUMN
$PF_BOTTOM_RIGHT_COLUMN
$PF_BOTTOM_ROW_FP
$PF_BOTTOM_COLOUR
////////////////////////////////////////////////////////////
//
// Initialise playing field
//
////////////////////////////////////////////////////////////
&init_playing_field
    SET [$PF_TOP_LEFT_COLUMN] #3
    SET [$PF_TOP_RIGHT_COLUMN] #16
    
    // Row index 2 - 
    SET [$PF_TOP_ROW_FP] #0b0000_0000_0010_1111
    SET [$PF_TOP_COLOUR] #0b0000_0000_0000_0011

    SET [$PF_BOTTOM_LEFT_COLUMN] #3
    SET [$PF_BOTTOM_RIGHT_COLUMN] #16
    
    // Row index 13
    SET [$PF_BOTTOM_ROW_FP] #0b0000_0000_1101_0000
    SET [$PF_BOTTOM_COLOUR] #0b0000_0000_0000_0011

    RETURN

////////////////////////////////////////////////////////////
//
// Draw playing field
//
////////////////////////////////////////////////////////////
&draw_playing_field
    LOAD [$PF_TOP_ROW_FP] ACC
    SHIFT_RIGHT ACC
    SHIFT_RIGHT ACC
    SHIFT_RIGHT ACC
    SHIFT_RIGHT ACC
    STORE ACC [!VIDEO_CURSOR_ROW]
    LOAD [$PF_TOP_LEFT_COLUMN] ACC
    STORE ACC [!VIDEO_CURSOR_COL]
    LOAD [$PF_TOP_RIGHT_COLUMN] B
    LOAD [$PF_TOP_COLOUR] C
    
&draw_playing_field_top_line_loop
    STORE C [!VIDEO_DATA]
    INCR ACC
    JUMP_IF_ACC_GT B &draw_playing_field_bottom_line
    STORE ACC [!VIDEO_CURSOR_COL]
    JUMP &draw_playing_field_top_line_loop

&draw_playing_field_bottom_line
    LOAD [$PF_BOTTOM_ROW_FP] ACC
    SHIFT_RIGHT ACC
    SHIFT_RIGHT ACC
    SHIFT_RIGHT ACC
    SHIFT_RIGHT ACC
    STORE ACC [!VIDEO_CURSOR_ROW]
    LOAD [$PF_BOTTOM_LEFT_COLUMN] ACC
    STORE ACC [!VIDEO_CURSOR_COL]
    LOAD [$PF_BOTTOM_RIGHT_COLUMN] B
    LOAD [$PF_BOTTOM_COLOUR] C
    
&draw_playing_field_bottom_line_loop
    STORE C [!VIDEO_DATA]
    INCR ACC
    JUMP_IF_ACC_GT B &draw_playing_field_done
    STORE ACC [!VIDEO_CURSOR_COL]
    JUMP &draw_playing_field_bottom_line_loop

&draw_playing_field_done
    RETURN


$BALL_ROW_FP
$BALL_COLUMN_FP
$BALL_COLOUR
$BALL_ROW_SPEED_FP
$BALL_COLUMN_SPEED_FP
////////////////////////////////////////////////////////////
//
// Initialise ball
//
////////////////////////////////////////////////////////////
&init_ball
    SET [$BALL_ROW_FP] #0b0000_0000_0110_0000
    SET [$BALL_COLUMN_FP] #0b0000_0000_1001_0000
    SET [$BALL_COLOUR] #0b0000_0000_0011_0000
    SET [$BALL_ROW_SPEED_FP] #10
    SET [$BALL_COLUMN_SPEED_FP] #9

    RETURN

////////////////////////////////////////////////////////////
//
// Update ball
//
////////////////////////////////////////////////////////////
&update_ball

    // Check if the ball isn't moving up or down - if so - no need for vertical checks
    LOAD [$BALL_ROW_SPEED_FP] A
    JUMP_IF_EQ_ZERO A &update_ball_left_right

    // Check if the ball is moving up - i.e. row speed is negative
    SET_ZERO ACC
    ADD A
    JUMP_IF_NOT_NEGATIVE_FLAG &update_ball_moving_down
    
    // See how far past the barrier the ball is after the move (in the direction of travel)
    LOAD [$BALL_ROW_FP] ACC
    ADD [$BALL_ROW_SPEED_FP]
    STORE ACC [$BALL_ROW_FP] // (Store unchecked result)
    COPY ACC A
    LOAD [$PF_TOP_ROW_FP] ACC
    SUB A

    // If the result is < 0, we're OK, stick with the already stored position,
    // Move on to left/right checks
    JUMP_IF_NEGATIVE_FLAG &update_ball_left_right
    
    // Otherwise add the distance and 2 to the barrier to determine the new position
    COPY ACC A
    LOAD [$PF_TOP_ROW_FP] ACC
    ADD #2
    ADD A
    STORE ACC [$BALL_ROW_FP]

    // Negate the speed
    SET_ZERO ACC 
    SUB [$BALL_ROW_SPEED_FP]
    STORE ACC [$BALL_ROW_SPEED_FP]

    // Move on to left and right checks
    JUMP &update_ball_left_right
    

&update_ball_moving_down
    // See how far past the barrier the ball is after the move (in the direction of travel)
    LOAD [$BALL_ROW_FP] ACC
    ADD [$BALL_ROW_SPEED_FP]
    STORE ACC [$BALL_ROW_FP] // (Store unchecked result)
    SUB [$PF_BOTTOM_ROW_FP]
    
    // If the result is < 0 we're OK, stick with the alredy stored position, move
    // on to the left right checks
    JUMP_IF_NEGATIVE_FLAG &update_ball_left_right

    // Otherwise subtract the distance and 2 from the barrier to determine the new position
    COPY ACC A
    LOAD [$PF_BOTTOM_ROW_FP] ACC
    SUB #2
    SUB A
    STORE ACC [$BALL_ROW_FP]

    // Negate the speed
    SET_ZERO ACC 
    SUB [$BALL_ROW_SPEED_FP]
    STORE ACC [$BALL_ROW_SPEED_FP]

    // Move on to left and right checks
    JUMP &update_ball_left_right

    
&update_ball_left_right
    // Check if the ball is moving to the right
    SET_ZERO ACC
    ADD [$BALL_COLUMN_SPEED_FP]
    JUMP_IF_NEGATIVE_FLAG &update_ball_moving_left

    // If the pos plus speed is less than the right paddle column, it's fine
    LOAD [$BALL_COLUMN_FP] ACC
    ADD [$BALL_COLUMN_SPEED_FP]
    JUMP_IF_ACC_LT [$R_PADDLE_COLUMN_FP] &update_ball_moving_right_no_collision

    // Otherwise we need to resolve the collision
    // Calculate new ball position
    LOAD [$R_PADDLE_COLUMN_FP] ACC
    SHIFT_LEFT ACC
    SUB [$BALL_COLUMN_FP]
    SUB [$BALL_COLUMN_SPEED_FP]
    SUB #2
    STORE ACC [$BALL_COLUMN_FP]

    // Reverse direction
    SET_ZERO ACC
    SUB [$BALL_COLUMN_SPEED_FP]
    STORE ACC [$BALL_COLUMN_SPEED_FP]
    RETURN
    
&update_ball_moving_right_no_collision
    STORE ACC [$BALL_COLUMN_FP]
    RETURN

&update_ball_moving_left
    // If the pos plus speed is greater than the left paddle column, it's fine
    LOAD [$BALL_COLUMN_FP] ACC
    ADD [$BALL_COLUMN_SPEED_FP]
    JUMP_IF_ACC_GT [$L_PADDLE_COLUMN_FP] &update_ball_moving_left_no_collision

    // Otherwise we need to resolve the collision
    // Calculate new ball position
    LOAD [$L_PADDLE_COLUMN_FP] ACC
    SHIFT_LEFT ACC
    SUB [$BALL_COLUMN_FP]
    SUB [$BALL_COLUMN_SPEED_FP]
    ADD #2
    STORE ACC [$BALL_COLUMN_FP]

    // Reverse direction
    SET_ZERO ACC
    SUB [$BALL_COLUMN_SPEED_FP]
    STORE ACC [$BALL_COLUMN_SPEED_FP]
    RETURN

&update_ball_moving_left_no_collision
    STORE ACC [$BALL_COLUMN_FP]
    RETURN


////////////////////////////////////////////////////////////
//
// Draw ball
//
////////////////////////////////////////////////////////////
&draw_ball
    LOAD [$BALL_ROW_FP] ACC
    SHIFT_RIGHT ACC
    SHIFT_RIGHT ACC
    SHIFT_RIGHT ACC
    SHIFT_RIGHT ACC
    STORE ACC [!VIDEO_CURSOR_ROW]

    LOAD [$BALL_COLUMN_FP] ACC
    SHIFT_RIGHT ACC
    SHIFT_RIGHT ACC
    SHIFT_RIGHT ACC
    SHIFT_RIGHT ACC
    STORE ACC [!VIDEO_CURSOR_COL]

    LOAD [$BALL_COLOUR] ACC
    STORE ACC [!VIDEO_DATA]
    RETURN


$L_PADDLE_COLUMN_FP
$L_PADDLE_TOP_ROW_FP
$L_PADDLE_BOTTOM_ROW_FP
$L_PADDLE_SPEED_FP
$L_PADDLE_COLOUR
////////////////////////////////////////////////////////////
//
// Initialise left_paddle
//
////////////////////////////////////////////////////////////
&init_left_paddle
    SET [$L_PADDLE_COLUMN_FP] #0b0000_0000_0010_1111
    SET [$L_PADDLE_TOP_ROW_FP] #0b0000_0000_0101_0000
    SET [$L_PADDLE_BOTTOM_ROW_FP] #0b0000_0000_1000_1111
    SET [$L_PADDLE_SPEED_FP] #0
    SET [$L_PADDLE_COLOUR] #0b0000_0000_0011_1111
    RETURN

////////////////////////////////////////////////////////////
//
// Draw left_paddle
//
////////////////////////////////////////////////////////////
&draw_left_paddle
    LOAD [$L_PADDLE_COLUMN_FP] ACC
    SHIFT_RIGHT ACC
    SHIFT_RIGHT ACC
    SHIFT_RIGHT ACC
    SHIFT_RIGHT ACC
    STORE ACC [!VIDEO_CURSOR_COL]
    
    LOAD [$L_PADDLE_TOP_ROW_FP] ACC
    SHIFT_RIGHT ACC
    SHIFT_RIGHT ACC
    SHIFT_RIGHT ACC
    SHIFT_RIGHT ACC
    STORE ACC [!VIDEO_CURSOR_ROW]
    LOAD [$L_PADDLE_BOTTOM_ROW_FP] A
    SHIFT_RIGHT A
    SHIFT_RIGHT A
    SHIFT_RIGHT A
    SHIFT_RIGHT A

    LOAD [$L_PADDLE_COLOUR] C

&draw_left_paddle_col_loop
    STORE C [!VIDEO_DATA]
    INCR ACC
    STORE ACC [!VIDEO_CURSOR_ROW]
    JUMP_IF_ACC_LTE A &draw_left_paddle_col_loop
    RETURN


$R_PADDLE_COLUMN_FP
$R_PADDLE_TOP_ROW_FP
$R_PADDLE_BOTTOM_ROW_FP
$R_PADDLE_SPEED_FP
$R_PADDLE_COLOUR
////////////////////////////////////////////////////////////
//
// Initialise right paddle
//
////////////////////////////////////////////////////////////
&init_right_paddle
    // 18
    SET [$R_PADDLE_COLUMN_FP] #0b0000_0001_0001_0000
    SET [$R_PADDLE_TOP_ROW_FP] #0b0000_0000_0101_0000
    SET [$R_PADDLE_BOTTOM_ROW_FP] #0b0000_0000_1000_1111
    SET [$R_PADDLE_SPEED_FP] #0
    SET [$R_PADDLE_COLOUR] #0b0000_0000_0011_1111
    RETURN

////////////////////////////////////////////////////////////
//
// Draw right paddle
//
////////////////////////////////////////////////////////////
&draw_right_paddle
    LOAD [$R_PADDLE_COLUMN_FP] ACC
    SHIFT_RIGHT ACC
    SHIFT_RIGHT ACC
    SHIFT_RIGHT ACC
    SHIFT_RIGHT ACC
    STORE ACC [!VIDEO_CURSOR_COL]
    
    LOAD [$R_PADDLE_TOP_ROW_FP] ACC
    SHIFT_RIGHT ACC
    SHIFT_RIGHT ACC
    SHIFT_RIGHT ACC
    SHIFT_RIGHT ACC
    STORE ACC [!VIDEO_CURSOR_ROW]
    LOAD [$R_PADDLE_BOTTOM_ROW_FP] A
    SHIFT_RIGHT A
    SHIFT_RIGHT A
    SHIFT_RIGHT A
    SHIFT_RIGHT A

    LOAD [$R_PADDLE_COLOUR] C

&draw_right_paddle_col_loop
    STORE C [!VIDEO_DATA]
    INCR ACC
    STORE ACC [!VIDEO_CURSOR_ROW]
    JUMP_IF_ACC_LTE A &draw_right_paddle_col_loop
    RETURN





















