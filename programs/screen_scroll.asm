!video_status #65531
!cursor_row #65532
!cursor_col #65533
!video_data #65534

// Init
    // Set res to 160 x 120
    SET ACC #0b0000_0000_0000_0000
    STORE ACC [!video_status]

    // Set row and col to 0
    SET_ZERO ACC
    STORE ACC [!cursor_row]
    STORE ACC [!cursor_col]

    // Set C to be where the cursor column is
    SET C !cursor_col

    // Set A to be where the video data is
    SET A !video_data

&init_pixel_loop
    // Set column to 0
    SET_ZERO ACC
    STORE ACC [C]

    // Store the value of the pixel in col 0 in B
    LOAD [A] B

    // Set current column to 159
    SET ACC #159
    STORE ACC [!cursor_col]

&pixel_loop
    // current pix to tmp
    LOAD [A] ACC

    // put last pix in current
    STORE B [A]

    // tmp to last pix
    COPY ACC B

    // decr column
    DECR [C]

    // If column is not zero, back to pixel loop, else run through
    // to last pixel
    JUMP_IF_NOT_ZERO_FLAG &pixel_loop

    // put last pix in current
    STORE B [A]    

    // Run through to wait for vblank

&wait_for_vblank
    // Grab status

    // If vblank

        // Switch bank

        // Init pixel loop

    // Else
        
        // Wait for vblank