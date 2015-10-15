# Copyright (c) 2015 Fabian Kochem


class Transaction:
    def __init__(self, connection):
        self.connection = connection

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

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
