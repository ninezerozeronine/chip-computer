&init
    SET SP #512
    SET_ZERO ACC
    SET_ZERO C
    STORE ACC [$last_button_state]
    STORE ACC [$button_state]
    STORE ACC [$loop_count]

    // Player variables
    STORE ACC [$player_height]
    SET ACC !ps_on_floor
    STORE ACC [$player_state]

    // Obstacle variables
    SET ACC #1
    STORE ACC [$obstacle_position]
    SET ACC !ot_short
    STORE ACC [$obstacle_type]

    // Game state
    SET ACC !gs_playing
    STORE ACC [$game_state]

    // Position of the player
    !player_position #0b0010_0000_0000_0000


// Constants for main loop
!loop_count_max #5000
$loop_count

/////////////////////////////////////////////
&main_loop
/////////////////////////////////////////////
    LOAD [$loop_count] ACC
    INCR ACC
    STORE ACC [$loop_count]

    // If the loop count is less than max, rerun the loop
    JUMP_IF_ACC_LT !loop_count_max &main_loop

    // Otherwise
    // Reset count
    SET_ZERO ACC
    STORE ACC [$loop_count]
    
    // Run the tick
    CALL &tick

    // Start loop again
    JUMP &main_loop


$tick_indicator

/////////////////////////////////////////////
&tick
/////////////////////////////////////////////

    CALL &update_game_state

    // If game state is playing, continue, otherwise return
    LOAD [$game_state] ACC
    JUMP_IF_ACC_NEQ !gs_playing &tick_return

    CALL &update_button_state

    CALL &update_player_state

    CALL &update_obstacle

    CALL &draw

    CALL &collision_check

    RETURN

&tick_return
    CALL &draw
    RETURN


// Game state
$game_state
!gs_playing #0
!gs_game_over #1

$remaining_game_over_ticks
!max_game_over_ticks #20

/////////////////////////////////////////////
&update_game_state
/////////////////////////////////////////////

    // If game state is game over, continue, otherwise return
    LOAD [$game_state] ACC
    JUMP_IF_ACC_NEQ !gs_game_over &ugs_return

    // Decrement remaining ticks by one
    LOAD [$remaining_game_over_ticks] ACC
    DECR ACC
    STORE ACC [$remaining_game_over_ticks]

    // If ticks is not zero, return, otherwise continue
    JUMP_IF_NOT_ZERO_FLAG &ugs_return

    // Restart the game
    CALL &start_game
    RETURN

&ugs_return
    RETURN




/////////////////////////////////////////////
&start_game
/////////////////////////////////////////////
    // Set the game state to playing
    SET ACC !gs_playing
    STORE ACC [$game_state]

    // Set obstacle pos to 1
    SET ACC #1
    STORE ACC [$obstacle_position]

    // Set player state to on ground
    SET ACC !ps_on_floor
    STORE ACC [$player_state]

    // Set player height to 0
    SET_ZERO ACC
    STORE ACC [$player_height]

    RETURN



// Constants for controller
!controller_address #0xFFFF
!jump_button #0b0000_0000_0000_0001
!released #0
!just_pressed #1
!held #2

// Variables for controller
$button_state
$last_button_state

/////////////////////////////////////////////
&update_button_state
/////////////////////////////////////////////
    // Get controller state
    LOAD [!controller_address] ACC

    // Isolate button press
    AND !jump_button

    // Store button press for later
    COPY ACC A

    // If button is currently pressed, continue, otherwise jump to released
    JUMP_IF_ACC_NEQ !jump_button &ubs_released

    // If the last button state was released, continue, otherwise jump to held
    LOAD [$last_button_state] ACC
    JUMP_IF_ACC_NEQ !released &ubs_held

    // Set the button state to just prssed, then update last state
    SET ACC !just_pressed
    STORE ACC [$button_state]
    JUMP &ubs_update_last_state

&ubs_held
    SET ACC !held
    STORE ACC [$button_state]
    JUMP &ubs_update_last_state

&ubs_released
    SET ACC !released
    STORE ACC [$button_state]

