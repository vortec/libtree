try:
    import builtins
except ImportError:
    import __builtin__ as builtins


class Node(object):
    __slots__ = [
        '_Node__id',
        '_Node__parent',
        '_Node__type',
        '_Node__position',
        '_Node__attributes',
        '_Node__properties',
    ]

    def __init__(self, id=None, parent=None, type=None, position=None,
                 attributes=None, properties=None):
        self.__id = None
        if id is not None:
            self.__id = int(id)

        self.__parent = None
        if parent is not None:
            self.__parent = int(parent)

        self.__type = type

        self.__position = None
        if position is not None:
            self.__position = int(position)

        if builtins.type(attributes) == dict:
            self.__attributes = attributes
        else:
            self.__attributes = {}

        if builtins.type(properties) == dict:
            self.__properties = properties
        else:
            self.__properties = {}

    def __int__(self):
        return self.id

    def __repr__(self):
        ret = '<Node id={!r}, parent={!r}, type={!r}, position={!r}>'
        return ret.format(self.id, self.parent, self.type, self.position)

    @property
    def id(self):
        return self.__id

    @property
    def parent(self):
        return self.__parent

    @property
    def type(self):
        return self.__type

    @property
    def position(self):
        return self.__position

    @property
    def attributes(self):
        return self.__attributes

    @property
    def properties(self):
        return self.__properties
