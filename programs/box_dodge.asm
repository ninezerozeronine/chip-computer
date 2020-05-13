//
//
//
//
// DONT FORGET TO: 
// Change the player collision checks to JUMP_IF_NEQ_ACCs
// Update the checks against the controller to proper values
// Make a jump if not negative flag
// Double check rown and column check maths/way around for player and boxes
//
//


// This function needs to keep track of a few things:
// * Current box index (C)
// * Width progress
// * Height progress (B)
// * Resultant row
// * Resultant column

// box_index = num_boxes - 1
// while box_index > 0
//     box_row_counter = box_widths[box_index]
//     while box_row_counter > 0
//         pixel_row = box_rows[box_index] + box_row_counter
//         if pixel_row >= 0 and pixel_row < 30
//             box_column_counter = box_heights[box_index]
//             while box_column_counter > 0
//                 pixel_column = box_columns[box_index] + box_column_counter
//                 if pixel_column >= 0 and pixel_column < 40
//                     video_row = pixel_row
//                     video_column = pixel_column
//                     video_data = box_colours[box_index]
//                     if pixel_row == player_row and pixel_column == player_column
//                         $player_dead = 1
//                 box_column_counter -= 1
//         box_row_counter -= 1
//     box_index -= 1






@draw_boxes
    SET_ZERO A
    STORE A [$player_collision]
    LOAD [$num_boxes] C
            
@draw_boxes_box_loop
    // Decrement box index and jump to done if all boxes drawn (result negative)
    DECR C
    JUMP_IF_NEGATIVE_FLAG @draw_boxes_done

    // Index into box widths array
    SET ACC $box_widths
    ADD C

    // Load this box's width into ACC, then store in the row counter
    LOAD [ACC] ACC
    STORE ACC [$box_row_counter]

@draw_boxes_box_row_loop
    // Decrement box_row_counter and jump to next box if all rows drawn (result negative)
    LOAD [$box_row_counter] A
    DECR A
    JUMP_IF_NEGATIVE_FLAG @draw_boxes_box_loop

    // Otherwise store new row counter
    STORE A [$box_row_counter]

    // Index into box rows array
    SET ACC $box_rows
    ADD C

    // Load this boxs row into ACC
    LOAD [ACC] ACC

    // Add the row offset (ACC will contains pixel row)
    LOAD [$box_row_counter] A
    ADD A

    // Jump to next row if row < 0
    JUMP_IF_LT_ACC #0 @draw_boxes_box_row_loop

    // Otherwise Jump to next row if row >= 30
    JUMP_IF_GTE_ACC #30 @draw_boxes_box_row_loop

    // Otherwise store the pixel row
    STORE ACC [$pixel_row]

    // Index into box heights array 
    SET ACC $box_heights
    ADD C

    // Load this boxs column into B (B will contain this box's height, and is the column counter)
    LOAD [ACC] B

@draw_boxes_column_loop
    // Decrement box column counter, jump to next row if all columns in this row finished (result negative)
    DECR B
    JUMP_IF_NEGATIVE_FLAG @draw_boxes_box_row_loop

    // Index into box columns array
    SET ACC $box_columns
    ADD C

    // Load this box's column into ACC
    LOAD [ACC] ACC

    // Add the column counter (ACC will contain the pixel column)
    ADD B
    STORE ACC [$column_counter]

    // Jump to next pixel in the row if column < 0
    JUMP_IF_LT_ACC #0 @draw_boxes_column_loop

    // Otherwise jump to next pixel in the row if column >= 40
    JUMP_IF_GTE_ACC #40 @draw_boxes_column_loop

    // Otherwise set video coords to pixel
    LOAD [$pixel_row] A
    STORE A [$video_row]
    STORE ACC [$video_column]

    // Index into box colours array
    SET ACC $box_colours
    ADD C

    // Load this box's colour into ACC
    LOAD [ACC] ACC
    STORE ACC [$video_data]

    // Jump to next pixel in the row if player not in same row
    LOAD [$pixel_row] ACC
    LOAD [$player_row] A
    JUMP_IF_EQ_ACC A @draw_boxes_column_loop

    // Otherwise Jump to next pixel in the row if player not in same column
    LOAD [$column_counter] ACC
    LOAD [$player_column] A
    JUMP_IF_EQ_ACC A @draw_boxes_column_loop

    // Otherwise set player collision flag
    SET A #1
    STORE A [$player_collision]

    // Go to the next pixel in this row
    JUMP @draw_boxes_column_loop

@draw_boxes_done
    RETURN







