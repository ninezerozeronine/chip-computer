                  // #0b1111_1111_1111_0000
                  // #0b1111_1111_1111_0001
                  // #0b1111_1111_1111_0010
                  // #0b1111_1111_1111_0011
                  // #0b1111_1111_1111_0100
                  // #0b1111_1111_1111_0101
                  // #0b1111_1111_1111_0110
!SOUND_SQUARE        #0b1111_1111_1111_0111
!GAME_PAD_2          #0b1111_1111_1111_1000
!GAME_PAD_1          #0b1111_1111_1111_1001
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

!VID_COL_WHITE   #0b0000_0000_0011_1111

!CHAR_C             #0b01110_10001_01010_0
!CHAR_E             #0b11111_10101_10101_0
!CHAR_O             #0b01110_10001_01110_0
!CHAR_P             #0b11111_10100_01000_0
!CHAR_R             #0b11111_10100_01011_0
!CHAR_S             #0b01001_10101_10010_0
!CHAR_EXCLM         #0b00000_11101_00000_0
!CHAR_COLON         #0b00000_01010_00000_0
!CHAR_0             #0b11111_10001_11111_0
!CHAR_1             #0b01001_11111_00001_0
!CHAR_2             #0b10011_10101_01001_0
!CHAR_3             #0b10001_10101_01010_0
!CHAR_4             #0b11100_00100_11111_0
!CHAR_5             #0b11101_10101_10010_0


!SNES_PAD_UP     #0b0000_0000_0001_0000
!SNES_PAD_DOWN   #0b0000_0000_0010_0000
!SNES_PAD_SELECT #0b0000_0000_0000_0100

!NES_PAD_UP     #0b0000_0000_0001_0000
!NES_PAD_DOWN   #0b0000_0000_0010_0000
!NES_PAD_LEFT   #0b0000_0000_0100_0000
!NES_PAD_RIGHT  #0b0000_0000_1000_0000
!NES_PAD_A      #0b0000_0000_0000_0001
!NES_PAD_B      #0b0000_0000_0000_0010
!NES_PAD_START  #0b0000_0000_0000_1000
!NES_PAD_SELECT #0b0000_0000_0000_0100


!L_PADDLE_INIT_TOP_ROW     #14
!L_PADDLE_INIT_BOTTOM_ROW  #20
!L_PADDLE_INIT_COLUMN      #2
!L_PADDLE_INIT_COLOUR      #0b0000_0000_0011_0000
!L_PADDLE_MOVE_TICKER_INCR #0b0100_0000_0000_0000

!R_PADDLE_INIT_TOP_ROW     #14
!R_PADDLE_INIT_BOTTOM_ROW  #20
!R_PADDLE_INIT_COLUMN      #37
!R_PADDLE_INIT_COLOUR      #0b0000_0000_0000_1100
!R_PADDLE_MOVE_TICKER_INCR #0b0100_0000_0000_0000

!PADDLE_HIGHEST_ROW        #7
!PADDLE_LOWEST_ROW         #28


!BALL_INIT_ROW                      #17
!BALL_INIT_COLUMN                   #19
!BALL_INIT_COLOUR                   #0b0000_0000_0011_1111
!BALL_HORIZ_MOVE_TICKER_INCR        #0b0100_0000_0000_0000
!BALL_VERT_MOVE_TICKER_INCR_UNIT    #0b0100_0000_0000_0000


!PF_INIT_TOP_LEFT_COLUMN #3
!PF_INIT_TOP_RIGHT_COLUMN #36
!PF_INIT_TOP_ROW #8
!PF_INIT_TOP_COLOUR #0b0000_0000_0000_0011

!PF_INIT_BOTTOM_LEFT_COLUMN #3
!PF_INIT_BOTTOM_RIGHT_COLUMN #36
!PF_INIT_BOTTOM_ROW #27
!PF_INIT_BOTTOM_COLOUR #0b0000_0000_0000_0011

!GAME_MODE_READY #0
!GAME_MODE_PLAYING #1
!GAME_MODE_POINT_SCORED #2
!GAME_MODE_WINNER #3


    SET SP #0b0001_1111_1111_0000

    CALL &init
    CALL &main_loop

$NUM_SCREEN_ROWS
$NUM_SCREEN_COLUMNS
$GAME_MODE
$POINT_SCORED_COUNTER
$WHO_SCORED

////////////////////////////////////////////////////////////
//
// Initialise the program
//
////////////////////////////////////////////////////////////
&init
    SET [$GAME_MODE] !GAME_MODE_PLAYING
    CALL &set_res_to_40x30
    CALL &initialise_sound
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
    CALL &check_select
    CALL &update_sound

    LOAD [$GAME_MODE] ACC
    JUMP_IF_ACC_EQ !GAME_MODE_PLAYING &main_loop_playing
    JUMP_IF_ACC_EQ !GAME_MODE_POINT_SCORED &main_loop_point_scored

&main_loop_playing
    CALL &update_left_paddle
    CALL &update_right_paddle
    CALL &update_ball
    SET C #0
    CALL &fill_screen
    CALL &draw_playing_field
    CALL &draw_left_paddle
    CALL &draw_right_paddle
    CALL &draw_ball
    CALL &draw_score
    JUMP &main_loop_end

&main_loop_point_scored
    CALL &update_point_scored
    SET C #0
    CALL &fill_screen
    CALL &draw_playing_field
    CALL &draw_left_paddle
    CALL &draw_right_paddle
    CALL &draw_ball
    CALL &draw_score
    CALL &draw_point_scorer
    JUMP &main_loop_end

&main_loop_end
    SET [!STATUS_WORD] #0b0000_0000_0000_0000
    CALL &wait_for_frame_end
    CALL &flip_draw_buffer
    JUMP &main_loop

