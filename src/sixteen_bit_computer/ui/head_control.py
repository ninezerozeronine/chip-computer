from qtpy import QtCore, QtWidgets

class HeadControl(QtWidgets.QWidget):
    """
    Widget to control the read/write head
    """
    def __init__(self, parent=None):
        """
        Initialise class.
        """
        super().__init__(parent=parent)

        self.decr_head_button = QtWidgets.QPushButton("Decr head")
        self.incr_head_button = QtWidgets.QPushButton("Incr head")
        self.set_head_button = QtWidgets.QPushButton("Set head")
        self.get_word_on_head_change_checkbox = QtWidgets.QCheckBox("Get word")

        self.set_word_button = QtWidgets.QPushButton("Set word")
        self.get_word_button = QtWidgets.QPushButton("Get word")

        main_layout = QtWidgets.QGridLayout()
        main_layout.setContentsMargins(QtCore.QMargins(0,0,0,0))
        main_layout.addWidget(self.decr_head_button, 0, 0)
        main_layout.addWidget(self.set_head_button, 0, 1)
        main_layout.addWidget(self.incr_head_button, 0, 2)
        main_layout.addWidget(self.get_word_on_head_change_checkbox, 0, 3)
        main_layout.addWidget(self.set_word_button, 1, 0)
        main_layout.addWidget(self.get_word_button, 1, 1)

        self.setLayout(main_layout)
