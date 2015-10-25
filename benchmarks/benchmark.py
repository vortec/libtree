import time
import sys

if sys.platform == "win32":
    default_timer = time.clock
else:
    default_timer = time.time


class Benchmark():

    def __init__(self, func, name, repeat=3):
        self.func = func
        self.repeat = repeat
        self.name = name

    def __str__(self):
        return "<Benchmark {}>".format(self.name)

    def run(self, transaction):
        self.results = []
        for x in range(self.repeat):
            start = default_timer()
            self.func()
            end = default_timer()
            elapsed = end - start
            self.results.append(elapsed)
            transaction.rollback()
        return min(self.results)
