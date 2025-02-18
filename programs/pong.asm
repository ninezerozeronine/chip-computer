                  // #0b1111_1111_1111_0000
                  // #0b1111_1111_1111_0001
                  // #0b1111_1111_1111_0010
                  // #0b1111_1111_1111_0011
                  // #0b1111_1111_1111_0100
                  // #0b1111_1111_1111_0101
                  // #0b1111_1111_1111_0110
                  // #0b1111_1111_1111_0111
                  // #0b1111_1111_1111_1000
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


!SNES_PAD_UP     #0b0000_0000_0001_0000
!SNES_PAD_DOWN   #0b0000_0000_0010_0000
!SNES_PAD_SELECT #0b0000_0000_0000_0100


!L_PADDLE_INIT_TOP_ROW     #5
!L_PADDLE_INIT_BOTTOM_ROW  #9
!L_PADDLE_INIT_COLUMN      #2
!L_PADDLE_INIT_COLOUR      #0b0000_0000_0011_1111
!L_PADDLE_MOVE_TICKER_INCR #0b0100_0000_0000_0000

!R_PADDLE_INIT_TOP_ROW     #5
!R_PADDLE_INIT_BOTTOM_ROW  #9
!R_PADDLE_INIT_COLUMN      #18
!R_PADDLE_INIT_COLOUR      #0b0000_0000_0011_1111
!R_PADDLE_MOVE_TICKER_INCR #0b0100_0000_0000_0000

!PADDLE_HIGHEST_ROW        #0
!PADDLE_LOWEST_ROW         #14


!BALL_INIT_ROW                  #7
!BALL_INIT_COLUMN               #9
!BALL_INIT_COLOUR               #0b0000_0000_0011_0000
!BALL_HORIZ_MOVE_TICKER_INCR    #0b0100_0000_0000_0000
!BALL_VERT_MOVE_TICKER_INCR     #0b0001_0000_0000_0000


!PF_INIT_TOP_LEFT_COLUMN #3
!PF_INIT_TOP_RIGHT_COLUMN #16
!PF_INIT_TOP_ROW #2
!PF_INIT_TOP_COLOUR #0b0000_0000_0000_0011

!PF_INIT_BOTTOM_LEFT_COLUMN #3
!PF_INIT_BOTTOM_RIGHT_COLUMN #16
!PF_INIT_BOTTOM_ROW #12
!PF_INIT_BOTTOM_COLOUR #0b0000_0000_0000_0011


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
    CALL &update_left_paddle
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
    CALL &check_select
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
    SET [$BALL_VERT_DIR] #1
    SET [$BALL_VERT_MOVE_TICKER] #0
    SET [$BALL_VERT_MOVE_TICKER_INCR] !BALL_VERT_MOVE_TICKER_INCR

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
    JUMP_IF_NOT_CARRY &update_ball_up_down

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
    CALL &ball_paddle_hit_update_vert_speed_and_dir

    RETURN
    
&update_ball_moving_right_no_collision
    STORE ACC [$BALL_COLUMN]
    RETURN

&update_ball_moving_left
    // If the pos plus speed is greater than the left paddle column, it's fine
    LOAD [$BALL_COLUMN] ACC
    DECR ACC
    JUMP_IF_ACC_GT [$L_PADDLE_COLUMN] &update_ball_moving_left_no_collision

    // Otherwise we need to resolve the collision - have it bounce off the paddle
    ADD #2
    STORE ACC [$BALL_COLUMN]

    // Reverse direction
    SET [$BALL_HORIZ_DIR] #1

    // Update ball vertical speed and dir
    CALL &ball_paddle_hit_update_vert_speed_and_dir

    RETURN

&update_ball_moving_left_no_collision
    STORE ACC [$BALL_COLUMN]
    RETURN

&update_ball_right_paddle_miss
    RETURN

