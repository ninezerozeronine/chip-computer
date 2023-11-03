&init
    SET SP #512
    SET_ZERO ACC
    SET_ZERO C
    STORE ACC [$last_button_state]
    STORE ACC [$button_state]
    STORE ACC [$loop_count]


// Constants for main loop
!loop_count_max #4000
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
    INCR C
    CALL &tick

    // Start loop again
    JUMP &main_loop




/////////////////////////////////////////////
&tick
/////////////////////////////////////////////
    CALL &update_button_state

    CALL &update_player_state

    CALL &draw

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
    LOAD [$button_state] B
    
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
    // If the player is beginning a jump, continue, otherwise jump to test if big jump hang 1
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
    // If the player is at big jump 1 continue, otherwise jump to test if at hang 2
    LOAD [$player_state] ACC
    JUMP_IF_ACC_NEQ !ps_big_jump_1 &ups_t_bj2

    // Set player state to big jump 2, no need to set height, already set at 2. Return
    SET ACC !ps_big_jump_2
    STORE ACC [$player_state]
    RETURN

&ups_t_bj2
    // If the player is at big jump 2 continue, otherwise jump to test if at end
    LOAD [$player_state] ACC
    JUMP_IF_ACC_NEQ !ps_big_jump_2 &ups_t_end

    // Set player state to jump end, height to 1. Return
    JUMP &ups_jump_end

&ups_t_end
    // If the player is at jump end continue, otherwise jump to return
    LOAD [$player_state] ACC
    JUMP_IF_ACC_NEQ !ps_jump_end &ups_ret

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




/////////////////////////////////////////////
&draw
/////////////////////////////////////////////
    // If the player height is zero continue, otherwise jump to test if player height is 1
    LOAD [$player_state] ACC
    JUMP_IF_NEQ_ZERO ACC &draw_t1

    // Set C and B to 0, and A to 1
    SET_ZERO C
    SET_ZERO B
    SET A #1
    RETURN

&draw_t1
    // If the player height is 1 continue, otherwise jump to test if player height is 2
    LOAD [$player_state] ACC
    JUMP_IF_ACC_NEQ #1 &draw_t2

    // Set C to zero, B to 1, and A to 0
    SET_ZERO C
    SET B #1
    SET_ZERO A
    RETURN

&draw_t2
    // If the player height is 2 continue, otherwise jump to return
    LOAD [$player_state] ACC
    JUMP_IF_ACC_NEQ #2 &draw_ret

    // Set C to 1, B to 0, and A to 0
    SET B #1
    SET_ZERO B
    SET_ZERO A
    RETURN

&draw_ret
    RETURN