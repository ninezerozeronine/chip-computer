$VIDEO_ROW
$VIDEO_COLUMN
$VIDEO_DATA

$BG_COL
$WALL_COL

$SNAKE_ROW_VEL
$SNAKE_COL_VEL
$SNAKE_ROW_POSNS
$SNAKE_COL_POSNS
$CURR_SNAKE_LEN
$MAX_SNAKE_LEN
$SNAKE_COLOUR

$APPLE_COL_POSNS
$APPLE_ROW_POSNS
$NUM_APPLES
$CURR_APPLE_INDEX
$APPLE_EATEN_COLOUR
$APPLE_NEXT_COLOUR
$APPLE_TO_EAT_COLOUR

$CONTROLLER
$CONTROLLER_UP
$CONTROLLER_RIGHT
$CONTROLLER_DOWN
$CONTROLLER_LEFT

$COLLISION_CHECK







// This is basically a double for loop.
// We use A as the current row, and B as the current column.
// It also checks if the snake has collided with the wall. If it has, it
// Sets the collision check flag and returns early.


@draw_bg
    SET_ZERO A
    SET_ZERO B
    STORE A [$VIDEO_ROW]

@draw_bg_next_column
    // Set column in video coords
    STORE B [$VIDEO_COLUMN]

    // Draw wall if row == 0
    JUMP_IF_EQ_ZERO A @draw_bg_draw_wall

    // Draw wall if col == 0
    JUMP_IF_EQ_ZERO B @draw_bg_draw_wall

    // Draw wall if row == 29
    SET ACC #29
    JUMP_IF_EQ_ACC A @draw_bg_draw_wall

    // Draw wall if col == 39
    SET ACC #39
    JUMP_IF_EQ_ACC B @draw_bg_draw_wall

    // If we didnt jump, draw bg col
    LOAD [$BG_COL] ACC
    STORE ACC [$VIDEO_DATA]
    JUMP @draw_bg_incr_column

@draw_bg_draw_wall
    // Store the wall colour in video data
    LOAD [$WALL_COL] ACC
    STORE ACC [$VIDEO_DATA]

    // Check for snake collision
    COPY A ACC
    LOAD [$SNAKE_ROW_POSNS] C
    JUMP_IF_EQ_ACC C @draw_bg_check_snake_column
    JUMP @draw_bg_incr_column

@draw_bg_check_snake_column
    COPY B ACC
    LOAD [$SNAKE_COL_POSNS] C
    JUMP_IF_EQ_ACC C @draw_bg_snake_wall_collision
    JUMP @draw_bg_incr_column

@draw_bg_snake_wall_collision
    SET ACC #1
    STORE ACC [$COLLISION_CHECK]
    RETURN

@draw_bg_incr_column
    // Increment column
    INCR B

    // If we're past the last column, jump to next row
    SET ACC #39
    JUMP_IF_GT_ACC B @draw_bg_next_row

    // Go to next pixel
    JUMP @draw_bg_next_column

@draw_bg_next_row
    // Increment row
    INCR A

    // If we're past the last row, jump to done
    SET ACC #29
    JUMP_IF_GT_ACC A @draw_bg_done

    // Set row in video coords
    STORE A [$VIDEO_ROW]

    // Reset column
    SET_ZERO B

    // Go to next pixel
    JUMP @draw_bg_next_column

@draw_bg_done
    RETURN




@draw_snake
    SET_ZERO A

@draw_snake_loop
    // Set ACC to start of snake row posns
    SET ACC $SNAKE_ROW_POSNS

    // Add the loop index
    ADD A

    // Load the row posn into ACC
    LOAD [ACC] ACC

    // Store in video row coord
    STORE ACC [$VIDEO_ROW]

    // Set ACC to start of snake col posns
    SET ACC $SNAKE_COL_POSNS

    // Add the loop index
    ADD A

    // Load the col posn into ACC
    LOAD [ACC] ACC

    // Store in video col coord
    STORE ACC [$VIDEO_COL]

    // Set ACC to the colour
    SET ACC $SNAKE_COL

    // Write pixel
    STORE ACC [$VIDEO_DATA]

    // Increment loop count
    INCR A

    // Set ACC to snake len
    SET ACC $CURRENT_SNAKE_LEN

    // Jump to top of loop if less than snake len
    JUMP_IF_LT_ACC A @draw_snake_loop

    // Otherwise we're done
    RETURN



@draw_apples
    // Set A to zero - this is the loop index
    SET_ZERO A

@draw_apples_loop
    // If loop index greater than or equal to next apple index, skip to next check
    LOAD [$NEXT_APPLE_INDEX] ACC
    JUMP_IF_GTE_ACC A @draw_apple_next_check

    // Otherwise set eaten colour and draw pixel
    SET C $APPLE_EATEN_COLOUR
    JUMP @draw_apples_draw_pixel

@draw_apple_next_check
    // If loop index greater than next apple index, skip to next check
    JUMP_IF_GT_ACC A @draw_apple_to_eat_check

    // Otherwise set next colour and draw pixel
    SET C $APPLE_NEXT_COLOUR
    JUMP @draw_apples_draw_pixel

@draw_apple_to_eat_check
    // If loop index equal to num apples, we're done
    LOAD [$NUM_APPLES] ACC
    JUMP_IF_EQ_ACC A @draw_apples_done

    // Otherwise set to eat colour and draw pixel
    SET C $APPLE_TO_EAT_COLOUR

