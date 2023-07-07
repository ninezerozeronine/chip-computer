// Stack looks something like:
// 100 ...
// 99  Top left column
// 98  Top left row
// 97  Bottom right column
// 96  Bottom right row
// 95  Return Address        <-- Stack pointer

// Find mid point of line

    // Find mid point of column
        // Put the smaller/left column value in X
        COPY SP ACC
        SUB #4
        LOAD [ACC] X

        // Put the larger/right column value in Y
        COPY SP ACC
        SUB #2
        LOAD [ACC] Y

        // Subtract the left from the right to find the column span
        COPY Y ACC
        SUB X

        // Divide the span by 2
        RSHIFT ACC

        // Add the span to the left column to find the mid point
        ADD X
        STORE ACC [$MID_COLUMN]

    // Find mid point of row
        // Put the smaller/top row value in X
        COPY SP ACC
        SUB #3
        LOAD [ACC] X

        // Put the larger/bottom row value in Y
        COPY SP ACC
        SUB #1
        LOAD [ACC] Y

        // Subtract the top from the bottom to find the row span
        COPY Y ACC
        SUB X

        // Divide the span by 2
        RSHIFT ACC

        // Add the span to the top row to find the mid point
        ADD X
        STORE ACC [$MID_ROW]

// Check if mid point is one of the original points

    

@notsamerow





