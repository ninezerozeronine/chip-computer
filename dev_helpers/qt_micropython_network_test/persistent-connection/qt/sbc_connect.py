from PyQt5 import QtGui, QtCore, QtWidgets, QtNetwork
from functools import partial
import json
 
class SBCConnect(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SBCConnect, self).__init__(parent)
 
        self.header_read = False
        self.num_message_bytes = 0
        self.in_socket = None
        self.header_read = False
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
        
        message_label = QtWidgets.QLabel("Message:")
        self.message_line_edit = QtWidgets.QLineEdit("Hello!")
        message_label.setBuddy(self.message_line_edit)

        connect_layout = QtWidgets.QGridLayout()
        connect_layout.addWidget(host_label, 0, 0)
        connect_layout.addWidget(self.host_line_edit, 0, 1)
        connect_layout.addWidget(port_label, 1, 0)
        connect_layout.addWidget(self.port_line_edit, 1, 1)
        connect_layout.addWidget(message_label, 2, 0)
        connect_layout.addWidget(self.message_line_edit, 2, 1)

        # Connect
        self.connect_button = QtWidgets.QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect)

        self.disconnect_button = QtWidgets.QPushButton("Disconnect")
        self.disconnect_button.clicked.connect(self.socket.disconnectFromHost)
        self.disconnect_button.setEnabled(False)

        # Send
        self.send_button = QtWidgets.QPushButton("Send")
        self.send_button.clicked.connect(self.send)
        self.send_button.setEnabled(False)

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
        main_layout.addWidget(self.send_button)
        main_layout.addLayout(quit_layout)

        self.setLayout(main_layout)

        self.setWindowTitle("SBC Connect")
        self.port_line_edit.setFocus()

 
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
        self.send_button.setEnabled(True)
        self.connect_button.setEnabled(False)
        self.disconnect_button.setEnabled(True)
        self.header_read = False

    def socket_disconnected(self):
        self.send_button.setEnabled(False)
        self.connect_button.setEnabled(True)
        self.disconnect_button.setEnabled(False)
        self.header_read = False

    def state_changed(self, state):
        print(f"Socket state changed: {decode_state(state)}")

    def read_from_socket(self):
        """

        """

        if not self.header_read:
            if self.socket.bytesAvailable() < 2:
                return

            self.num_message_bytes = int.from_bytes(
                self.socket.read(2),
                byteorder="big"
            )
            self.header_read = True

        if self.num_message_bytes == 0:
            print("No data in transmission, waiting for next")
            self.header_read = False
 
        num_available = self.socket.bytesAvailable()
        if num_available < self.num_message_bytes:
            print(f"Only {num_available} bytes are available, waiting for {self.num_message_bytes}")
            return

        data_str = self.socket.read(self.num_message_bytes).decode("ascii")
        data = json.loads(data_str)
        print(f"recieved {data}")
        self.header_read = False

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