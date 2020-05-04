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

    // Check for snake collision


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





// The snake body positions are held in two arrays for row and column positions.
// The snakes head is always as the beginning (index 0) of the array
// The current length of the snake is held in $CURRENT_SNAKE_LEN



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