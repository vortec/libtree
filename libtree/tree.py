# Copyright (c) 2015 Fabian Kochem


from contextlib import contextmanager
from libtree.node import Node
from libtree.transaction import Transaction


class Tree:
    """
    Context manager for creating thread-safe transactions in which
    libtree operations can be executed.

    It yields a :class:`libtree.transaction.Transaction` object which
    can be used for accessing the tree. When the context manager gets
    exited, all changes will be committed to the database. If an
    exception occured, the transaction will be rolled back.

    It requires either a ``connection`` or ``pool`` object from the
    `psycopg2 <http://initd.org/psycopg/docs/index.html>`_ package.

    When libtree is used in a threaded environment (usually in
    production), it's recommended to use a `pool
    <http://initd.org/psycopg/docs/pool.html>`_ object.

    When libtree is used in a single-threaded environment (usually
    during development), it's enough to pass a standard `connection
    <http://initd.org/psycopg/docs/connection.html>`_ object.

    By default the built-in :class:`libtree.node.Node` class is used to
    create node objects, but it's possible to pass a different one via
    ``node_factory``.

    :param connection: psycopg2 connection object
    :type connection: psycopg2.connection
    :param pool: psycopg2 pool object
    :type pool: psycopg2.pool.ThreadedConnectionPool
    :param object node_factory: Factory class for creating node objects
                                (default:
                                :class:`libtree.node.Node`)
    """
    def __init__(self, connection=None, pool=None, node_factory=Node):
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
        """
        Get a new transaction object using a connection from the pool
        or the manually assigned one.
        """
        if self.pool is None:
            _connection = self.connection
        else:
            _connection = self.pool.getconn()

        return Transaction(_connection, self.node_factory)

    def close(self):
        """
        Close all connections in pool or the manually assigned one.
        """
        if self.pool is not None:
            self.pool.closeall()
        else:
            self.connection.close()