////////////////////////////////////////////////////////////
//
// Check to see if the game should reset
//
////////////////////////////////////////////////////////////
&check_select
    // Read up button on controller
    LOAD [!GAME_PAD_1] ACC
    AND !SNES_PAD_SELECT
    JUMP_IF_ZERO_FLAG &check_select_done
    CALL &init
    RETURN

&check_select_done
    RETURN

////////////////////////////////////////////////////////////
//
// Set the video resolutions
//
////////////////////////////////////////////////////////////
&set_res_to_40x30
    SET [$NUM_SCREEN_COLUMNS] #40
    SET [$NUM_SCREEN_ROWS] #30
    LOAD [!VIDEO_STATUS] ACC
    AND !VIDEO_RES_40x30_AND
    OR !VIDEO_RES_40x30_OR
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
$PF_TOP_ROW
$PF_TOP_COLOUR

$PF_BOTTOM_LEFT_COLUMN
$PF_BOTTOM_RIGHT_COLUMN
$PF_BOTTOM_ROW
$PF_BOTTOM_COLOUR
////////////////////////////////////////////////////////////
//
// Initialise playing field
//
////////////////////////////////////////////////////////////
&init_playing_field
    SET [$PF_TOP_LEFT_COLUMN] !PF_INIT_TOP_LEFT_COLUMN
    SET [$PF_TOP_RIGHT_COLUMN] !PF_INIT_TOP_RIGHT_COLUMN
    SET [$PF_TOP_ROW] !PF_INIT_TOP_ROW
    SET [$PF_TOP_COLOUR] !PF_INIT_TOP_COLOUR

    SET [$PF_BOTTOM_LEFT_COLUMN] !PF_INIT_BOTTOM_LEFT_COLUMN
    SET [$PF_BOTTOM_RIGHT_COLUMN] !PF_INIT_BOTTOM_RIGHT_COLUMN
    SET [$PF_BOTTOM_ROW] !PF_INIT_BOTTOM_ROW
    SET [$PF_BOTTOM_COLOUR] !PF_INIT_BOTTOM_COLOUR

    RETURN

////////////////////////////////////////////////////////////
//
// Draw playing field
//
////////////////////////////////////////////////////////////
&draw_playing_field
    LOAD [$PF_TOP_ROW] ACC
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
    LOAD [$PF_BOTTOM_ROW] ACC
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


$BALL_ROW
$BALL_COLUMN
$BALL_COLOUR
$BALL_HORIZ_DIR
$BALL_HORIZ_MOVE_TICKER
$BALL_HORIZ_MOVE_TICKER_INCR
$BALL_VERT_DIR
$BALL_VERT_MOVE_TICKER
$BALL_VERT_MOVE_TICKER_INCR
$BALL_PREV_ROW_1
$BALL_PREV_ROW_2
$BALL_PREV_ROW_3
$BALL_PREV_COLUMN_1
$BALL_PREV_COLUMN_2
$BALL_PREV_COLUMN_3
$BALL_PREV_COLOUR_1
$BALL_PREV_COLOUR_2
$BALL_PREV_COLOUR_3
////////////////////////////////////////////////////////////
//
// Initialise ball
//
////////////////////////////////////////////////////////////
&init_ball
    SET [$BALL_ROW] !BALL_INIT_ROW
    SET [$BALL_COLUMN] !BALL_INIT_COLUMN
    SET [$BALL_COLOUR] !BALL_INIT_COLOUR
    SET [$BALL_HORIZ_DIR] #1
    SET [$BALL_HORIZ_MOVE_TICKER] #0
    SET [$BALL_HORIZ_MOVE_TICKER_INCR] !BALL_HORIZ_MOVE_TICKER_INCR
    SET [$BALL_VERT_DIR] #0
    SET [$BALL_VERT_MOVE_TICKER] #0
    SET [$BALL_VERT_MOVE_TICKER_INCR] #0

    SET [$BALL_PREV_ROW_1] !BALL_INIT_ROW
    SET [$BALL_PREV_ROW_2] !BALL_INIT_ROW
    SET [$BALL_PREV_COLUMN_1] !BALL_INIT_COLUMN
    SET [$BALL_PREV_COLUMN_2] !BALL_INIT_COLUMN
    SET [$BALL_PREV_COLOUR_1] !BALL_INIT_COLOUR
    SET [$BALL_PREV_COLOUR_2] !BALL_INIT_COLOUR

    RETURN

////////////////////////////////////////////////////////////
//
// Update ball
//
////////////////////////////////////////////////////////////
&update_ball

    // See if it's time to move the ball horizontally
    LOAD [$BALL_HORIZ_MOVE_TICKER] ACC
    ADD [$BALL_HORIZ_MOVE_TICKER_INCR]
    STORE ACC [$BALL_HORIZ_MOVE_TICKER]
    JUMP_IF_NOT_CARRY &update_ball_done

    // Take the current attrs of the ball and store them for the trail
    CALL &update_ball_set_prev_attrs

    // Check if the ball is moving to the right
    LOAD [$BALL_HORIZ_DIR] ACC
    JUMP_IF_ACC_NEQ #1 &update_ball_moving_left

    // Ball is moving to the right
    // If the pos plus speed is less than the right paddle column, it's fine
    LOAD [$BALL_COLUMN] ACC
    INCR ACC
    JUMP_IF_ACC_LT [$R_PADDLE_COLUMN] &update_ball_moving_right_no_collision

    // Otherwise we need to check if we hit the paddle
    // Check if it's above the top
    LOAD [$BALL_ROW] ACC
    LOAD [$R_PADDLE_TOP_ROW] A
    JUMP_IF_ACC_LT A &update_ball_right_paddle_miss

    // Check if it's below the bottom
    LOAD [$R_PADDLE_BOTTOM_ROW] A
    JUMP_IF_ACC_GT A &update_ball_right_paddle_miss

    // Update the ball position - make it bounce off the paddle
    DECR [$BALL_COLUMN]

    // Reverse direction
    SET [$BALL_HORIZ_DIR] #-1

    // Update ball vertical speed and dir
    LOAD [$R_PADDLE_VERT_DIR] A
    CALL &ball_paddle_hit_update_vert_speed_and_dir

    // Make a sound
    SET A #0b0111_0000_0011_1111
    SET B #5
    CALL &add_note

    JUMP &update_ball_up_down
    
