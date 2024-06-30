from qtpy import QtWidgets

from .text_file_editor import TextFileEditor
from .assembly_highlighter import AssemblyHighlighter
from .. import assembler
from .. import utils
from .. import assembly_export
from .. import exceptions
from ..network.job import Job

class Assembler(QtWidgets.QWidget):
    """
    Widget assemble and send machine code
    """
    def __init__(self, job_manager_model_ref, parent=None):
        """
        Initialise class.
        """
        super().__init__(parent=parent)

        self.job_manager_model_ref = job_manager_model_ref

        # Editor
        self.text_file_editor = TextFileEditor(
            file_filter="Assembly files (*.asm);;All files (*))"
        )
        self.highlighter = AssemblyHighlighter(
            parent=self.text_file_editor.line_number_text_edit.document()
        )
        self.text_file_editor.clear_editor(force=True)

        # Controls
        self.assemble_button = QtWidgets.QPushButton("Assemble")
        self.assemble_and_send_button = QtWidgets.QPushButton(
            "Assemble and send"
        )
        self.assemble_and_send_button.setEnabled(False)
        self.assemble_button.clicked.connect(self.assemble)
        self.assemble_and_send_button.clicked.connect(self.assemble_and_send)
        controls_layout = QtWidgets.QHBoxLayout()
        controls_layout.addStretch()
        controls_layout.addWidget(self.assemble_button)
        controls_layout.addWidget(self.assemble_and_send_button)

        # Status
        self.status_label = QtWidgets.QLabel("Status:")
        self.status_line_edit = QtWidgets.QLineEdit()
        self.status_line_edit.setReadOnly(True)
        status_layout = QtWidgets.QHBoxLayout()
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.status_line_edit)

        # Main layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.text_file_editor)
        main_layout.addLayout(controls_layout)
        main_layout.addLayout(status_layout)
        main_layout.setStretch(0, 5)

        self.setLayout(main_layout)

    def assemble(self):
        """
        Assemble the assembly in the editor
        """
        lines = self.text_file_editor.line_number_text_edit.toPlainText().splitlines()
        processed_assembly = None
        try:
            processed_assembly = assembler.assemble(lines)
        except exceptions.AssemblyError as exception:
            self.status_line_edit.setText(exception.args[0])

        if processed_assembly is not None:
            self.status_line_edit.setText("Assembled successfully")

    def assemble_and_send(self):
        """
        Assemble the assembly in the editor, then send it to the computer
        """
        lines = self.text_file_editor.line_number_text_edit.toPlainText().splitlines()
        processed_assembly = None
        try:
            processed_assembly = assembler.assemble(lines)
        except exceptions.AssemblyError as exception:
            self.status_line_edit.setText(exception.args[0])

        if processed_assembly is not None:
            machinecode = assembly_export.assembly_lines_to_address_word_pairs(processed_assembly)
            if machinecode:
                machinecode_chunks = list(utils.chunker(machinecode, 100))
                num_chunks = len(machinecode_chunks)
                for counter, chunk in enumerate(machinecode_chunks, start=1):
                    job = Job(
                        "set_words",
                        args=[chunk],
                        human_description=f"Assembly send chunk {counter} of {num_chunks}."
                    )
                    self.job_manager_model_ref.sumbit_job(job)
                self.status_line_edit.setText("Sent successfully")
            else:
                self.status_line_edit.setText("No assembly to send.")


