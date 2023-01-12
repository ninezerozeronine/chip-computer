{
    "name":"XXXX",
    "content": (
        (0, 110),        # Line: 0002     SET A #1
        (1, 1),          # Line: 0002
        (2, 111),        # Line: 0003     SET B #1
        (3, 1),          # Line: 0003
        (4, 112),        # Line: 0004     SET C #1
        (5, 1),          # Line: 0004
        (6, 26),         # Line: 0007     COPY A ACC
        (7, 1),          # Line: 0008     ADD B
        (8, 161),        # Line: 0009     JUMP_IF_ACC_GT #1597 &set_initial
        (9, 1597),       # Line: 0009
        (10, 0),         # Line: 0009
        (11, 24),        # Line: 0010     COPY ACC C // To display
        (12, 31),        # Line: 0011     COPY B A
        (13, 23),        # Line: 0012     COPY ACC B
        (14, 125),       # Line: 0013     JUMP &fib_loop
        (15, 6),         # Line: 0013
    )
}