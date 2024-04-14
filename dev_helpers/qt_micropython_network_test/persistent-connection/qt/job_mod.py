from enum import Enum, auto
import datetime
import json

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
#     "purpose": "func_call,
#     "job_id": 123456,
#     "method": "do_a_thing",
#     "args": [1, "a"],
#     "kwargs": {"foo": 4, "bar":"hello"}
# }

# Recieve this
# {
#     "purpose": "job_comms",
#     "id": 123456,
#     "body": {
#         "type": "completion",
#         "success": False,
#         "return": 34,
#         "message": "Ya dun goofed"
#     }
# }

# {
#     "purpose": "job_comms",
#     "id": 123456,
#     "body": {
#         "type": "progress",
#         "percentage": 45
#     }
# }



class Job():

    def __init__(self, command):
        self.state = State.new
        self.job_id = None
        self.command = command

        self.created_at = datetime.datetime.now()
        self.sent_at = None
        self.last_comm_recieved_at = None
        self.cancelled_at = None
        self.completed_at = None

        self.complete_callback=None
        self.cancelled_callback=None


    def send(self, socket):
        print(f"Sending {self.command} for job {self.job_id}.")

        to_send = {
            "purpose": "test",
            "job_id": self.job_id,
            "msg": self.command
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

    def process_comms(self, data):
        self.last_comm_recieved_at = datetime.datetime.now()

        # Check data is correct type
        if not isinstance(data, dict):
            print(f"Malformed communication recieved - not a dict: {data}")
            return

        if "type" not in data:
            print(f"Missing type key in data: {data}")
            return

        if data["type"] != "completion":
            print(f"Unknown communication type {data['type']} in data: {data}")
            return

        print(f"Job ID {self.job_id} got: {data['message']}")

        self.completed_at = datetime.datetime.now()
        self.state = State.complete

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


