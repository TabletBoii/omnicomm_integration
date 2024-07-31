import datetime


class WrongTimeToRun(Exception):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f"Wrong time to run this script: {datetime.datetime.now()}"
