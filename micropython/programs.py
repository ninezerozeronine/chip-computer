"""
Programs that can be loaded into the computer
"""

PROGRAMS = (
    {
        "name":"Dum1",
        "content": (
            (0, 0),
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
        )
    },
    {
        "name":"Dum2",
        "content": (
            (0, 5),
            (1, 4),
            (2, 3),
            (3, 2),
            (4, 1),
            (1234, 1234),
        )
    },
    {
        "name":"Fibb",
        "content": (
            (0, 113),        # Line: 0016     SET SP #1
            (1, 1),          # Line: 0016
            (2, 110),        # Line: 0017     SET A #1
            (3, 1),          # Line: 0017
            (4, 43),         # Line: 0020     COPY SP ACC
            (5, 0),          # Line: 0021     ADD A
            (6, 161),        # Line: 0022     JUMP_IF_ACC_GT #1597 &set_initial
            (7, 1597),       # Line: 0022
            (8, 0),          # Line: 0022
            (9, 29),         # Line: 0023     COPY A SP
            (10, 22),        # Line: 0024     COPY ACC A
            (11, 125),       # Line: 0025     JUMP &fib_loop
            (12, 4),         # Line: 0025
        )
    }
)