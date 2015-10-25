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
        self.verbose = False

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

    def __str__(self):
        s = format_duration(min(self.results))

        if self.verbose:
            s_min = format_duration(min(self.results))
            s_avg = format_duration(sum(self.results) / len(self.results))
            s_max = format_duration(max(self.results))
            s_all = [format_duration(t) for t in self.results]
            s += "(min={} avg={} max={} all={})".format(s_min,
                                                        s_avg, s_max, s_all)
        return s