&update_ball_moving_right_no_collision
    STORE ACC [$BALL_COLUMN]
    JUMP &update_ball_up_down

&update_ball_moving_left
    // If the pos plus speed is greater than the left paddle column, it's fine
    LOAD [$BALL_COLUMN] ACC
    DECR ACC
    JUMP_IF_ACC_GT [$L_PADDLE_COLUMN] &update_ball_moving_left_no_collision

    // Otherwise we need to check if we hit the paddle
    // Check if it's above the top
    LOAD [$BALL_ROW] ACC
    LOAD [$L_PADDLE_TOP_ROW] A
    JUMP_IF_ACC_LT A &update_ball_left_paddle_miss

    // Check if it's below the bottom
    LOAD [$L_PADDLE_BOTTOM_ROW] A
    JUMP_IF_ACC_GT A &update_ball_left_paddle_miss

    // Otherwise we need to resolve the collision - have it bounce off the paddle
    INCR [$BALL_COLUMN]

    // Reverse direction
    SET [$BALL_HORIZ_DIR] #1

    // Update ball vertical speed and dir
    LOAD [$L_PADDLE_VERT_DIR] A
    CALL &ball_paddle_hit_update_vert_speed_and_dir

    // Make a sound
    SET A #0b0111_0000_1111_1111
    SET B #5
    CALL &add_note

    // Proceed to up down checks
    JUMP &update_ball_up_down

&update_ball_moving_left_no_collision
    STORE ACC [$BALL_COLUMN]
    JUMP &update_ball_up_down

&update_ball_right_paddle_miss
    INCR [$L_SCORE]
    SET [$WHO_SCORED] #1
    CALL &set_game_mode_point_scored
    RETURN

&update_ball_left_paddle_miss
    INCR [$R_SCORE]
    SET [$WHO_SCORED] #2
    CALL &set_game_mode_point_scored
    RETURN

&update_ball_up_down

    // See if it's time to move the ball vertically
    LOAD [$BALL_VERT_MOVE_TICKER] ACC
    ADD [$BALL_VERT_MOVE_TICKER_INCR]
    STORE ACC [$BALL_VERT_MOVE_TICKER]
    JUMP_IF_NOT_CARRY &update_ball_done

    // Check if the ball isn't moving up or down - if so - no need for vertical checks
    LOAD [$BALL_VERT_DIR] ACC
    JUMP_IF_ACC_EQ #0 &update_ball_done

    // Check if the ball is moving down - i.e. vert dir is +ve
    COPY ACC A
    SET_ZERO ACC
    ADD A
    JUMP_IF_NOT_NEGATIVE_FLAG &update_ball_moving_down
    
    // Otherwise we're moving up
    // Calculate new position
    DECR [$BALL_ROW]
    LOAD [$BALL_ROW] ACC

    // Check we haven't collided with the barrier
    JUMP_IF_ACC_GT [$PF_TOP_ROW] &update_ball_done

    // Otherwise we've collided

    // Update the position
    ADD #2
    STORE ACC [$BALL_ROW]

    // Flip direction (so we're moving down)
    SET_ZERO ACC
    SUB [$BALL_VERT_DIR]
    STORE ACC [$BALL_VERT_DIR]

    // Done
    RETURN

&update_ball_moving_down

    // Calculate new position
    INCR [$BALL_ROW]
    LOAD [$BALL_ROW] ACC

    // Check we haven't collided with the barrier
    JUMP_IF_ACC_LT [$PF_BOTTOM_ROW] &update_ball_done

    // Otherwise we've collided

    // Update the position
    SUB #2
    STORE ACC [$BALL_ROW]

    // Flip direction (so we're moving up)
    SET_ZERO ACC
    SUB [$BALL_VERT_DIR]
    STORE ACC [$BALL_VERT_DIR]

    // Done
    RETURN

&update_ball_done
    RETURN

&update_ball_set_prev_attrs
    LOAD [$BALL_PREV_ROW_1] ACC
    STORE ACC [$BALL_PREV_ROW_2]
    LOAD [$BALL_ROW] ACC
    STORE ACC [$BALL_PREV_ROW_1]

    LOAD [$BALL_PREV_COLUMN_1] ACC
    STORE ACC [$BALL_PREV_COLUMN_2]
    LOAD [$BALL_COLUMN] ACC
    STORE ACC [$BALL_PREV_COLUMN_1]

    LOAD [$BALL_PREV_COLOUR_1] ACC
    STORE ACC [$BALL_PREV_COLOUR_2]
    LOAD [$BALL_COLOUR] ACC
    STORE ACC [$BALL_PREV_COLOUR_1]
    RETURN

