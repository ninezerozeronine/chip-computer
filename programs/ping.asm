// ball always has a position and row/col direction
// on update:
// try_new_pos
// if new row pos is blocked
//     flip row dir (v bounce)
//     -> try_new_pos
// if new col pos is blocked
//     flip col dir (h bounce)
//     -> try_new_pos
// if row and column blocked
//     flip row and column dir (corner bounce)
//     -> try_new_pos
// move into new pos
// 
// 
// 
// paddle has a position and velocity
// paddle speed can spin the ball and affect it's direction.


$ball_row_dir
$ball_col_dir

$ball_row_pos
$ball_col_pos

$ball_proposed_row
$ball_proposed_col

$ball_pos_check_res



// paddle posns are in an array:
// 
// left_paddle_start
// left_paddle_end
// right_paddle_start
// right_paddle_end
//
// This ends up taking more instruction bytes than direct memory ref loads because of the incrs :(








@check_proposed_ball_pos
    // Sets ACC to 0 if there's no collision, 1 if there is.
    // Assumes:
    // - A contains the proposed row
    // - B contains the proposed column

    // Check if in left paddle
    // Skip to next check if col is not zero
    COPY B ACC
    JUMP_IF_LT_ACC #0 @check_proposed_ball_pos_right_paddle

    // Otherwise check if in the paddle
    LOAD [$left_paddle_start] ACC

    // Skip if pos is less than min
    JUMP_IF_LT_ACC A @check_proposed_ball_pos_right_paddle

    // Otherwise skip if more than max
    LOAD [$left_paddle_end] ACC
    JUMP_IF_GT_ACC A @check_proposed_ball_pos_right_paddle

    // Otherwise it's colliding
    JUMP @check_proposed_ball_pos_collision


@check_proposed_ball_pos_right_paddle
    // Check if in in right paddle
    // If col == 39
    // Skip to next check if col is not 39
    COPY B ACC
    JUMP_IF_GT_ACC #39 @check_proposed_ball_pos_below_floor

    // Otherwise check if in the paddle
    LOAD [$right_paddle_start] ACC

    // Skip if pos is less than min
    JUMP_IF_LT_ACC A @check_proposed_ball_pos_below_floor

    // Otherwise skip if more than max
    LOAD [$right_paddle_end] ACC
    JUMP_IF_GT_ACC A @check_proposed_ball_pos_below_floor

    // Otherwise it's colliding
    JUMP @check_proposed_ball_pos_collision


@check_proposed_ball_pos_below_floor
    // Below floor (< 0)
    COPY A ACC
    DECR ACC

    // Skip if above the floor
    JUMP_IF_NEGATIVE_FLAG @check_proposed_ball_pos_above_ceiling

    // Otherwise its below the floor - return collision
    JUMP @check_proposed_ball_pos_collision

@check_proposed_ball_pos_above_ceiling
    // Above ceiling (> 29)
    COPY A ACC

    // Skip if below ceiling
    JUMP_IF_LTE_ACC #29 @check_proposed_ball_pos_no_collision

    // Otherwise its above ceiling - return collision
    JUMP @check_proposed_ball_pos_collision

@check_proposed_ball_pos_no_collision
    SET_ZERO ACC
    RETURN

@check_proposed_ball_pos_collision
    SET ACC #1
    RETURN













@update_ball
    // Calculate new ball pos for row change
    CALL @calc_new_row
    LOAD [$ball_col_pos] B

    // Check the new row pos
    CALL @check_proposed_ball_pos

    // If there's no collision, move on to checking the ball pos for the column
    JUMP_IF_EQ_ZERO ACC @update_ball_col_check

    // Otherwise flip the row dir and try again
    CALL @flip_row_dir
    JUMP @update_ball

@update_ball_col_check  
    // Calculate new ball pos for col change
    CALL @calc_new_col
    LOAD [$ball_row_pos] A

    // Check the new row pos
    CALL @check_proposed_ball_pos

    // If there's no collision, move on to checking the ball pos for the column and row together
    JUMP_IF_EQ_ZERO ACC @update_ball_row_col_check

    // Otherwise flip the col dir and try again
    CALL @flip_col_dir
    JUMP @update_ball

@update_ball_row_col_check
    // Calculate new row and column position together
    CALL @calc_new_row
    CALL @calc_new_col

    // Check the new pos
    CALL @check_proposed_ball_pos

    // If there's no collision, update the position
    JUMP_IF_EQ_ZERO ACC @update_ball_update_pos

    // Otherwise flip row and column and try again
    CALL @flip_row_dir
    CALL @flip_col_dir
    JUMP @update_ball

@update_ball_update_pos
    STORE A [$ball_row_pos]
    STORE B [$ball_col_pos]
    RETURN

@calc_new_row
    // Puts the proposed row in A
    LOAD [$ball_row_pos] ACC
    LOAD [$ball_row_dir] A
    ADD A
    COPY ACC A
    RETURN

