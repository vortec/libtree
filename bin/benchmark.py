from libtree.config import config
from libtree.persistance import *
from libtree.tree import *
import os
import sys
from time import time


sys.setrecursionlimit(100000)

per = PostgreSQLPersistance(config['postgres']['details'])
stats = list()
averages = list()
average = lambda a: sum(a) / len(a)

def populate_tree(per, node, levels, per_level, depth=0):
    global stats
    for i in range(0, per_level):
        start = time()
        new_node = insert_node(per, node, '{}-{}'.format(depth, i+1))
        duration = time() - start
        stats.append(duration)

        if depth < levels:
            populate_tree(per, new_node, levels, per_level, depth+1)

def benchmark(per_level, levels):
    global per, stats, averages
    stats = list()
    per.drop_tables()
    per.create_schema()
    per.create_triggers()
    root = insert_node(per, None, 'root')
    per.commit()

    start = time()
    populate_tree(per, root, levels, per_level)
    end = time() - start
    output = '{} nodes per level, {} levels = {} nodes total, {} seconds'
    output = output + ' ({} seconds average)'
    _average = average(stats)
    averages.append(_average)
    print(output.format(per_level, levels, len(stats), end, _average))


benchmark(1, 10000)
per.commit()
csv = '\n'.join(map(lambda s: s.replace('.', ','), map(str, stats)))
open('stats.csv', 'w').write(csv)

#print(averages)
#print("Overall average INSERT speed per node: {}".format(average(averages)))
#import pdb; pdb.set_trace()
