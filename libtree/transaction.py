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

    def install(self):
        core.create_schema(self.cursor)
        core.create_triggers(self.cursor)

    def uninstall(self):
        core.drop_tables(self.cursor)

    def clear(self):
        core.flush_tables(self.cursor)

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

    def get_child_at_position(self, node_id, position):
        pass
        # node_data = core.get_child_at_position(self.cursor, position)
        # return self.make_node(node_data.xid)
        # return self.transaction.(xid)
