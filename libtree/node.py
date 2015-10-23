# Copyright (c) 2015 Fabian Kochem


from libtree import core


class Node:
    """ """
    def __init__(self, transaction, id):
        self.transaction = transaction
        self.id = id

        self._cursor = transaction.cursor

    def __eq__(self, other):
        nd_self = self._node_data
        nd_other = core.get_node(self._cursor, other.id)
        return nd_self.to_dict() == nd_other.to_dict()

    @property
    def _node_data(self):
        return core.get_node(self._cursor, self.id)

    @property
    def parent(self):
        return Node(self.transaction, self._node_data.parent)

    @property
    def position(self):
        return self._node_data.position

    @property
    def properties(self):
        return self._node_data.properties

    def delete(self):
        return core.delete_node(self._cursor, self.id)

    def insert_child(self, properties=None, position=-1):
        node_data = core.insert_node(self._cursor, self.id, properties,
                                     position=position, auto_position=True)
        return Node(self.transaction, node_data.id)

    def move(self, target, position=-1):
        core.change_parent(self._cursor, self.id, target.id,
                           position=position, auto_position=True)

    def set_position(self, new_position):
        pass

    def shift_positions(self):
        pass

    def swap_node_positions(self):
        pass

    def get_inherited_properties(self):
        pass

    def get_inherited_property_value(self):
        pass

    def set_properties(self):
        pass

    def update_properties(self):
        pass

    def set_property_value(self):
        pass

    def get_children(self):
        pass

    def get_child_at_position(self, position):
        pass

    def get_child_ids(self):
        pass

    def get_children_count(self):
        pass

    def get_ancestors(self):
        pass

    def get_ancestor_ids(self):
        pass

    def get_descendants(self):
        pass

    def get_descendant_ids(self):
        pass
