# Copyright (c) 2015 Fabian Kochem


try:
    from psycopg2cffi import compat
except ImportError:
    pass
else:
    compat.register()

from psycopg2.extras import RealDictCursor
from libtree import core


class Transaction:
    """ """
    def __init__(self, connection, node_factory):
        connection.autocommit = False  # We handle transactions manually
        self.connection = connection
        self.cursor = connection.cursor(cursor_factory=RealDictCursor)
        self.node_factory = node_factory

        # for method in core:
        #    setattr(self, method.name) = partial(getattr(core, method),
        # self.cursor)

        # self.get_child_at_position = partial(core.)

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

    def is_compatible_postgres_version(self):
        """ """
        return core.is_compatible_postgres_version(self.cursor)

    def install(self):
        core.create_schema(self.cursor)
        core.create_triggers(self.cursor)
        return True

    def uninstall(self):
        return core.drop_tables(self.cursor)

    def clear(self):
        return core.flush_tables(self.cursor)

    def print_tree(self):
        return core.print_tree(self.cursor)

    def get_tree_size(self):
        return core.get_tree_size(self.cursor)

    def get_root_node(self):
        return core.get_root_node(self.cursor)

    def insert_root_node(self, properties=None):
        return core.insert_node(self.cursor, properties)

    def get_node(self, node_id):
        return core.get_node(self.cursor, node_id)

    def get_nodes_by_property_dict(self, query):
        return core.get_nodes_by_property_dict(self.cursor, query)

    def get_nodes_by_property_key(self, key):
        return core.get_nodes_by_property_key(self.cursor, key)

    def get_nodes_by_property_value(self, key, value):
        return core.get_nodes_by_property_value(self.cursor, key, value)
