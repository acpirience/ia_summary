from timeit import default_timer as timer


class Chrono:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = timer()

    def stop(self):
        self.end_time = timer()

    def elapsed_time(self):
        if self.start_time is None or self.end_time is None:
            raise ValueError("Chrono has not been started and stopped properly.")
        return self.end_time - self.start_time
