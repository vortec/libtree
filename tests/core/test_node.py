# Copyright (c) 2015 Fabian Kochem


from libtree.core.node import Node


def test_basic_representation():
    node = Node(11, 22)
    assert repr(node) == "<Node id=11, parent=22, position=None>"


def test_title_representation():
    node = Node(11, 22, properties={'title': 'my test'})
    assert repr(node) == "<Node id=11, title='my test'>"


def test_to_dict_conversion():
    kwargs = {
        'id': 11,
        'parent': 22,
        'position': 4,
        'properties': {'a': 1}
    }
    node = Node(**kwargs)
    assert node.to_dict() == kwargs