@calc_new_col
    // Puts the proposed col in B
    LOAD [$ball_col_pos] ACC
    LOAD [$ball_col_dir] A
    ADD A
    COPY ACC B
    RETURN

@flip_row_dir
    SET_ZERO ACC
    LOAD [$ball_row_dir] A
    SUB A
    STORE ACC [$ball_row_dir]
    RETURN

@flip_col_dir
    SET_ZERO ACC
    LOAD [$ball_col_dir] A
    SUB A
    STORE ACC [$ball_col_dir]
    RETURN





@update_paddles
    // Copy left controller and paddles to sideless vars
    LOAD [$left_controller] A
    LOAD [$left_paddle_start] B
    LOAD [$left_paddle_end] C

    // Call sideless move
    CALL @update_paddle

    // Copy sideless vars back to left
    STORE B [$left_paddle_start]
    STORE C [$left_paddle_end]

    // Copy right controller and paddles to sideless vars
    LOAD [$right_controller] A
    LOAD [$right_paddle_start] B
    LOAD [$right_paddle_end] C

    // Call sideless move
    CALL @update_paddle

    // Copy sideless vars back to right
    STORE B [$right_paddle_start]
    STORE C [$right_paddle_end]

@update_paddle
    // A = controller value
    // B = paddle start
    // C = paddle end
    // If up is pressed
    COPY A ACC
    AND #0b00001000
    JUMP_IF_EQ_ACC #0b00001000 @update_paddle_up

    // If down is pressed
    COPY A ACC
    AND #0b00000100
    JUMP_IF_EQ_ACC A @update_paddle_down

    // Otherwise don't move
    RETURN

@update_paddle_up
    // Decrease row by one
    COPY B ACC
    DECR ACC

    // Skip to invalid if now negative
    JUMP_IF_NEGATIVE_FLAG @update_paddle_invalid_move

    // Otherwise update start and end
    COPY ACC B
    DECR C
    RETURN

@update_paddle_down
    // Increase row by one
    COPY C ACC
    INCR ACC

    // Skip to invalid move if end of paddle now > 39
    JUMP_IF_LT_ACC #39 @update_paddle_invalid_move

    // Otherwise update start and end
    COPY ACC C
    INCR B
    RETURN

@update_paddle_invalid_move
    RETURN










@draw
    // A is current row
    // B is current column
    SET_ZERO A
    SET_ZERO B

@draw_draw_bg_pixel
    STORE A [$video_row]
    STORE B [$video_col]
    SET_ZERO ACC
    STORE ACC [$video_data]

    // Next column
    INCR B

    // Go to next row if we're past the last column
    SET ACC #39
    JUMP_IF_LT_ACC B @draw_next_row

    // Otherwise draw next pixel
    JUMP @draw_draw_bg_pixel

@draw_next_row
    // Increment row
    INCR A

    // Finish bg if we're past the last row
    SET ACC #29
    JUMP_IF_LT_ACC B @draw_draw_ball

    // Otherwise start drawing next row
    JUMP @draw_draw_bg_pixel

@draw_draw_ball
    LOAD [$ball_row_pos] ACC
    STORE ACC [$video_row]
    LOAD [$ball_col_pos] ACC
    STORE ACC [$video_col]
    SET ACC #0b00110000
    STORE ACC [$video_data]












@loop
    // If 1/128 of a second has passed - tick the program
    LOAD [$timer] ACC
    AND #0b00100000

    // Loop if 1/128 of a second hasn't passed
    JUMP_IF_EQ_ACC A @loop

    // Otherwise tick
    // Store the current time check pattern for the next loop
    STORE ACC [$last_timecheck]

    // decrement ball counter
    LOAD [$ball_tick_counter] ACC
    DECR ACC

    // If not underflow, go to next check
    JUMP_IF_NOT_UNDERFLOW_FLAG @loop_paddles_counter

    // Otherwise call ball update and reset counter
    CALL @update_ball
    SET ACC #12
    STORE ACC [$ball_tick_counter]

    // Also check end condition

@loop_paddles_counter
    // decrement paddles counter
    LOAD [$paddle_tick_counter] ACC
    DECR ACC

    // If not underflow, go to next check
    JUMP_IF_NOT_UNDERFLOW_FLAG @loop_draw_counter

    // Otherwise call ball update and reset counter
    CALL @update_paddles
    SET ACC #8
    STORE ACC [$paddle_tick_counter]

@loop_draw_counter
    // decrement draw counter
    LOAD [$draw_tick_counter] ACC
    DECR ACC

    // If not underflow, go to next check
    JUMP_IF_NOT_UNDERFLOW_FLAG @loop_end_of_loop

    // Otherwise call ball update and reset counter
    CALL @draw
    SET ACC #20
    STORE ACC [$draw_tick_counter]

@loop_end_of_loop
    // Go back to start of loop
    LOAD [$last_timecheck] A
    JUMP @loop