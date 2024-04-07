from PyQt5 import QtGui, QtCore, QtWidgets, QtNetwork
from functools import partial
import json
 
class SBCConnect(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SBCConnect, self).__init__(parent)
 
        self.header_read = False
        self.num_message_bytes = 0
        self.in_socket = None
 
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

        # Control buttons
        send_button = QtWidgets.QPushButton("Send")
        send_button.clicked.connect(self.send)

        #Quit
        quit_button = QtWidgets.QPushButton("Quit")
        quit_button.clicked.connect(self.close)
        quit_layout = QtWidgets.QHBoxLayout()
        quit_layout.addStretch(1)
        quit_layout.addWidget(quit_button)
 
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(connect_layout)
        main_layout.addWidget(send_button)
        main_layout.addLayout(quit_layout)

        self.setLayout(main_layout)
 
        self.tcpSocket = QtNetwork.QTcpSocket(self)
        self.tcpSocket.error.connect(self.display_error)
        self.tcpSocket.stateChanged.connect(decode_state)
 
        self.setWindowTitle("SBC Connect")
        self.port_line_edit.setFocus()

        self.tcpServer = QtNetwork.QTcpServer(self)
        if not self.tcpServer.listen():
            QtWidgets.QMessageBox.critical(self, "SBC Connect",
                    "Unable to start the server: %s." % self.tcpServer.errorString())
            self.close()
            return
 
        print(f"The server is running on port {self.tcpServer.serverPort()}")
        self.tcpServer.newConnection.connect(self.handle_connection)
 

    def handle_connection(self):
        """

        """
        self.header_read = False
        self.num_message_bytes = 0
        self.in_socket = self.tcpServer.nextPendingConnection()
        if self.in_socket is None:
            print("NextPendingConnection was None.")
            return
        self.in_socket.readyRead.connect(self.handle_data)
        self.in_socket.disconnected.connect(self.in_socket.deleteLater)
 
    def handle_data(self):
        """

        """
        print("Handling data")
        if not self.header_read:
            if self.in_socket.bytesAvailable() < 2:
                print("< 2 bytes available")
                return

        self.num_message_bytes = int.from_bytes(
            self.in_socket.read(2),
            byteorder="big"
        )
        self.header_read = True

        if self.num_message_bytes == 0:
            print("Empty message, closing socket")
            self.in_socket.disconnectFromHost()
 
        num_available = self.in_socket.bytesAvailable()
        if num_available < self.num_message_bytes:
            print(f"< {self.num_message_bytes} bytes available. {num_available} are available")
            return
 
        message = self.in_socket.read(self.num_message_bytes).decode("ascii")
        print(f"Recieved {message}")
        self.in_socket.disconnectFromHost()

    def send(self):
        """

        """
        print("Send A")
        try:
            self.tcpSocket.connected.disconnect()
        except TypeError:
            print("Nothing was connected in send_A")
        self.tcpSocket.connectToHost(
            self.host_line_edit.text(),
            int(self.port_line_edit.text())
        )
        # print(decode_state(self.tcpSocket.state()))
        self.tcpSocket.connected.connect(self.send_data)

    def send_data(self):
        message = self.message_line_edit.text()

        data = {
            "ret_prt": self.tcpServer.serverPort(),
            "msg": message
        }
        data_str=json.dumps(data)




        print(f"Sending {data_str}")
        # block = QtCore.QByteArray()
        # out = QtCore.QDataStream(block, QtCore.QIODevice.WriteOnly)
        # out.setVersion(QtCore.QDataStream.Qt_4_0)
        # bytes_to_send = bytes(data, encoding='ascii')
        # out.writeString(bytes_to_send)
        to_send = bytearray(2)
        msg_bytes = bytes(data_str, encoding="ascii")
        to_send.extend(msg_bytes)
        uint16_len_bytes = len(msg_bytes).to_bytes(2, byteorder="big", signed=False)
        to_send[0] = uint16_len_bytes[0]
        to_send[1] = uint16_len_bytes[1]

        self.tcpSocket.write(to_send)
        self.tcpSocket.disconnectFromHost()

        try:
            self.tcpSocket.connected.disconnect()
        except TypeError:
            print("Nothing was connected in send_data")


    # def requestNewFortune(self):
    #     self.getFortuneButton.setEnabled(False)
    #     self.blockSize = 0
    #     self.tcpSocket.abort()
    #     self.tcpSocket.connectToHost(self.hostLineEdit.text(),
    #             int(self.portLineEdit.text()))
 
    # def readFortune(self):
    #     instr = QtCore.QDataStream(self.tcpSocket)
    #     instr.setVersion(QtCore.QDataStream.Qt_4_0)
 
    #     if self.blockSize == 0:
    #         if self.tcpSocket.bytesAvailable() < 2:
    #             return
 
    #     self.blockSize = instr.readUInt16()
 
    #     if self.tcpSocket.bytesAvailable() < self.blockSize:
    #         return
 
    #     nextFortune = instr.readString()
 
    #     try:
    #         # Python v3.
    #         nextFortune = str(nextFortune, encoding='ascii')
    #     except TypeError:
    #         # Python v2.
    #         pass
 
    #     if nextFortune == self.currentFortune:
    #         QtCore.QTimer.singleShot(0, self.requestNewFortune)
    #         return
 
    #     self.currentFortune = nextFortune
    #     self.statusLabel.setText(self.currentFortune)
    #     self.getFortuneButton.setEnabled(True)
 
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
                    "The following error occurred: %s." % self.tcpSocket.errorString())
 
def decode_state(state):
    if state == QtNetwork.QAbstractSocket.UnconnectedState:
        print("The socket is not connected.")
    elif state == QtNetwork.QAbstractSocket.HostLookupState:
        print("The socket is performing a host name lookup.")
    elif state == QtNetwork.QAbstractSocket.ConnectingState:
        print("The socket has started establishing a connection.")
    elif state == QtNetwork.QAbstractSocket.ConnectedState:
        print("A connection is established.")
    elif state == QtNetwork.QAbstractSocket.BoundState:
        print("The socket is bound to an address and port.")
    elif state == QtNetwork.QAbstractSocket.ClosingState:
        print("The socket is about to close (data may still be waiting to be written).")
    elif state == QtNetwork.QAbstractSocket.ListeningState:
        print("For internal use only.")
    else:
        print("Unknown state")


if __name__ == '__main__':
 
    import sys
 
    app = QtWidgets.QApplication(sys.argv)
    server = SBCConnect()
    sys.exit(server.exec_())