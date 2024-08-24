import datetime
import time
import threading


class HeartbeatProcessor:
    def __init__(self, die_time):
        """
        Initializes the HeartbeatProcessor with the die_time

        Args:
            die_time (float): The time in seconds
        """
        self.die_time = die_time
        self.last_heartbeat = None
        self.heartbeat_started = False
        threading.Thread(target=self.check_alive).start()

    def recieve_heartbeat(self):
        self.last_heartbeat = datetime.datetime.now()
        self.heartbeat_started = True

    def is_alive(self):
        if self.last_heartbeat is None:
            return False
        return (datetime.datetime.now() - self.last_heartbeat).seconds < self.die_time

    def check_alive(self):
        while True:
            if not self.heartbeat_started:
                continue

            if not self.is_alive():
                print("Node is dead")
                break

            time.sleep(1)
