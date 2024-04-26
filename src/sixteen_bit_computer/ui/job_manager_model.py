from PyQt5 import QtCore

from ..network.job_manager import JobManager
from ..network.job import Job

class JobManagerModel(QtCore.QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.manager = JobManager()

    def rowCount(self, index):
        return self.manager.num_jobs()

    def columnCount(self, index):
        return Job.get_num_columns()

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self.manager.get_table_data(index.row(), index.column())

    def headerData(self, index, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return Job.get_header_data(index)

    def sumbit_job(self, job):
        num_jobs = self.manager.num_jobs()
        self.beginInsertRows(QtCore.QModelIndex(), num_jobs+1, num_jobs+1)
        job_id = self.manager.sumbit_job(job)
        self.endInsertRows()
        return job_id

    def cancel_job(self, job_id):
        self.manager.cancel_job(job_id)
        row = self.manager.job_id_to_row_index(job_id)
        self.dataChanged.emit(
            self.createIndex(row, 0),
            self.createIndex(row, Job.get_num_columns())
        )

    def relay_comms(self, job_id, outcome):
        self.manager.relay_comms(job_id, outcome)
        row = self.manager.job_id_to_row_index(job_id)
        self.dataChanged.emit(
            self.createIndex(row, 0),
            self.createIndex(row, Job.get_num_columns())
        )

    def work_on_queue(self, socket):
        top_job_row_index = self.manager.top_job_row_index()
        if top_job_row_index != -1:
            made_change = self.manager.work_on_queue(socket)
            if made_change:
                self.dataChanged.emit(
                    self.createIndex(top_job_row_index, 0),
                    self.createIndex(top_job_row_index, Job.get_num_columns())
                )

    def cancel_jobs_in_rows(self, rows):
        for row in rows:
            self.cancel_job(self.manager.job_id_from_model_row(row))

    def job_id_exists(self, job_id):
        return self.manager.job_id_exists(job_id)