class MySQLPersistance(object):
    protocol = 'mysql'

    def __init__(self, **kwargs):
        import MySQLdb  # noqa
        import MySQLdb.cursors  # noqa

        dict_cursor = MySQLdb.cursors.DictCursor
        connection = MySQLdb.connect(cursorclass=dict_cursor, **kwargs)
        connection.autocommit(False)
        cursor = connection.cursor()

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
        return self._cursor.lastrowid

    def create_tables(self):
        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS
                ancestor (
                    node int(11) NOT NULL,
                    ancestor int(11) NOT NULL
                )
            ENGINE=InnoDB
            DEFAULT CHARSET=utf8;
        """)
        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS
                nodes (
                    id int(11) NOT NULL,
                    parent int(11) DEFAULT NULL,
                    type varchar(11) NOT NULL,
                    position int(11) NOT NULL DEFAULT '0',
                    description varchar(255) NOT NULL
                )
            ENGINE=InnoDB
            DEFAULT CHARSET=utf8;
        """)
        self._cursor.execute("""
            ALTER TABLE
                ancestor
            ADD UNIQUE KEY idx (node,ancestor) USING BTREE,
            ADD KEY node (node),
            ADD KEY ancestor (ancestor) USING BTREE;
        """)
        self._cursor.execute("""
            ALTER TABLE
                nodes
            ADD PRIMARY KEY (id);
        """)
        self._cursor.execute("""
            ALTER TABLE
                nodes
            MODIFY
                id int(11) NOT NULL AUTO_INCREMENT;
        """)

    def drop_tables(self):
        self._cursor.execute("DROP TABLE IF EXISTS nodes;")
        self._cursor.execute("DROP TABLE IF EXISTS ancestor;")

    def flush_tables(self):
        self._cursor.execute("TRUNCATE TABLE nodes;")
        self._cursor.execute("TRUNCATE TABLE ancestor;")
        self._cursor.execute("ALTER TABLE nodes AUTO_INCREMENT=1;")


class PostgreSQLPersistance(object):
    protocol = 'postgres'

    def __init__(self, details):
        import psycopg2  # noqa
        import psycopg2.extras  # noqa

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
