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