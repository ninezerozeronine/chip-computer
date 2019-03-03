Arithmetic Logic Unit
=====================

The Arithmetic Logic Unit (ALU) performs arithmetical and logical operations
using one or both of it's inputs. The result is stored internally when desired
and the value of that internal storage is also output when desired.

As well as calculating the result, pieces of information (flags) about the
result or the two inputs are also stored internally and the state of that
internal storage is always output.

Interface and Operation
-----------------------

This is the interface of the ALU:

.. image:: images/alu/alu_block.png

This is how it operates:

+----------------------+-----------+------------------------------------------------------------------------------------------------------------------------+
| Name                 | Bit width | Description                                                                                                            |
+======================+===========+========================================================================================================================+
| carry_in             | 1         | If high, supply a carry in to the arithmetical operation.                                                              |
+----------------------+-----------+------------------------------------------------------------------------------------------------------------------------+
| M                    | 1         | Choose between arithmetical and logical operations.                                                                    |
+----------------------+-----------+------------------------------------------------------------------------------------------------------------------------+
| S0-3                 | 4         | Specify which arithmetical or logical operation.                                                                       |
+----------------------+-----------+------------------------------------------------------------------------------------------------------------------------+
| store_result         | 1         | While high, the result of the operation will be stored internally on a rising clock egde.                              |
+----------------------+-----------+------------------------------------------------------------------------------------------------------------------------+
| store_flags          | 1         | While high, flags resulting from the current operation/inputs/result will be stored internally on a rising clock egde. |
+----------------------+-----------+------------------------------------------------------------------------------------------------------------------------+
| output_stored_result | 1         | Assert the value of the stored result onto the result_stored connection.                                               |
+----------------------+-----------+------------------------------------------------------------------------------------------------------------------------+
| clock                | 1         | A rising edge triggers result and flag storage if enabled.                                                                        |
+----------------------+-----------+------------------------------------------------------------------------------------------------------------------------+
| A                    | 8         | The A input to the operation.                                                                                          |
+----------------------+-----------+------------------------------------------------------------------------------------------------------------------------+
| B                    | 8         | The B input to the operation.                                                                                          |
+----------------------+-----------+------------------------------------------------------------------------------------------------------------------------+
| result_live          | 8         | The result of the current operation with the current inputs.                                                           |
+----------------------+-----------+------------------------------------------------------------------------------------------------------------------------+
| result_stored        | 8         | The value of the stored result while output_stored_result is high, not connected otherwise.                            |
+----------------------+-----------+------------------------------------------------------------------------------------------------------------------------+
| flags_live           | 4         | Flags resulting from the current operation/inputs/result.                                                              |
+----------------------+-----------+------------------------------------------------------------------------------------------------------------------------+
| flags_stored         | 4         | The value of the stored result while output_stored_result is high, not connected otherwise.                            |
+----------------------+-----------+------------------------------------------------------------------------------------------------------------------------+

``carry_in``, ``M``, and ``S0-3`` are used to select from the available operations (from the datasheet_).:

.. _datasheet: http://www.ti.com/lit/ds/symlink/sn54ls181.pdf

.. image:: images/alu/operation_select.jpg
    :width: 100%

Implementation
--------------

A :ref:`safe_clock_enable` circuit is not required as it's natively implemented
in the 74HCT377 and 74HCT171.