@draw_apples_draw_pixel
    // Add loop index to row array start
    SET ACC $APPLE_ROW_POSNS
    ADD A

    // Set the video row position
    LOAD [ACC] B
    STORE B [$VIDEO_ROW]

    // Add loop index to col array start
    SET ACC $APPLE_COL_POSNS
    ADD A

    // Set the video col position
    LOAD [ACC] B
    STORE B [$VIDEO_COL]

    // Store the previously set colour in C
    STORE C [$VIDEO_DATA]

    // Increment loop index
    INCR A

    // Back to top of loop
    JUMP @draw_apples_loop

@draw_apples_done
    RETURN









@check_eating_apple
    // Get the index in memory of the nex apples row posn in ACC
    SET ACC $APPLE_ROW_POSNS
    LOAD [$NEXT_APPLE_INDEX] A
    ADD A

    // Load this apples row into ACC
    LOAD [ACC] ACC

    // Load snake head row (at start of array) into B
    LOAD [$SNAKE_ROW_POSNS] B    

    // If the rows match, continue
    JUMP_IF_EQ_ACC B @check_eating_apple_col_check

    // Otherwise, we're not on the apple
    RETURN

@check_eating_apple_col_check
    // Get the index in memory of the nex apples col posn in ACC
    SET ACC $APPLE_COL_POSNS
    LOAD [$NEXT_APPLE_INDEX] A
    ADD A

    // Load this apples col into ACC
    LOAD [ACC] ACC

    // Load snake head row (at start of array) into B
    LOAD [$SNAKE_COL_POSNS] B   

    // If the column matches, we're eating the next apple
    JUMP_IF_EQ_ACC B @check_eating_apple_success

    // Otherwise, we're not on the apple
    RETURN

@check_eating_apple_success
    // Subtract (num apples - 1) from next apple index
    LOAD [$NEXT_APPLE_INDEX] ACC
    LOAD [$NUM_APPLES] A
    DECR A
    SUB A

    // If zero/just ate the last apple, game win!
    JUMP_IF_ZERO_FLAG @check_eating_apple_game_win

    // Otherwise, just ate an apple. Increase snake len
    LOAD [$CURR_SNAKE_LEN] ACC
    INCR ACC
    STORE ACC [$CURR_SNAKE_LEN]

    // Increment next apple
    LOAD [$NEXT_APPLE_INDEX] ACC
    INCR ACC
    STORE ACC [$NEXT_APPLE_INDEX]

    // Done
    RETURN

@check_eating_apple_game_win
    // Set win flag
    SET ACC #1
    STORE ACC [$GAME_WIN_FLAG]

    // Done
    RETURN










// The snake body position is held in two arrays for row and column positions.
// The snakes head is always as the beginning (index 0) of the array
// The maximum length of the snake is held in $MAX_SNAKE_LEN
//
// When setting the next snake position, all the existing positions are first
// copied down one.
// e.g. lets say the array starts at index 20, and the snake row positions are
// 6, 5, 4, 3, 2, and the max snake len is 5. This shows the data after the
// copy down:
//
// 19  X -> X
// 20  6 -> 6
// 21  5 -> 6
// 22  4 -> 5
// 23  3 -> 4
// 24  2 -> 3
// 25  X -> X
// 
// The shuffle starts at end of the array -1 and works it's way back to the start.


@set_next_snake_pos
    LOAD [$MAX_SNAKE_LEN] A
    DECR A
    DECR A

@set_next_snake_pos_shuffle_loop
    // Load row pos address into ACC
    SET ACC $SNAKE_ROW_POSNS

    // Add offset
    ADD A

    // Load row into B
    LOAD [ACC] B

    // Add one to address
    INCR ACC

    // Store B in new addr
    STORE B [ACC]

    // Load col pos address into ACC
    SET ACC $SNAKE_COL_POSNS

    // Add offset
    ADD A

    // Load row into B
    LOAD [ACC] B

    // Add one to address
    INCR ACC

    // Store B in new addr
    STORE B [ACC]

    // Decrement counter
    DECR A

    // Jump to setting new head if underflow/all positions have been copied down
    JUMP_IF_UNDERFLOW_FLAG @set_next_snake_pos_new_head

    // Otherwise jump to next loop
    JUMP @set_next_snake_pos_shuffle_loop

// Once all the positions have been shuffled down, the old head position is retrieved
// and the velocity added to it.

@set_next_snake_pos_new_head
    // Load row pos address into ACC
    SET ACC $SNAKE_ROW_POSNS

    // Add one
    INCR ACC

    // Load old head row pos into ACC
    LOAD [ACC] ACC

    // Load row vel into A
    LOAD [$SNAKE_ROW_VEL] A

    // Add vel to position
    ADD A

    // Store updated row position
    STORE ACC [$SNAKE_ROW_POSNS]

    // Load col pos address into ACC
    SET ACC $SNAKE_COL_POSNS

    // Add one
    INCR ACC

    // Load old head col pos into ACC
    LOAD [ACC] ACC

    // Load col vel into A
    LOAD [$SNAKE_COL_VEL] A

    // Add vel to position
    ADD A

    // Store updated col position
    STORE ACC [$SNAKE_COL_POSNS]

    RETURN