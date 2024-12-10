from micropython import const

DATA = const(
(
        (0, 71),         # Line: 0013     SET A #1
        (1, 1),          # Line: 0013
        (2, 72),         # Line: 0014     SET B #1
        (3, 1),          # Line: 0014
        (4, 51),         # Line: 0015     STORE A [!status_word_addr]
        (5, 65530),      # Line: 0015
        (6, 8),          # Line: 0018     COPY A ACC
        (7, 202),        # Line: 0019     ADD B
        (8, 119),        # Line: 0020     JUMP_IF_ACC_GT #1597 &set_initial
        (9, 1597),       # Line: 0020
        (10, 0),         # Line: 0020
        (11, 51),        # Line: 0021     STORE A [!status_word_addr] // To display
        (12, 65530),     # Line: 0021
        (13, 12),        # Line: 0022     COPY B A
        (14, 2),         # Line: 0023     COPY ACC B
        (15, 84),        # Line: 0024     JUMP &fib_loop
        (16, 6),         # Line: 0024
    )
)