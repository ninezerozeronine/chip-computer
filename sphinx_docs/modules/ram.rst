RAM
===

The RAM provides 256 bytes of program memory (instruction bytes) and 256
bytes of data memory (global variables and the stack).

Interface and Operation
-----------------------

This is the interface of the RAM:

.. image:: images/ram/ram_block.png

This is how it operates:

+----------------------+-----------+-----------------------------------------------------------------------------------------------------------+
| Name                 | Bit width | Description                                                                                               |
+======================+===========+===========================================================================================================+
| data_in              | 8         | Data to be stored is read from here.                                                                      |
+----------------------+-----------+-----------------------------------------------------------------------------------------------------------+
| data_out             | 8         | Data at current address is output here.                                                                   |
+----------------------+-----------+-----------------------------------------------------------------------------------------------------------+
| address              | 8         | Index in memory to read from or write to.                                                                 |
+----------------------+-----------+-----------------------------------------------------------------------------------------------------------+
| input_enable         | 1         | While high, the data on data_in will be stored at the currently seleceted address on a rising clock egde. |
+----------------------+-----------+-----------------------------------------------------------------------------------------------------------+
| output_enable        | 1         | While high, the RAM asserts the data at the currently selected address onto data_out.                     |
+----------------------+-----------+-----------------------------------------------------------------------------------------------------------+
| prog_data_mem_select | 1         | When low, selects program memory addresses, when high selects data memory addresses.                      |
+----------------------+-----------+-----------------------------------------------------------------------------------------------------------+
| clock                | 1         | Data is written on a rising clock edge when input_enable is high.                                         |
+----------------------+-----------+-----------------------------------------------------------------------------------------------------------+

Implementation
--------------