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




@check_proposed_ball_pos
    // Sets ACC to 0 if there's no collision, 1 if there is.

    // Check if in left paddle
    // Skip to next check if col is not zero
    LOAD [$ball_proposed_col] ACC
    JUMP_IF_LT_ACC #0 @check_proposed_ball_pos_right_paddle

    // Otherwise check if in the paddle
    LOAD [$left_paddle_start] ACC
    LOAD [$ball_proposed_row] A

    // Skip if pos is less than min
    JUMP_IF_LT_ACC A @check_proposed_ball_pos_right_paddle

    // Otherwise skip if more than max
    LOAD [$left_paddle_end] ACC
    JUMP_IF_GT_ACC A @check_proposed_ball_pos_right_paddle

    // Otherwise it's colliding
    JUMP @check_proposed_ball_pos_collision


@check_proposed_ball_pos_right_paddle
    // Check if in In right paddle
    // If col == 39
    // Skip to next check if col is not 39
    LOAD [$ball_proposed_col] ACC
    JUMP_IF_GT_ACC #39 @check_proposed_ball_pos_below_floor

    // Otherwise check if in the paddle
    LOAD [$right_paddle_start] ACC
    LOAD [$ball_proposed_row] A

    // Skip if pos is less than min
    JUMP_IF_LT_ACC A @check_proposed_ball_pos_below_floor

    // Otherwise skip if more than max
    LOAD [$right_paddle_end] ACC
    JUMP_IF_GT_ACC A @check_proposed_ball_pos_below_floor

    // Otherwise it's colliding
    JUMP @check_proposed_ball_pos_collision


@check_proposed_ball_pos_below_floor
    // Below floor (< 0)
    LOAD [$ball_proposed_row] ACC
    DECR ACC

    // Skip if above the floor
    JUMP_IF_NEGATIVE_FLAG @check_proposed_ball_pos_above_ceiling

    // Otherwise its below the floor - return collision
    JUMP @check_proposed_ball_pos_collision

@check_proposed_ball_pos_above_ceiling
    // Above ceiling (> 29)
    LOAD [$ball_proposed_row] ACC

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
    LOAD [$ball_col_pos] ACC
    STORE ACC [$ball_proposed_col]

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
    LOAD [$ball_row_pos] ACC
    STORE ACC [$ball_proposed_row]

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
    LOAD [$ball_proposed_row] ACC
    STORE ACC [$ball_row_pos]
    LOAD [$ball_proposed_col] ACC
    STORE ACC [$ball_col_pos]
    RETURN

@calc_new_row
    LOAD [$ball_row_pos] ACC
    LOAD [$ball_row_dir] A
    ADD A
    STORE A [$ball_proposed_row]
    RETURN

@calc_new_col
    LOAD [$ball_col_pos] ACC
    LOAD [$ball_col_dir] A
    ADD A
    STORE A [$ball_proposed_col]
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


@move_paddles
    // Copy left controller and paddles to sideless vars
    LOAD [$left_controller] A
    LOAD [$left_paddle_start] B
    LOAD [$left_paddle_end] C

    // Call sideless move
    CALL @move_paddle

    // Copy sideless vars back to left
    STORE B [$left_paddle_start]
    STORE C [$left_paddle_end]

    // Copy right controller and paddles to sideless vars
    LOAD [$right_controller] A
    LOAD [$right_paddle_start] B
    LOAD [$right_paddle_end] C

    // Call sideless move
    CALL @move_paddle

    // Copy sideless vars back to right
    STORE B [$right_paddle_start]
    STORE C [$right_paddle_end]

@move_paddle
    // A = controller value
    // B = paddle start
    // C = paddle end
    // If up is pressed
    COPY A ACC
    AND #0b00001000
    JUMP_IF_EQ_ACC #0b00001000 @move_paddle_up

    // If down is pressed
    COPY A ACC
    AND #0b00000100
    JUMP_IF_EQ_ACC A @move_paddle_down

    // Otherwise don't move
    RETURN

@move_paddle_up
    // Decrease row by one
    COPY B ACC
    DECR ACC

    // Skip to invalid if now negative
    JUMP_IF_NEGATIVE_FLAG @move_paddle_invalid_move

    // Otherwise update start and end
    COPY ACC B
    DECR C
    RETURN

@move_paddle_down
    // Increase row by one
    COPY C ACC
    INCR ACC

    // Skip to invalid move if end of paddle now > 39
    JUMP_IF_LT_ACC #39 @move_paddle_invalid_move

    // Otherwise update start and end
    COPY ACC C
    INCR B
    RETURN

@move_paddle_invalid_move
    RETURN


@loop
    // If it's been 1/128 of a second