&update_ball_up_down

    // See if it's time to move the ball vertically
    LOAD [$BALL_VERT_MOVE_TICKER] ACC
    ADD [$BALL_VERT_MOVE_TICKER_INCR]
    STORE ACC [$BALL_VERT_MOVE_TICKER]
    JUMP_IF_NOT_CARRY &update_ball_up_down_done

    // Check if the ball isn't moving up or down - if so - no need for vertical checks
    LOAD [$BALL_VERT_DIR] ACC
    JUMP_IF_ACC_EQ #0 &update_ball_up_down_done

    // Check if the ball is moving down - i.e. vert dir is 1
    JUMP_IF_ACC_EQ #1 &update_ball_moving_down
    
    // Otherwise we're moving up
    // Calculate new position
    DECR [$BALL_ROW]
    LOAD [$BALL_ROW] ACC

    // Check we haven't collided with the barrier
    JUMP_IF_ACC_GT [$PF_TOP_ROW] &update_ball_up_down_done

    // Otherwise we've collided

    // Update the position
    ADD #2
    STORE ACC [$BALL_ROW]

    // Flip direction (so we're moving down)
    SET [$BALL_VERT_DIR] #1

    // Done
    RETURN

&update_ball_moving_down

    // Calculate new position
    INCR [$BALL_ROW]
    LOAD [$BALL_ROW] ACC

    // Check we haven't collided with the barrier
    JUMP_IF_ACC_LT [$PF_BOTTOM_ROW] &update_ball_up_down_done

    // Otherwise we've collided

    // Update the position
    SUB #2
    STORE ACC [$BALL_ROW]

    // Flip direction (so we're moving up)
    SET [$BALL_VERT_DIR] #-1

    // Done
    RETURN

&update_ball_up_down_done
    RETURN


////////////////////////////////////////////////////////////
//
// Resolve ball vertical motion on paddle collision
//
////////////////////////////////////////////////////////////
&ball_paddle_hit_update_vert_speed_and_dir
    RETURN
    // If paddle stationary

        // No vertical change necessary

    // If paddle up

        // If ball up

            // Incr vert incr

            // Clamp vert incr

        // If ball down

            // Decr vert incr

                // If ticker is zero

                    // Set vert dir to zero

                // If ticker is negative

                    // Clamp to zero

                    // Set vert dir to zero
        
        // If ball horiz

            // Incr vert incr

            // Set vert dir up
        
    // If paddle down

        // If ball down

            // Incr vert incr

            // Clamp vert incr
        
        // If ball up

            // Decr vert incr

                // If incr is zero

                    // Set virt dir to zero

                // If incr is negative

                    // Clamp to zero

                    // Set vert dir to zero

        // If ball horiz

            // Incr vert incr

            // Set vert dir down

    // Update the vertical update ticker
    LOAD [$BALL_VERT_MOVE_TICKER_INCR] ACC
    ADD [L_PADDLE_VERT_TICKER_DIFF]
    STORE ACC [$BALL_VERT_MOVE_TICKER_INCR]

    JUMP_IF_ZERO_FLAG &update_ball_collide_stationary_paddle
    JUMP_IF_NEGATIVE_FLAG &update_ball_collide_stationary_paddle

    RETURN









////////////////////////////////////////////////////////////
//
// Draw ball
//
////////////////////////////////////////////////////////////
&draw_ball
    LOAD [$BALL_ROW] ACC
    STORE ACC [!VIDEO_CURSOR_ROW]

    LOAD [$BALL_COLUMN] ACC
    STORE ACC [!VIDEO_CURSOR_COL]

    LOAD [$BALL_COLOUR] ACC
    STORE ACC [!VIDEO_DATA]
    RETURN


$L_PADDLE_COLUMN
$L_PADDLE_TOP_ROW
$L_PADDLE_BOTTOM_ROW
$L_PADDLE_MOVE_TICKER
$L_PADDLE_MOVE_TICKER_INCR
$L_PADDLE_VERT_DIR
$L_PADDLE_COLOUR
////////////////////////////////////////////////////////////
//
// Initialise left_paddle
//
////////////////////////////////////////////////////////////
&init_left_paddle
    SET [$L_PADDLE_COLUMN] !L_PADDLE_INIT_COLUMN
    SET [$L_PADDLE_TOP_ROW] !L_PADDLE_INIT_TOP_ROW
    SET [$L_PADDLE_BOTTOM_ROW] !L_PADDLE_INIT_BOTTOM_ROW
    SET [$L_PADDLE_MOVE_TICKER] #0
    SET [$L_PADDLE_MOVE_TICKER_INCR] !L_PADDLE_MOVE_TICKER_INCR
    SET [$L_PADDLE_VERT_DIR] #0
    SET [$L_PADDLE_COLOUR] !L_PADDLE_INIT_COLOUR
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
    RETURN

////////////////////////////////////////////////////////////
//
// Update right paddle
//
////////////////////////////////////////////////////////////
&update_right_paddle
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