////////////////////////////////////////////////////////////
//
// Resolve ball vertical motion on paddle collision
//
// Value in A is the paddle dir
//
////////////////////////////////////////////////////////////
&ball_paddle_hit_update_vert_speed_and_dir
    // Assume the result of adding the paddle vel to the ball dir
    // is positive
    SET_ZERO B

    // Add paddle vel to ball
    LOAD [$BALL_VERT_DIR] ACC
    ADD A

    // If negative
    JUMP_IF_NOT_NEGATIVE_FLAG &bph_neg_check_done

        // Store that it's negative
        SET B #1

        // Flip it to positive
        COPY ACC C
        SET_ZERO ACC
        SUB C

    &bph_neg_check_done
    // If > 3
    JUMP_IF_ACC_LTE #3 &bph_calc_new_incr

        // Clamp to 3
        SET ACC #3

    &bph_calc_new_incr
    COPY ACC A // We might need to invert this at the end

    // Incr = incr * vel
    COPY ACC C
    SET_ZERO ACC

    &bph_inc_ticker_loop
    DECR C
    JUMP_IF_NEGATIVE_FLAG &bph_ticker_loop_done
    ADD !BALL_VERT_MOVE_TICKER_INCR_UNIT
    JUMP &bph_inc_ticker_loop

    &bph_ticker_loop_done
    STORE ACC [$BALL_VERT_MOVE_TICKER_INCR]

    // Assume dir was positive and store result
    STORE A [$BALL_VERT_DIR]

    // If was negative
    SET_ZERO ACC
    ADD B
    JUMP_IF_ZERO_FLAG &bph_done

        // Flip ball vert dir and store it
        SET_ZERO ACC
        SUB A
        STORE ACC [$BALL_VERT_DIR]

    &bph_done
    RETURN


////////////////////////////////////////////////////////////
//
// Draw ball
//
////////////////////////////////////////////////////////////
&draw_ball
    LOAD [$BALL_PREV_ROW_2] ACC
    STORE ACC [!VIDEO_CURSOR_ROW]
    LOAD [$BALL_PREV_COLUMN_2] ACC
    STORE ACC [!VIDEO_CURSOR_COL]
    LOAD [$BALL_PREV_COLOUR_2] C
    CALL &reduce_colour_by_1
    CALL &reduce_colour_by_1
    STORE C [!VIDEO_DATA]

    LOAD [$BALL_PREV_ROW_1] ACC
    STORE ACC [!VIDEO_CURSOR_ROW]
    LOAD [$BALL_PREV_COLUMN_1] ACC
    STORE ACC [!VIDEO_CURSOR_COL]
    LOAD [$BALL_PREV_COLOUR_2] C
    CALL &reduce_colour_by_1
    STORE C [!VIDEO_DATA]
    STORE ACC [!VIDEO_DATA]

    LOAD [$BALL_ROW] ACC
    STORE ACC [!VIDEO_CURSOR_ROW]
    LOAD [$BALL_COLUMN] ACC
    STORE ACC [!VIDEO_CURSOR_COL]
    LOAD [$BALL_COLOUR] ACC
    STORE ACC [!VIDEO_DATA]

    RETURN

////////////////////////////////////////////////////////////
//
// Reduce colour by 1
//
// Reduce all the values of the colour by 1
//
// C: The colour - edited in place
//
////////////////////////////////////////////////////////////
&reduce_colour_by_1
    // Reduce R
    COPY C ACC
    AND #0b0000_0000_0011_0000
    SUB #0b0000_0000_0001_0000
    AND #0b0000_0000_0011_0000
    COPY ACC A
    COPY C ACC
    AND #0b1111_1111_1100_1111
    OR A

    // Reduce G
    COPY ACC C
    AND #0b0000_0000_0000_1100
    SUB #0b0000_0000_0000_0100
    AND #0b0000_0000_0000_1100
    COPY ACC A
    COPY C ACC
    AND #0b1111_1111_1111_0011
    OR A

    // Reduce B
    COPY ACC C
    AND #0b0000_0000_0000_0011
    SUB #1
    JUMP_IF_NOT_BORROW &reduce_colour_by_1_skip_reset_to_zero
    SET_ZERO ACC
&reduce_colour_by_1_skip_reset_to_zero
    COPY ACC A
    COPY C ACC
    AND #0b1111_1111_1111_1100
    OR A
    COPY ACC C
    RETURN


$L_PADDLE_COLUMN
$L_PADDLE_TOP_ROW
$L_PADDLE_BOTTOM_ROW
$L_PADDLE_MOVE_TICKER
$L_PADDLE_MOVE_TICKER_INCR
$L_PADDLE_VERT_DIR
$L_PADDLE_COLOUR
$L_SCORE
////////////////////////////////////////////////////////////
//
// Initialise left_paddle
//
////////////////////////////////////////////////////////////
&init_left_paddle
    CALL &reset_left_paddle_pos
    SET [$L_PADDLE_COLOUR] !L_PADDLE_INIT_COLOUR
    SET [$L_SCORE] #0
    RETURN

////////////////////////////////////////////////////////////
//
// Reset left paddle pos
//
////////////////////////////////////////////////////////////
&reset_left_paddle_pos
    SET [$L_PADDLE_COLUMN] !L_PADDLE_INIT_COLUMN
    SET [$L_PADDLE_TOP_ROW] !L_PADDLE_INIT_TOP_ROW
    SET [$L_PADDLE_BOTTOM_ROW] !L_PADDLE_INIT_BOTTOM_ROW
    SET [$L_PADDLE_MOVE_TICKER] #0
    SET [$L_PADDLE_MOVE_TICKER_INCR] !L_PADDLE_MOVE_TICKER_INCR
    SET [$L_PADDLE_VERT_DIR] #0
    RETURN

