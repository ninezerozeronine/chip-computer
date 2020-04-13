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

    // Jump to next part if underflow
    JUMP_IF_UNDERFLOW_FLAG @set_next_snake_pos_new_head

    // Otherwise jump to next loop
    JUMP @set_next_snake_pos_shuffle_loop

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


@update_snake_velocity
    // Get controller direction
    LOAD [$CONTROLLER] ACC

    JUMP_IF_EQ_ACC $CONTROLLER_UP @update_snake_velocity_up
    JUMP_IF_EQ_ACC $CONTROLLER_LEFT @update_snake_velocity_left
    JUMP_IF_EQ_ACC $CONTROLLER_DOWN @update_snake_velocity_down
    JUMP_IF_EQ_ACC $CONTROLLER_RIGHT @update_snake_velocity_right
    RETURN

@update_snake_velocity_up
    SET ACC #1
    STORE ACC [$SNAKE_ROW_VEL]
    SET_ZERO ACC
    STORE ACC [$SNAKE_COL_VEL]
    RETURN

@update_snake_velocity_right
    SET_ZERO ACC
    STORE ACC [$SNAKE_ROW_VEL]
    SET ACC #1
    STORE ACC [$SNAKE_COL_VEL]
    RETURN

@update_snake_velocity_down
    SET ACC #-1
    STORE ACC [$SNAKE_ROW_VEL]
    SET_ZERO ACC
    STORE ACC [$SNAKE_COL_VEL]
    RETURN

@update_snake_velocity_left
    SET_ZERO ACC
    STORE ACC [$SNAKE_ROW_VEL]
    SET ACC #-1
    STORE ACC [$SNAKE_COL_VEL]
    RETURN



@apple_collisions
    // Set A to zero - this is the loop index
    SET_ZERO A

@apple_collisions_loop
    // If loop index equal to next apple index, skip to next loop
    LOAD [$NEXT_APPLE_INDEX] ACC
    JUMP_IF_EQ_ACC A @apple_collisions_next_loop

    // If loop index equal to num apples, we're done
    LOAD [$NUM_APPLES] ACC
    JUMP_IF_EQ_ACC A @apple_collisions_done

    // Add loop index to row array start
    SET ACC $APPLE_ROW_POSNS
    ADD A

    // Load this apples row into ACC
    LOAD [ACC] ACC

    // Load snake head row (at start of array) into B
    LOAD [$SNAKE_ROW_POSNS] B

    // If the rows match, continue
    JUMP_IF_EQ_ACC B @apple_collisions_col_check

    // Otherwise, next loop
    JUMP @apple_collisions_next_loop

@apple_collisions_col_check
    // Add loop index to col array start
    SET ACC $APPLE_COL_POSNS
    ADD A

    // Load this apples col into ACC
    LOAD [ACC] ACC

    // Load snake head col (at start of array) into B
    LOAD [$SNAKE_COL_POSNS] B

    // If the cols match, set flag, exit
    JUMP_IF_EQ_ACC B @apple_collisions_set_collision_flag_exit

    // Otherwise carry on to next loop 

@apple_collisions_next_loop
    // Increment index and loop
    INCR A
    JUMP @apple_collisions_loop

@apple_collisions_done
    RETURN

@apple_collisions_set_collision_flag_exit
    SET ACC #1
    STORE ACC [$COLLISION_CHECK]
    RETURN



@wall_collisions
    // Load head row into A
    LOAD [$SNAKE_ROW_POSNS] A

    // Set flag if head row == 29
    SET ACC #29
    JUMP_IF_EQ_ACC A @wall_collisions_set_flag_exit

    // Set flag if head row == 0
    JUMP_IF_EQ_ZERO A @wall_collisions_set_flag_exit

    // Load head col into A
    LOAD [$SNAKE_COL_POSNS] A

    // Set flag if head col == 39
    SET ACC #39
    JUMP_IF_EQ_ACC A @wall_collisions_set_flag_exit

    // Set flag is head col == 0
    JUMP_IF_EQ_ZERO A @wall_collisions_set_flag_exit

    // No collisions, return
    RETURN

@wall_collisions_set_flag_exit
    SET ACC #1
    STORE ACC [$COLLISION_CHECK]
    RETURN



// @draw_bg
// @draw_apples
// @draw_snake
// 
// set collision flag to 0
// wall collisions
// apple collisions
// 
// if collision
//     game over
// 
// if on_next_apple
//     incr apple index
//     lengthen snake
// 
// @set_next_pos