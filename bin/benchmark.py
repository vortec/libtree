from libtree.config import config
from libtree.persistance import *
from libtree.tree import *
import os
import statistics
from time import time

per = PostgreSQLPersistance(config['postgres']['details'])
stats = list()

def populate_tree(per, node, levels, per_level, depth=0):
    global stats
    for i in range(0, per_level):
        start = time()
        new_node = create_node(per, node, '{}-{}'.format(depth, i+1))
        duration = time() - start
        stats.append(duration)

        if depth < levels:
            populate_tree(per, new_node, levels, per_level, depth+1)

def benchmark(per_level, levels):
    global per, stats
    stats = list()
    per.drop_tables()
    per.create_tables()
    root = create_node(per, None, 'root')
    per.commit()

    start = time()
    populate_tree(per, root, levels, per_level)
    end = time() - start
    output = '{} nodes per level, {} levels = {} nodes total, {} seconds'
    output = output + ' ({} seconds average)'
    print(output.format(per_level, levels, len(stats), end,
          statistics.mean(stats)))

benchmark(1, 1)
benchmark(1, 100)
benchmark(2, 10)
benchmark(2, 11)
benchmark(2, 12)
#import pdb; pdb.set_trace()
benchmark(2, 13)
benchmark(3, 5)
benchmark(5, 5)
benchmark(6, 6)
benchmark(7, 7)
"""benchmark(8, 8)"""
per.commit()
#import pdb; pdb.set_trace()