////////////////////////////////////////////////////////////
//
// Update left_paddle
//
////////////////////////////////////////////////////////////
&update_left_paddle
    // Read up button on controller
    LOAD [!GAME_PAD_1] A

    // Check if up is pressed
    COPY A ACC
    AND !SNES_PAD_UP
    JUMP_IF_NOT_ZERO_FLAG &update_left_paddle_up_pressed

    // Check if down is pressed
    COPY A ACC
    AND !SNES_PAD_DOWN
    JUMP_IF_NOT_ZERO_FLAG &update_left_paddle_down_pressed

    // Otherwise nothing is pressed
    JUMP &update_left_paddle_nothing_pressed

&update_left_paddle_up_pressed
    // See if there's room to move up
    LOAD [$L_PADDLE_TOP_ROW] ACC
    JUMP_IF_ACC_EQ !PADDLE_HIGHEST_ROW &update_left_paddle_hit_top

    // There's room for the paddle to move up
    // Set the direction for ref in paddle collisions
    SET [$L_PADDLE_VERT_DIR] #-1

    // See if it's time to move the paddle
    LOAD [$L_PADDLE_MOVE_TICKER] ACC
    ADD [$L_PADDLE_MOVE_TICKER_INCR]
    STORE ACC [$L_PADDLE_MOVE_TICKER]
    JUMP_IF_NOT_CARRY &update_left_paddle_done

    // Move the paddle up
    DECR [$L_PADDLE_TOP_ROW]
    DECR [$L_PADDLE_BOTTOM_ROW]

    // Done
    RETURN

&update_left_paddle_hit_top
    // No room to move the paddle up - reset the direction ref to still
    SET [$L_PADDLE_VERT_DIR] #0
    RETURN

&update_left_paddle_down_pressed
    // See if there's room to move down
    LOAD [$L_PADDLE_BOTTOM_ROW] ACC
    JUMP_IF_ACC_EQ !PADDLE_LOWEST_ROW &update_left_paddle_hit_bottom

    // There's room for the paddle to move down
    // Set the direction for ref in paddle collisions
    SET [$L_PADDLE_VERT_DIR] #1

    // See if it's time to move the paddle
    LOAD [$L_PADDLE_MOVE_TICKER] ACC
    ADD [$L_PADDLE_MOVE_TICKER_INCR]
    STORE ACC [$L_PADDLE_MOVE_TICKER]
    JUMP_IF_NOT_CARRY &update_left_paddle_done

    // Move the paddle down
    INCR [$L_PADDLE_TOP_ROW]
    INCR [$L_PADDLE_BOTTOM_ROW]

    // Done!
    RETURN

&update_left_paddle_hit_bottom
    // No room to move the paddle down - reset the direction ref to still
    SET [$L_PADDLE_VERT_DIR] #0
    RETURN

&update_left_paddle_nothing_pressed
    // Set the direction for ref in paddle collisions
    SET [$L_PADDLE_VERT_DIR] #0

&update_left_paddle_done
    RETURN

////////////////////////////////////////////////////////////
//
// Draw left_paddle
//
////////////////////////////////////////////////////////////
&draw_left_paddle
    LOAD [$L_PADDLE_COLUMN] ACC
    STORE ACC [!VIDEO_CURSOR_COL]
    
    LOAD [$L_PADDLE_TOP_ROW] ACC
    STORE ACC [!VIDEO_CURSOR_ROW]
    LOAD [$L_PADDLE_BOTTOM_ROW] A

    LOAD [$L_PADDLE_COLOUR] C

&draw_left_paddle_col_loop
    STORE C [!VIDEO_DATA]
    INCR ACC
    STORE ACC [!VIDEO_CURSOR_ROW]
    JUMP_IF_ACC_LTE A &draw_left_paddle_col_loop
    RETURN


$R_PADDLE_COLUMN
$R_PADDLE_TOP_ROW
$R_PADDLE_BOTTOM_ROW
$R_PADDLE_MOVE_TICKER
$R_PADDLE_MOVE_TICKER_INCR
$R_PADDLE_VERT_DIR
$R_PADDLE_COLOUR
$R_SCORE
////////////////////////////////////////////////////////////
//
// Initialise right paddle
//
////////////////////////////////////////////////////////////
&init_right_paddle
    SET [$R_PADDLE_COLUMN] !R_PADDLE_INIT_COLUMN
    SET [$R_PADDLE_TOP_ROW] !R_PADDLE_INIT_TOP_ROW
    SET [$R_PADDLE_BOTTOM_ROW] !R_PADDLE_INIT_BOTTOM_ROW
    SET [$R_PADDLE_MOVE_TICKER] #0
    SET [$R_PADDLE_MOVE_TICKER_INCR] !R_PADDLE_MOVE_TICKER_INCR
    SET [$R_PADDLE_VERT_DIR] #0
    SET [$R_PADDLE_COLOUR] !R_PADDLE_INIT_COLOUR
    SET [$R_SCORE] #0
    RETURN

////////////////////////////////////////////////////////////
//
// Reset right paddle pos
//
////////////////////////////////////////////////////////////
&reset_right_paddle_pos
    SET [$R_PADDLE_COLUMN] !R_PADDLE_INIT_COLUMN
    SET [$R_PADDLE_TOP_ROW] !R_PADDLE_INIT_TOP_ROW
    SET [$R_PADDLE_BOTTOM_ROW] !R_PADDLE_INIT_BOTTOM_ROW
    SET [$R_PADDLE_MOVE_TICKER] #0
    SET [$R_PADDLE_MOVE_TICKER_INCR] !R_PADDLE_MOVE_TICKER_INCR
    SET [$R_PADDLE_VERT_DIR] #0


