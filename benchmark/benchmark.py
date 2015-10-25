import time
import sys
from utils import format_duration

if sys.platform == "win32":
    default_timer = time.clock
else:
    default_timer = time.time


class Benchmark():

    def __init__(self, func, name="", repeat=5):
        self.func = func
        self.repeat = repeat
        self.name = name

    def run(self, conn):
        self.results = []
        for x in range(self.repeat):
            start = default_timer()
            self.func()
            end = default_timer()
            elapsed = end - start
            self.results.append(elapsed)
            conn.rollback()
        return min(self.results)
