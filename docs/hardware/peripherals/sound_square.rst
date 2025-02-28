.. _sound_square:

Sound Square
============

The sound square card provides two mono voices that operate independently.

Control of each voice is achieved by writing to the address the voice is located at.

The 4 most signifcant bits of the word ontrol volume. 0 is off, 15 is max volume.

The 12 least significant bits control the pitch - higher number give a lower pitch.
