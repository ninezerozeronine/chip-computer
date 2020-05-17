ball always has a position and row/col direction
on update:
try_new_pos
if new row pos is blocked
    flip row dir (v bounce)
    -> try_new_pos
if new col pos is blocked
    flip col dir (h bounce)
    -> try_new_pos
if row and column blocked
    flip row and column dir (corner bounce)
    -> try_new_pos
move into new pos