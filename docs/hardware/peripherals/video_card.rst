.. _video_card:

Video Card
==========

The screen is a rectangular grid of square pixels made up of horizontal rows and vertical columns. The top left pixel is row 0, column 0.

64 colours are supported, 2 bits each for red, green and blue. The 6 least significant bits of the word contain the colour in the order RRGGBB. E.g.: ``010011`` is 25% strength red, 0% strength green, and 100% strength blue.

There are 4 supported resolutions:

* 20 x 15
* 40 x 30
* 80 x 60
* 160 x 120

Frames are drawn at 60 fps.

There are 2 frame buffers, when one is being accessed by the CPU, the other is being drawn.

Control of the video card is via 4 words in memory:

* Status
* Cursor Column
* Cursor Row
* Data

Status
------

The 8 least significant bits of the status word are used.

Bits 0-2 are read only and provide a running count of the number of frames, wrapping back to 0 after the 7th frame. The count increments when vblank goes from high to low - i.e. the start of the frame.

Bits 3 and 4 are read and write and select the resolution:

* ``xxx1_1xxx``: 20 x 15
* ``xxx1_0xxx``: 40 x 30
* ``xxx0_1xxx``: 80 x 60
* ``xxx0_0xxx``: 160 x 120

Bit 5 is read and write and selects the active buffer.

Bits 6 and 7 are read only and provide the state of the Horizontal blanking and Vertical blanking control lines respectively.

Cursor Column
-------------

The index of the column of the cursor. Can be read from and written to.

Cursor Row
----------

The index of the row of the cursor. Can be read from and written to.

Data
----

The value of the pixel pointed at by the cursor in the buffer currently being accessed by the CPU.