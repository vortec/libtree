# Copyright (c) 2015 Fabian Kochem


try:
    from psycopg2cffi import compat
except ImportError:
    pass
else:
    compat.register()

from psycopg2.extras import RealDictCursor
from functools import partial
from libtree import core


class Transaction:
    def __init__(self, connection, node_factory):
        connection.autocommit = False  # We handle transactions manually
        self.connection = connection
        self.cursor = connection.cursor(cursor_factory=RealDictCursor)
        self.node_factory = node_factory

        self._install_partials()
        print(dir(core))

        # for method in core:
        #    setattr(self, method.name) = partial(getattr(core, method),
        # self.cursor)

        # self.get_child_at_position = partial(core.)

    def _install_partials(self):
        # positioning.py
        self.ensure_free_position = partial(core.ensure_free_position,
                                            self.cursor)
        self.find_highest_position = partial(core.find_highest_position,
                                             self.cursor)
        self.set_position = partial(core.set_position, self.cursor)
        self.shift_positions = partial(core.shift_positions, self.cursor)
        self.swap_node_positions = partial(core.swap_node_positions,
                                           self.cursor)

        # positioning.py
        _func = core.get_nodes_by_property_dict
        self.get_nodes_by_property_dict = partial(_func, self.cursor)
        _func = core.get_nodes_by_property_key
        self.get_nodes_by_property_key = partial(_func, self.cursor)
        _func = core.get_nodes_by_property_value
        self.get_nodes_by_property_value = partial(_func, self.cursor)
        _func = core.get_inherited_properties
        self.get_inherited_properties = partial(_func, self.cursor)
        _func = core.get_inherited_property_value
        self.get_inherited_property_value = partial(_func, self.cursor)
        self.set_properties = partial(core.set_properties, self.cursor)
        self.update_properties = partial(core.update_properties, self.cursor)
        self.set_property_value = partial(core.set_property_value, self.cursor)

        # query.py
        self.get_tree_size = partial(core.get_tree_size, self.cursor)
        self.get_root_node = partial(core.get_root_node, self.cursor)
        self.get_node = partial(core.get_node, self.cursor)
        self.get_node_at_position = partial(core.get_node_at_position,
                                            self.cursor)
        self.get_children = partial(core.get_children, self.cursor)
        self.get_child_ids = partial(core.get_child_ids, self.cursor)
        self.get_children_count = partial(core.get_children_count, self.cursor)
        self.get_ancestors = partial(core.get_ancestors, self.cursor)
        self.get_ancestor_ids = partial(core.get_ancestor_ids, self.cursor)
        self.get_descendants = partial(core.get_descendants, self.cursor)
        self.get_descendant_ids = partial(core.get_descendant_ids, self.cursor)

        # tree.py
        self.print_tree = partial(core.print_tree, self.cursor)
        self.insert_node = partial(core.insert_node, self.cursor)
        self.delete_node = partial(core.delete_node, self.cursor)
        self.change_parent = partial(core.change_parent, self.cursor)

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
