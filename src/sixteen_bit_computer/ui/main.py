import sys
import json
import time

from PyQt5 import QtGui, QtCore, QtWidgets, QtNetwork, QtTest

from .value_edit import ValueEdit
from .value_view import ValueView
from .run_control import RunControl
from .head_control import HeadControl
from .connect_control import ConnectControl
from .job_control import JobControl
from .job_manager_model import JobManagerModel
from .assembler import Assembler
from .batch_mem_read_writer import BatchMemReadWriter
from ..network.job import Job
from . import constants

class Main(QtWidgets.QDialog):
    def __init__(self, parent=None):
        """
        Initialise the class
        """
        super().__init__(parent=parent)


        self.waiting_for = "header"
        self.num_data_bytes = 0
        self.socket = QtNetwork.QTcpSocket(self)
        self.socket.readyRead.connect(self.read_from_socket)
        self.socket.error.connect(self.display_error)
        self.socket.stateChanged.connect(self.state_changed)
        self.socket.connected.connect(self.socket_connected)
        self.socket.disconnected.connect(self.socket_disconnected)

        self.job_manager_model = JobManagerModel()
        self.job_queue_timer = QtCore.QTimer(self)
        self.job_queue_timer.setInterval(100)
        self.job_queue_timer.timeout.connect(self.run_job_manager_model)

        self.build_ui()
        self.connect_ui()

        self.add_dummy_jobs()

        self.setWindowTitle("SBC Connect")

    def add_dummy_jobs(self):
        self.job_manager_model.sumbit_job(Job("dummy_method3", human_description="abc"))
        time.sleep(0.05)
        self.job_manager_model.sumbit_job(Job("dummy_method1", human_description="aba"))
        time.sleep(0.05)
        self.job_manager_model.sumbit_job(Job("dummy_method2", human_description="bbb"))
        time.sleep(0.05)
        self.job_manager_model.sumbit_job(Job("dummy_method2", human_description="zzz"))
        time.sleep(0.05)
        self.job_manager_model.sumbit_job(Job("dummy_method1", human_description="yyy"))

    def build_ui(self):
        """
        Create UI widgets and add them to layouts.
        """
        connect_box = QtWidgets.QGroupBox("Connection")
        connect_layout = QtWidgets.QVBoxLayout()
        self.connect_control = ConnectControl()
        self.connect_control.disconnect_button.setEnabled(False)
        connect_layout.addWidget(self.connect_control)
        connect_box.setLayout(connect_layout)

        self.input_box = QtWidgets.QGroupBox("Input")
        self.input_box.setEnabled(False)
        self.input_layout = QtWidgets.QVBoxLayout()
        self.input_widget = ValueEdit()
        self.input_widget.set_values(
            dec=True,
            hex_=True,
            bin_line=True,
            bin_buttons=True
        )
        self.input_layout.addWidget(self.input_widget)
        self.input_box.setLayout(self.input_layout)

        self.address_view_box = QtWidgets.QGroupBox("Address/Head")
        self.address_view_box.setEnabled(False)
        self.address_layout = QtWidgets.QVBoxLayout()
        self.address_view = ValueView()
        self.address_layout.addWidget(self.address_view)
        self.address_view_box.setLayout(self.address_layout)

        self.data_view_box = QtWidgets.QGroupBox("Data")
        self.data_view_box.setEnabled(False)
        self.data_layout = QtWidgets.QVBoxLayout()
        self.data_view = ValueView()
        self.data_layout.addWidget(self.data_view)
        self.data_view_box.setLayout(self.data_layout)

        self.head_control_box = QtWidgets.QGroupBox("Head Control")
        self.head_control_box.setEnabled(False)
        self.head_control_layout = QtWidgets.QVBoxLayout()
        self.head_control = HeadControl()
        self.head_control_layout.addWidget(self.head_control)
        self.head_control_layout.addStretch()
        self.head_control_box.setLayout(self.head_control_layout)   

        self.run_control_box = QtWidgets.QGroupBox("Run Control")
        self.run_control_box.setEnabled(False)
        self.run_control_layout = QtWidgets.QVBoxLayout()
        self.run_control = RunControl()
        self.run_control_layout.addWidget(self.run_control)
        self.run_control_box.setLayout(self.run_control_layout)

        self.panel_layout = QtWidgets.QGridLayout()
        self.panel_layout.setContentsMargins(QtCore.QMargins(0,0,0,0))
        self.panel_layout.addWidget(connect_box, 0, 0, 1, 2)
        self.panel_layout.addWidget(self.input_box, 1, 0)
        self.panel_layout.addWidget(self.address_view_box, 1, 1)
        self.panel_layout.addWidget(self.head_control_box, 2, 0)
        self.panel_layout.addWidget(self.data_view_box, 2, 1)
        self.panel_layout.addWidget(self.run_control_box, 3, 0, 1, 2)
        self.panel_layout.addWidget(QtWidgets.QWidget(), 4, 0)
        self.panel_layout.setRowStretch(4, 2)

        self.panel_widget = QtWidgets.QWidget()
        self.panel_widget.setLayout(self.panel_layout)

        self.assembler = Assembler(self.job_manager_model)
        self.assembler.setAutoFillBackground(True)

        self.batch_mem_read_writer = BatchMemReadWriter(self.job_manager_model)
        self.batch_mem_read_writer.setAutoFillBackground(True)

        self.job_control = JobControl(self.job_manager_model)
        self.job_control.setAutoFillBackground(True)

        self.tab_widget = QtWidgets.QTabWidget()
        self.tab_widget.addTab(self.assembler, "Assembler")
        self.tab_widget.addTab(self.batch_mem_read_writer, "Batch memory R/W")
        self.tab_widget.addTab(self.job_control, "Jobs")

        self.splitter = QtWidgets.QSplitter()
        self.splitter.addWidget(self.panel_widget)
        self.splitter.addWidget(self.tab_widget)
        handle = self.splitter.handle(1)
        palette = handle.palette()
        palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor("lightGray"))
        handle.setPalette(palette)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.splitter)

        self.setLayout(self.main_layout)

    def connect_ui(self):
        """
        Connect UI events to callbacks
        """
        self.connect_control.connect_button.clicked.connect(self.connect)
        self.connect_control.disconnect_button.clicked.connect(
            self.socket.disconnectFromHost
        )
        self.head_control.decr_head_button.clicked.connect(self.decr_head)
        self.head_control.set_head_button.clicked.connect(self.set_head)
        self.head_control.incr_head_button.clicked.connect(self.incr_head)
        self.head_control.set_word_button.clicked.connect(self.set_word)
        self.head_control.get_word_button.clicked.connect(self.get_word)

        self.run_control.run_button.clicked.connect(self.set_mode_to_run)
        self.run_control.step_button.clicked.connect(self.set_mode_to_step)
        self.run_control.stop_button.clicked.connect(self.set_mode_to_stop)
        self.run_control.half_step_button.clicked.connect(self.send_half_steps)
        self.run_control.full_step_button.clicked.connect(self.send_full_steps)
        self.run_control.reset_button.pressed.connect(self.press_reset)
        self.run_control.reset_button.released.connect(self.release_reset)

        self.run_control.clock_mode_crystal_button.clicked.connect(
            self.set_clock_to_crystal
        )
        self.run_control.clock_mode_custom_button.clicked.connect(
            self.set_clock_to_custom
        )
        self.run_control.custom_freq_set_button.clicked.connect(self.set_custom_freq)
        self.run_control.load_program_button.clicked.connect(self.load_program)

    def connect(self):
        """
        Atempt to connect to the Pico
        """
        state = self.socket.state()
        if state != QtNetwork.QAbstractSocket.UnconnectedState:
            print("Cannot connect - socket is in incorrect state, state is:")
            print(decode_state(state))
        else:
            self.socket.connectToHost(
                self.connect_control.ip_line_edit.text(),
                int(self.connect_control.port_line_edit.text())
            )

    def decr_head(self):
        """
        Decrement the read write head, optionally reading the word at
        the new location.
        """
        
        get_word = self.head_control.get_word_on_head_change_checkbox.isChecked()
        job = Job(
            "decr_head",
            kwargs={"get_word":get_word},
            human_description="Decrement the head."
        )
        self.job_manager_model.sumbit_job(job)

    def set_head(self):
        """
        Set the location of the read/write head to the current input
        """
        get_word = self.head_control.get_word_on_head_change_checkbox.isChecked()
        new_val = self.input_widget.value
        job = Job(
            "set_head",
            args=[new_val],
            kwargs={"get_word":get_word},
            human_description=f"Set the head to {new_val}."
        )
        self.job_manager_model.sumbit_job(job)

    def incr_head(self):
        """
        Increment the read write head, optionally reading the word at
        the new location.
        """
        get_word = self.head_control.get_word_on_head_change_checkbox.isChecked()
        job = Job(
            "incr_head",
            kwargs={"get_word":get_word},
            human_description="Increment the head."
        )
        self.job_manager_model.sumbit_job(job)

    def set_word(self):
        """
        Set the word at the current read write head position to the
        value in the input.
        """
        new_word = self.input_widget.value
        job = Job(
            "set_word_at_head",
            args=[new_word],
            human_description=f"Set word at current head pos to {new_word}."
        )
        self.job_manager_model.sumbit_job(job)

    def get_word(self):
        """
        Get the word at the current read write head position.
        """
        job = Job(
            "get_word_at_head",
            human_description="Get word at current head pos."
        )
        self.job_manager_model.sumbit_job(job)

    def set_mode_to_run(self):
        """
        Set mode to run mode
        """
        job = Job(
            "set_mode_to_run",
            human_description="Set mode to run."
        )
        self.job_manager_model.sumbit_job(job)

    def set_mode_to_step(self):
        """
        Set mode to step
        """
        job = Job(
            "set_mode_to_step",
            human_description="Set mode to step."
        )
        self.job_manager_model.sumbit_job(job)

    def set_mode_to_stop(self):
        """
        Set mode to stop
        """
        job = Job(
            "set_mode_to_stop",
            human_description="Set mode to stop."
        )
        self.job_manager_model.sumbit_job(job)

    def send_half_steps(self):
        """
        Send the number of half steps specified by the user
        """
        num_half_steps = int(self.run_control.num_steps_line_edit.text())
        job = Job(
            "half_steps",
            kwargs={
                "num_steps": num_half_steps
            },
            human_description=f"Step {num_half_steps} half steps."
        )
        self.job_manager_model.sumbit_job(job)

    def send_full_steps(self):
        """
        Send the number of full steps specified by the user
        """
        num_full_steps = int(self.run_control.num_steps_line_edit.text())
        job = Job(
            "full_steps",
            kwargs={
                "num_steps": num_full_steps
            },
            human_description=f"Step {num_full_steps} full steps."
        )
        self.job_manager_model.sumbit_job(job)

    def press_reset(self):
        """
        Set reset state high.
        """
        job = Job(
            "set_reset",
            args=[True],
            human_description="Set reset high."
        )
        self.job_manager_model.sumbit_job(job)

    def release_reset(self):
        """
        Set reset state low.
        """
        job = Job(
            "set_reset",
            args=[False],
            human_description="Set reset low."
        )
        self.job_manager_model.sumbit_job(job)

    def set_clock_to_crystal(self):
        """
        Set the clock to crystal mode
        """
        job = Job(
            "set_clock_source",
            args=[constants.CPU_CLK_SRC_CRYSTAL],
            human_description="Set the clock source to crystal."
        )
        self.job_manager_model.sumbit_job(job)

    def set_clock_to_custom(self):
        """
        Set the clock to custom mode
        """
        job = Job(
            "set_clock_source",
            args=[constants.CPU_CLK_SRC_PANEL],
            human_description="Set the clock source to custom."
        )
        self.job_manager_model.sumbit_job(job)

    def set_custom_freq(self):
        """
        Set a custom frequency.
        """
        new_freq = self.run_control.custom_freq_input_line_edit.text()
        job = Job(
            "set_frequency",
            args=[new_freq],
            human_description=f"Set the clock frequency to {new_freq} Hz."
        )
        self.job_manager_model.sumbit_job(job)

    def load_program(self):
        """
        Load the program selected in the combobox.
        """
        program_index = self.run_control.program_combobox.currentIndex()
        program_name = self.run_control.program_combobox.currentText()
        job = Job(
            "load_program",
            args=[program_index],
            human_description=f"Load the program {program_name} at index {program_index}"
        )
        self.job_manager_model.sumbit_job(job)

    def run_job_manager_model(self):
        """
        Process the job queue.

        Call this repeatedly.
        """
        self.job_manager_model.work_on_queue(self.socket)

    def read_from_socket(self):
        """
        Process data when it's ready to be read fomr the socket.

        We expect to get data in the form of json dumped dictionaries
        like:

        .. code-block:: none

            {
                "purpose": "job_comms",
                "body": {
                    "job_id": 123456,
                    "outcome": {
                        "success": False,
                        "data": 34,
                        "message": "Ya dun goofed"
                    }
                }
            }
        
        .. code-block:: none

            {
                "purpose": "display_update",
                "body": {
                    "head": "4561",
                    "program_name": "FIBB"
                }
            }

        We never know how many bytes of data are ready in the read
        buffer, so the logic/statefulness has to account for that.
        """

        while True:
            if self.waiting_for == "header":
                num_bytes_available = self.socket.bytesAvailable()
                if num_bytes_available < 2:
                    print(f"Waiting for header data, only {num_bytes_available} bytes available, need 2.")
                    break
                else:
                    header_bytes = self.socket.read(2)
                    self.num_data_bytes = int.from_bytes(
                        header_bytes,
                        byteorder="big"
                    )
                    print(f"Decoded header, data is {self.num_data_bytes} bytes long")

                    if self.num_data_bytes == 0:
                        print("No data in transmission, waiting for next")
                        self.waiting_for = "header"
                    else:
                        self.waiting_for = "data"

            if self.waiting_for == "data":
                num_bytes_available = self.socket.bytesAvailable()
                if num_bytes_available < self.num_data_bytes:
                    print(f"Waiting for main data, only {num_bytes_available} bytes are available, need {self.num_data_bytes}.")
                    break
                else:
                    data_bytes = self.socket.read(self.num_data_bytes)
                    data_str = data_bytes.decode("ascii")
                    data = json.loads(data_str)
                    print(f"Decoded main data: {data}")
                    self.waiting_for = "header"

                    if not isinstance(data, dict):
                        print(f"Recieved invalid datatype - needs to be a dict.")
                        break

                    if "purpose" not in data:
                        print(f"'purpose' key not in data.")
                        break

                    if "body" not in data:
                        print(f"'body' key not in data.")
                        break

                    purpose = data["purpose"]
                    if purpose == "job_comms":
                        self.process_job_comms(data["body"])
                    elif purpose == "display_update":
                        self.process_display_update(data["body"])
                    else:
                        print(f"Unknown purpose: {purpose}")

                    # back around to the top in case there's another header ready to be read

    def process_job_comms(self, body):
        """
        Handle some data being sent back to a job call.

        Args:
            body (dict): The body of the message sent from the Pico.
        """
        if "job_id" not in body:
            print(f"'job_id' key not in body.")
            return

        if "outcome" not in body:
            print(f"'outcome' key not in body.")
            return

        if not isinstance(body["job_id"], int):
            print(f"Value for 'job_id' key is not an int.")
            return

        if not self.job_manager_model.job_id_exists(body["job_id"]):
            print(f"Job with job_id {body['job_id']} does not exist.")
        else:
            self.job_manager_model.relay_comms(body["job_id"], body["outcome"])

    def process_display_update(self, body):
        """
        Handle a display update

        Args:
            body (dict): The body of the message sent from the Pico with
                info about what needs to be displayed.
        """

        if "address" in body:
            self.address_view.set_value(body["address"])
        if "data" in body:
            self.data_view.set_value(body["data"])
        if "panel_mode" in body:
            self.run_control.run_mode_line_edit.setText(
                constants.PANEL_MODE_TO_NAME.get(
                    body["panel_mode"],
                    "Unknown mode"
                )
            )
        if "clock_source" in body:
            self.run_control.clock_mode_line_edit.setText(
                constants.CLOCK_MODE_TO_NAME.get(
                    body["clock_source"],
                    "Unknown mode"
                )
            )
        if "frequency" in body:
            self.run_control.custom_freq_display_line_edit.setText(
                str(body["frequency"])
            )

    def display_error(self, socket_error):
        """
        Show an error relating to the socket.
        """
        if socket_error == QtNetwork.QAbstractSocket.RemoteHostClosedError:
            pass
        elif socket_error == QtNetwork.QAbstractSocket.HostNotFoundError:
            QtWidgets.QMessageBox.information(
                self,
                "SBC Connect",
                (
                    "The host was not found. Please check the IP and "
                    "port settings."
                )
            )
        elif socket_error == QtNetwork.QAbstractSocket.ConnectionRefusedError:
            QtWidgets.QMessageBox.information(
                self,
                "SBC Connect",
                (
                    "The connection was refused by the peer. Make sure the "
                    "SBC Pico is running, and check that the IP "
                    "and port settings are correct."
                )
            )
        else:
            QtWidgets.QMessageBox.information(
                self,
                "SBC Connect",
                f"The following error occurred: {self.socket.errorString()}"
            )

    def state_changed(self, state):
        """
        React to the state of the socket changing
        """
        print(f"Socket state changed: {decode_state(state)}")

    def socket_connected(self):
        """
        Handle the sockect connection to the Pico being made.
        """
        self.connect_control.connect_button.setEnabled(False)
        self.connect_control.disconnect_button.setEnabled(True)
        self.input_box.setEnabled(True)
        self.address_view_box.setEnabled(True)
        self.head_control_box.setEnabled(True)
        self.data_view_box.setEnabled(True)
        self.run_control_box.setEnabled(True)
        self.assembler.assemble_and_send_button.setEnabled(True)
        self.batch_mem_read_writer.send_button.setEnabled(True)
        self.batch_mem_read_writer.send_selected_button.setEnabled(True)
        self.job_queue_timer.start()
        self.waiting_for = "header"

    def socket_disconnected(self):
        """
        Handle the sockect connection to the Pico being broken.
        """
        self.connect_control.connect_button.setEnabled(True)
        self.connect_control.disconnect_button.setEnabled(False)
        self.input_box.setEnabled(False)
        self.address_view_box.setEnabled(False)
        self.head_control_box.setEnabled(False)
        self.data_view_box.setEnabled(False)
        self.run_control_box.setEnabled(False)
        self.assembler.assemble_and_send_button.setEnabled(False)
        self.batch_mem_read_writer.send_button.setEnabled(False)
        self.batch_mem_read_writer.send_selected_button.setEnabled(False)
        self.job_queue_timer.stop()
        self.waiting_for = "header"


def decode_state(state):
    """
    Decode a network state.

    https://doc.qt.io/qtforpython-6/PySide6/QtNetwork/QAbstractSocket.html#PySide6.QtNetwork.QAbstractSocket.SocketState

    Args:
        state (QtNetwork.QAbstractSocket.SocketState): The state to be
            decoded.
    Returns:
        str: Human readable state.
    """
    if state == QtNetwork.QAbstractSocket.UnconnectedState:
        return "The socket is not connected."
    elif state == QtNetwork.QAbstractSocket.HostLookupState:
        return "The socket is performing a host name lookup."
    elif state == QtNetwork.QAbstractSocket.ConnectingState:
        return "The socket has started establishing a connection."
    elif state == QtNetwork.QAbstractSocket.ConnectedState:
        return "A connection is established."
    elif state == QtNetwork.QAbstractSocket.BoundState:
        return "The socket is bound to an address and port."
    elif state == QtNetwork.QAbstractSocket.ClosingState:
        return "The socket is about to close (data may still be waiting to be written)."
    elif state == QtNetwork.QAbstractSocket.ListeningState:
        return "For internal use only."
    else:
        return "Unknown state"


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    sys.exit(main.exec_())