# Copyright (c) 2015 Fabian Kochem


try:
    from psycopg2cffi import compat
except ImportError:
    pass
else:
    compat.register()

from psycopg2.extras import RealDictCursor

from libtree.core import database


class Transaction:
    def __init__(self, connection):
        connection.autocommit = False  # We handle transactions manually
        self.connection = connection
        self.cursor = connection.cursor(cursor_factory=RealDictCursor)

    def commit(self):
        """
        See `commit()
        <http://initd.org/psycopg/docs/connection.html#connection.commit>`_
        .
        """
        return self.connection.commit()

    def rollback(self):
        """
        See `rollback()
        <http://initd.org/psycopg/docs/connection.html#connection.rollback>`_
        .
        """
        return self.connection.rollback()

    def install(self):
        database.create_schema(self.cursor)
        database.create_triggers(self.cursor)

    def uninstall(self):
        database.drop_tables(self.cursor)

    def clear(self):
        database.flush_tables(self.cursor)

    def print_tree(self):
        pass

    def get_tree_size(self):
        pass

    def get_root_node(self):
        pass

    def insert_root_node(self):
        pass

    def get_node(self):
        pass

    def get_node_at_position(self):
        pass

    def get_nodes_by_property_dict(self):
        pass

    def get_nodes_by_property_key(self):
        pass

    def get_nodes_by_property_value(self):
        pass
