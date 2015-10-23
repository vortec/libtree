# Copyright (c) 2015 Fabian Kochem


from libtree import Node


def xtest_it_compares_against_other_nodes():
    assert nd1 == nd2
    assert nd1 is nd2
    raise NotImplementedError


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


def xtest_insert_child():
    raise NotImplementedError


def xtest_delete():
    raise NotImplementedError


def xtest_change_parent():
    raise NotImplementedError


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
