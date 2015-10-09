# Copyright (c) 2015 CaT Concepts and Training GmbH


class Node(object):
    """Immutable data-holding object which represents a tree node. Its
    attributes are identical to the columns in the ``nodes`` table
    (see :ref:`db_model`).

    Since the object is immutable, you must retrieve a new instance
    of the same node using :func:`libtree.query.get_node` to get
    updated values.

    To manipulate the values, you must use one of the following
    functions:

    * :func:`libtree.tree.change_parent`
    * :ref:`api-positioning`
    * :ref:`api-properties`

    Most ``libtree`` functions need a database ID in order to know on
    which data they should operate, but also accept ``Node`` objects
    to make handling with them easier.

    All parameters are optional and default to ``None``.

    :param int id: ID of the node as returned from the database
    :param parent: Reference to a parent node
    :type parent: Node or int
    :param int position: Position in between siblings
                         (see :ref:`positioning`)
    :param dict properties: Inheritable key/value pairs
                             (see :ref:`properties`)
    """
    __slots__ = [
        '_Node__id',
        '_Node__parent',
        '_Node__position',
        '_Node__properties',
    ]

    def __init__(self, id=None, parent=None, position=None, properties=None):
        self.__id = None
        if id is not None:
            self.__id = int(id)

        self.__parent = None
        if parent is not None:
            self.__parent = int(parent)

        self.__position = None
        if position is not None:
            self.__position = int(position)

        if type(properties) == dict:
            self.__properties = properties
        else:
            self.__properties = {}

    def __int__(self):
        return self.id

    def to_dict(self):
        """ Return dictionary containing all values of the object. """
        return {
            'id': self.id,
            'parent': self.parent,
            'position': self.position,
            'properties': self.properties
        }

    def __repr__(self):
        if 'title' in self.properties:
            ret = '<Node id={!r}, title={!r}>'
            return ret.format(self.id, self.properties['title'])
        else:
            ret = '<Node id={!r}, parent={!r}, position={!r}>'
            return ret.format(self.id, self.parent, self.position)

    @property
    def id(self):
        """ Node ID """
        return self.__id

    @property
    def parent(self):
        """ Parent ID """
        return self.__parent

    @property
    def position(self):
        """ Position in between its siblings """
        return self.__position

    @property
    def properties(self):
        """ Node properties """
        return self.__properties
