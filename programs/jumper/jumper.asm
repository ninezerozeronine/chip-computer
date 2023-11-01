!controller_address #0xFFFF
!jump_button #0b0000_0000_0010_0000
!just_pressed
!held
!released



&update_button_state
    // Store controller
    LOAD [!controller_address] C
    COPY C ACC
    AND !jump_button

    // If button is currently pressed, continue, otherwise jump to released
    JUMP_IF_ACC_NEQ !jump_button &ubs_released

    // If the last button state was released, continue, otherwise jump to held
    LOAD [$last_button_state] ACC
    JUMP_IF_ACC_NEQ !released &ubs_held

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

    RETURN