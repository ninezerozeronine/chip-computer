import sys

from PyQt5 import QtGui, QtCore, QtWidgets

from .value_edit import ValueEdit
from .value_view import ValueView
from .run_control import RunControl
from .head_control import HeadControl
from .connect_control import ConnectControl
    
class Main(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        connect_box = QtWidgets.QGroupBox("Connection")
        connect_layout = QtWidgets.QVBoxLayout()
        self.connect_control = ConnectControl()
        connect_layout.addWidget(self.connect_control)
        connect_box.setLayout(connect_layout)

        self.input_box = QtWidgets.QGroupBox("Input")
        self.input_layout = QtWidgets.QVBoxLayout()
        self.input_widget = ValueEdit()
        self.input_widget.set_values(
            0,
            dec=True,
            hex_=True,
            bin_line=True,
            bin_buttons=True
        )
        self.input_layout.addWidget(self.input_widget)
        self.input_box.setLayout(self.input_layout)

        self.head_view_box = QtWidgets.QGroupBox("Head")
        self.head_layout = QtWidgets.QVBoxLayout()
        self.head_view = ValueView()
        self.head_layout.addWidget(self.head_view)
        self.head_view_box.setLayout(self.head_layout)

        self.data_view_box = QtWidgets.QGroupBox("Last read word")
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

        self.input_widget.value_changed.connect(self.head_view.set_value)
        self.input_widget.value_changed.connect(self.data_view.set_value)

        self.main_layout = QtWidgets.QGridLayout()
        self.main_layout.addWidget(connect_box, 0, 0, 1, 2)
        self.main_layout.addWidget(self.input_box, 1, 0)
        self.main_layout.addWidget(self.head_view_box, 1, 1)
        self.main_layout.addWidget(self.head_control_box, 2, 0)
        self.main_layout.addWidget(self.data_view_box, 2, 1)
        self.main_layout.addWidget(self.run_control_box, 3, 0, 1, 2)

        self.setLayout(self.main_layout)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    sys.exit(main.exec_())