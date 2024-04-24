class Outcome():
    def __init__(self, success, data=None, message=None):
        self.success = success
        self.data = data
        self.message = message

    def to_dict(self):
        return {
            "success": self.success,
            "data": self.data,
            "message": self.message
        }

    @classmethod
    def from_dict(cls, in_dict):
        return cls(
            in_dict["success"],
            data=in_dict.get("data"),
            message=in_dict.get("message")
        )