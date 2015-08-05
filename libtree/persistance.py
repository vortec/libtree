try:
    from psycopg2cffi import compat
except ImportError:
    pass
else:
    compat.register()


import os
import psycopg2
import psycopg2.extras


class PostgreSQLPersistance(object):
    protocol = 'postgres'

    def __init__(self, details, autocommit=False):
        connection = psycopg2.connect(details)
        connection.autocommit = autocommit
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        self._connection = connection
        self._cursor = cursor

    def __iter__(self):
        for iter in self._cursor:
            yield iter

    def commit(self):
        return self._connection.commit()

    def rollback(self):
        return self._connection.rollback()

    def execute(self, *args, **kwargs):
        return self._cursor.execute(*args, **kwargs)

    def executemany(self, *args, **kwargs):
        return self._cursor.executemany(*args, **kwargs)

    def fetchone(self):
        return self._cursor.fetchone()

    def set_autocommit(self, autocommit):
        self._connection.autocommit = autocommit

    def get_last_row_id(self):
        self._cursor.execute("SELECT LASTVAL();")
        return self._cursor.fetchone()['lastval']

    def create_tables(self):
        script_folder = os.path.split(os.path.realpath(__file__))[0]
        path = os.path.join(script_folder, '..', 'sql', 'schema.sql')
        self._cursor.execute(open(path).read())

    def create_triggers(self):
        script_folder = os.path.split(os.path.realpath(__file__))[0]
        path = os.path.join(script_folder, '..', 'sql', 'triggers.sql')
        self._cursor.execute(open(path).read())

    def drop_tables(self):
        self._cursor.execute("DROP TABLE IF EXISTS nodes;")
        self._cursor.execute("DROP TABLE IF EXISTS ancestor;")

    def flush_tables(self):
        self._cursor.execute("TRUNCATE TABLE nodes RESTART IDENTITY;")
        self._cursor.execute("TRUNCATE TABLE ancestor;")
