from queue import Queue


class TelemetryBus:
    def __init__(self):
        self.queue = Queue()

    def publish(self, packet):
        self.queue.put(packet)

    def consume(self):
        if self.queue.empty():
            return None

        return self.queue.get()