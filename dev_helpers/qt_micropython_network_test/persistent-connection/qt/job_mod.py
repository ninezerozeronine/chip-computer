from enum import Enum, auto
import datetime
import json

from . import outcome_mod

class State(Enum):
    """
    Possible states a job can be in
    """
    new = auto()
    sent = auto()
    in_progress = auto()
    complete = auto()
    cancelled = auto()


def human_readable_state(state):
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



# Send this:
# {
#     "purpose": "panel_method_call",
#     "body": {
#         "job_id": 123456,
#         "method": "do_a_thing",
#         "args": [1, "a"], # optional
#         "kwargs": {"foo": 4, "bar":"hello"} # optional
#     }
# }

# Recieve this
# {
#     "purpose": "job_comms",
#     "body": {
#         "job_id": 123456,
#         "outcome": {
#             "success": False,
#             "data": 34,
#             "message": "Ya dun goofed"
#         }
#     }
# }

# {
#     "purpose": "panel_display_update",
#     "body": {
#         "user_input": "4561",
#         "program_name": "FIBB"
#     }
# }




class Job():

    def __init__(self, method, args=None, kwargs=None):
        self.state = State.new
        self.job_id = None
        self.method = method
        self.args = args
        self.kwargs = kwargs

        self.created_at = datetime.datetime.now()
        self.sent_at = None
        self.last_comm_recieved_at = None
        self.cancelled_at = None
        self.completed_at = None

        self.complete_callback=None
        self.cancelled_callback=None


    def send(self, socket):
        #print(f"Sending {self.command} for job {self.job_id}.")

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
        self.last_comm_recieved_at = datetime.datetime.now()

        # Check data is correct type
        if not isinstance(outcome, dict):
            print(f"Malformed communication recieved - not a dict: {outcome}")
            return

        print(f"Job ID {self.job_id} got: {outcome}")

        self.completed_at = datetime.datetime.now()
        self.state = State.complete

        if self.complete_callback is not None:
            self.complete_callback(outcome_mod.Outcome.from_dict(outcome))

    def cancel(self):
        self.cancelled_at = datetime.datetime.now()
        self.state = State.cancelled
        if self.cancelled_callback is not None:
            cancelled_callback()

    def get_table_data(self, column):
        if column == 0:
            return self.job_id
        if column == 1:
            return human_readable_state(self.state)

        return "Invalid column"

    @classmethod
    def get_num_columns(cls):
        return 2

    @classmethod
    def get_header_data(cls, column):
        if column == 0:
            return "ID"
        if column == 1:
            return "State"

        return "Invalid column header"


