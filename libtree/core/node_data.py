# Copyright (c) 2015 Fabian Kochem


class NodeData(object):
    """
    Immutable data-holding object which represents tree node data. Its
    attributes are identical to the columns in the ``nodes`` table
    (see :ref:`db_model`).

    Since the object is immutable, you must retrieve a new instance
    of the same node using :func:`libtree.core.query.get_node` to get
    updated values.

    To manipulate the values, you must use one of the following
    functions:

    * :func:`libtree.core.tree.change_parent`
    * :ref:`core-positioning`
    * :ref:`core-properties`

    Most ``libtree`` functions need a database ID in order to know on
    which data they should operate, but also accept ``Node`` objects
    to make handling with them easier.

    All parameters are optional and default to ``None``.

    :param int id: ID of the node as returned from the database
    :param parent: Reference to a parent node
    :type parent: Node or int
    :param int position: Position in between siblings
                         (see :ref:`core-positioning`)
    :param dict properties: Inheritable key/value pairs
                            (see :ref:`core-properties`)
    """
    __slots__ = [
        '_NodeData__id',
        '_NodeData__parent',
        '_NodeData__position',
        '_NodeData__properties',
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
            ret = "<NodeData id={!r}, title='{!s}'>"
            return ret.format(self.id, self.properties['title'])
        else:
            ret = '<NodeData id={!r}>'
            return ret.format(self.id, self.parent)

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
