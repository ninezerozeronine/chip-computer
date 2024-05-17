from PyQt5 import QtGui, QtCore, QtWidgets

class Assembler(QtWidgets.QWidget):
    """
    Widget assemble and send machine code
    """
    def __init__(self, parent=None):
        """
        Initialise class.
        """
        super().__init__(parent=parent)

        self.last_send = []

        self.editor = QtWidgets.QTextEdit()
        self.assemble_and_send_button = QtWidgets.QPushButton("Assemble and send")
        self.only_changes_checkbox = QtWidgets.QCheckBox("Only send changes")
        self.status_label = QtWidgets.QLabel("Status:")
        self.status_line_edit = QtWidgets.QLineEdit()

        send_layout = QtWidgets.QHBoxLayout()
        send_layout.addStretch()
        send_layout.addWidget(self.only_changes_checkbox)
        send_layout.addWidget(self.assemble_and_send_button)

        status_layout = QtWidgets.QHBoxLayout()
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.status_line_edit)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.editor)
        main_layout.addLayout(send_layout)
        main_layout.addLayout(status_layout)
        main_layout.setStretch(0, 5)

        self.setLayout(main_layout)