////////////////////////////////////////////////////////////
//
// Update right paddle
//
////////////////////////////////////////////////////////////
&update_right_paddle
    // Read up button on controller
    LOAD [!GAME_PAD_2] A

    // Check if up is pressed
    COPY A ACC
    AND !NES_PAD_UP
    JUMP_IF_NOT_ZERO_FLAG &update_right_paddle_up_pressed

    // Check if down is pressed
    COPY A ACC
    AND !NES_PAD_DOWN
    JUMP_IF_NOT_ZERO_FLAG &update_right_paddle_down_pressed

    // Otherwise nothing is pressed
    JUMP &update_right_paddle_nothing_pressed

&update_right_paddle_up_pressed
    // See if there's room to move up
    LOAD [$R_PADDLE_TOP_ROW] ACC
    JUMP_IF_ACC_EQ !PADDLE_HIGHEST_ROW &update_right_paddle_hit_top

    // There's room for the paddle to move up
    // Set the direction for ref in paddle collisions
    SET [$R_PADDLE_VERT_DIR] #-1

    // See if it's time to move the paddle
    LOAD [$R_PADDLE_MOVE_TICKER] ACC
    ADD [$R_PADDLE_MOVE_TICKER_INCR]
    STORE ACC [$R_PADDLE_MOVE_TICKER]
    JUMP_IF_NOT_CARRY &update_right_paddle_done

    // Move the paddle up
    DECR [$R_PADDLE_TOP_ROW]
    DECR [$R_PADDLE_BOTTOM_ROW]

    // Done
    RETURN

&update_right_paddle_hit_top
    // No room to move the paddle up - reset the direction ref to still
    SET [$R_PADDLE_VERT_DIR] #0
    RETURN

&update_right_paddle_down_pressed
    // See if there's room to move down
    LOAD [$R_PADDLE_BOTTOM_ROW] ACC
    JUMP_IF_ACC_EQ !PADDLE_LOWEST_ROW &update_right_paddle_hit_bottom

    // There's room for the paddle to move down
    // Set the direction for ref in paddle collisions
    SET [$R_PADDLE_VERT_DIR] #1

    // See if it's time to move the paddle
    LOAD [$R_PADDLE_MOVE_TICKER] ACC
    ADD [$R_PADDLE_MOVE_TICKER_INCR]
    STORE ACC [$R_PADDLE_MOVE_TICKER]
    JUMP_IF_NOT_CARRY &update_right_paddle_done

    // Move the paddle down
    INCR [$R_PADDLE_TOP_ROW]
    INCR [$R_PADDLE_BOTTOM_ROW]

    // Done!
    RETURN

&update_right_paddle_hit_bottom
    // No room to move the paddle down - reset the direction ref to still
    SET [$R_PADDLE_VERT_DIR] #0
    RETURN

&update_right_paddle_nothing_pressed
    // Set the direction for ref in paddle collisions
    SET [$R_PADDLE_VERT_DIR] #0

&update_right_paddle_done
    RETURN

////////////////////////////////////////////////////////////
//
// Draw right_paddle
//
////////////////////////////////////////////////////////////
&draw_right_paddle
    LOAD [$R_PADDLE_COLUMN] ACC
    STORE ACC [!VIDEO_CURSOR_COL]
    
    LOAD [$R_PADDLE_TOP_ROW] ACC
    STORE ACC [!VIDEO_CURSOR_ROW]
    LOAD [$R_PADDLE_BOTTOM_ROW] A

    LOAD [$R_PADDLE_COLOUR] C

&draw_right_paddle_col_loop
    STORE C [!VIDEO_DATA]
    INCR ACC
    STORE ACC [!VIDEO_CURSOR_ROW]
    JUMP_IF_ACC_LTE A &draw_right_paddle_col_loop
    RETURN

////////////////////////////////////////////////////////////
//
// Check if a point was scored
//
////////////////////////////////////////////////////////////
&point_score

    // Reset the ball

    RETURN

////////////////////////////////////////////////////////////
//
// Check if the game has ended
//
////////////////////////////////////////////////////////////
&game_end
    LOAD [$L_SCORE] ACC
    JUMP_IF_ACC_EQ #5 &game_end_points

    LOAD [$R_SCORE] ACC
    JUMP_IF_ACC_EQ #5 &game_end_points

&game_end_points

    RETURN

////////////////////////////////////////////////////////////
//
// Draw the score
//
////////////////////////////////////////////////////////////
&draw_score

    // Left paddle/P1
    SET [!VIDEO_CURSOR_COL] #1
    SET [!VIDEO_CURSOR_ROW] #1
    LOAD [$L_PADDLE_COLOUR] C
    SET A !CHAR_P
    CALL &draw_character
    SET A !CHAR_1
    CALL &draw_character
    SET A !CHAR_COLON
    CALL &draw_character
    LOAD [$L_SCORE] ACC
    JUMP_IF_ACC_EQ #0 &draw_score_set_l_char_0
    JUMP_IF_ACC_EQ #1 &draw_score_set_l_char_1
    JUMP_IF_ACC_EQ #2 &draw_score_set_l_char_2
    JUMP_IF_ACC_EQ #3 &draw_score_set_l_char_3
    JUMP_IF_ACC_EQ #4 &draw_score_set_l_char_4
    JUMP_IF_ACC_EQ #5 &draw_score_set_l_char_5

&draw_score_set_l_char_0
    SET A !CHAR_0
    JUMP &draw_score_set_l_char_done

&draw_score_set_l_char_1
    SET A !CHAR_1
    JUMP &draw_score_set_l_char_done

&draw_score_set_l_char_2
    SET A !CHAR_2
    JUMP &draw_score_set_l_char_done

&draw_score_set_l_char_3
    SET A !CHAR_3
    JUMP &draw_score_set_l_char_done

&draw_score_set_l_char_4
    SET A !CHAR_4
    JUMP &draw_score_set_l_char_done

