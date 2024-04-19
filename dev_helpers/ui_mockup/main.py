import sys

from PyQt5 import QtGui, QtCore, QtWidgets


class ValueView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)


        self.min_val = (2**16 / 2) * -1
        self.max_val = 2**16 - 1
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
        Set the value to be dispalyed

        Args:
            value (int): The value to set.
        """

        if self.min_val <= value <= self.max_val:
            self.signed_value = value
            self.unsigned_value = value
            if value < 0:
                self.unsigned_value = value + 2**16

        self._redraw()


    def _redraw(self):
        """

        """
        self.dec_line_edit.setText(self._dec_str())
        self.hex_line_edit.setText(self._hex_str())
        self.bin_line_edit.setText(self._bin_str())


    def _dec_str(self):
        """

        """
        if self.signed_checkbox.isChecked():
            return str(self.signed_value)
        else:
            return str(self.unsigned_value)

    def _hex_str(self):
        """
        
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

        """
        packed = "{num:016b}".format(num=self.unsigned_value)
        unpacked = "{0} {1} {2} {3}".format(
            packed[0:4],
            packed[4:8],
            packed[8:12],
            packed[12:16]
        )
        return unpacked
    

class BinButton(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.value = 0

        self.clicked.connect(self.toggle_value)
        self._redraw()

    def _get_text(self):
        if self.value == 0:
            return "0"
        else:
            return "1"

    def set_value(self, value):
        self.value = value
        self._redraw()

    def toggle_value(self):
        if self.value == 0:
            self.value = 1
        else:
            self.value = 0
        self._redraw()

    def _redraw(self):
        self.setText(self._get_text())


class BinButtonRow(QtWidgets.QWidget):

    value_edited = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        """

        """
        super().__init__(parent=parent)

        self.bin_buttons = []
        self.value = 0
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setContentsMargins(QtCore.QMargins(0,0,0,0))
        button_layout.setDirection(QtWidgets.QBoxLayout.RightToLeft)
        button_layout.setSpacing(2)
        for index in range(16):
            bin_button = BinButton()
            bin_button.setMaximumWidth(25)
            bin_button.clicked.connect(self._update_value)
            self.bin_buttons.append(bin_button)
            button_layout.addWidget(bin_button)
            if index in (3, 7, 11):
                button_layout.addStretch()
                button_layout.addSpacing(12)
                button_layout.addStretch()
        self.setLayout(button_layout)

    def _update_value(self):
        """

        """
        new_val = 0
        for index, button in enumerate(self.bin_buttons):
            if button.value == 1:
                new_val += 2**index
        self.value = new_val
        self.value_edited.emit(self.value)

    def set_value(self, value):
        """

        """
        # Get positive equivalent
        if value < 0:
            value = value + 2**16

        # Determine bit values at each index and set on the buttons
        for index in range(16):
            bit_value = 1 if value & (1 << index) else 0
            self.bin_buttons[index].set_value(bit_value)




class ValueEdit(QtWidgets.QWidget):
    value_changed = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)


        self.min_val = (2**16 / 2) * -1
        self.max_val = 2**16 - 1
        self.value = 0

        dec_label = QtWidgets.QLabel("Dec:")
        self.dec_line_edit = QtWidgets.QLineEdit()
        self.dec_line_edit.setValidator(QtGui.QIntValidator(-32768, 65535, self))
        self.dec_line_edit.textEdited.connect(self.dec_edited)

        hex_label = QtWidgets.QLabel("Hex:")
        self.hex_line_edit = QtWidgets.QLineEdit()
        self.hex_line_edit.textEdited.connect(self.hex_edited)

        bin_label = QtWidgets.QLabel("Bin:")
        self.bin_line_edit = QtWidgets.QLineEdit()
        self.bin_line_edit.textEdited.connect(self.bin_line_edited)

        self.bin_buttons = BinButtonRow()
        self.bin_buttons.value_edited.connect(self.bin_buttons_edited)

        value_layout = QtWidgets.QGridLayout()
        value_layout.addWidget(dec_label, 0, 0)
        value_layout.addWidget(self.dec_line_edit, 0, 1)
        value_layout.addWidget(hex_label, 1, 0)
        value_layout.addWidget(self.hex_line_edit, 1, 1)
        value_layout.addWidget(bin_label, 2, 0)
        value_layout.addWidget(self.bin_line_edit, 2, 1)
        value_layout.addWidget(self.bin_buttons, 3, 1)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(QtCore.QMargins(0,0,0,0))
        main_layout.addLayout(value_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)


    def dec_edited(self, new_text):
        try:
            new_value = int(new_text)
        except:
            new_value = 0
        self.set_values(
            new_value,
            _hex=True,
            bin_line=True,
            bin_buttons=True
        )
        self.value_changed.emit(new_value)

    def hex_edited(self, new_text):
        try:
            new_value = int(new_text, 16)
        except:
            new_value = 0
        self.set_values(
            new_value,
            dec=True,
            bin_line=True,
            bin_buttons=True
        )
        self.value_changed.emit(new_value)

    def bin_line_edited(self, new_text):
        try:
            new_value = int(new_text, 2)
        except:
            new_value = 0
        self.set_values(
            new_value,
            dec=True,
            _hex=True,
            bin_buttons=True
        )
        self.value_changed.emit(new_value)

    def bin_buttons_edited(self, new_value):
        self.set_values(
            new_value,
            dec=True,
            _hex=True,
            bin_line=True,
        )
        self.value_changed.emit(new_value)

    def set_values(
        self,
        value,
        dec=False,
        _hex=False,
        bin_line=False,
        bin_buttons=False
    ):
        if dec:
            self.dec_line_edit.setText(str(value))

        if _hex:
            self.hex_line_edit.setText(f"{value:X}")

        if bin_line:
            # Get positive equivalent
            pos_value = value
            if pos_value < 0:
                pos_value = pos_value + 2**16

            self.bin_line_edit.setText(f"{pos_value:016b}")

        if bin_buttons:
            self.bin_buttons.set_value(value)



# class HexValidator(QtCore.QValidator):
#     def validate(self, curr_input, cursor_pos):
#         print(curr_input)







class Main(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.input_box = QtWidgets.QGroupBox("Input")
        self.input_layout = QtWidgets.QVBoxLayout()
        self.input_widget = ValueEdit()
        self.input_layout.addWidget(self.input_widget)
        self.input_box.setLayout(self.input_layout)

        self.head_view_box = QtWidgets.QGroupBox("Head")
        self.head_layout = QtWidgets.QVBoxLayout()
        self.head_view = ValueView()
        self.head_layout.addWidget(self.head_view)
        self.head_view_box.setLayout(self.head_layout)

        self.data_view_box = QtWidgets.QGroupBox("Data")
        self.data_layout = QtWidgets.QVBoxLayout()
        self.data_view = ValueView()
        self.data_layout.addWidget(self.data_view)
        self.data_view_box.setLayout(self.data_layout)

        # self.value_set = QtWidgets.QLineEdit()
        # self.value_set.setValidator(QtGui.QIntValidator(-32768, 65535, self))
        # self.value_set.textEdited.connect(self.convert_to_int_and_set)

        self.main_layout = QtWidgets.QGridLayout()
        self.main_layout.addWidget(self.input_box, 0, 0)
        self.main_layout.addWidget(self.head_view_box, 0, 1)
        self.main_layout.addWidget(self.data_view_box, 1, 1)
        #self.main_layout.addWidget(self.value_set, 1, 0)

        self.setLayout(self.main_layout)

    def convert_to_int_and_set(self, num_string):
        try:
            int(num_string)
        except:
            num_string = "0"

        self.data_view.set_value(int(num_string))
        self.head_view.set_value(int(num_string))
        self.bin_buttons.set_value(int(num_string))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    sys.exit(main.exec_())