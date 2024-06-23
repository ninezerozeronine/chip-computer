from qtpy import QtCore, QtWidgets

from .. import number_utils

class ValueView(QtWidgets.QWidget):
    """
    Widget to view a 16 bit value
    """
    def __init__(self, parent=None):
        """
        Initialise class.
        """
        super().__init__(parent=parent)

        self.signed_value = 0
        self.unsigned_value = 0

        dec_label = QtWidgets.QLabel("Dec:")
        self.dec_line_edit = QtWidgets.QLineEdit()
        self.dec_line_edit.setReadOnly(True)
        hex_label = QtWidgets.QLabel("Hex:")
        self.hex_line_edit = QtWidgets.QLineEdit()
        self.hex_line_edit.setReadOnly(True)
        bin_label = QtWidgets.QLabel("Bin:")
        self.bin_line_edit = QtWidgets.QLineEdit()
        self.bin_line_edit.setReadOnly(True)
        self.signed_checkbox = QtWidgets.QCheckBox("Signed")

        value_layout = QtWidgets.QGridLayout()
        value_layout.addWidget(dec_label, 0, 0)
        value_layout.addWidget(self.dec_line_edit, 0, 1)
        value_layout.addWidget(hex_label, 1, 0)
        value_layout.addWidget(self.hex_line_edit, 1, 1)
        value_layout.addWidget(bin_label, 2, 0)
        value_layout.addWidget(self.bin_line_edit, 2, 1)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(QtCore.QMargins(0,0,0,0))
        main_layout.addLayout(value_layout)
        main_layout.addWidget(self.signed_checkbox)
        main_layout.addStretch()

        self.setLayout(main_layout)

        self._redraw()
        self.signed_checkbox.clicked.connect(self._redraw)

    def set_value(self, value):
        """
        Set the value to be dispalyed.

        Args:
            value (int): The value to set.
        """

        if number_utils.number_is_within_bit_limit(value, bit_width=16):
            self.signed_value = number_utils.get_signed_equivalent(
                value, bit_width=16
            )
            self.unsigned_value = number_utils.get_positive_equivalent(
                value, bitwidth=16
            )

            self._redraw()


    def _redraw(self):
        """
        Redraw all the views.

        Generally used when the value changes.
        """
        self.dec_line_edit.setText(self._dec_str())
        self.hex_line_edit.setText(self._hex_str())
        self.bin_line_edit.setText(self._bin_str())


    def _dec_str(self):
        """
        Get the string to display the value in decimal.
        """
        if self.signed_checkbox.isChecked():
            return str(self.signed_value)
        else:
            return str(self.unsigned_value)

    def _hex_str(self):
        """
        Get the string to display the value in hexadecimal.
        """
        if self.signed_checkbox.isChecked():
            return "{num:0{width}X}".format(
                num=self.signed_value,
                width=5 if self.signed_value < 0 else 4
            )
        else:
            return "{num:04X}".format(num=self.unsigned_value)

    def _bin_str(self):
        """
        Get the string to display the value in binary.
        """
        packed = number_utils.number_to_bitstring(
            self.unsigned_value, bit_width=16
        )
        unpacked = "{0} {1} {2} {3}".format(
            packed[0:4],
            packed[4:8],
            packed[8:12],
            packed[12:16]
        )
        return unpacked