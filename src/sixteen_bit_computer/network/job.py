from enum import Enum, auto
import datetime
import json

from .outcome import Outcome

class State(Enum):
    """
    Defines the possible states a job can be in
    """
    new = auto()
    sent = auto()
    in_progress = auto()
    complete = auto()
    cancelled = auto()


def human_readable_state(state):
    """
    Get a human readable equivalent of the State enum.

    Args:
        state (State): The state to decode
    Return:
        str: Human readable equivalent of the state.
    """
    if state == State.new:
        return "New"
    if state == State.sent:
        return "Sent"
    if state == State.in_progress:
        return "In Progress"
    if state == State.complete:
        return "Complete"
    if state == State.cancelled:
        return "Cancelled"
    return "Invalid state"


class Job():
    """
    A job that gets sent to the Pico.

    A job is mostly just a method call performed remotely, and we
    expect to get a response back from (see the Outcome class) once
    complete.

    At present the jobs must be a method call on the Panel object
    held by the Manager on the Pico.
    """

    def __init__(self, method, args=None, kwargs=None, human_description=None):
        """
        Initialise the class

        Args:
            method (str): Name of the method we want to call on the
                panel.
        Keyword Args:
            args (list(str) or None): The arguments to call the method
                with
            kwargs (dict or None): The keyword arguments to call the
                method with.
            human_description (str): Short human readable description
                of what the job does.
        """
        self.state = State.new
        self.job_id = None
        self.method = method
        self.args = args
        self.kwargs = kwargs
        self.human_description = human_description

        self.created_at = datetime.datetime.now()
        self.sent_at = None
        self.last_comm_recieved_at = None
        self.cancelled_at = None
        self.completed_at = None

        # This will be called and passed the outcome when the job
        # completes
        self.complete_callback=None

        # This will be called with no arguments when the job is
        # cancelled
        self.cancelled_callback=None


    def send(self, socket):
        """
        Send the job to the Pico.

        The job is ultimately a dictionary that looks something like:

        .. code-block:: none

            {
                "purpose": "panel_method_call",
                "body": {
                    "job_id": 123456,
                    "method": "do_a_thing",
                    "args": [1, "a"], # optional
                    "kwargs": {"foo": 4, "bar":"hello"} # optional
                }
            }

        Args:
            socket (PyQt5.QtNetwork.QTcpSocket): Socket to send the job
                with.
        """

        body = {
            "job_id": self.job_id,
            "method": self.method
        }
        if self.args is not None:
            body["args"] = self.args
        if self.kwargs is not None:
            body["kwargs"] = self.kwargs

        to_send = {
            "purpose": "panel_method_call",
            "body": body
        }

        data_str=json.dumps(to_send)
        print(f"Sending {data_str}")
        print(self.human_description)
        to_send = bytearray(2)
        msg_bytes = bytes(data_str, encoding="ascii")
        to_send.extend(msg_bytes)
        uint16_len_bytes = len(msg_bytes).to_bytes(2, byteorder="big", signed=False)
        to_send[0] = uint16_len_bytes[0]
        to_send[1] = uint16_len_bytes[1]
        num_bytes_to_send = len(to_send)
        num_bytes_sent = socket.write(to_send)
        print(f"Wanted to send {num_bytes_to_send} bytes, actually sent {num_bytes_sent}")

        self.sent_at = datetime.datetime.now()
        self.state = State.sent

    def process_comms(self, outcome):
        """
        Process communication from the Pico.

        At present this is the Pico sending back the result of method
        call as a "serialised" (to a dictionary) Outcome object. This
        may extend in future to support progress updates.

        This is called by the JobManager.

        Args:
            outcome (dict): The outcome of the remote method call
                "serialised" to a dictionary.
        """
        self.last_comm_recieved_at = datetime.datetime.now()

        # Check data is correct type
        if not isinstance(outcome, dict):
            print(f"Malformed communication recieved - not a dict: {outcome}")
            return

        print(f"Job ID {self.job_id} got: {outcome}")

        # Ignore the communication if the job has been cancelled.
        if self.state == State.cancelled:
            return

        self.completed_at = datetime.datetime.now()
        self.state = State.complete

        if self.complete_callback is not None:
            self.complete_callback(Outcome.from_dict(outcome))

    def cancel(self):
        """
        Cancel the job.

        If it was new this means it will no longer be sent. if it was
        cancelled, this means any comms recieved will be ignored.
        """

        self.cancelled_at = datetime.datetime.now()
        self.state = State.cancelled
        if self.cancelled_callback is not None:
            cancelled_callback()

    def get_table_data(self, column):
        """
        Helper method to display this job in a table.

        Args:
            column (int): Index of the column in the table.
        Returns:
            The data that should be displayed in that column
        """
        if column == 0:
            return self.job_id
        if column == 1:
            return human_readable_state(self.state)
        if column == 2:
            return self.human_description
        if column == 3:
            return str(self.created_at)

        return "Invalid column"

    @classmethod
    def get_num_columns(cls):
        """
        Helper function to draw jobs in a table.

        Returns:
            int: The number of columns needed to display all the
                properties of a job.
        """
        return 4

    @classmethod
    def get_header_data(cls, column):
        """
        Helper function to draw the header for a column in a table of jobs.

        Args:
            column (int): The index of the column
        """
        if column == 0:
            return "ID"
        if column == 1:
            return "State"
        if column == 2:
            return "Description"
        if column == 3:
            return "Submission Time"

        return "Invalid column header"


