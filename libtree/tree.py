# Copyright (c) 2015 Fabian Kochem


from contextlib import contextmanager
from libtree.transaction import Transaction


class Tree:
    """ """
    def __init__(self, connection=None, pool=None, prefix=''):
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
        self.pool = pool
        self.prefix = prefix

    @contextmanager
    def __call__(self):
        if self.pool is None:
            _connection = self.connection
        else:
            _connection = self.pool.getconn()

        try:
            yield Transaction(_connection)
            _connection.commit()
        except Exception:
            _connection.rollback()
            raise
        finally:
            if self.pool is not None:
                self.pool.putconn(_connection)

    def close(self):
        if self.pool is not None:
            self.pool.closeall()
        else:
            self.connection.close()
