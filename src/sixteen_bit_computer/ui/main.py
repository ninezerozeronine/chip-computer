import sys

from PyQt5 import QtGui, QtCore, QtWidgets

from .value_edit import ValueEdit
from .value_view import ValueView

    




# class HexValidator(QtCore.QValidator):
#     def validate(self, curr_input, cursor_pos):
#         print(curr_input)







class Main(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.input_box = QtWidgets.QGroupBox("Input")
        self.input_layout = QtWidgets.QVBoxLayout()
        self.input_widget = ValueEdit()
        self.input_layout.addWidget(self.input_widget)
        self.input_box.setLayout(self.input_layout)

        self.head_view_box = QtWidgets.QGroupBox("Head")
        self.head_layout = QtWidgets.QVBoxLayout()
        self.head_view = ValueView()
        self.head_layout.addWidget(self.head_view)
        self.head_view_box.setLayout(self.head_layout)

        self.data_view_box = QtWidgets.QGroupBox("Data")
        self.data_layout = QtWidgets.QVBoxLayout()
        self.data_view = ValueView()
        self.data_layout.addWidget(self.data_view)
        self.data_view_box.setLayout(self.data_layout)

        # self.value_set = QtWidgets.QLineEdit()
        # self.value_set.setValidator(QtGui.QIntValidator(-32768, 65535, self))
        # self.value_set.textEdited.connect(self.convert_to_int_and_set)

        self.main_layout = QtWidgets.QGridLayout()
        self.main_layout.addWidget(self.input_box, 0, 0)
        self.main_layout.addWidget(self.head_view_box, 0, 1)
        self.main_layout.addWidget(self.data_view_box, 1, 1)
        #self.main_layout.addWidget(self.value_set, 1, 0)

        self.setLayout(self.main_layout)

    def convert_to_int_and_set(self, num_string):
        try:
            int(num_string)
        except:
            num_string = "0"

        self.data_view.set_value(int(num_string))
        self.head_view.set_value(int(num_string))
        self.bin_buttons.set_value(int(num_string))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    sys.exit(main.exec_())