&ubs_update_last_state
    STORE A [$last_button_state]
    
    RETURN





// Player state constants
!ps_on_floor #0
!ps_jump_begin #1
!ps_jump_end #2
!ps_big_jump_1 #3
!ps_big_jump_2 #4

// Player state variables
$player_state
$player_height

/////////////////////////////////////////////
&update_player_state
/////////////////////////////////////////////

    // If the player is on the floor continue, otherwise jump to test if jump begin
    LOAD [$player_state] ACC
    JUMP_IF_ACC_NEQ !ps_on_floor &ups_t_jb

    // If the button was just pressed, continue, otherwise jump to return
    LOAD [$button_state] ACC
    JUMP_IF_ACC_NEQ !just_pressed &ups_ret

    // Set state and player height, then return
    SET ACC !ps_jump_begin
    STORE ACC [$player_state]
    SET ACC #1
    STORE ACC [$player_height]
    RETURN

&ups_t_jb
    // If the player is beginning a jump, continue, otherwise jump to test if big jump  1
    LOAD [$player_state] ACC
    JUMP_IF_ACC_NEQ !ps_jump_begin &ups_t_bj1

    // If the button is held, continue, otherwise jump to jump end
    LOAD [$button_state] ACC
    JUMP_IF_ACC_NEQ !held &ups_jump_end

    // Set state and height, return
    SET ACC !ps_big_jump_1
    STORE ACC [$player_state]
    SET ACC #2
    STORE ACC [$player_height]
    RETURN

&ups_t_bj1
    // If the player is at big jump 1 continue, otherwise jump to test if at big jump 2
    LOAD [$player_state] ACC
    JUMP_IF_ACC_NEQ !ps_big_jump_1 &ups_t_bj2

    // Set player state to big jump 2, set height to 2. Return
    SET ACC !ps_big_jump_2
    STORE ACC [$player_state]
    SET ACC #2
    STORE ACC [$player_height]
    RETURN

&ups_t_bj2
    // If the player is at big jump 2 continue, otherwise jump to test if at end
    LOAD [$player_state] ACC
    JUMP_IF_ACC_NEQ !ps_big_jump_2 &ups_t_end

    // Set player state to jump end, height to 1. Return
    JUMP &ups_jump_end

&ups_t_end
    // If the player is at jump end continue, otherwise jump to unknown condition
    LOAD [$player_state] ACC
    JUMP_IF_ACC_NEQ !ps_jump_end &ups_unknown

    // Set player state to on floor, height to 0. Return
    SET ACC !ps_on_floor
    STORE ACC [$player_state]
    SET_ZERO ACC
    STORE ACC [$player_height]
    RETURN

&ups_jump_end
    // Set player state to jump end, height to 1. Return
    SET ACC !ps_jump_end
    STORE ACC [$player_state]
    SET ACC #1
    STORE ACC [$player_height]
    RETURN

&ups_ret
    RETURN

&ups_unknown
    // Set player state to on floor, height to 0. Return
    SET ACC !ps_on_floor
    STORE ACC [$player_state]
    SET_ZERO ACC
    STORE ACC [$player_height]
    RETURN


/////////////////////////////////////////////
&draw
/////////////////////////////////////////////
    LOAD [$player_height] ACC

    // If the player height is zero continue, otherwise jump to test if player height is 1
    JUMP_IF_NEQ_ZERO ACC &draw_player_t1

    // Set C and B to 0, and A to player pos
    SET_ZERO C
    SET_ZERO B
    SET A !player_position
    JUMP &draw_obstacle

&draw_player_t1
    // If the player height is 1 continue, otherwise jump to test if player height is 2
    JUMP_IF_ACC_NEQ #1 &draw_player_t2

    // Set C to zero, B to player pos, and A to 0
    SET_ZERO C
    SET B !player_position
    SET_ZERO A
    JUMP &draw_obstacle

&draw_player_t2
    // If the player height is 2 continue, otherwise jump to return
    JUMP_IF_ACC_NEQ #2 &draw_obstacle

    // Set C to player pos, B to 0, and A to 0
    SET C !player_position
    SET_ZERO B
    SET_ZERO A

