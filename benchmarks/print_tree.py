
from run import config
from libtree import PostgreSQLPersistence, print_tree


per = PostgreSQLPersistence(config['benchmark_db'])
print_tree(per)
