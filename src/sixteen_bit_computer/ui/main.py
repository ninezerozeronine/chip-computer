import sys
import json

from PyQt5 import QtGui, QtCore, QtWidgets, QtNetwork

from .value_edit import ValueEdit
from .value_view import ValueView
from .run_control import RunControl
from .head_control import HeadControl
from .connect_control import ConnectControl
from .job_manager_model import JobManagerModel
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
        self.job_queue_timer.start()

        self.build_ui()
        self.connect_ui()

        self.setWindowTitle("SBC Connect")


    def build_ui(self):
        """
        Create UI widgets and add them to layouts.
        """
        connect_box = QtWidgets.QGroupBox("Connection")
        connect_layout = QtWidgets.QVBoxLayout()
        self.connect_control = ConnectControl()
        connect_layout.addWidget(self.connect_control)
        connect_box.setLayout(connect_layout)

        self.input_box = QtWidgets.QGroupBox("Input")
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
        self.address_layout = QtWidgets.QVBoxLayout()
        self.address_view = ValueView()
        self.address_layout.addWidget(self.address_view)
        self.address_view_box.setLayout(self.address_layout)

        self.data_view_box = QtWidgets.QGroupBox("Data")
        self.data_layout = QtWidgets.QVBoxLayout()
        self.data_view = ValueView()
        self.data_layout.addWidget(self.data_view)
        self.data_view_box.setLayout(self.data_layout)

        self.head_control_box = QtWidgets.QGroupBox("Head Control")
        self.head_control_layout = QtWidgets.QVBoxLayout()
        self.head_control = HeadControl()
        self.head_control_layout.addWidget(self.head_control)
        self.head_control_layout.addStretch()
        self.head_control_box.setLayout(self.head_control_layout)   

        self.run_control_box = QtWidgets.QGroupBox("Run Control")
        self.run_control_layout = QtWidgets.QVBoxLayout()
        self.run_control = RunControl()
        self.run_control_layout.addWidget(self.run_control)
        self.run_control_box.setLayout(self.run_control_layout)

        self.main_layout = QtWidgets.QGridLayout()
        self.main_layout.addWidget(connect_box, 0, 0, 1, 2)
        self.main_layout.addWidget(self.input_box, 1, 0)
        self.main_layout.addWidget(self.address_view_box, 1, 1)
        self.main_layout.addWidget(self.head_control_box, 2, 0)
        self.main_layout.addWidget(self.data_view_box, 2, 1)
        self.main_layout.addWidget(self.run_control_box, 3, 0, 1, 2)

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
        # self.run_control.half_step_button.clicked.connect(self.send_half_steps)
        # self.run_control.full_step_button.clicked.connect(self.send_full_steps)
        # self.run_control.reset_button.pressed.connect(self.press_reset)
        # self.run_control.reset_button.released.connect(self.release_reset)

        self.run_control.clock_mode_crystal_button.clicked.connect(
            self.set_clock_to_crystal
        )
        self.run_control.clock_mode_custom_button.clicked.connect(
            self.set_clock_to_custom
        )
        # self.run_control.custom_freq_set_button.clicked.connect(self.set_custom_freq)
        # self.run_control.load_program_button.clicked.connect(self.load_program)

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
        job = Job("decr_head", kwargs={"get_word":get_word})
        self.job_manager_model.sumbit_job(job)

    def set_head(self):
        """
        Set the location of the read/write head to the current input
        """
        get_word = self.head_control.get_word_on_head_change_checkbox.isChecked()
        job = Job(
            "set_head",
            args=[self.input_widget.value],
            kwargs={"get_word":get_word}
        )
        self.job_manager_model.sumbit_job(job)

    def incr_head(self):
        """
        Increment the read write head, optionally reading the word at
        the new location.
        """
        get_word = self.head_control.get_word_on_head_change_checkbox.isChecked()
        job = Job("incr_head", kwargs={"get_word":get_word})
        self.job_manager_model.sumbit_job(job)

    def set_word(self):
        """
        Set the word at the current read write head position to the
        value in the input.
        """
        job = Job("set_data", args=[self.input_widget.value])
        self.job_manager_model.sumbit_job(job)

    def get_word(self):
        """
        Get the word at the current read write head position.
        """
        job = Job("get_word_at_current_head")
        self.job_manager_model.sumbit_job(job)

    def set_mode_to_run(self):
        """
        Set mode to run mode
        """
        job = Job("set_mode_to_run")
        self.job_manager_model.sumbit_job(job)

    def set_mode_to_step(self):
        """
        Set mode to step
        """
        job = Job("set_mode_to_step")
        self.job_manager_model.sumbit_job(job)

    def set_mode_to_stop(self):
        """
        Set mode to stop
        """
        job = Job("set_mode_to_stop")
        self.job_manager_model.sumbit_job(job)

    def send_half_steps(self):
        """
        Send the number of half steps specified by the user
        """
        job = Job(
            "half_steps",
            kwargs={
                "num_steps": int(self.num_steps_line_edit.text())
            }
        )
        self.job_manager_model.sumbit_job(job)

    def send_full_steps(self):
        """
        Send the number of full steps specified by the user
        """
        job = Job(
            "full_steps",
            kwargs={
                "num_steps": int(self.num_steps_line_edit.text())
            }
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
        pass

    def load_program(self):
        """
        Load the program selected in the combobox.
        """
        pass


    def run_job_manager_model(self):
        self.job_manager_model.work_on_queue(self.socket)


    def read_from_socket(self):
        """

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

    def process_display_update(self, data):
        if "address" in data:
            self.address_view.set_value(data["address"])
        if "data" in data:
            self.data_view.set_value(data["data"])
        if "panel_mode" in data:
            self.run_control.run_mode_line_edit.setText(
                constants.PANEL_MODE_TO_NAME.get(
                    data["panel_mode"],
                    "Unknown mode"
                )
            )
        if "clock_source" in data:
            self.run_control.clock_mode_line_edit.setText(
                constants.CLOCK_MODE_TO_NAME.get(
                    data["clock_source"],
                    "Unknown mode"
                )
            )
        if "frequency" in data:
            self.run_control.custom_freq_display_line_edit.setText(
                str(data["frequency"])
            )

    def display_error(self, socket_error):
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
        print(f"Socket state changed: {decode_state(state)}")



    def socket_connected(self):
        self.connect_control.connect_button.setEnabled(False)
        self.connect_control.disconnect_button.setEnabled(True)
        self.input_box.setEnabled(True)
        self.address_view_box.setEnabled(True)
        self.head_control_box.setEnabled(True)
        self.data_view_box.setEnabled(True)
        self.run_control_box.setEnabled(True)
        self.job_queue_timer.start()
        self.header_read = False

    def socket_disconnected(self):
        self.connect_control.connect_button.setEnabled(True)
        self.connect_control.disconnect_button.setEnabled(False)
        self.input_box.setEnabled(False)
        self.address_view_box.setEnabled(False)
        self.head_control_box.setEnabled(False)
        self.data_view_box.setEnabled(False)
        self.run_control_box.setEnabled(False)
        self.job_queue_timer.stop()
        self.header_read = False






def decode_state(state):
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