from PyQt5 import QtGui, QtCore, QtWidgets

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
