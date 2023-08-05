import datetime
from xmlrpc.client import DateTime, boolean

class ptick_ptock:
    current_time = None 

    def isTicked(self) -> boolean:
        return self.current_time == None
    def ptick(self) -> None:
        self.current_time = datetime.datetime.now()
        return
    def datetime_ptock(self) -> DateTime:
        elapsed = datetime.datetime.now() - self.current_time
        return elapsed
    def print_ptock(self) -> None:
        print(datetime.datetime.now() - self.current_time)
        