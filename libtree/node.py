class Node(object):
    __slots__ = [
        '_Node__id',
        '_Node__parent',
        '_Node__type',
        '_Node__position',
        '_Node__description'
    ]

    def __init__(self, id=None, parent=None, type=None, position=None,
                 description=''):
        self.__id = None
        if id is not None:
            self.__id = int(id)

        self.__parent = None
        if parent is not None:
            self.__parent = int(parent)

        self.__position = None
        if position is not None:
            self.__position = int(position)

        self.__type = type
        self.__description = description

    def __int__(self):
        return self.id

    def __repr__(self):
        ret = '<Node id={!r}, parent={!r}, type={!r}, position={!r}>'
        return ret.format(self.id, self.parent, self.type, self.position,
                          self.description)

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
    def description(self):
        return self.__description
