//
//
//
//
// DONT FORGET TO CHANGE THE PLAYER COLLISION CHECKS TO JUMP_IF_NEQ_ACCs!
//
//
//
//


// This function needs to keep track of a few things:
// * Current box index 
// * Width progress
// * Height progress (B)
// * Resultant row
// * Resultant column (C)

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
    LOAD [$num_boxes] A
    STORE A [$box_index]
            
@draw_boxes_box_loop
    // Decrement box index and jump to done if all boxes drawn (result negative)
    LOAD [$box_index] A
    DECR A
    JUMP_IF_NEGATIVE_FLAG @draw_boxes_done

    // Store new box index
    STORE A [$box_index]

    // Index into box widths array
    SET ACC $box_widths
    ADD A

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
    LOAD [$box_index] A
    ADD A

    // Load this boxs row into ACC
    LOAD [ACC] ACC

    // Add the row offset (ACC will contains pixel row)
    LOAD [$box_row_counter] A
    ADD A

    // Jump to next row if row < 0
    SET_ZERO A
    JUMP_IF_LT_ACC A @draw_boxes_box_row_loop

    // Otherwise Jump to next row if row >= 30
    SET A #30
    JUMP_IF_GTE_ACC A @draw_boxes_box_row_loop

    // Otherwise store the pixel row
    STORE ACC [$pixel_row]

    // Index into box heights array 
    SET ACC $box_heights
    LOAD [$box_index] A
    ADD A

    // Load this boxs column into B (B will contain this box's height, and is the column counter)
    LOAD [ACC] B

@draw_boxes_column_loop
    // Decrement box column counter, jump to next row if all columns in this row finished (result negative)
    DECR B
    JUMP_IF_NEGATIVE_FLAG @draw_boxes_box_row_loop

    // Index into box columns array
    SET ACC $box_columns
    LOAD [$box_index] A
    ADD A

    // Load this box's column into ACC
    LOAD [ACC] ACC

    // Add the column counter (ACC will contain the pixel column)
    ADD B
    COPY ACC C

    // Jump to next pixel in the row if column < 0
    SET_ZERO A
    JUMP_IF_LT_ACC A @draw_boxes_column_loop

    // Otherwise jump to next pixel in the row if column >= 40
    SET A #40
    JUMP_IF_GTE_ACC A @draw_boxes_column_loop

    // Otherwise set video coords to pixel
    LOAD [$pixel_row] A
    STORE A [$video_row]
    STORE ACC [$video_column]

    // Index into box columns array
    SET ACC $box_colours
    LOAD [$box_index] A
    ADD A

    // Load this box's colour into ACC
    LOAD [ACC] ACC
    STORE ACC [$video_data]

    // Jump to next pixel in the row if player not in same row
    LOAD [$pixel_row] ACC
    LOAD [$player_row] A
    JUMP_IF_EQ_ACC A @draw_boxes_column_loop

    // Otherwise Jump to next pixel in the row if player not in same column
    COPY C ACC
    LOAD [$player_column] A
    JUMP_IF_EQ_ACC A @draw_boxes_column_loop

    // Otherwise set player collision flag
    SET A #1
    STORE A [$player_collision]

    // Go to the next pixel in this row
    JUMP @draw_boxes_column_loop


@draw_boxes_done
    RETURN
