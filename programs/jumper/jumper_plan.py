game_state
    running
    game_over

def tick():
    
    update_button_state()

    update_player_state()

    advance_obstacle()

    check_for_collisions()

    if game_state == game_over:
        update_game_over()

    draw()




last_button_state
button_state
    just_pressed
    held
    released
def update_button_state():
    current_button_state = read_from_controller
    if current_button_state == pressed
        if last_button_state == released
            button_state = just_pressed
        else:
            button_state = held
    else:
        button_state = released
    last_button_state = current_button_state



player_state
    on_floor
    jump_begin
    jump_end
    big_jump_1
    big_jump_2
player_height
    0
    1
    2
def update_player_state():
    if player_state == on_floor:
        if button_state == just_pressed:
            state = jump_begin
            player_height = 1
    elif player_state == jump_begin:
        if button_state == held:
            state = big_jump_hang_1
            player_height = 2
        else:
            state = jump_end
            player_height = 1
    elif player_state == big_jump_hang_1:
        state = big_jump_hang_2
        player_height = 2
    elif player_state == big_jump_hang_2:
        state = jump_end
        player_height = 1
    elif player_state == jump_end:
        state = on_floor
        player_height = 0



obstacle_type
    short
    tall
    gap
obstacle_position
def update_obstacle():
    obstacle_position = move_one_space_left
    if obstacle_position == offscreen:
        obstacle_type = random_type
        obstacle_position = just_off_screen




def check_for_collisions
    if obstacle_position == player_position:
        if obstacle_type == short
            if player_height == 0:
                game_state = game_over
        elif obstacle_type == tall
            if player_height != 2:
                game_state = game_over
        elif obstacle_type == gap
            if player_height != 1:
                game_state = game_over