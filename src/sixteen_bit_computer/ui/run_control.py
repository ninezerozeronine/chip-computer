from PyQt5 import QtGui, QtCore, QtWidgets

class RunControl(QtWidgets.QWidget):
    """
    Widget to control the running of the machine
    """
    def __init__(self, parent=None):
        """
        Initialise class.
        """
        super().__init__(parent=parent)

        run_mode_label = QtWidgets.QLabel("Run mode:")
        self.run_mode_line_edit = QtWidgets.QLineEdit()
        self.run_mode_line_edit.setReadOnly(True)
        run_display_layout = QtWidgets.QHBoxLayout()
        run_display_layout.addWidget(run_mode_label)
        run_display_layout.addWidget(self.run_mode_line_edit)

        self.run_button = QtWidgets.QPushButton("Run")
        self.step_button = QtWidgets.QPushButton("Step")
        self.stop_button = QtWidgets.QPushButton("Stop")
        run_buttons_layout = QtWidgets.QHBoxLayout()
        run_buttons_layout.addWidget(self.run_button)
        run_buttons_layout.addWidget(self.step_button)
        run_buttons_layout.addWidget(self.stop_button)

        num_steps_label = QtWidgets.QLabel("Num steps:")
        self.num_steps_line_edit = QtWidgets.QLineEdit("1")
        self.num_steps_line_edit.setValidator(QtGui.QIntValidator(1, 1000))
        steps_choose_layout = QtWidgets.QHBoxLayout()
        steps_choose_layout.addWidget(num_steps_label)
        steps_choose_layout.addWidget(self.num_steps_line_edit)

        self.half_step_button = QtWidgets.QPushButton("Half Steps")
        self.full_step_button = QtWidgets.QPushButton("Full Steps")
        step_buttons_layout = QtWidgets.QHBoxLayout()
        step_buttons_layout.addWidget(self.half_step_button)
        step_buttons_layout.addWidget(self.full_step_button)

        self.reset_button = QtWidgets.QPushButton("Reset")

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(QtCore.QMargins(0,0,0,0))
        main_layout.addLayout(run_display_layout)
        main_layout.addLayout(run_buttons_layout)
        main_layout.addLayout(steps_choose_layout)
        main_layout.addLayout(step_buttons_layout)
        main_layout.addWidget(self.reset_button)

        self.setLayout(main_layout)

