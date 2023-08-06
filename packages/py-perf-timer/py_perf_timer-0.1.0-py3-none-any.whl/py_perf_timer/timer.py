import time


class TimerMeasurement:
    def __init__(self):
        self.total_time = 0
        self.start_time = None

    def start(self):
        if self.start_time is not None:
            raise Exception("Already started")
        self.start_time = time.time()

    def stop(self):
        self.total_time += time.time() - self.start_time
        self.start_time = None
