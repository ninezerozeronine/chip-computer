"""
Line numbers inspired by:

"""

from PyQt5 import Qt, QtGui, QtCore, QtWidgets

from .line_number_text_edit import LineNumberTextEdit

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
        self.current_file = None

        # File controls
        self.clear_button = QtWidgets.QPushButton("Clear")
        self.open_button = QtWidgets.QPushButton("Open")
        self.save_button = QtWidgets.QPushButton("Save")
        self.save_as_button = QtWidgets.QPushButton("Save As")
        file_controls_layout = QtWidgets.QHBoxLayout()
        file_controls_layout.addWidget(self.clear_button)
        file_controls_layout.addWidget(self.open_button)
        file_controls_layout.addWidget(self.save_button)
        file_controls_layout.addWidget(self.save_as_button)
        self.clear_button.clicked.connect(self.clear_editor)
        self.open_button.clicked.connect(self.open_file)
        self.save_button.clicked.connect(self.save_editor)
        self.save_as_button.clicked.connect(self.save_editor_as)

        # File status
        self.current_file_label = QtWidgets.QLabel("File:")
        self.current_file_line_edit = QtWidgets.QLineEdit()
        self.current_file_line_edit.setReadOnly(True)
        file_status_layout = QtWidgets.QHBoxLayout()
        file_status_layout.addWidget(self.current_file_label)
        file_status_layout.addWidget(self.current_file_line_edit)
        file_status_layout.setStretch(1, 5)

        # Editor
        self.line_numer_text_edit = LineNumberTextEdit()

        # Controls
        self.line_wrap_checkbox = QtWidgets.QCheckBox("Line wrap")
        self.assemble_and_send_button = QtWidgets.QPushButton(
            "Assemble and send"
        )
        self.only_changes_checkbox = QtWidgets.QCheckBox(
            "Only send changes"
        )
        controls_layout = QtWidgets.QHBoxLayout()
        controls_layout.addWidget(self.line_wrap_checkbox)
        controls_layout.addStretch()
        controls_layout.addWidget(self.only_changes_checkbox)
        controls_layout.addWidget(self.assemble_and_send_button)
        self.line_wrap_checkbox.clicked.connect(self.set_line_wrap)

        # Status
        self.status_label = QtWidgets.QLabel("Status:")
        self.status_line_edit = QtWidgets.QLineEdit()
        self.status_line_edit.setReadOnly(True)
        status_layout = QtWidgets.QHBoxLayout()
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.status_line_edit)

        # Main layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(file_controls_layout)
        main_layout.addLayout(file_status_layout)
        main_layout.addWidget(self.line_numer_text_edit)
        main_layout.addLayout(controls_layout)
        main_layout.addLayout(status_layout)
        main_layout.setStretch(0, 5)

        self.setLayout(main_layout)


    def set_line_wrap(self):
        """
        Set line wrap for editor based on checkbox state.
        """

        if self.line_wrap_checkbox.isChecked():
            self.line_numer_text_edit.setLineWrapMode(
                self.line_numer_text_edit.WidgetWidth
            )
        else:
            self.line_numer_text_edit.setLineWrapMode(
                self.line_numer_text_edit.NoWrap
            )

    def clear_editor(self):
        """

        """
        pass

    def open_file(self):
        """

        """
        filepath, file_filter = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption="Open assembly file",
            filter="Assmebly files (*.asm);;All files (*)"
        )
        print(filepath)

    def save_editor(self):
        """

        """
        pass

    def save_editor_as(self):
        """

        """
        filepath, file_filter = QtWidgets.QFileDialog.getSaveFileName(
            parent=self,
            caption="Save assembly as",
            filter="Assmebly files (*.asm);;All files (*)"
        )
        print(filepath)

    def assemble_and_send(self):
        """

        """
        pass
