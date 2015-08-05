try:
    from psycopg2cffi import compat
except ImportError:
    pass
else:
    compat.register()


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
              "position" smallint DEFAULT NULL,
              description character varying(255),
              CONSTRAINT "primary" PRIMARY KEY (id)
            )
            WITH (
              OIDS=FALSE
            );
        """)
        self._cursor.execute("""
            CREATE INDEX idx_parent
              ON nodes
              USING btree
              (parent);
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

    def create_triggers(self):
        self._cursor.execute("""
            CREATE OR REPLACE FUNCTION
              update_ancestors_after_insert()
            RETURNS TRIGGER AS
            $BODY$
            BEGIN
              IF NEW.parent IS NOT NULL THEN

                INSERT INTO
                  ancestor
                  (node, ancestor)

                  SELECT
                    NEW.id, ancestor
                  FROM
                    ancestor
                  WHERE
                    node=NEW.parent
                  UNION
                    SELECT NEW.id, NEW.parent;
              END IF;

              RETURN NEW;
            END;
            $BODY$
            LANGUAGE plpgsql;
        """)
        self._cursor.execute("""
            CREATE CONSTRAINT TRIGGER update_ancestors_after_insert
            AFTER INSERT
            ON nodes
            FOR EACH ROW
            EXECUTE PROCEDURE update_ancestors_after_insert()
        """)

        self._cursor.execute("""
            CREATE OR REPLACE FUNCTION
              update_ancestors_after_delete()
            RETURNS TRIGGER AS
            $BODY$
            BEGIN

              DELETE FROM
                nodes
              WHERE
                id IN
                  (
                    SELECT
                      node
                    FROM
                      ancestor
                    WHERE
                      ancestor=OLD.id
                  );

              DELETE FROM
                ancestor
              WHERE
                node IN
                  (
                    SELECT
                      node
                    FROM
                      ancestor
                    WHERE
                      ancestor=OLD.id
                    UNION
                      SELECT OLD.id
                  )
              OR
                ancestor IN
                  (
                    SELECT
                      node
                    FROM
                      ancestor
                    WHERE
                      ancestor=OLD.id
                    UNION
                      SELECT OLD.id
                  );

              RETURN OLD;

            END;
            $BODY$
            LANGUAGE plpgsql;
        """)
        self._cursor.execute("""
            CREATE CONSTRAINT TRIGGER update_ancestors_after_delete
            AFTER DELETE
            ON nodes
            FOR EACH ROW
            EXECUTE PROCEDURE update_ancestors_after_delete()
        """)

        self._cursor.execute("""
            CREATE OR REPLACE FUNCTION
                update_ancestors_after_update()
              RETURNS TRIGGER AS
              $BODY$
              BEGIN

                DELETE FROM
                  ancestor
                WHERE
                  ancestor
                IN
                  (
                    SELECT
                      ancestor
                    FROM
                      ancestor
                    WHERE
                      node=NEW.id
                    )
                AND
                  node
                IN
                  (
                    SELECT
                      node
                    FROM
                      ancestor
                    WHERE
                      ancestor=NEW.id
                    OR
                      node=NEW.id
                    );

                INSERT INTO
                  ancestor
                SELECT
                  sub.node, par.ancestor
                FROM
                  ancestor AS sub
                JOIN
                  (
                    SELECT
                      ancestor
                    FROM
                      ancestor
                    WHERE
                      node=NEW.parent
                    UNION SELECT NEW.parent
                  ) AS par
                ON TRUE
                WHERE
                  sub.ancestor = NEW.id
                OR
                  sub.node = NEW.id;

                IF NEW.parent IS NOT NULL THEN

                  INSERT INTO
                    ancestor
                    (node, ancestor)

                    SELECT
                      NEW.id, ancestor
                    FROM
                      ancestor
                    WHERE
                      node=NEW.parent
                    UNION
                      SELECT NEW.id, NEW.parent;
                END IF;

                RETURN NEW;
              END;
              $BODY$
              LANGUAGE plpgsql;
        """)
        self._cursor.execute("""
            CREATE CONSTRAINT TRIGGER update_ancestors_after_update
            AFTER UPDATE
            ON nodes
            FOR EACH ROW
            EXECUTE PROCEDURE update_ancestors_after_update()
        """)

    def drop_tables(self):
        self._cursor.execute("DROP TABLE IF EXISTS nodes;")
        self._cursor.execute("DROP TABLE IF EXISTS ancestor;")

    def flush_tables(self):
        self._cursor.execute("TRUNCATE TABLE nodes RESTART IDENTITY;")
        self._cursor.execute("TRUNCATE TABLE ancestor;")
