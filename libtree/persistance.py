# Copyright (c) 2015 CaT Concepts and Training GmbH


try:
    from psycopg2cffi import compat
except ImportError:
    pass
else:
    compat.register()


import os
import psycopg2
import psycopg2.extras

REQUIRED_POSTGRES_VERSION = (9, 4, 0)


class PostgreSQLPersistance(object):
    """
    Service-wrapping object which holds a connection to `PostgreSQL
    <postgresql.org>`_ using `psycopg2 <http://initd.org/psycopg/>`_ (or
    `psycopg2cffi <https://pypi.python.org/pypi/psycopg2cffi>`_ when
    using `PyPy <http://pypy.org/>`_).

    It should behave exactly like psycopg2 but also has some methods
    which help installing `libtree` or getting the last row ID.

    :param str details: `libpq connection string
                        <http://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-CONNSTRING>`_
    :param bool autocommit: `auto commit
                             <http://initd.org/psycopg/docs/connection.html#connection.autocommit>`_
                             (default: ``False``)
    """
    protocol = 'postgres'

    def __init__(self, details, autocommit=False):
        connection = psycopg2.connect(details)
        connection.autocommit = autocommit
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        self._connection = connection
        self._cursor = cursor

        self.check_postgres_version()
        self.rollback()

    def __iter__(self):
        for iter in self._cursor:
            yield iter

    def commit(self):
        """
        See `commit()
        <http://initd.org/psycopg/docs/connection.html#connection.commit>`_
        .
        """
        return self._connection.commit()

    def rollback(self):
        """
        See `rollback()
        <http://initd.org/psycopg/docs/connection.html#connection.rollback>`_
        .
        """
        return self._connection.rollback()

    def execute(self, *args, **kwargs):
        """
        See `execute()
        <http://initd.org/psycopg/docs/cursor.html#cursor.execute>`_
        .
        """
        return self._cursor.execute(*args, **kwargs)

    def executemany(self, *args, **kwargs):
        """
        See `executemany()
        <http://initd.org/psycopg/docs/cursor.html#cursor.executemany>`_
        .
        """
        return self._cursor.executemany(*args, **kwargs)

    def fetchone(self):
        """
        See `fetchone()
        <http://initd.org/psycopg/docs/cursor.html#cursor.fetchone>`_
        .
        """
        return self._cursor.fetchone()

    def set_autocommit(self, autocommit):
        """
        Set `auto commit
        <http://initd.org/psycopg/docs/connection.html#connection.autocommit>`_
        .
        """
        self._connection.autocommit = autocommit

    def get_last_row_id(self):
        """ Return last row ID. """
        self._cursor.execute("SELECT LASTVAL();")
        return self._cursor.fetchone()['lastval']

    def check_postgres_version(self):
        """
        Raise ``EnvironmentError`` if PostgreSQL server is running an
        outdated version.
        """
        self._cursor.execute("SHOW server_version;")
        result = self._cursor.fetchone()['server_version']
        server_version = tuple(map(int, result.split('.')))

        if server_version < REQUIRED_POSTGRES_VERSION:
            msg = 'Insufficient Postgres version: {}, required: {}'
            msg = msg.format('.'.join(map(str, server_version)),
                             '.'.join(map(str, REQUIRED_POSTGRES_VERSION)))
            raise EnvironmentError(msg)

    def install(self):
        """ Create table schema and triggers. """
        self.create_schema()
        self.create_triggers()

    def create_schema(self):
        """ Create table schema. """
        script_folder = os.path.split(os.path.realpath(__file__))[0]
        path = os.path.join(script_folder, 'sql', 'schema.sql')
        self._cursor.execute(open(path).read())

    def create_triggers(self):
        """ Create triggers. """
        script_folder = os.path.split(os.path.realpath(__file__))[0]
        path = os.path.join(script_folder, 'sql', 'triggers.sql')
        self._cursor.execute(open(path).read())

    def drop_tables(self):
        """ Drop all tables. """
        self._cursor.execute("DROP TABLE IF EXISTS nodes;")
        self._cursor.execute("DROP TABLE IF EXISTS ancestors;")

    def flush_tables(self):
        """ Empty all tables. """
        self._cursor.execute("TRUNCATE TABLE nodes RESTART IDENTITY;")
        self._cursor.execute("TRUNCATE TABLE ancestors;")
