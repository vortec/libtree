# Copyright (c) 2015 Fabian Kochem


from contextlib import contextmanager
from libtree.node import Node
from libtree.transaction import Transaction


class Tree:
    """ """
    def __init__(self, connection=None, pool=None, prefix='',
                 node_factory=Node):
        if connection is None and pool is None:
            msg = (
                "__init__() missing 1 required positional argument:",
                "'connection' or 'pool"
            )
            raise TypeError(' '.join(msg))

        if connection is not None and pool is not None:
            msg = (
                "__init__() accepts only 1 required positional argument:",
                "'connection' or 'pool"
            )
            raise TypeError(' '.join(msg))

        self.connection = connection
        self.node_factory = node_factory
        self.pool = pool
        self.prefix = prefix

    @contextmanager
    def __call__(self):
        transaction = self.make_transaction()
        connection = transaction.connection

        try:
            yield transaction
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            if self.pool is not None:
                self.pool.putconn(connection)

    def make_transaction(self):
        if self.pool is None:
            _connection = self.connection
        else:
            _connection = self.pool.getconn()

        return Transaction(_connection, self.node_factory)

    def close(self):
        if self.pool is not None:
            self.pool.closeall()
        else:
            self.connection.close()