&draw_score_set_l_char_5
    SET A !CHAR_5
    JUMP &draw_score_set_l_char_done

&draw_score_set_l_char_done
    CALL &draw_character

    // Right paddle/P2
    SET [!VIDEO_CURSOR_COL] #24
    SET [!VIDEO_CURSOR_ROW] #1
    LOAD [$R_PADDLE_COLOUR] C
    SET A !CHAR_P
    CALL &draw_character
    SET A !CHAR_2
    CALL &draw_character
    SET A !CHAR_COLON
    CALL &draw_character
    LOAD [$R_SCORE] ACC
    JUMP_IF_ACC_EQ #0 &draw_score_set_r_char_0
    JUMP_IF_ACC_EQ #1 &draw_score_set_r_char_1
    JUMP_IF_ACC_EQ #2 &draw_score_set_r_char_2
    JUMP_IF_ACC_EQ #3 &draw_score_set_r_char_3
    JUMP_IF_ACC_EQ #4 &draw_score_set_r_char_4
    JUMP_IF_ACC_EQ #5 &draw_score_set_r_char_5

&draw_score_set_r_char_0
    SET A !CHAR_0
    JUMP &draw_score_set_r_char_done

&draw_score_set_r_char_1
    SET A !CHAR_1
    JUMP &draw_score_set_r_char_done

&draw_score_set_r_char_2
    SET A !CHAR_2
    JUMP &draw_score_set_r_char_done

&draw_score_set_r_char_3
    SET A !CHAR_3
    JUMP &draw_score_set_r_char_done

&draw_score_set_r_char_4
    SET A !CHAR_4
    JUMP &draw_score_set_r_char_done

&draw_score_set_r_char_5
    SET A !CHAR_5
    JUMP &draw_score_set_r_char_done

&draw_score_set_r_char_done
    CALL &draw_character

    RETURN


    // Left paddle score
    // SET [!VIDEO_CURSOR_COL] #0
    // SET [!VIDEO_CURSOR_ROW] #0
    // LOAD [$L_PADDLE_COLOUR] C
    // LOAD [$L_SCORE] ACC
    // CALL &draw_score_dots

    // Right paddle score
    // SET [!VIDEO_CURSOR_COL] #11
    // SET [!VIDEO_CURSOR_ROW] #0
    // LOAD [$R_PADDLE_COLOUR] C
    // LOAD [$R_SCORE] ACC
    // CALL &draw_score_dots
    // RETURN

////////////////////////////////////////////////////////////
//
// Draw the score dots
//
// Video cursor should be where first dot will be
// C is colour of dots
// ACC is score
////////////////////////////////////////////////////////////
&draw_score_dots

    // Decr score
    DECR ACC

    // If borrow, done
    JUMP_IF_BORROW &draw_score_dots_done

    // Otherwise Draw l colour dot
    STORE C [!VIDEO_DATA]

    // Inrc cursor col by 2
    INCR [!VIDEO_CURSOR_COL]
    INCR [!VIDEO_CURSOR_COL]

    // Back to loop
    JUMP &draw_score_dots

&draw_score_dots_done
    RETURN

////////////////////////////////////////////////////////////
//
// Draw character
//
// Video cursor should be at the top left pixel of the character
// C is colour of character
// A is the character to draw
//
// Pixels are drawn left to right then top to bottom
////////////////////////////////////////////////////////////
&draw_character

    LOAD [!VIDEO_CURSOR_ROW] B
    CALL &draw_character_column
    CALL &draw_character_column
    CALL &draw_character_column

&draw_character_column
    // set counter to 4
    SET ACC #4

&draw_character_column_loop
    // Pop out msb
    SHIFT_LEFT A

    // If bit is not 1, skip drawing pixel
    JUMP_IF_NOT_CARRY &draw_character_column_loop_incr_cursor

    // Draw the pixel
    STORE C [!VIDEO_DATA]

&draw_character_column_loop_incr_cursor
    // increment cursor row
    INCR [!VIDEO_CURSOR_ROW]

    // decr counter
    DECR ACC

    // If not negative, next iteration of loop
    JUMP_IF_NOT_NEGATIVE_FLAG &draw_character_column_loop

    // Otherwise done
    STORE B [!VIDEO_CURSOR_ROW]
    INCR [!VIDEO_CURSOR_COL]
    RETURN


////////////////////////////////////////////////////////////
//
// Draw a message to whoever scored
//
////////////////////////////////////////////////////////////
&draw_point_scorer
    SET [!VIDEO_CURSOR_COL] #16
    SET [!VIDEO_CURSOR_ROW] #12
    SET C !L_PADDLE_INIT_COLOUR
    SET B !CHAR_1
    LOAD [$WHO_SCORED] ACC
    JUMP_IF_ACC_EQ #1 &draw_point_scorer_draw
    SET C !R_PADDLE_INIT_COLOUR
    SET B !CHAR_2
    
&draw_point_scorer_draw
    COPY B ACC
    COPY ACC X
    SET A !CHAR_P
    CALL &draw_character
    COPY X ACC
    COPY ACC A
    CALL &draw_character

    SET [!VIDEO_CURSOR_COL] #9
    SET [!VIDEO_CURSOR_ROW] #19
    SET A !CHAR_S
    CALL &draw_character
    SET A !CHAR_C
    CALL &draw_character
    SET A !CHAR_O
    CALL &draw_character
    SET A !CHAR_R
    CALL &draw_character
    SET A !CHAR_E
    CALL &draw_character
    SET A !CHAR_EXCLM
    CALL &draw_character

    RETURN


