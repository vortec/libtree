# Copyright (c) 2016 Fabian Kochem


from libtree.core.node_data import NodeData


def test_basic_representation():
    node = NodeData(11, 22)
    assert repr(node) == "<NodeData id=11>"


def test_title_representation():
    node = NodeData(11, 22, properties={'title': 'my test'})
    assert repr(node) == "<NodeData id=11, title='my test'>"


def test_to_dict_conversion():
    kwargs = {
        'id': 11,
        'parent': 22,
        'position': 4,
        'properties': {'a': 1}
    }
    node = NodeData(**kwargs)
    assert node.to_dict() == kwargs
