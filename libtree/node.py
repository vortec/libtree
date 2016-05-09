# Copyright (c) 2016 Fabian Kochem


from libtree import core


class Node:
    """
    Representation of a tree node and entrypoint for local tree
    operations.

    It's a thin wrapper around the underlaying core functions. It does
    not contain any data besides the database ID and must therefore
    query the database every time the value of an attribute like
    ``parent`` has been requested. This decision has been made to avoid
    race conditions when working in concurrent or distributed
    environments, but comes at the cost of slower runtime execution
    speeds. If this becomes a problem for you, grab the the
    corresponding :class:`libtree.core.node_data.NodeData` object via
    :attr:`libtree.node.Node.node_data`.

    This object is tightly coupled to a
    :class:`libtree.transaction.Transaction` object. It behaves like a
    partial which passes a database cursor and node ID into every
    :mod:`libtree.core` function. It also has a few convenience features
    like attribute access via Python properties and shorter method
    names.

    :param transaction: Transaction object
    :type transaction: Transaction
    :param int id: Database node ID
    .. automethod:: __len__
    .. automethod:: __eq__

    """
    __slots__ = [
        '_cursor',
        '_Node__id',
        '_transaction'
    ]

    def __init__(self, transaction, id):
        self.__id = id

        self._transaction = transaction
        self._cursor = transaction.cursor

    def __repr__(self):
        if 'title' in self.properties:
            ret = "<Node id={!r}, title='{!s}'>"
            return ret.format(self.id, self.properties['title'])
        else:
            ret = '<Node id={!r}>'
            return ret.format(self.id)

    def __eq__(self, other):
        """ Determine if this node is equal to ``other``. """
        if other.__class__ == Node:
            nd_self = self.node_data
            nd_other = core.get_node(self._cursor, other.id)
            return nd_self.to_dict() == nd_other.to_dict()
        return False

    def __hash__(self):
        return hash('<Node {}>'.format(self.id))

    def __len__(self):
        """ Return amount of child nodes. """
        return int(core.get_children_count(self._cursor, self.id))

    @property
    def id(self):
        """ Database ID """
        return self.__id

    @property
    def node_data(self):
        """
        Get a :class:`libtree.core.node_data.NodeData` object for
        current node ID from database.
        """
        return core.get_node(self._cursor, self.id)

    @property
    def parent(self):
        """ Get parent node. """
        parent = self.node_data.parent
        if parent is not None:
            return Node(self._transaction, self.node_data.parent)
        return None

    @property
    def position(self):
        """ Get position in between sibling nodes. """
        return self.node_data.position

    @property
    def properties(self):
        """ Get property dictionary. """
        return self.node_data.properties

    @property
    def inherited_properties(self):
        """ Get inherited property dictionary. """
        return core.get_inherited_properties(self._cursor, self.id)

    @property
    def children(self):
        """ Get list of immediate child nodes. """
        ret = []
        for _id in core.get_child_ids(self._cursor, self.id):
            node = Node(self._transaction, _id)
            ret.append(node)
        return ret

    @property
    def has_children(self):
        """ Return whether immediate children exist. """
        return core.get_children_count(self._cursor, self.id) > 0

    @property
    def ancestors(self):
        """ Get list of ancestor nodes. """
        ret = []
        for _id in core.get_ancestor_ids(self._cursor, self.id):
            node = Node(self._transaction, _id)
            ret.append(node)
        return ret

    @property
    def descendants(self):
        """ Get list of descendant nodes. """
        ret = []
        for _id in core.get_descendant_ids(self._cursor, self.id):
            node = Node(self._transaction, _id)
            ret.append(node)
        return ret

    def delete(self):
        """ Delete node and its subtree. """
        return core.delete_node(self._cursor, self.id)

    def insert_child(self, properties=None, position=-1):
        """
        Create a child node and return it.

        :param dict properties: Inheritable key/value pairs
                                (see :ref:`core-properties`)
        :param int position: Position in between siblings. If 0, the
                             node will be inserted at the beginning of
                             the parents children. If -1, the node will
                             be inserted the the end of the parents
                             children.
        """
        node_data = core.insert_node(self._cursor, self.id, properties,
                                     position=position, auto_position=True)
        return Node(self._transaction, node_data.id)

    def move(self, target, position=-1):
        """
        Move node and its subtree from its current to another parent
        node. Raises ``ValueError`` if ``target`` is inside this nodes'
        subtree.

        :param target: New parent node
        :type target: Node
        :param int position: Position in between siblings. If 0, the
                             node will be inserted at the beginning of
                             the parents children. If -1, the node will
                             be inserted the the end of the parents
                             children.
        """
        core.change_parent(self._cursor, self.id, target.id,
                           position=position, auto_position=True)

    def swap_position(self, other):
        """
        Swap position with ``other`` position.

        :param other: Node to swap the position with
        :type other: Node
        """
        core.swap_node_positions(self._cursor, self.id, other.id)

    def set_properties(self, properties):
        """
        Set properties.

        :param dict properties: Property dictionary
        """
        core.set_properties(self._cursor, self.id, properties)

    def set_position(self, new_position):
        """
        Set position.

        :param int position: Position in between siblings. If 0, the
                             node will be inserted at the beginning of
                             the parents children. If -1, the node will
                             be inserted the the end of the parents
                             children.
        """
        core.set_position(self._cursor, self.id, new_position,
                          auto_position=True)

    def get_child_at_position(self, position):
        """
        Get child node at certain position.

        :param int position: Position to get the child node from
        """
        return core.get_node_at_position(self._cursor, self.id, position)
