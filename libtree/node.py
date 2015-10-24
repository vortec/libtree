# Copyright (c) 2015 Fabian Kochem


from libtree import core


class Node:
    """ """
    def __init__(self, transaction, id):
        self.transaction = transaction
        self.id = id

        self._cursor = transaction.cursor

    def __repr__(self):
        if 'title' in self.properties:
            ret = '<Node id={!r}, title={!r}>'
            return ret.format(self.id, self.properties['title'])
        else:
            ret = '<Node id={!r}>'
            return ret.format(self.id)

    def __eq__(self, other):
        if other.__class__ == Node:
            nd_self = self._node_data
            nd_other = core.get_node(self._cursor, other.id)
            return nd_self.to_dict() == nd_other.to_dict()
        return False

    def __len__(self):
        return int(core.get_children_count(self._cursor, self.id))

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

    @property
    def inherited_properties(self):
        return core.get_inherited_properties(self._cursor, self.id)

    @property
    def children(self):
        ret = []
        for _id in core.get_child_ids(self._cursor, self.id):
            node = Node(self.transaction, _id)
            ret.append(node)
        return ret

    @property
    def ancestors(self):
        ret = []
        for _id in core.get_ancestor_ids(self._cursor, self.id):
            node = Node(self.transaction, _id)
            ret.append(node)
        return ret

    @property
    def descendants(self):
        ret = []
        for _id in core.get_descendant_ids(self._cursor, self.id):
            node = Node(self.transaction, _id)
            ret.append(node)
        return ret

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

    def swap_position(self, other):
        core.swap_node_positions(self._cursor, self.id, other.id)

    def set_properties(self):
        pass

    def get_child_at_position(self, position):
        return core.get_node_at_position(self._cursor, self.id, position)