@move_player
    // Get controller direction
    LOAD [$controller] ACC

    JUMP_IF_EQ_ACC $CONTROLLER_UP @move_player_up
    JUMP_IF_EQ_ACC $CONTROLLER_LEFT @move_player_right
    JUMP_IF_EQ_ACC $CONTROLLER_DOWN @move_player_down
    JUMP_IF_EQ_ACC $CONTROLLER_RIGHT @move_player_left
    RETURN

@move_player_up
    LOAD [$player_row] ACC
    DECR ACC
    JUMP_IF_NEGATIVE_FLAG @move_player_done
    STORE ACC [$player_row]
    RETURN

@move_player_right
    LOAD [$player_column] ACC
    INCR ACC
    JUMP_IF_GTE_ACC #40 @move_player_done
    STORE ACC [$player_column]
    RETURN

@move_player_down
    LOAD [$player_row] ACC
    DECR ACC
    JUMP_IF_GTE_ACC #30 @move_player_done
    STORE ACC [$player_row]
    RETURN

@move_player_left
    LOAD [$player_column] ACC
    DECR ACC
    JUMP_IF_NEGATIVE_FLAG @move_player_done
    STORE ACC [$player_column]
    RETURN

@move_player_done
    RETURN










@move_boxes
    // Initialise the box index (C will contain the current box index)
    LOAD [$num_boxes] C
            
@move_boxes_box_loop
    // Decrement box index and jump to done if all boxes moved (result negative)
    DECR C
    JUMP_IF_NEGATIVE_FLAG @move_boxes_done

    // Index into box counters array (ACC will contain box counter addr)
    SET ACC $box_move_counters
    ADD C

    // Get this boxes counter
    LOAD [ACC] A

    // Decrement the box update counter
    DECR A
    STORE A [ACC]
    JUMP_IF_EQ_ZERO A @move_boxes_update_box

    // Otherwise go to next box
    JUMP @move_boxes_box_loop

@move_boxes_update_box
    // Index into box counter maxes (ACC will contain current box counter max addr)
    SET ACC $box_move_counter_maxes
    ADD C

    // Load this boxes max counter
    LOAD [ACC] A

    // Index into box counters array (ACC will contain current box counter addr)
    SET ACC $box_move_counters
    ADD C

    // Reset this boxes counter
    STORE A [ACC]

    // Index into row_speed (ACC will contain current box row speed addr)
    SET ACC $box_row_speeds
    ADD C

    // Get current row speed (A will contain current box row speed)
    LOAD [ACC] A

    // Index into box_row_positions (B will contain current box row position addr)
    SET ACC $box_row_positions
    ADD C
    COPY ACC B

    // Add row speed to position, and store it (ACC will contain new row position)
    LOAD [B] ACC
    ADD A
    STORE ACC [B]

    // Jump to less than max check if new pos is greater than min (>= -10)
    JUMP_IF_LTE_ACC #-10 @move_boxes_row_pos_less_than_max_check

    // Otherwise reset position
    SET ACC #40
    STORE ACC [B]
    JUMP @move_boxes_update_box_column

@move_boxes_row_pos_less_than_max_check
    // Jump to update columns if row pos is less than max (ACC still contains new row position)
    JUMP_IF_GTE_ACC #40 @move_boxes_update_box_column

    // Otherwise reset position
    SET ACC #-10
    STORE ACC [B]

    // Then continue

@move_boxes_update_box_column
    // Index into column_speeds (ACC will contain current box column speed addr)
    SET ACC $box_column_speeds
    ADD C

    // Get current column speed (A will contain current box column speed)
    LOAD [ACC] A

    // Index into box_column_positions (B will contain current box column position addr)
    SET ACC $box_column_positions
    ADD C
    COPY ACC B

    // Add column speed to position, and store it (ACC will contain new column position)
    LOAD [B] ACC
    ADD A
    STORE ACC [B]

    // Jump to less than max check if new column pos is greater than min (>= -10)
    JUMP_IF_LTE_ACC #-10 @move_boxes_column_pos_less_than_max_check

    // Otherwise reset position, go to next box
    SET ACC #50
    STORE ACC [B]
    JUMP @move_boxes_box_loop

@move_boxes_column_pos_less_than_max_check
    // Jump to next box if row pos is less than max (ACC still contains new row position)
    JUMP_IF_GTE_ACC #50 @move_boxes_box_loop

    // Otherwise reset position
    SET ACC #-10
    STORE ACC [B]



@move_boxes_done
    RETURN



// Things left to do
// Update on tick only
// Reset player if collision
// Colour player if win




