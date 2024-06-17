from PyQt5 import Qt, QtGui, QtCore, QtWidgets

from ..network import job

class JobControl(QtWidgets.QWidget):
    """
    Display and manage the job queue.
    """
    def __init__(self, job_manager_model_ref, parent=None):
        """
        Initialise class.
        """
        super().__init__(parent=parent)

        self.job_manager_model_ref = job_manager_model_ref
        self.job_table = QtWidgets.QTableView()
        self.job_model_proxy = JobModelProxy()
        self.job_model_proxy.setSourceModel(self.job_manager_model_ref)
        self.job_table.setModel(self.job_model_proxy)
        self.job_table.horizontalHeader().setSectionsMovable(True)
        self.job_table.verticalHeader().hide()
        self.job_table.setSortingEnabled(True)

        self.cancel_selected_button = QtWidgets.QPushButton("Cancel Selected")
        self.cancel_selected_button.clicked.connect(self.cancel_selected)

        self.state_checkboxes = []
        for state in job.get_all_states():
            label = job.human_readable_state(state)
            checkbox = QtWidgets.QCheckBox(label)
            checkbox.setChecked(True)
            checkbox.filter_state = state
            checkbox.clicked.connect(self.update_state_filters)
            self.state_checkboxes.append(checkbox)

        self.state_filters_box = QtWidgets.QGroupBox("Job state filters")
        self.state_checkboxes_layout = QtWidgets.QVBoxLayout()
        for checkbox in self.state_checkboxes:
            self.state_checkboxes_layout.addWidget(checkbox)
        self.state_filters_box.setLayout(self.state_checkboxes_layout)

        self.controls_layout = QtWidgets.QHBoxLayout()
        self.controls_layout.addWidget(self.state_filters_box)
        self.controls_layout.addStretch()
        self.cancel_layout = QtWidgets.QVBoxLayout()
        self.cancel_layout.addStretch()
        self.cancel_layout.addWidget(self.cancel_selected_button)
        self.controls_layout.addLayout(self.cancel_layout)
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.job_table)
        main_layout.addLayout(self.controls_layout)
        main_layout.setStretch(0, 2)
        self.setLayout(main_layout)

    def cancel_selected(self):
        row_indexes_to_cancel = [
            self.job_model_proxy.mapToSource(index).row()
            for index in self.job_table.selectedIndexes()
        ]
        self.job_manager_model_ref.cancel_jobs_in_rows(row_indexes_to_cancel)

    def update_state_filters(self):
        """

        """
        states = []
        for checkbox in self.state_checkboxes:
            if checkbox.isChecked():
                states.append(checkbox.filter_state)
        self.job_model_proxy.filter_states = states
        self.job_model_proxy.invalidateFilter()


class JobModelProxy(QtCore.QSortFilterProxyModel):
    """

    """
    def __init__(self, parent=None):
        """

        """
        super().__init__(parent=parent)
        self.filter_states = job.get_all_states()

    def filterAcceptsRow(self, source_row, source_parent):
        """

        """
        source_index = self.sourceModel().index(source_row, 1, source_parent)
        source_state = self.sourceModel().data(source_index, QtCore.Qt.UserRole)
        return source_state in self.filter_states