from libtree.node import Node


def test_basic_representation():
    node = Node(11, 22)
    assert repr(node) == "<Node id=11, parent=22, position=None>"


def test_title_representation():
    node = Node(11, 22, attributes={'title': 'my test'})
    assert repr(node) == "<Node id=11, title='my test'>"
