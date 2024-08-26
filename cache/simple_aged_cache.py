import time

class SimpleAgedCache:
    def __init__(self, clock=None):
        self.clock = clock

    def put(self, key, value, retention_in_millis):
        pass

    def is_empty(self):
        return False

    def size(self):
        return 0

    def get(self, key):
        return None