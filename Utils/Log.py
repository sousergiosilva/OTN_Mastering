from datetime import datetime
from Utils.File import WriteToFile


class Log:
    _instance = None
    message = ""

    def __init__(self):
        self.fileName = str(int(datetime.now().timestamp()))

    def __new__(cls, *args, **kwargs):  # creates a singleton pattern
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def log(self, msg):
        self.message += msg
        self.message += "\n"

    def save(self):
        WriteToFile(self.fileName, self.message)