&draw_obstacle
    LOAD [$obstacle_type] ACC
    // If obstacle_type is short, continue otherwise jump to test if tall
    JUMP_IF_ACC_NEQ !ot_short &draw_obstacle_t_tall

    COPY A ACC
    OR [$obstacle_position]
    COPY ACC A
    JUMP &draw_game_over

    // If obstacle_type is tall, continue otherwise jump to test if gap
&draw_obstacle_t_tall
    JUMP_IF_ACC_NEQ !ot_tall &draw_obstacle_t_gap

    COPY A ACC
    OR [$obstacle_position]
    COPY ACC A
    COPY B ACC
    OR [$obstacle_position]
    COPY ACC B
    JUMP &draw_game_over

    // If obstacle_type is gap, continue otherwise jump to draw game over
&draw_obstacle_t_gap
    JUMP_IF_ACC_NEQ !ot_gap &draw_game_over
    COPY A ACC
    OR [$obstacle_position]
    COPY ACC A
    COPY C ACC
    OR [$obstacle_position]
    COPY ACC C

&draw_game_over
    // If the game state is game over, continue, otherwise return
    LOAD [$game_state] ACC
    JUMP_IF_ACC_NEQ !gs_game_over &draw_ret

    // Invert the display
    NOT A
    NOT B
    NOT C

    RETURN

&draw_ret
    RETURN



$obstacle_position
$obstacle_type
!ot_short #0
!ot_tall #1
!ot_gap #2

/////////////////////////////////////////////
&update_obstacle
/////////////////////////////////////////////

    // Move the obstacle one place to the left, wrapping at the end
    LOAD [$obstacle_position] ACC
    ROT_LEFT ACC
    STORE ACC [$obstacle_position]

    // If we didn't wrap, continue, otherwise return
    JUMP_IF_NOT_CARRYBORROW_FLAG &uo_ret

    // Update obstacle_type
    LOAD [$obstacle_type] ACC
    DECR ACC
    STORE ACC [$obstacle_type]

    // If the type wrapped, continue, otherwise return
    JUMP_IF_CARRYBORROW_FLAG &uo_ret

    // Set the type to the highest number
    SET ACC #2
    STORE ACC [$obstacle_type]

&uo_ret
    RETURN




/////////////////////////////////////////////
&collision_check
/////////////////////////////////////////////

    // If the obstacle and player are in the same position
    // continue, otherwise return
    LOAD [$obstacle_position] ACC
    JUMP_IF_ACC_NEQ !player_position &cc_ret

    // If it's a short obstacle, continue, otherwise test if tall
    LOAD [$obstacle_type] ACC
    JUMP_IF_ACC_NEQ !ot_short &cc_test_tall

    // If the player height is 0, continue, otherwise return
    LOAD [$player_height] ACC
    JUMP_IF_NEQ_ZERO ACC &cc_ret

    // Hit short obstacle - game over!
    JUMP &cc_game_over

&cc_test_tall
    // If it's a tall obstacle, continue, otherwise test if gap
    JUMP_IF_ACC_NEQ !ot_tall &cc_test_gap

    // If the player height is 2, jump to return, otherwise continue
    LOAD [$player_height] ACC
    JUMP_IF_ACC_EQ #2 &cc_ret

    // Hit tall obstacle - game over!
    JUMP &cc_game_over

&cc_test_gap
    // If it's a gap obstacle, continue, otherwise return
    JUMP_IF_ACC_NEQ !ot_gap &cc_ret

    // If the player height is 1, jump to return, otherwise continue
    LOAD [$player_height] ACC
    JUMP_IF_ACC_EQ #1 &cc_ret

    // Hit gap obstacle - game over!
    // Continue execution

&cc_game_over
    // Game over
    SET ACC !gs_game_over
    STORE ACC [$game_state]
    SET ACC !max_game_over_ticks
    STORE ACC [$remaining_game_over_ticks]
    RETURN

&cc_ret
    RETURN



























