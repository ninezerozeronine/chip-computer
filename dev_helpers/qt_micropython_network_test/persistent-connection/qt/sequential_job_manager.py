from . import job_mod

class SequentialJobManager():

    def __init__(self):
        self.queue = []
        self.job_order = []
        self.jobs = {}
        self.next_id = 555

    def num_jobs(self):
        return len(self.jobs)

    def sumbit_job(self, job):
        job_id = self.next_id
        self.next_id += 1

        job.job_id = job_id
        self.jobs[job_id] = job
        self.job_order.append(job_id)
        self.queue.append(job_id)
        return job_id

    def cancel_job(self, job_id):
        if job_id not in self.jobs:
            print(f"Found no job with id: {job_id}")
            return

        self.jobs[job_id].cancel()

    def relay_comms(self, job_id, data):
        if job_id not in self.jobs:
            print(f"Found no job with id: {job_id}")
            return

        self.jobs[job_id].process_comms(data)

    def work_on_top_job(self, socket):
        """
        Call this repeatedly

        Returns true if a change was made, false if not.
        """
        if not self.queue:
            return False

        job = self.jobs[self.queue[0]]

        # If it's new, send it
        if job.state == job_mod.State.new:
            job.send(socket)
            return True

        # If it's been sent or is in progress, nothing to do
        if job.state in (job_mod.State.sent, job_mod.State.in_progress):
            return False

        # If it's complete or cancelled, move on to the next job
        if job.state in (job_mod.State.complete, job_mod.State.cancelled):
            del self.queue[0]
            return False

    def get_table_data(self, row, column):
        """
        Helper function to display jobs in a table
        """

        return self.jobs[self.job_order[row]].get_table_data(column)

    def job_id_to_row_index(self, job_id):
        return self.job_order.index(job_id)

    def top_job_row_index(self):
        index = -1
        if self.queue:
            index = self.job_order.index(self.queue[0])
        return index

    def job_id_from_model_row(self, row):
        return self.job_order[row]

    def job_id_exists(self, job_id):
        return job_id in self.jobs
