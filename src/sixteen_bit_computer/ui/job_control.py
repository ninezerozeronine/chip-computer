from PyQt5 import Qt, QtGui, QtCore, QtWidgets

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
        self.job_model_proxy = QtCore.QSortFilterProxyModel()
        self.job_model_proxy.setSourceModel(self.job_manager_model_ref)
        self.job_table.setModel(self.job_model_proxy)
        self.job_table.horizontalHeader().setSectionsMovable(True)
        self.job_table.verticalHeader().hide()
        self.job_table.setSortingEnabled(True)


        self.cancel_selected_button = QtWidgets.QPushButton("Cancel Selected")
        self.cancel_selected_button.clicked.connect(self.cancel_selected)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.job_table)
        main_layout.addWidget(self.cancel_selected_button)

        self.setLayout(main_layout)

    def cancel_selected(self):
        row_indexes_to_cancel = [
            self.job_model_proxy.mapToSource(index).row()
            for index in self.job_table.selectedIndexes()
        ]
        self.job_manager_model_ref.cancel_jobs_in_rows(row_indexes_to_cancel)
