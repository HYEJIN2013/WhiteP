import threading


class Queue(object):
    def __init__(self, max_size):
        self.max_size = max_size
        self.mutex = threading.Lock()
        self.is_full = threading.Condition(self.mutex)
        self.is_empty = threading.Condition(self.mutex)
        self._queue = []

    def put(self, item):
        with self.mutex:
            while len(self._queue) == self.max_size:
                self.is_full.wait()
            self._queue.append(item)
            self.is_empty.notify_all()

    def get(self):
        with self.mutex:
            while len(self._queue) == 0:
                self.is_empty.wait()
            item = self._queue.pop(0)
            self.is_full.notify_all()
        return item
