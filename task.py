import time

class Task:
    def __init__(self, description, due_time, estimated_time):
        self.description = description
        self.due_time = due_time
        self.estimated_time = estimated_time
        self.remaining_time = self.parse_time(estimated_time)
        self.start_time = None
        self.complete = False

    def parse_time(self, time_str):
        hours, minutes = map(int, time_str.split(':'))
        return hours * 3600 + minutes * 60

    def mark_as_complete(self):
        self.complete = True

    def start_task(self):
        self.start_time = time.time()

    def stop_task(self):
        if self.start_time:
            elapsed = time.time() - self.start_time
            self.remaining_time -= int(elapsed)
            self.start_time = None

    def update_remaining_time(self):
        if self.start_time:
            elapsed = time.time() - self.start_time
            self.remaining_time -= int(elapsed)
            self.start_time = time.time()

    def __str__(self):
        status = "Complete" if self.complete else "Incomplete"
        return f"{self.description} (Due: {self.due_time}, Est: {self.estimated_time}, Status: {status})"
