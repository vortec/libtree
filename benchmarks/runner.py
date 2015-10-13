# Copyright (c) 2015 Fabian Kochem


from libtree.config import config
from libtree.persistence import PostgreSQLPersistence
from glob import glob


per = PostgreSQLPersistence(config['postgres']['benchmark_details'])
per.drop_tables()
per.install()

for fn in glob('benchmark-??-*.py'):
    module = fn[:-3]
    benchmark_name = module.split('-', 1)[-1]
    benchmark = __import__(module)
    print('Setting up {}...'.format(benchmark_name))
    benchmark.setup(per)
    print('Running {}...'.format(benchmark_name))
    benchmark.run(per)
    print()
    print('*' * 25)
    print()

