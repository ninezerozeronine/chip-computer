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
        self.job_table.setModel(self.job_manager_model_ref)
        self.job_table.verticalHeader().hide()