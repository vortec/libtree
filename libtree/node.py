class Node:
    """ """
    def __init__(self, transaction, xid):
        self.transaction = transaction
        self.xid = xid

    def insert_child(self):
        pass

    def delete(self):
        pass

    @property
    def position(self):
        pass
        # return core.get_node(self.xid).property

    def set_position(self, new_position):
        pass
        # core.set_position(self.transaction.cursor, self.xid, new_position)

    def change_parent(self):
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
        # children = core.get_children(self.transaction.cursor, self.data.id)
        # return [Node]

    def get_child_at_position(self, position):
        pass
        # return self.transaction.get_child_at_position(self.xid, position)

        # node_data = core.get_child_at_position(self.transaction.cursor,
        # position)
        # return self.transaction.make_node(node_data.xid)
        # return self.transaction.(xid)

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
