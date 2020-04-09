$VIDEO_ROW
$VIDEO_COLUMN
$VIDEO_DATA

@draw_bg
    SET_ZERO A
    SET_ZERO B
    STORE A [$VIDEO_ROW]
    STORE B [$VIDEO_COLUMN]

@draw_bg_next_pixel
    // Store the colour in video data
    STORE C [$VIDEO_DATA]

    // Increment column
    INCR B

    // If we're past the last column, jump to next row
    SET ACC #40
    JUMP_IF_GT_ACC B @draw_bg_next_row

    // Set new column in video coords
    STORE B [$VIDEO_COLUMN]

    // Go to next pixel
    JUMP @draw_bg_next_pixel


@draw_bg_next_row
    // Increment row
    INCR A

    // If we're past the last row, jump to done
    SET ACC #30
    JUMP_IF_GT_ACC A @draw_bg_done

    // Set row in video coords
    STORE A [$VIDEO_ROW]

    // Reset column
    SET_ZERO B

    // Set column in video coords
    STORE B [$VIDEO_COLUMN]

    // Go to next pixel
    JUMP @draw_bg_next_pixel


@draw_bg_done
    RETURN
