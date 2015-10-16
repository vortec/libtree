# Copyright (c) 2015 Fabian Kochem


from libtree.core.query import (get_ancestors, get_child_ids, get_children,
                                get_children_count, get_descendants,
                                get_descendant_ids, get_node, get_root_node,
                                get_tree_size)
import libtree
import pytest


def test_get_root_node_non_existing(cur):
    with pytest.raises(ValueError):
        get_root_node(cur)


def test_get_node_non_existing(cur):
    with pytest.raises(ValueError):
        get_node(cur, 1)


def test_get_root_node(cur, root, node1, node2, node2_1, node2_1_1, node3):
    root = get_root_node(cur)
    assert root.parent is None


def test_get_node(cur, node1):
    node = get_node(cur, node1.id)
    assert node.id == node1.id
    assert node.parent == node1.parent


def test_get_tree_size(cur):
    assert get_tree_size(cur) == 6


def test_get_node_needs_number(cur, root):
    with pytest.raises(TypeError):
        get_node(cur, root)


def test_get_children(cur, root, node1, node2, node3):
    ids = {child.id for child in get_children(cur, root)}
    assert len(ids) == 3
    assert node1.id in ids
    assert node2.id in ids
    assert node3.id in ids


def test_get_child_ids(cur, root, node1, node2, node3):
    ids = set(get_child_ids(cur, root))
    assert len(ids) == 3
    assert node1.id in ids
    assert node2.id in ids
    assert node3.id in ids


def test_get_children_correct_positioning(cur, root, node1, node2, node3):
    ids = [child.id for child in get_children(cur, root)]
    expected = [node1.id, node2.id, node3.id]
    assert ids == expected


def test_get_child_ids_correct_positioning(cur, root, node1, node2, node3):
    ids = list(get_child_ids(cur, root))
    expected = [node1.id, node2.id, node3.id]
    assert ids == expected


def test_get_children_count(cur, root):
    assert get_children_count(cur, root) == 3


def test_get_ancestors(cur, root, node2, node2_1):
    ancestors = list(get_ancestors(cur, node2_1))
    assert len(ancestors) == 2
    assert ancestors[0].id == root.id
    assert ancestors[1].id == node2.id


def test_get_ancestors(cur, root, node2, node2_1, node2_1_1, node2_leaf):
    expected = {root.id, node2.id, node2_1.id, node2_1_1.id}
    ids = set(map(int, get_ancestors(cur, node2_leaf, sort=False)))
    assert ids == expected


def test_get_ancestors_returns_correct_order(cur, root, node2, node2_1,
                                             node2_1_1, node2_leaf):
    expected = [root.id, node2.id, node2_1.id, node2_1_1.id]
    ids = list(map(int, get_ancestors(cur, node2_leaf, sort=True)))
    assert ids == expected


# TODO: mock always returns False, why?
def xtest_get_ancestors_calls_vectorize_nodes(cur, node2_leaf):
    with patch.object(libtree.tree, 'vectorize_nodes') as func:
        get_ancestors(cur, node2_leaf, sort=True)
        assert func.called


def test_get_descendant_ids(cur, root, node1, node2, node3, node2_1, node2_1_1,
                            node2_leaf):
    ids = get_descendant_ids(cur, root)
    expected_nodes = {node1, node2, node3, node2_1, node2_1_1, node2_leaf}
    expected_ids = {node.id for node in expected_nodes}
    assert set(ids) == expected_ids


def test_get_descendants(cur, root, node1, node2, node3, node2_1, node2_1_1,
                         node2_leaf):
    nodes = get_descendants(cur, root)
    ids = {node.id for node in nodes}
    expected_nodes = {node1, node2, node3, node2_1, node2_1_1, node2_leaf}
    expected_ids = {node.id for node in expected_nodes}
    assert ids == expected_ids


def xtest_get_inherited_properties():
    raise NotImplementedError


def xtest_get_inherited_property():
    raise NotImplementedError
