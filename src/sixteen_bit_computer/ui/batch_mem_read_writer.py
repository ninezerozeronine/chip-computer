from qtpy import QtWidgets

from .text_file_editor import TextFileEditor
from .batch_mem_read_write_highlighter import BatchMemReadWriteHighlighter
from ..network.job import Job
from .. import number_utils
from .. import utils

class BatchMemReadWriter(QtWidgets.QWidget):
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
            file_filter="Batch Memory Read Write files (*.bmrw);;All files (*))"
        )
        self.highlighter = BatchMemReadWriteHighlighter(
            parent=self.text_file_editor.line_number_text_edit.document()
        )
        self.text_file_editor.clear_editor(force=True)

        # Controls
        self.check_button = QtWidgets.QPushButton("Check")
        self.check_button.clicked.connect(self.check)
        self.send_selection_button = QtWidgets.QPushButton("Send Selection")
        self.send_selection_button.setEnabled(False)
        self.send_selection_button.clicked.connect(self.send_selection)
        self.send_button = QtWidgets.QPushButton("Send")
        self.send_button.setEnabled(False)
        self.send_button.clicked.connect(self.send)
        controls_layout = QtWidgets.QHBoxLayout()
        controls_layout.addStretch()
        controls_layout.addWidget(self.check_button)
        controls_layout.addWidget(self.send_selection_button)
        controls_layout.addWidget(self.send_button)

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


    def validate_and_extract(self, lines):
        """

        """

        valid = True
        message = "Batch Memory Read Write file is valid"
        commands = []

        for line_no, orig_line in enumerate(lines, start=1):
            # Trim whitespace from ends
            line = orig_line.strip()

            # Skip blank lines
            if not line:
                continue

            # Remove any comments
            comment_index = line.find("//")
            if comment_index >= 0:
                line = line[:comment_index]

            # Line may be blank after removing comments
            if not line:
                continue

            # Get the tokens
            tokens = line.split()
            if len(tokens) not in (2,3):
                valid = False
                message = (
                    f"Error on line {line_no}, ({orig_line}), line can "
                    f"only have 2 or 3 tokens."
                )
                break

            # Check command is R or W
            command = tokens[0]
            if command not in ("R", "W"):
                valid = False
                message = (
                    f"Error on line {line_no}, ({orig_line}), command "
                    f"token must be 'R' or 'W'."
                )
                break

            # Check R commands
            if command == "R":

                # Check there are 2 tokens
                if len(tokens) != 2:
                    valid = False
                    message = (
                        f"Error on line {line_no}, ({orig_line}), read "
                        "commands must be followed by one token."
                    )
                    break

                # Check address is a number
                address = tokens[1]
                try:
                    address_int = int(address, 0)
                except ValueError:
                    valid = False
                    message = (
                        f"Error on line {line_no}, ({orig_line}), value "
                        "for the address to read was not a number."
                    )
                    break

                # Check the address is in range
                min_val, max_val =  number_utils.get_min_max_values(16)
                if not (0 <= address_int <= max_val):
                    valid = False
                    message = (
                        f"Error on line {line_no}, ({orig_line}), value "
                        "for address to read is outside the range that "
                        "can be stored in 16 bits."
                    )
                    break

                commands.append(("R", address_int))

            # Check W commands
            if command == "W":

                # Check there are 3 tokens
                if len(tokens) != 3:
                    valid = False
                    message = (
                        f"Error on line {line_no}, ({orig_line}), write "
                        "commands must be followed by two tokens."
                    )
                    break

                # Check address is a number
                address = tokens[1]
                try:
                    address_int = int(address, 0)
                except ValueError:
                    valid = False
                    message = (
                        f"Error on line {line_no}, ({orig_line}), value "
                        "for the address to write to was not a number."
                    )
                    break

                # Check the address is in range
                min_val, max_val =  number_utils.get_min_max_values(16)
                if not (0 <= address_int <= max_val):
                    valid = False
                    message = (
                        f"Error on line {line_no}, ({orig_line}), value "
                        "for the address to write to is outside the "
                        "range that can be stored in 16 bits."
                    )
                    break

                # Check the data is a number
                data = tokens[2]
                try:
                    data_int = int(data, 0)
                except ValueError:
                    valid = False
                    message = (
                        f"Error on line {line_no}, ({orig_line}), value "
                        "for the data to write is not a number."
                    )
                    break

                # Check the data is in range
                if not number_utils.number_is_within_bit_limit(data_int, bit_width=16):
                    valid = False
                    message = (
                        f"Error on line {line_no}, ({orig_line}), value "
                        "for the data to write is outside of the range "
                        "that can be stored in 16 bits."
                    )
                    break

                commands.append(
                    (
                        "W",
                        address_int,
                        number_utils.get_positive_equivalent(data_int, bitwidth=16)
                    )
                )

        if valid:
            return valid, message, commands
        else:
            return valid, message, []


    def send_selection(self):
        """
        Check and send the selected lines.
        """
        lines = self.text_file_editor.line_number_text_edit.textCursor().selectedText().splitlines()
        valid, message, commands = self.validate_and_extract(lines)
        _send(valid, message, commands)


    def send(self):
        """
        Send the memory read write commands to the computer
        """
        lines = self.text_file_editor.line_number_text_edit.toPlainText().splitlines()
        valid, message, commands = self.validate_and_extract(lines)
        _send(valid, message, commands)


    def _send(self, valid, message, commands):
        """

        """
        if valid:
            if commands:
                command_chunks = list(utils.chunker(commands, 75))
                num_chunks = len(command_chunks)
                for counter, chunk in enumerate(command_chunks, start=1):
                    job = Job(
                        "batch_mem_read_write",
                        args=[chunk],
                        human_description=f"Batch mem read write send chunk {counter} of {num_chunks}."
                    )
                    self.job_manager_model_ref.sumbit_job(job)
            else:
                self.status_line_edit.setText("No commands to send.")
        else:
            self.status_line_edit.setText(message)

    def check(self):
        """
        Check the read and write commands
        """

        lines = self.text_file_editor.line_number_text_edit.toPlainText().splitlines()

        valid, message, commands = self.validate_and_extract(lines)

        if valid:
            if commands:
                self.status_line_edit.setText("Commands are valid.")
                print(commands)
            else:
                self.status_line_edit.setText("No commands to send.")
        else:
            self.status_line_edit.setText(message)
