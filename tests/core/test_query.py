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


def test_get_root_node(cur, root, nd1, nd2, nd2_1, nd2_1_1, nd3):
    root = get_root_node(cur)
    assert root.parent is None


def test_get_node(cur, nd1):
    node = get_node(cur, nd1.id)
    assert node.id == nd1.id
    assert node.parent == nd1.parent


def test_get_tree_size(cur):
    assert get_tree_size(cur) == 6


def test_get_node_needs_number(cur, root):
    with pytest.raises(TypeError):
        get_node(cur, root)


def test_get_children(cur, root, nd1, nd2, nd3):
    ids = {child.id for child in get_children(cur, root)}
    assert len(ids) == 3
    assert nd1.id in ids
    assert nd2.id in ids
    assert nd3.id in ids


def test_get_child_ids(cur, root, nd1, nd2, nd3):
    ids = set(get_child_ids(cur, root))
    assert len(ids) == 3
    assert nd1.id in ids
    assert nd2.id in ids
    assert nd3.id in ids


def test_get_children_correct_positioning(cur, root, nd1, nd2, nd3):
    ids = [child.id for child in get_children(cur, root)]
    expected = [nd1.id, nd2.id, nd3.id]
    assert ids == expected


def test_get_child_ids_correct_positioning(cur, root, nd1, nd2, nd3):
    ids = list(get_child_ids(cur, root))
    expected = [nd1.id, nd2.id, nd3.id]
    assert ids == expected


def test_get_children_count(cur, root):
    assert get_children_count(cur, root) == 3


def test_get_ancestors(cur, root, nd2, nd2_1):
    ancestors = list(get_ancestors(cur, nd2_1))
    assert len(ancestors) == 2
    assert ancestors[0].id == root.id
    assert ancestors[1].id == nd2.id


def test_get_ancestors(cur, root, nd2, nd2_1, nd2_1_1, nd2_leaf):
    expected = {root.id, nd2.id, nd2_1.id, nd2_1_1.id}
    ids = set(map(int, get_ancestors(cur, nd2_leaf, sort=False)))
    assert ids == expected


def test_get_ancestors_returns_correct_order(cur, root, nd2, nd2_1,
                                             nd2_1_1, nd2_leaf):
    expected = [root.id, nd2.id, nd2_1.id, nd2_1_1.id]
    ids = list(map(int, get_ancestors(cur, nd2_leaf, sort=True)))
    assert ids == expected


# TODO: mock always returns False, why?
def xtest_get_ancestors_calls_vectorize_nodes(cur, nd2_leaf):
    with patch.object(libtree.tree, 'vectorize_nodes') as func:
        get_ancestors(cur, nd2_leaf, sort=True)
        assert func.called


def test_get_descendant_ids(cur, root, nd1, nd2, nd3, nd2_1, nd2_1_1,
                            nd2_leaf):
    ids = get_descendant_ids(cur, root)
    expected_nodes = {nd1, nd2, nd3, nd2_1, nd2_1_1, nd2_leaf}
    expected_ids = {node.id for node in expected_nodes}
    assert set(ids) == expected_ids


def test_get_descendants(cur, root, nd1, nd2, nd3, nd2_1, nd2_1_1,
                         nd2_leaf):
    nodes = get_descendants(cur, root)
    ids = {node.id for node in nodes}
    expected_nodes = {nd1, nd2, nd3, nd2_1, nd2_1_1, nd2_leaf}
    expected_ids = {node.id for node in expected_nodes}
    assert ids == expected_ids


def xtest_get_inherited_properties():
    raise NotImplementedError


def xtest_get_inherited_property():
    raise NotImplementedError
