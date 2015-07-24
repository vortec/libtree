import psycopg2
import psycopg2.extras


class PostgreSQLPersistance(object):
    protocol = 'postgres'

    def __init__(self, details):
        connection = psycopg2.connect(details)
        connection.autocommit = False
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        self._connection = connection
        self._cursor = cursor

    def __getattr__(self, name, *args):
        if len(args) == 1:
            return getattr(self._cursor, name, args[0])
        else:
            return getattr(self._cursor, name)

    def __iter__(self):
        for iter in self._cursor:
            yield iter

    def commit(self):
        return self._connection.commit()

    def get_last_row_id(self):
        self._cursor.execute("SELECT LASTVAL();")
        return self._cursor.fetchone()['lastval']

    def create_tables(self):
        self._cursor.execute("""
            CREATE TABLE ancestor
            (
              node integer NOT NULL,
              ancestor integer NOT NULL,
              CONSTRAINT idx UNIQUE (node, ancestor)
            )
            WITH (
              OIDS=FALSE
            );
        """)
        self._cursor.execute("""
            CREATE TABLE nodes
            (
              id serial NOT NULL,
              parent integer,
              type character varying(255),
              "position" smallint DEFAULT 0,
              description character varying(255),
              CONSTRAINT "primary" PRIMARY KEY (id)
            )
            WITH (
              OIDS=FALSE
            );
        """)
        self._cursor.execute("""
            CREATE INDEX idx_ancestor
              ON ancestor
              USING btree
              (ancestor);
        """)
        self._cursor.execute("""
            CREATE INDEX idx_node
              ON ancestor
              USING btree
              (node);
        """)

    def drop_tables(self):
        self._cursor.execute("DROP TABLE IF EXISTS nodes;")
        self._cursor.execute("DROP TABLE IF EXISTS ancestor;")

    def flush_tables(self):
        self._cursor.execute("TRUNCATE TABLE nodes RESTART IDENTITY;")
        self._cursor.execute("TRUNCATE TABLE ancestor;")
