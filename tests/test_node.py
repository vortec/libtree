# Copyright (c) 2015 Fabian Kochem


from libtree import core, Node
from mock import patch


def test_it_compares_against_other_nodes(trans, nd1, nd2):
    node1a = Node(trans, nd1.id)
    node1b = Node(trans, nd1.id)
    node2 = Node(trans, nd2.id)
    assert node1a == node1b
    assert node1a != node2


def test_get_parent(trans, nd2_1_1, nd2_leaf):
    node = Node(trans, nd2_leaf.id)
    parent = node.parent
    assert parent.id == nd2_1_1.id


def test_get_position(trans, nd3):
    node = Node(trans, nd3.id)
    assert node.position == nd3.position


def test_get_properties(trans, nd3):
    node = Node(trans, nd3.id)
    assert node.properties == nd3.properties


@patch.object(core, 'insert_node')
def test_insert_child(mock, trans, cur, nd3):
    node = Node(trans, nd3.id)
    properties = {'type': 'new_child'}
    node.insert_child(properties)
    mock.assert_called_with(cur, node.id, properties, position=-1,
                            auto_position=True)


@patch.object(core, 'delete_node')
def test_delete(mock, trans, cur, nd3):
    node = Node(trans, nd3.id)
    node.delete()
    mock.assert_called_with(cur, node.id)


@patch.object(core, 'change_parent')
def test_delete(mock, trans, cur, nd2_leaf, nd3):
    node = Node(trans, nd2_leaf.id)
    target_node = Node(trans, nd3.id)
    node.move(target_node)
    mock.assert_called_with(cur, node.id, target_node.id, position=-1,
                            auto_position=True)


def xtest_shift_positions():
    raise NotImplementedError


def xtest_swap_node_positions():
    raise NotImplementedError


def xtest_get_inherited_properties():
    raise NotImplementedError


def xtest_get_inherited_property_value():
    raise NotImplementedError


def xtest_set_properties():
    raise NotImplementedError


def xtest_update_properties():
    raise NotImplementedError


def xtest_set_property_value():
    raise NotImplementedError


def xtest_get_children():
    raise NotImplementedError


def xtest_get_child_at_position():
    raise NotImplementedError


def xtest_get_child_ids():
    raise NotImplementedError


def xtest_get_children_count():
    raise NotImplementedError


def xtest_get_ancestors():
    raise NotImplementedError


def xtest_get_ancestor_ids():
    raise NotImplementedError


def xtest_get_descendants():
    raise NotImplementedError


def xtest_get_descendant_ids():
    raise NotImplementedError