////////////////////////////////////////////////////////////
//
// Transition to playing mode
//
////////////////////////////////////////////////////////////
&set_game_mode_playing
    CALL &init_ball
    CALL &reset_left_paddle_pos
    CALL &reset_right_paddle_pos
    SET [$GAME_MODE] !GAME_MODE_PLAYING
    RETURN


////////////////////////////////////////////////////////////
//
// Transition to point scored mode
//
////////////////////////////////////////////////////////////
&set_game_mode_point_scored
    SET [$POINT_SCORED_COUNTER] #90
    SET [$GAME_MODE] !GAME_MODE_POINT_SCORED

    // Play a small tune
    SET A #0b0111_0000_0111_1111
    SET B #5
    CALL &add_note
    SET A #0b0111_0000_0110_1111
    SET B #5
    CALL &add_note
    SET A #0b0111_0000_0101_1111
    SET B #5
    CALL &add_note
    RETURN


////////////////////////////////////////////////////////////
//
// Update when in point scored mode
//
////////////////////////////////////////////////////////////
&update_point_scored
    DECR [$POINT_SCORED_COUNTER]
    JUMP_IF_NOT_BORROW &update_point_scored_done
    CALL &set_game_mode_playing

&update_point_scored_done
    RETURN

$NEXT_NOTE
$END_NOTE
$NEXT_DURATION
$END_DURATION

$NUM_NOTES

$NOTES #0 #0 #0 #0
$LAST_NOTE
$DURATIONS #0 #0 #0 #0
$LAST_DURATION

$NOTE_TIMER
////////////////////////////////////////////////////////////
//
// Initialise the sound system
//
////////////////////////////////////////////////////////////
&initialise_sound
    // Count the number of notes
    SET ACC $LAST_NOTE
    SUB $NOTES
    INCR ACC
    STORE ACC [$NUM_NOTES]

    // Set next and end note to be the same, at beginning of notes
    SET [$NEXT_NOTE] $NOTES
    SET [$END_NOTE] $NOTES

    // Set next and end duration to be the same, at beginning of durations
    SET [$NEXT_DURATION] $DURATIONS
    SET [$END_DURATION] $DURATIONS

    SET [$NOTE_TIMER] #0

    RETURN

////////////////////////////////////////////////////////////
//
// Update the sound system
//
////////////////////////////////////////////////////////////
&update_sound
    // If timer != 0
    LOAD [$NOTE_TIMER] ACC
    JUMP_IF_EQ_ZERO ACC &update_sound_timer_is_zero
        // Decrement timer
        DECR [$NOTE_TIMER]

        // If timer == 0
        JUMP_IF_NOT_ZERO_FLAG &update_sound_time_left_in_note

            // If next != end
            LOAD [$NEXT_NOTE] ACC
            LOAD [$END_NOTE] A
            JUMP_IF_ACC_EQ A &update_sound_stop_note
                
                // Move on to next note
                CALL &update_sound_move_on_to_next_note
                RETURN

&update_sound_stop_note
            // Else
                // Stop note
                SET [!SOUND_SQUARE] #0
                RETURN

&update_sound_time_left_in_note
        // Else
            // Keep playing note
            RETURN
        
&update_sound_timer_is_zero
    // Else
        // If next != end
        LOAD [$NEXT_NOTE] ACC
        LOAD [$END_NOTE] A
        JUMP_IF_ACC_EQ A &update_sound_nothing_to_do
            
            // Move on to next note
            CALL &update_sound_move_on_to_next_note
            RETURN

&update_sound_nothing_to_do
        // Else
            // Nothing to do
            RETURN

&update_sound_move_on_to_next_note
    // Increment next note, wrapping
    INCR [$NEXT_NOTE]
    SET ACC $NOTES
    ADD [$NUM_NOTES]
    DECR ACC
    LOAD [$NEXT_NOTE] A
    JUMP_IF_ACC_GTE A &update_sound_store_next_note
    SET A $NOTES
&update_sound_store_next_note
    STORE A [$NEXT_NOTE]

    // Increment next duration, wrapping
    INCR [$NEXT_DURATION]
    SET ACC $DURATIONS
    ADD [$NUM_NOTES]
    DECR ACC
    LOAD [$NEXT_DURATION] A
    JUMP_IF_ACC_GTE A &update_sound_store_next_duration
    SET A $DURATIONS
&update_sound_store_next_duration
    STORE A [$NEXT_DURATION]

    // Set volume and pitch
    LOAD [$NEXT_NOTE] ACC
    LOAD [ACC] A
    STORE A [!SOUND_SQUARE]

    // Set the duration counter
    LOAD [$NEXT_DURATION] ACC
    LOAD [ACC] A
    STORE A [$NOTE_TIMER]

    RETURN


////////////////////////////////////////////////////////////
//
// Add a note to play in the system
//
// A is the volume and pitch
// B is the duration in frames
//
////////////////////////////////////////////////////////////
&add_note
    // Increment end note, wrapping
    INCR [$END_NOTE]
    SET ACC $NOTES
    ADD [$NUM_NOTES]
    DECR ACC
    LOAD [$END_NOTE] C
    JUMP_IF_ACC_GTE C &add_note_store_end_note
    SET C $NOTES
&add_note_store_end_note
    STORE C [$END_NOTE]

    // Increment end duration, wrapping
    INCR [$END_DURATION]
    SET ACC $DURATIONS
    ADD [$NUM_NOTES]
    DECR ACC
    LOAD [$END_DURATION] C
    JUMP_IF_ACC_GTE C &add_note_store_end_duration
    SET C $DURATIONS
&add_note_store_end_duration
    STORE C [$END_DURATION]

    // Write into end
    LOAD [$END_NOTE] ACC
    STORE A [ACC]
    LOAD [$END_DURATION] ACC
    STORE B [ACC]

    RETURN