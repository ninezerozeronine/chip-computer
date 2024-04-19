from PyQt5 import QtGui, QtCore, QtWidgets, QtNetwork
from functools import partial
import json

from . import job_mod
from . import sequential_job_manager


class SBCConnect(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SBCConnect, self).__init__(parent)
 
        self.waiting_for = "header"
        self.num_data_bytes = 0
        self.socket = QtNetwork.QTcpSocket(self)
        self.socket.readyRead.connect(self.read_from_socket)
        self.socket.error.connect(self.display_error)
        self.socket.stateChanged.connect(self.state_changed)
        self.socket.connected.connect(self.socket_connected)
        self.socket.disconnected.connect(self.socket_disconnected)


        # Connection details
        host_label = QtWidgets.QLabel("Pico IP:")
        self.host_line_edit = QtWidgets.QLineEdit("192.168.1.XXX")
        host_label.setBuddy(self.host_line_edit)

        port_label = QtWidgets.QLabel("Pico port:")
        self.port_line_edit = QtWidgets.QLineEdit("8888")
        self.port_line_edit.setValidator(QtGui.QIntValidator(1, 65535, self))
        port_label.setBuddy(self.port_line_edit)
        
        # message_label = QtWidgets.QLabel("Message:")
        # self.message_line_edit = QtWidgets.QLineEdit("Hello!")
        # message_label.setBuddy(self.message_line_edit)

        connect_layout = QtWidgets.QGridLayout()
        connect_layout.addWidget(host_label, 0, 0)
        connect_layout.addWidget(self.host_line_edit, 0, 1)
        connect_layout.addWidget(port_label, 1, 0)
        connect_layout.addWidget(self.port_line_edit, 1, 1)
        # connect_layout.addWidget(message_label, 2, 0)
        # connect_layout.addWidget(self.message_line_edit, 2, 1)

        # Connect
        self.connect_button = QtWidgets.QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect)

        self.disconnect_button = QtWidgets.QPushButton("Disconnect")
        self.disconnect_button.clicked.connect(self.socket.disconnectFromHost)
        self.disconnect_button.setEnabled(False)

        # Send
        # self.send_button = QtWidgets.QPushButton("Send")
        # self.send_button.clicked.connect(self.send)
        # self.send_button.setEnabled(False)

        # Char send
        char_label = QtWidgets.QLabel("Character:")
        self.char_line_edit = QtWidgets.QLineEdit()
        self.char_send_button = QtWidgets.QPushButton("Send")
        self.char_send_button.clicked.connect(self.send_char)
        char_layout = QtWidgets.QHBoxLayout()
        char_layout.addWidget(char_label)
        char_layout.addWidget(self.char_line_edit)
        char_layout.addWidget(self.char_send_button)

        # LED control
        self.led_on_button = QtWidgets.QPushButton("LED On")
        self.led_on_button.clicked.connect(partial(self.set_led, True))
        self.led_off_button = QtWidgets.QPushButton("LED Off")
        self.led_off_button.clicked.connect(partial(self.set_led, False))
        led_on_off_layout = QtWidgets.QHBoxLayout()
        led_on_off_layout.addWidget(self.led_on_button)
        led_on_off_layout.addWidget(self.led_off_button)

        # user_input
        user_input_label = QtWidgets.QLabel("User input:")
        self.user_input_line_edit = QtWidgets.QLineEdit()
        self.user_input_line_edit.setReadOnly(True)
        user_input_layout = QtWidgets.QHBoxLayout()
        user_input_layout.addWidget(user_input_label)
        user_input_layout.addWidget(self.user_input_line_edit)

        # Pin State
        pinstate_label = QtWidgets.QLabel("Pin State:")
        self.pinstate_line_edit = QtWidgets.QLineEdit()
        self.pinstate_line_edit.setReadOnly(True)
        self.pinstate_send_button = QtWidgets.QPushButton("Get")
        self.pinstate_send_button.clicked.connect(self.get_pinstate)
        pinstate_layout = QtWidgets.QHBoxLayout()
        pinstate_layout.addWidget(pinstate_label)
        pinstate_layout.addWidget(self.pinstate_line_edit)
        pinstate_layout.addWidget(self.pinstate_send_button)

        # Add job
        # add_job_button = QtWidgets.QPushButton("Add job")
        # add_job_button.clicked.connect(self.make_job)

        # Cancel selected job
        cancel_job_button = QtWidgets.QPushButton("Cancel selected jobs")
        cancel_job_button.clicked.connect(self.cancel_selected_jobs)

        # Table
        self.job_manager_model = SequentialJobManagerModel()
        self.job_table = QtWidgets.QTableView()
        self.job_table.setModel(self.job_manager_model)
        self.job_table.verticalHeader().hide()

        # Quit
        quit_button = QtWidgets.QPushButton("Quit")
        quit_button.clicked.connect(self.close)
        quit_layout = QtWidgets.QHBoxLayout()
        quit_layout.addStretch(1)
        quit_layout.addWidget(quit_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(connect_layout)
        main_layout.addWidget(self.connect_button)
        main_layout.addWidget(self.disconnect_button)
        main_layout.addLayout(char_layout)
        main_layout.addLayout(led_on_off_layout)
        main_layout.addLayout(user_input_layout)
        main_layout.addLayout(pinstate_layout)
        # main_layout.addWidget(self.send_button)
        # main_layout.addWidget(add_job_button)
        main_layout.addWidget(cancel_job_button)
        main_layout.addWidget(self.job_table)
        main_layout.addLayout(quit_layout)

        self.setLayout(main_layout)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.work_on_top_job)
        self.timer.start()

        self.setWindowTitle("SBC Connect")
        self.port_line_edit.setFocus()

    def get_pinstate(self):
        job = job_mod.Job("read_pin_state")
        job.complete_callback = self.pinstate_complete
        self.job_manager_model.sumbit_job(job)

    def pinstate_complete(self, outcome):
        self.pinstate_line_edit.setText(str(outcome.data))

    def set_led(self, state):
        job = job_mod.Job("set_led_state", args=[state])
        self.job_manager_model.sumbit_job(job)

    def send_char(self):
        char = self.char_line_edit.text()
        if char:
            char = char[0]
            job = job_mod.Job("set_user_input_char", args=[char])
            self.job_manager_model.sumbit_job(job)

    def work_on_top_job(self):
        # if self.socket.state() == QtNetwork.QAbstractSocket.ConnectedState
        self.job_manager_model.work_on_top_job(self.socket)

    # def make_job(self):
    #     job = job_mod.Job(self.message_line_edit.text())
    #     self.job_manager_model.sumbit_job(job)

    def cancel_selected_jobs(self):
        row_indexes_to_cancel = [
            index.row()
            for index in self.job_table.selectedIndexes()
        ]
        self.job_manager_model.cancel_jobs_in_rows(row_indexes_to_cancel)

 
    def connect(self):
        state = self.socket.state()
        if state != QtNetwork.QAbstractSocket.UnconnectedState:
            print("Cannot connect - socket is in incorrect state, state is:")
            print(decode_state(state))
        else:
            self.socket.connectToHost(
                self.host_line_edit.text(),
                int(self.port_line_edit.text())
            )
        # print(decode_state(self.socket.state()))
        # self.socket.connected.connect(self.send_data)

    def socket_connected(self):
        # self.send_button.setEnabled(True)
        self.connect_button.setEnabled(False)
        self.disconnect_button.setEnabled(True)
        self.header_read = False

    def socket_disconnected(self):
        # self.send_button.setEnabled(False)
        self.connect_button.setEnabled(True)
        self.disconnect_button.setEnabled(False)
        self.header_read = False

    def state_changed(self, state):
        print(f"Socket state changed: {decode_state(state)}")

    def read_from_socket(self):
        """

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

                    purpose = data["purpose"]
                    if purpose == "job_comms":
                        self.process_job_comms(data)
                    elif purpose == "panel_display_update":
                        self.process_panel_update(data)
                    else:
                        print(f"Unknown purpose: {purpose}")

                    # back around to the top in case there's another header ready to be read


    def process_job_comms(self, data):
        if "body" not in data:
            print(f"'body' key not in data for.")
            return

        body = data["body"]

        if "job_id" not in body:
            print(f"'job_id' key not in body.")
            return

        if "outcome" not in body:
            print(f"'outcome' key not in body.")
            return

        if not isinstance(body["job_id"], int):
            print(f"Value for 'job_id' key is not an int.")
            return

        # if not self.job_manager_model.job_id_exists(body["job_id"]):
        #     print(f"Job with job_id {body['job_id']} does not exist.")
        #     return

        self.job_manager_model.relay_comms(body["job_id"], body["outcome"])

    def process_panel_update(self, data):
        if "body" not in data:
            print(f"'body' key not in data.")
            return

        self.user_input_line_edit.setText(data["body"]["user_input"])


    def send(self):
        """

        """
        if self.socket.state() != QtNetwork.QAbstractSocket.ConnectedState:
            print("Cant send - socket not connected")
        else:
            message = self.message_line_edit.text()
            data = {
                "msg": message
            }
            data_str=json.dumps(data)
            print(f"Sending {data_str}")
            to_send = bytearray(2)
            msg_bytes = bytes(data_str, encoding="ascii")
            to_send.extend(msg_bytes)
            uint16_len_bytes = len(msg_bytes).to_bytes(2, byteorder="big", signed=False)
            to_send[0] = uint16_len_bytes[0]
            to_send[1] = uint16_len_bytes[1]
            num_bytes_to_send = len(to_send)
            num_bytes_sent = self.socket.write(to_send)
            print(f"Wanted to send {num_bytes_to_send} bytes, actually sent {num_bytes_sent}")

 
    def display_error(self, socketError):
        if socketError == QtNetwork.QAbstractSocket.RemoteHostClosedError:
            pass
        elif socketError == QtNetwork.QAbstractSocket.HostNotFoundError:
            QtWidgets.QMessageBox.information(self, "Fortune Client",
                    "The host was not found. Please check the host name and "
                    "port settings.")
        elif socketError == QtNetwork.QAbstractSocket.ConnectionRefusedError:
            QtWidgets.QMessageBox.information(self, "Fortune Client",
                    "The connection was refused by the peer. Make sure the "
                    "fortune server is running, and check that the host name "
                    "and port settings are correct.")
        else:
            QtWidgets.QMessageBox.information(self, "Fortune Client",
                    "The following error occurred: %s." % self.socket.errorString())


class SequentialJobManagerModel(QtCore.QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.manager = sequential_job_manager.SequentialJobManager()

    def rowCount(self, index):
        return self.manager.num_jobs()

    def columnCount(self, index):
        return job_mod.Job.get_num_columns()

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self.manager.get_table_data(index.row(), index.column())

    def headerData(self, index, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return job_mod.Job.get_header_data(index)

    def sumbit_job(self, job):
        num_jobs = self.manager.num_jobs()
        self.beginInsertRows(QtCore.QModelIndex(), num_jobs+1, num_jobs+1)
        job_id = self.manager.sumbit_job(job)
        self.endInsertRows()
        return job_id

    def cancel_job(self, job_id):
        self.manager.cancel_job(job_id)
        row = self.manager.job_id_to_row_index(job_id)
        self.dataChanged.emit(
            self.createIndex(row, 0),
            self.createIndex(row, job_mod.Job.get_num_columns())
        )

    def relay_comms(self, job_id, data):
        self.manager.relay_comms(job_id, data)
        row = self.manager.job_id_to_row_index(job_id)
        self.dataChanged.emit(
            self.createIndex(row, 0),
            self.createIndex(row, job_mod.Job.get_num_columns())
        )

    def work_on_top_job(self, socket):
        top_job_row_index = self.manager.top_job_row_index()
        made_change = self.manager.work_on_top_job(socket)
        if made_change:
            self.dataChanged.emit(
                self.createIndex(top_job_row_index, 0),
                self.createIndex(top_job_row_index, job_mod.Job.get_num_columns())
            )

    def cancel_jobs_in_rows(self, rows):
        for row in rows:
            self.cancel_job(self.manager.job_id_from_model_row(row))

    def id_exists(self, job_id):
        return self.manager.job_id_exists(job_id)



class TableModelTest(QtCore.QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.jobs = [
            {
                "id":"abc123",
                "msg": "foo",
                "state": "COMPLETE",
            },
            {
                "id":"def456",
                "msg": "bar",
                "state": "SENT",
            },
            {
                "id":"ghi789",
                "msg": "zip",
                "state": "NEW",
            },
            {
                "id":"jkl123",
                "msg": "mon",
                "state": "COMPLETE",
            },
            {
                "id":"mno456",
                "msg": "wip",
                "state": "NEW",
            },
        ]
        self.column_index_to_key = {
            0:"id",
            1:"msg",
            2:"state",
        }
        self.column_index_to_displayname = {
            0:"ID",
            1:"Message",
            2:"State",
        }

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self.jobs[index.row()][self.column_index_to_key[index.column()]]

    def rowCount(self, index):
        return len(self.jobs)

    def columnCount(self, index):
        return len(self.column_index_to_key)

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.column_index_to_displayname[section]

    def removeRows(self, start_row_index, num_rows, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(
            parent,
            start_row_index,
            start_row_index + num_rows - 1
        )
        for offset in reversed(range(num_rows)):
            del self.jobs[start_row_index + offset]
        self.endRemoveRows()
        return True

    def remove_first(self):
        if self.jobs:
            self.removeRows(0,1)

    def remove_first_hack(self):
        # If you do this - the selection doesn't move as
        # expected when removing a row.
        # Better to implement the removeRows method which
        # properly notifies the view to keep things in sync.
        if self.jobs:
            del self.jobs[0]
            self.layoutChanged.emit()

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
 
    import sys
 
    app = QtWidgets.QApplication(sys.argv)
    server = SBCConnect()
    sys.exit(server.exec_())