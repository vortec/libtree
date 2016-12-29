# Copyright (c) 2016 Fabian Kochem


from libtree import core, utils

from redis import Redis

redis = Redis()


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
    :param uuid4 id: Database node ID
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
        redis.incr('node.node_data')
        # self._transaction._node_cache[self.id] = 0
        # return core.get_node(self._cursor, self.id)

        node_data = self._transaction._node_cache.get(self.id, None)

        if node_data is None:
            node_data = core.get_node(self._cursor, self.id)
            self._transaction._node_cache[self.id] = node_data
            redis.incr('node.node_data.miss')
        else:
            redis.incr('node.node_data.hit')

        return node_data

    @property
    def parent(self):
        """ Get parent node. """
        parent = self.node_data.parent
        redis.incr('node.parent')
        if parent is not None:
            return Node(self._transaction, self.node_data.parent)
        return None

    @property
    def position(self):
        """ Get position in between sibling nodes. """
        redis.incr('node.position')
        return self.node_data.position

    @property
    def properties(self):
        """ Get property dictionary. """
        redis.incr('node.properties')
        return self.node_data.properties

    @property
    def inherited_properties(self):
        """ Get inherited property dictionary. """
        redis.incr('node.inherited_properties')
        return core.get_inherited_properties(self._cursor, self.id)

    @property
    def recursive_properties(self):
        """
        Get inherited and recursively merged property dictionary.
        """
        redis.incr('node.recursive_properties')
        return core.get_recursive_properties(self._cursor, self.id)

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
        redis.incr('node.has_children')
        return core.get_children_count(self._cursor, self.id) > 0

    @property
    def ancestors(self):
        """ Get bottom-up ordered list of ancestor nodes. """
        ret = []
        redis.incr('node.ancestors')
        for node in core.get_ancestors(self._cursor, self.id, sort=True):
            node = Node(self._transaction, node.id)
            ret.append(node)
        return utils.vectorize_nodes(ret)[::-1]

    @property
    def descendants(self):
        """ Get set of descendant nodes. """
        ret = set()
        redis.incr('node.descendants')
        for _id in core.get_descendant_ids(self._cursor, self.id):
            node = Node(self._transaction, _id)
            ret.add(node)
        return ret

    def delete(self):
        """ Delete node and its subtree. """
        del self._transaction._node_cache[self.id]
        return core.delete_node(self._cursor, self.id)

    def insert_child(self, properties=None, position=-1, id=None):
        """
        Create a child node and return it.

        :param dict properties: Inheritable key/value pairs
                                (see :ref:`core-properties`)
        :param int position: Position in between siblings. If 0, the
                             node will be inserted at the beginning of
                             the parents children. If -1, the node will
                             be inserted the the end of the parents
                             children.
        :param uuid4 id: Use this ID instead of automatically generating
                         one.
        """
        node_data = core.insert_node(self._cursor, self.id, properties,
                                     position=position, auto_position=True,
                                     id=id)
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
        del self._transaction._node_cache[self.id]
        core.change_parent(self._cursor, self.id, target.id,
                           position=position, auto_position=True)

    def swap_position(self, other):
        """
        Swap position with ``other`` position.

        :param other: Node to swap the position with
        :type other: Node
        """
        del self._transaction._node_cache[self.id]
        core.swap_node_positions(self._cursor, self.id, other.id)

    def set_properties(self, properties):
        """
        Set properties.

        :param dict properties: Property dictionary
        """
        del self._transaction._node_cache[self.id]
        core.set_properties(self._cursor, self.id, properties)

    def update_properties(self, properties):
        """
        Set properties.

        :param dict properties: Property dictionary
        """
        del self._transaction._node_cache[self.id]
        core.update_properties(self._cursor, self.id, properties)

    def set_position(self, new_position):
        """
        Set position.

        :param int position: Position in between siblings. If 0, the
                             node will be inserted at the beginning of
                             the parents children. If -1, the node will
                             be inserted the the end of the parents
                             children.
        """
        del self._transaction._node_cache[self.id]
        core.set_position(self._cursor, self.id, new_position,
                          auto_position=True)

    def get_child_at_position(self, position):
        """
        Get child node at certain position.

        :param int position: Position to get the child node from
        """
        return core.get_node_at_position(self._cursor, self.id, position)
