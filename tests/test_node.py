# Copyright (c) 2016 Fabian Kochem


from libtree import core, Node
from mock import patch


def test_basic_representation(trans, root):
    node = Node(trans, root.id)
    assert repr(node) == '<Node id={}>'.format(root.id, root.position)


def test_title_representation(trans, nd1):
    node = Node(trans, nd1.id)
    expected = "<Node id={}, title='Node 1'>".format(nd1.id)
    assert repr(node) == expected


def test_it_compares_other_nodes(trans, nd1, nd2):
    node1a = Node(trans, nd1.id)
    node1b = Node(trans, nd1.id)
    node2 = Node(trans, nd2.id)
    assert node1a == node1b
    assert node1a != node2


def test_it_wont_compare_other_types(trans, nd1, nd2):
    node = Node(trans, nd1.id)
    assert node != nd1


def test_hash(trans, nd1, nd2):
    node1a = Node(trans, nd1.id)
    node1b = Node(trans, nd1.id)
    node2 = Node(trans, nd2.id)
    assert hash(node1a) == hash(node1b)
    assert hash(node1a) != hash(node2)


def test_get_parent(trans, nd2_1_1, nd2_leaf):
    node = Node(trans, nd2_leaf.id)
    parent = node.parent
    assert parent.id == nd2_1_1.id


def test_get_parent_returns_none_for_root(trans, root):
    assert Node(trans, root.id).parent is None


def test_get_position(trans, nd3):
    node = Node(trans, nd3.id)
    assert node.position == nd3.position


def test_get_properties(trans, nd3):
    node = Node(trans, nd3.id)
    assert node.properties == nd3.properties


def test_get_children_count(trans, cur, root):
    node = Node(trans, root)
    assert len(node) == core.get_children_count(cur, root.id)


def test_get_children(trans, nd2, nd2_1):
    node = Node(trans, nd2.id)
    children = [Node(trans, nd2_1.id)]
    assert node.children == children


def test_has_children(trans, nd2, nd2_leaf):
    node = Node(trans, nd2.id)
    node2_leaf = Node(trans, nd2_leaf.id)
    assert node.has_children
    assert not node2_leaf.has_children


def test_get_ancestors(trans, root, nd2, nd2_1):
    node = Node(trans, nd2_1.id)
    ancestors = [Node(trans, nd2.id), Node(trans, root.id)]
    assert node.ancestors == ancestors


def test_get_descendants(trans, nd2_1, nd2_1_1, nd2_leaf):
    node = Node(trans, nd2_1.id)
    descendants = [Node(trans, nd2_1_1.id), Node(trans, nd2_leaf.id)]
    assert node.descendants == descendants


@patch.object(core, 'insert_node')
def test_insert_child(mock, trans, cur):
    node = Node(trans, 1)
    properties = {'type': 'new_child'}
    node.insert_child(properties)
    mock.assert_called_with(cur, node.id, properties, position=-1,
                            auto_position=True)


@patch.object(core, 'delete_node')
def test_delete(mock, trans, cur):
    node = Node(trans, 1)
    node.delete()
    mock.assert_called_with(cur, node.id)


@patch.object(core, 'change_parent')
def test_move(mock, trans, cur):
    node = Node(trans, 1)
    target_node = Node(trans, 2)
    node.move(target_node)
    mock.assert_called_with(cur, node.id, target_node.id, position=-1,
                            auto_position=True)


@patch.object(core, 'swap_node_positions')
def test_swap_position(mock, trans, cur):
    node1 = Node(trans, 1)
    node2 = Node(trans, 2)
    node1.swap_position(node2)
    mock.assert_called_with(cur, node1.id, node2.id)


@patch.object(core, 'get_inherited_properties')
def test_get_inherited_properties(mock, trans, cur):
    node = Node(trans, 1)
    node.inherited_properties
    mock.assert_called_with(cur, node.id)


@patch.object(core, 'set_properties')
def test_set_properties(mock, trans, cur):
    node = Node(trans, 1)
    node.set_properties({'foo': 'bar'})
    mock.assert_called_with(cur, node.id, {'foo': 'bar'})


@patch.object(core, 'set_position')
def test_set_position(mock, trans, cur):
    node = Node(trans, 1)
    node.set_position(1337)
    mock.assert_called_with(cur, node.id, 1337, auto_position=True)


@patch.object(core, 'get_node_at_position')
def test_get_child_at_position(mock, trans, cur):
    node = Node(trans, 1)
    node.get_child_at_position(2)
    mock.assert_called_with(cur, 1, 2)
