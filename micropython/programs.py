"""
Programs that can be loaded into the computer
"""

from micropython import const

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
)