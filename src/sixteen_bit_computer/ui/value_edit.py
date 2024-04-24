from PyQt5 import QtGui, QtCore, QtWidgets

from .. import number_utils

class BinButton(QtWidgets.QPushButton):
    """
    Button that holds a 1 or a zero and toggles when pressed.
    """
    def __init__(self, parent=None):
        """
        Initialise class
        """
        super().__init__(parent=parent)

        self.value = 0

        self.clicked.connect(self.toggle_value)
        self._redraw()

    def set_value(self, value):
        """
        Set the value the button currently holds.

        This will redraw the button.

        Args:
            value (int): The value to set. Must be 0 or 1.
        """
        if value in (0, 1):
            self.value = value
            self._redraw()

    def toggle_value(self):
        """
        Toggle the value that the button holds.

        This will redraw the button.
        """
        if self.value == 0:
            self.value = 1
        else:
            self.value = 0
        self._redraw()

    def _redraw(self):
        """
        Redraw the button.
        """
        self.setText(str(self.value))


class BinButtonRow(QtWidgets.QWidget):
    """
    Row of 16 buttons that represent a binary number.
    """

    #: Signal that gets emitted when the value of the row changes.
    value_edited = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        """
        Initialise the class
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
        Read the state of the buttons and update the value.
        """
        new_val = 0
        for index, button in enumerate(self.bin_buttons):
            if button.value == 1:
                new_val += 2**index
        self.value = new_val
        self.value_edited.emit(self.value)

    def set_value(self, value):
        """
        Set all the states of the buttons to represent the passed value.

        Args:
            value (int): The new value to set. Must fit in a 16 bit
                number.
        """
        if number_utils.number_is_within_bit_limit(value, bit_width=16):
            self.value = number_utils.get_positive_equivalent(
                value, bitwidth=16
            )

            # Determine bit values at each index and set on the buttons
            for index in range(16):
                bit_value = 1 if self.value & (1 << index) else 0
                self.bin_buttons[index].set_value(bit_value)


class HexValidator(QtGui.QValidator):
    """
    Validates a 16 bit hex number.
    """

    def validate(self, field_content, cursor_pos):
        """
        Args:
            field_content (str): The proposed content of the field
                to validate.
            cursor_pos (int): The position of the cursor in the input
                field.
        Return:
            tuple (QtGui.QValidator.State, str, int): The judgement of
                the proposed value, the proposed value, and the cursor
                position (not sure what happens if you modify the last
                two from what was passed as input).
        """

        if field_content in ("+", "-", ""):
            return (QtGui.QValidator.Intermediate, field_content, cursor_pos)

        try:
            value = int(field_content, 16)
        except:
            return (QtGui.QValidator.Invalid, field_content, cursor_pos)

        if number_utils.number_is_within_bit_limit(value, bit_width=16):
            return (QtGui.QValidator.Acceptable, field_content, cursor_pos)
        else:
            return (QtGui.QValidator.Invalid, field_content, cursor_pos)

class ValueEdit(QtWidgets.QWidget):
    """
    Widget that allows editing a value in decimal, hexadecimal, or binary.
    """

    #: Signal that gets emitted when the value of the widget changes.
    value_changed = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        """
        Initialise the class.
        """
        super().__init__(parent=parent)

        self.value = 0

        dec_label = QtWidgets.QLabel("Dec:")
        self.dec_line_edit = QtWidgets.QLineEdit()
        self.dec_line_edit.setValidator(QtGui.QIntValidator(-32768, 65535))
        self.dec_line_edit.textEdited.connect(self.dec_edited)

        hex_label = QtWidgets.QLabel("Hex:")
        self.hex_line_edit = QtWidgets.QLineEdit()
        self.hex_line_edit.setValidator(HexValidator())
        self.hex_line_edit.textEdited.connect(self.hex_edited)

        bin_label = QtWidgets.QLabel("Bin:")
        self.bin_line_edit = QtWidgets.QLineEdit()
        self.bin_line_edit.setValidator(
            QtGui.QRegularExpressionValidator(
                QtCore.QRegularExpression("[01]{0,16}")
            )
        )
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

        self.set_values(
            dec=True,
            hex_=True,
            bin_line=True,
            bin_buttons=True
        )


    def dec_edited(self, new_text):
        """
        Handle a new value being entered in the decimal field.

        This could be an incomplete/invalid value e.g. "-" if the user
        is typing a negative number. Or "".

        Args:
            new_text (str): The new text from the field.
        """
        try:
            self.value = int(new_text)
        except:
            self.value = 0
        if number_utils.number_is_within_bit_limit(self.value, bit_width=16):
            self.set_values(
                hex_=True,
                bin_line=True,
                bin_buttons=True
            )
            self.value_changed.emit(self.value)

    def hex_edited(self, new_text):
        """
        Handle a new value being entered in the hexadecimal field.

        This could be an incomplete/invalid value e.g. "-" if the user
        is typing a negative number. Or "".

        Args:
            new_text (str): The new text from the field.
        """
        try:
            self.value = int(new_text, 16)
        except:
            self.value = 0
        if number_utils.number_is_within_bit_limit(self.value, bit_width=16):
            self.set_values(
                dec=True,
                bin_line=True,
                bin_buttons=True
            )
            self.value_changed.emit(self.value)

    def bin_line_edited(self, new_text):
        """
        Handle a new value being entered in the binary field.

        This could be an incomplete/invalid value e.g. "".

        Args:
            new_text (str): The new text from the field.
        """
        try:
            self.value = int(new_text, 2)
        except:
            self.value = 0
        if number_utils.number_is_within_bit_limit(self.value, bit_width=16):
            self.set_values(
                dec=True,
                hex_=True,
                bin_buttons=True
            )
            self.value_changed.emit(self.value)

    def bin_buttons_edited(self, new_value):
        """
        Handle the value held by the binary buttons changing.

        Args:
            new_value (int): The new value from the buttons.
        """
        self.value = new_value
        self.set_values(
            dec=True,
            hex_=True,
            bin_line=True,
        )
        self.value_changed.emit(self.value)

    def set_values(
        self,
        dec=False,
        hex_=False,
        bin_line=False,
        bin_buttons=False
    ):
        """
        Set the given fields to the given value.

        Keyword Args:
            dec (bool): Whether or not to set the decimal field.
            hex_ (bool): Whether or not to set the hexadecimal field.
            bin_line (bool): Whether or not to set the binary text field.
            bin_buttons (bool): Whether or not to set the binary buttons.
        """
        if dec:
            self.dec_line_edit.setText(str(self.value))

        if hex_:
            self.hex_line_edit.setText(f"{self.value:X}")

        if bin_line:
            self.bin_line_edit.setText(
                number_utils.number_to_bitstring(self.value, bit_width=16)
            )

        if bin_buttons:
            self.bin_buttons.set_value(self.value)
