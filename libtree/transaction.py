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
    """
    Representation of a database transaction and entrypoint for global
    tree operations.

    :param connection: Postgres connection object. Its ``autocommit``
                       attribute will be set to ``False``.
    :type connection: Connection
    :param object node_factory: Factory class for creating node objects
    """
    def __init__(self, connection, node_factory):
        connection.autocommit = False  # we handle transactions manually
        self.connection = connection
        self.cursor = connection.cursor(cursor_factory=RealDictCursor)
        self.node_factory = node_factory

    def commit(self):
        """
        Write changes to databases. See `commit()
        <http://initd.org/psycopg/docs/connection.html#connection.commit>`_
        .
        """
        return self.connection.commit()

    def rollback(self):
        """
        Discard changes. See `rollback()
        <http://initd.org/psycopg/docs/connection.html#connection.rollback>`_
        .
        """
        return self.connection.rollback()

    def is_compatible_postgres_version(self):
        """
        Determine whether PostgreSQL server version is compatible with
        libtree.
        """
        return core.is_compatible_postgres_version(self.cursor)

    def install(self):
        """ Create tables and trigger functions in database. """
        core.create_schema(self.cursor)
        core.create_triggers(self.cursor)
        return True

    def uninstall(self):
        """ Remove libtree tables from database. """
        return core.drop_tables(self.cursor)

    def clear(self):
        """ Empty database tables. """
        return core.flush_tables(self.cursor)

    def print_tree(self):
        """ Simple function to print tree structure to stdout. """
        return core.print_tree(self.cursor)

    def get_tree_size(self):
        """ Get amount of nodes inside the tree. """
        return core.get_tree_size(self.cursor)

    def get_root_node(self):
        """ Get root node if exists, other ``None``. """
        node_id = core.get_root_node(self.cursor).id
        return self.node_factory(self, node_id)

    def insert_root_node(self, properties=None):
        """
        Create root node, then get it.

        :param dict properties: Inheritable key/value pairs
                                (see :ref:`core-properties`)
        """
        node_id = core.insert_node(self.cursor, properties).id
        return self.node_factory(self, node_id)

    def get_node(self, node_id):
        """
        Get node with given database ID.

        :param int node_id: Database ID
        """
        node_id = core.get_node(self.cursor, node_id).id
        return self.node_factory(self, node_id)

    def get_nodes_by_property_dict(self, query):
        """
        Get a set of nodes which have all key/value pairs of ``query``
        in their properties. Inherited properties are not considered.

        :param dict query: The dictionary to search for
        """
        ret = set()
        for _nd in core.get_nodes_by_property_dict(self.cursor, query):
            node = self.node_factory(self, _nd.id)
            ret.add(node)
        return ret

    def get_nodes_by_property_key(self, key):
        """
        Get a set of nodes which have a property named ``key`` in their
        properties. Inherited properties are not considered.

        :param str key: The key to search for
        """
        ret = set()
        for _nd in core.get_nodes_by_property_key(self.cursor, key):
            node = self.node_factory(self, _nd.id)
            ret.add(node)
        return ret

    def get_nodes_by_property_value(self, key, value):
        """
        Get a set of nodes which have a property ``key`` with value
        ``value``. Inherited properties are not considered.

        :param str key: The key to search for
        :param object value: The exact value to sarch for
        """
        ret = set()
        for _nd in core.get_nodes_by_property_value(self.cursor, key, value):
            node = self.node_factory(self, _nd.id)
            ret.add(node)
        return ret
