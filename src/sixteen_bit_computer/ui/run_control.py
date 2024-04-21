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

        clock_mode_label = QtWidgets.QLabel("Clock mode:")

        self.clock_mode_combobox = QtWidgets.QComboBox()
        self.clock_mode_combobox.addItems(["Crystal", "Arbitrary"])
        arb_freq_label = QtWidgets.QLabel("Arb. clock freq. (Hz):")
        self.arb_freq_line_edit = QtWidgets.QLineEdit("10.0")
        self.arb_freq_line_edit.setValidator(
            QtGui.QDoubleValidator(0.1, 4000000, 1)
        )
        self.arb_freq_line_edit.setEnabled(False)
        self.set_arb_frq_button = QtWidgets.QPushButton("Set arb. freq.")

        program_label = QtWidgets.QLabel("Program:")
        self.program_combobox = QtWidgets.QComboBox()
        self.program_combobox.addItems(["Fibbonaci", "Dummy"])
        self.load_program_button = QtWidgets.QPushButton("Load")


        main_layout = QtWidgets.QGridLayout()
        main_layout.setContentsMargins(QtCore.QMargins(0,0,0,0))

        # main_layout.addWidget(widget, row, col, rowspan, colspan)
        # Left side
        main_layout.addWidget(run_mode_label, 0, 0, 1, 2)
        main_layout.addWidget(self.run_mode_line_edit, 0, 2, 1, 4)

        main_layout.addWidget(self.run_button, 1, 0, 1, 2)
        main_layout.addWidget(self.step_button, 1, 2, 1, 2)
        main_layout.addWidget(self.stop_button, 1, 4, 1, 2)

        main_layout.addWidget(num_steps_label, 2, 0, 1, 2)
        main_layout.addWidget(self.num_steps_line_edit, 2, 2, 1, 4)

        main_layout.addWidget(self.half_step_button, 3, 0, 1, 3)
        main_layout.addWidget(self.full_step_button, 3, 3, 1, 3)

        main_layout.addWidget(self.reset_button, 4, 0, 1, 6)

        # Right side
        main_layout.addWidget(clock_mode_label, 0, 6, 1, 2)
        main_layout.addWidget(self.clock_mode_combobox, 0, 8, 1, 4)

        main_layout.addWidget(arb_freq_label, 1, 6, 1, 2)
        main_layout.addWidget(self.arb_freq_line_edit, 1, 8, 1, 4)

        main_layout.addWidget(self.set_arb_frq_button, 2, 10, 1, 2)

        main_layout.addWidget(program_label, 3, 6, 1, 2)
        main_layout.addWidget(self.program_combobox, 3, 8, 1, 4)

        main_layout.addWidget(self.load_program_button, 4, 10, 1, 2)

        self.setLayout(main_layout)