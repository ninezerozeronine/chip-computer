// The number to count to before running tick 
!tick_max #5

// Start by initialising variables
    LOAD [$tick_count] ACC
    SET_ZERO ACC
    STORE ACC [$tick_count]

    LOAD [$position] ACC
    SET ACC #1
    STORE ACC [$position]

&loop
    LOAD [$tick_count] ACC
    INCR ACC
    JUMP_IF_ACC_GT !tick_max &tick
    STORE ACC [$tick_count]
    JUMP &loop

&tick
    // Reset tick counter and store
    SET_ZERO ACC
    STORE ACC [$tick_count]

    // Load and shift position
    LOAD [$position] A
    LSHIFT A
    STORE A [$position]

    // If the position didn't fall off the end, wait for the next tick
    JUMP_IF_NEQ_ZERO A &loop

    // If it did fall off the end, reset it to the right, then wait for the next tick
    SET A #1
    STORE A [$position]
    JUMP &loop

$tick_count #0
$position #1