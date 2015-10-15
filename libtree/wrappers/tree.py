# Copyright (c) 2015 Fabian Kochem


from contextlib import contextmanager
from libtree.wrappers import Transaction


class Tree:
    """
    connection = psycopg2.connect("dbname=foo")
    pool = psycopg2.pool.ThreadedConnectionPool(maxconn=4, "dbname=foo")

    tree = Tree(connection=connection)
    tree = Tree(pool=pool, prefix='fabian_')

    with tree() as transaction:
        node = transaction.get_root_node()
        node.position = 12
        node.save()

    """
    def __init__(self, connection=None, pool=None, prefix=''):
        if connection is not None and pool is not None:
            msg = 'Can only deal with either connection or pool object'
            raise TypeError(msg)

        if connection is not None:
            self.connection = connection
        elif pool is not None:
            self.pool = pool
        else:
            msg = [
                "__init__() missing 1 required positional argument:",
                "'connection' or 'pool"
            ]
            raise TypeError(' '.join(msg))

        self.prefix = prefix

    @contextmanager
    def __call__(self):
        yield Transaction(self.connection)

    def close(self):
        if self.pool is not None:
            self.pool.closeall()

    def drop_tables(self):
        pass

    def flush_tables(self):
        pass

    def install(self):
        pass
