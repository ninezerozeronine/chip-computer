@loop
    // If 1/128 of a second has passed - tick the program
    LOAD [$timer] ACC
    AND #0b00100000

    // Loop if 1/128 of a second hasn't passed
    JUMP_IF_EQ_ACC #0b00100000 @loop

    // Otherwise tick
    // Store the current time check pattern for the next loop
    STORE ACC [$last_timecheck]

    // decrement ball counter
    LOAD [$ball_tick_counter] ACC
    DECR ACC

    // If not underflow, go to next check
    JUMP_IF_NOT_UNDERFLOW_FLAG @loop_zones_counter

    // Otherwise call ball update and reset counter
    CALL @update_ball
    SET ACC #12
    STORE ACC [$ball_tick_counter]

    // Also check end condition

@loop_zones_counter
    // decrement zones counter
    LOAD [$zones_tick_counter] ACC
    DECR ACC

    // If not underflow, go to next check
    JUMP_IF_NOT_UNDERFLOW_FLAG @loop_draw_counter

    // Otherwise call ball update and reset counter
    CALL @update_zones
    SET ACC #8
    STORE ACC [$zones_tick_counter]

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








@update_ball
    // Add direction to ball position
    LOAD [$ball_dir] A
    LOAD [$ball_pos] ACC
    ADD A
    STORE ACC [$ball_pos]
    $ball_pos

    // If ball > 39, jump to ball left win
    JUMP_IF_LT_ACC #39 @update_ball_left_win

    // If ball < 0
    COPY ACC A
    SET_ZERO ACC
    ADD A
    JUMP_IF_NEGATIVE_FLAG @update_ball_right_win

    // Otherwise we're done
    RETURN

@update_ball_left_win
    // Set ball to just in front of right zone, heading left
    SET ACC #30
    STORE ACC [$ball_pos]
    SET ACC #-1
    STORE ACC [$ball_dir]
    RETURN

@update_ball_right_win
    // Set ball to just in front of right zone, heading left
    SET ACC #10
    STORE ACC [$ball_pos]
    SET ACC #1
    STORE ACC [$ball_dir]
    RETURN







@update_zones
    // Get left button state
    // A will be non zero if buton pressed
    LOAD [$left_controller] ACC
    AND #0b00100000
    COPY ACC A

    // If the ball isn't in the left zone, skip to end of left
    LOAD [$ball_pos] ACC
    JUMP_IF_LT_ACC #5 @update_zones_end_left

    // Otherwise it is in the left zone. If button isn't pressed, skip to end of left
    JUMP_IF_EQ_ZERO A @update_zones_end_left

    // Otherwise, it is pressed. If it was pressed last time, skip to end of left
    LOAD [$left_zone_pres_state] ACC
    SET B #0b00100000
    JUMP_IF_EQ_ACC B @update_zones_end_left

    // Otherwise return the ball
    SET B #1
    STORE B [$ball_dir]

@update_zones_end_left
    // Store current pressed state in last pressed
    STORE A [$left_zone_press_state]

    // Now update right zone
    // Get right button state
    // A will be non zero if buton pressed
    LOAD [$right_controller] ACC
    AND #0b00100000
    COPY ACC A

    // If the ball isn't in the right zone, skip to end of right
    LOAD [$ball_pos] ACC
    JUMP_IF_GT_ACC #35 @update_zones_end_right

    // Otherwise it is in the right zone. If button isn't pressed, skip to end of right
    JUMP_IF_EQ_ZERO A @update_zones_end_right

    // Otherwise, it is pressed. If it was pressed last time, skip to end of right
    LOAD [$right_zone_press_state] ACC
    SET B #0b00100000
    JUMP_IF_EQ_ACC B @update_zones_end_right

    // Otherwise return the ball
    SET B #-1
    STORE B [$ball_dir]

@update_zones_end_right
    STORE A [$last_right_zone_press_state]
    RETURN










@draw
    // A is current row
    // B is current column
    // C is the pixel colour
    SET_ZERO A
    SET_ZERO B

@draw_next_pixel
    STORE A [$video_row]
    STORE B [$video_col]

    // Set C to bg colour
    SET_ZERO C

    // If in ball column, jump to set ball colour
    LOAD [$ball_pos] ACC
    JUMP_IF_EQ_ACC B @draw_set_ball_colour

    // Otherwise, if not in left zone, jump to right zone check
    COPY B ACC
    JUMP_IF_LT_ACC #5 @draw_right_zone_check

    // Otherwise in left zone
    // If left zone not pressed, jump to set left zone non presse colour
    LOAD [$left_zone_press_state] ACC
    JUMP_IF_EQ_ZERO ACC @draw_set_left_not_pressed_colour

    // Otherwise set left pressed colour, then jump to write pixel
    SET C #0b00110000
    JUMP @draw_write_pixel

@draw_set_left_not_pressed_colour
    SET C #0b00010000
    JUMP @draw_write_pixel

@draw_right_zone_check
    // If not in right zone, jump to write pixel using prev bg colour set
    COPY B ACC
    JUMP_IF_GT_ACC #35 @draw_write_pixel

    // If left zone not pressed, jump to set left zone non presse colour
    LOAD [$right_zone_press_state] ACC
    JUMP_IF_EQ_ZERO ACC @draw_set_right_not_pressed_colour

    // Otherwise set right pressed colour, then jump to write pixel
    SET C #0b00001100
    JUMP @draw_write_pixel

@draw_set_right_not_pressed_colour
    SET C #0b00000100
    JUMP @draw_write_pixel

@draw_set_ball_colour
    SET C #0b00111111

@draw_write_pixel
    STORE C [$video_data]

    // Next column
    INCR B

    // Go to next row if we're past the last column
    SET ACC #39
    JUMP_IF_LT_ACC B @draw_next_row

    // Otherwise draw next pixel
    JUMP @draw_next_pixel

@draw_next_row
    // Increment row
    INCR A

    // Reset column
    SET_ZERO B

    // Continue drawing if we're still in a visible row
    SET ACC #29
    JUMP_IF_LTE_ACC A @draw_next_pixel

    // Otherwise we're done
    // Flip the display buffer
    SET C #0b10000000
    STORE C [$video_data]

    // Return
    RETURN