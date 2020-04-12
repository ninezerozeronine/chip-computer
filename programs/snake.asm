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
$SNAKE_HEAD_OFFSET
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
    // Copy current head offset into A. A is now the current snake offset.
    LOAD [$SNAKE_HEAD_OFFSET] A

    // Copy current snake len into B. B is now remaining snake len
    LOAD [$CURR_SNAKE_LEN] B

@draw_snake_loop
    // Decrement remaining length
    DECR B

    // If there's no more snake to draw, we're done
    JUMP_IF_UNDERFLOW_FLAG @draw_snake_done

    // Otherwise, add the current snake offset to the start of the row position array
    SET ACC $SNAKE_ROW_POSNS
    ADD A

    // Set the video row
    STORE ACC [$VIDEO_ROW]

    // Add the current snake offset to the start of the column position array
    SET ACC $SNAKE_COL_POSNS
    ADD A

    // Set the video column
    STORE ACC [$VIDEO_COL]

    // Draw snake
    LOAD [$SNAKE_COLOUR] ACC
    STORE ACC [$VIDEO_DATA]

    // Decrement snake offset
    DECR C
    JUMP_IF_NOT_UNDERFLOW_FLAG @draw_snake_loop

    // Wrap snake offset
    LOAD [$MAX_SNAKE_LEN] A
    DECR A
    JUMP @draw_snake_loop

@draw_snake_done
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
    JUMP @draw_apples_draw_pixel 

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
    // Increment snake head offset
    LOAD [$SNAKE_HEAD_OFFSET] ACC

    // Store current offset in B
    COPY ACC B

    // Add one
    INCR ACC

    // Load the max len
    LOAD [$MAX_SNAKE_LEN] A

    // If offset is less than the max length, jump to set the next pos
    JUMP_IF_LT_ACC A @set_next_snake_pos_add_vel

    // Otherwise loop the head offset
    SET_ZERO ACC

@set_next_snake_pos_add_vel
    // Store the new offset in C
    COPY ACC C

    //
    // Update Row
    //
    // Set ACC to the address of the start of the row position array
    SET ACC $SNAKE_ROW_POSNS

    // Add current offset to the start
    ADD B

    // Load curent row into ACC
    LOAD [ACC] ACC

    // Load row vel into A
    LOAD [$SNAKE_ROW_VEL] A

    // Add vel to current row, store in A
    ADD A
    COPY ACC A

    // Set ACC to the address of the start of the row position array
    SET ACC $SNAKE_ROW_POSNS

    // Add new offset to the start
    ADD C

    // Store the updated row in the new slot
    STORE A [ACC]

    //
    // Update Col
    //
    // Set ACC to the address of the start of the col position array
    SET ACC $SNAKE_COL_POSNS

    // Add current offset to the start
    ADD B

    // Load curent col into ACC
    LOAD [ACC] ACC

    // Load col vel into A
    LOAD [$SNAKE_COL_VEL] A

    // Add vel to current col, store in A
    ADD A
    COPY ACC A

    // Set ACC to the address of the start of the col position array
    SET ACC $SNAKE_COL_POSNS

    // Add new offset to the start
    ADD C

    // Store the updated col in the new slot
    STORE A [ACC]

    // Done
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










// @apple_collisions
//     // Set A to zero - this is the loop index
//     SET_ZERO A
// 
// @apple_collisions_loop
//     // If loop index equal to next apple index, skip to next loop
//     LOAD [$NEXT_APPLE_INDEX] ACC
//     JUMP_IF_EQ_ACC A @apple_collisions_next_loop
// 
//     // If loop index equal to num apples, we're done
//     LOAD [$NUM_APPLES] ACC
//     JUMP_IF_EQ_ACC A @apple_collisions_done
// 
// @apple_collisions_check
// 
// 
// 
//     // Add loop index to row array start
//     SET ACC $APPLE_ROW_POSNS
//     ADD A
// 
//     // Load this apples row into ACC
//     LOAD [ACC] ACC
// 
//     // Load snake row into B
//     LOAD [$SNAKE_ROW]
//     STORE B [$VIDEO_ROW]
// 
//     // Add loop index to row array start
//     SET ACC $APPLE_COL_POSNS
//     ADD A
// 
//     // Set the video row position
//     LOAD [ACC] B
//     STORE B [$VIDEO_COL]
// 
//     // Store the previously set colour in C
//     STORE C [$VIDEO_DATA]
// 
//     // Increment loop index
//     INCR A
// 
//     // Back to top of loop
//     JUMP @draw_apples_loop
// 
// @apple_collisions_next_loop
//     // Increment index and loop
//     INCR A
//     JUMP @check_apple_collisions_loop
// 
// @apple_collisions_done
//     RETURN




// @draw_bg
// @draw_apples
// @draw_snake
// 
// if collision
//     game over
// 
// if on_next_apple
//     incr apple index
//     lengthen snake
// 
// @set_next_pos