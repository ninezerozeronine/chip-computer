&init
    SET SP #512
    SET_ZERO ACC
    SET_ZERO C
    STORE ACC [$last_button_state]
    STORE ACC [$button_state]
    STORE ACC [$loop_count]

!loop_count_max #4000
$loop_count
&main_loop
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

&tick
    CALL &update_button_state
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

&update_button_state
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