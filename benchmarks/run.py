import sys
import argparse
import psycopg2
from libtree import Tree
from utils import postgres_create_db, postgres_analyze_db, generate_tree, format_duration
from benchmarks import create_benchmarks

DBNAME = 'benchmark_libtree'

config = {
    'benchmark_db': 'dbname={} user=postgres'.format(DBNAME),
    'postgres_db': 'dbname=postgres user=postgres',
    'levels': 7,
    'per_level': 7,
    'test_node_id': 505,
    'generate_tree': True,
    'filter_benchmarks': None
}


def run():
    if config['generate_tree']:
        # drop existing database and recreate
        postgres_create_db(config['postgres_db'], DBNAME)

        connection = psycopg2.connect(config['benchmark_db'])
        tree = Tree(connection)

        with tree() as transaction:
            transaction.install()
            # create tree with test data
            generate_tree(transaction, config['levels'], config['per_level'])

    connection = psycopg2.connect(config['benchmark_db'])
    tree = Tree(connection)

    with tree() as transaction:
        postgres_analyze_db(transaction.cursor)

        # build a list of benchmarks to run
        benchmarks = create_benchmarks(transaction, config)
        benchmarks_to_run = []
        filter_benchmarks = config['filter_benchmarks']

        for b in benchmarks:
            if not filter_benchmarks or filter_benchmarks in b.name:
                benchmarks_to_run.append(b)

        print()

        if len(benchmarks_to_run):
            print("Running benchmarks..")

            for benchmark in benchmarks_to_run:
                print(benchmark.name.ljust(30), end="")
                sys.stdout.flush()
                duration = benchmark.run(transaction)
                print(format_duration(duration))

        else:
            print("No benchmarks to run")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--skip-tree-generation",
                        help="Skip the tree generation",
                        action="store_true")
    parser.add_argument("-f", "--filter-benchmarks",
                        help="Filter benchmarks by name")

    args = parser.parse_args()

    if args.skip_tree_generation:
        config['generate_tree'] = False
    if args.filter_benchmarks:
        config['filter_benchmarks'] = args.filter_benchmarks

    run()
