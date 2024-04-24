from PyQt5 import QtGui, QtCore, QtWidgets

class ConnectControl(QtWidgets.QWidget):
    """
    Widget to control connecting to the computer.
    """
    def __init__(self, parent=None):
        """
        Initialise class.
        """
        super().__init__(parent=parent)

        ip_label = QtWidgets.QLabel("IP:")
        self.ip_line_edit = QtWidgets.QLineEdit()
        # This still lets invalid IPs through, but is better than
        # nothing for now.
        self.ip_line_edit.setValidator(
            QtGui.QRegularExpressionValidator(
                QtCore.QRegularExpression("[0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}")
            )
        )
        self.ip_line_edit.setText("192.168.1.231")
        port_label = QtWidgets.QLabel("Port:")
        self.port_line_edit = QtWidgets.QLineEdit()
        self.port_line_edit.setValidator(QtGui.QIntValidator(1, 65535))
        self.port_line_edit.setText("8888")
        self.connect_button = QtWidgets.QPushButton("Connect")
        self.disconnect_button = QtWidgets.QPushButton("Disconnect")
        self.disconnect_button.setEnabled(False)

        main_layout = QtWidgets.QGridLayout()
        main_layout.setContentsMargins(QtCore.QMargins(0,0,0,0))
        main_layout.addWidget(ip_label, 0, 0)
        main_layout.addWidget(self.ip_line_edit, 0, 1)
        main_layout.addWidget(port_label, 1, 0)
        main_layout.addWidget(self.port_line_edit, 1, 1)
        main_layout.addWidget(self.connect_button, 0, 2)
        main_layout.addWidget(self.disconnect_button, 1, 2)
        main_layout.setColumnStretch(1,1)

        self.setLayout(main_layout)
