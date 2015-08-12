class Node(object):
    """Immutable data-holding object which represents a tree node. Its
    attributes are identical to the columns in the ``nodes`` table.

    Since it's immutable, you must use functions like :func:`get_node`
    or ``update_node()`` to talk to the database in any way
    (see :ref:`tree`).

    Most ``libtree`` functions need a database ID in order to know on
    which data they should operate, but also accept ``Node`` objects
    to make the handling with them easier.

    All parameters are optional and default to ``None``.

    :param int id: ID of the node as returned from the database
    :param parent: Reference to a parent node
    :type parent: Node or int
    :param int position: Position in between siblings
                         (see :ref:`positioning`)
    :param dict attributes: Non-inheritable key/value pairs
                            (see :ref:`attributes`)
    :param dict properties: Inheritable key/value pairs
                             (see :ref:`properties`)
    """
    __slots__ = [
        '_Node__id',
        '_Node__parent',
        '_Node__position',
        '_Node__attributes',
        '_Node__properties',
    ]

    def __init__(self, id=None, parent=None, position=None, attributes=None,
                 properties=None):
        self.__id = None
        if id is not None:
            self.__id = int(id)

        self.__parent = None
        if parent is not None:
            self.__parent = int(parent)

        self.__position = None
        if position is not None:
            self.__position = int(position)

        if type(attributes) == dict:
            self.__attributes = attributes
        else:
            self.__attributes = {}

        if type(properties) == dict:
            self.__properties = properties
        else:
            self.__properties = {}

    def __int__(self):
        return self.id

    def to_dict(self):
        return {
            'id': self.id,
            'parent': self.parent,
            'position': self.position,
            'attributes': self.attributes,
            'properties': self.properties
        }

    def __repr__(self):
        if 'title' in self.attributes:
            ret = '<Node id={!r}, title={!r}>'
            return ret.format(self.id, self.attributes['title'])
        else:
            ret = '<Node id={!r}, parent={!r}, position={!r}>'
            return ret.format(self.id, self.parent, self.position)

    @property
    def id(self):
        return self.__id

    @property
    def parent(self):
        return self.__parent

    @property
    def position(self):
        return self.__position

    @property
    def attributes(self):
        return self.__attributes

    @property
    def properties(self):
        return self.__properties
