# Copyright (c) 2015 CaT Concepts and Training GmbH


from libtree.query import (get_ancestors, get_child_ids, get_children,
                           get_children_count, get_descendants,
                           get_descendant_ids, get_node, get_root_node,
                           get_tree_size)
import libtree
import pytest


def test_get_root_node_non_existing(per):
    with pytest.raises(ValueError):
        get_root_node(per)


def test_get_node_non_existing(per):
    with pytest.raises(ValueError):
        get_node(per, 1)


def test_get_root_node(per, root, node1, node2, node2_1, node2_1_1, node3):
    root = get_root_node(per)
    assert root.parent is None


def test_get_node(per, node1):
    node = get_node(per, node1.id)
    assert node.id == node1.id
    assert node.parent == node1.parent


def test_get_tree_size(per):
    assert get_tree_size(per) == 6


def test_get_node_needs_number(per, root):
    with pytest.raises(TypeError):
        get_node(per, root)


def test_get_children(per, root, node1, node2, node3):
    ids = {child.id for child in get_children(per, root)}
    assert len(ids) == 3
    assert node1.id in ids
    assert node2.id in ids
    assert node3.id in ids


def test_get_child_ids(per, root, node1, node2, node3):
    ids = set(get_child_ids(per, root))
    assert len(ids) == 3
    assert node1.id in ids
    assert node2.id in ids
    assert node3.id in ids


def test_get_children_correct_positioning(per, root, node1, node2, node3):
    ids = [child.id for child in get_children(per, root)]
    expected = [node1.id, node2.id, node3.id]
    assert ids == expected


def test_get_child_ids_correct_positioning(per, root, node1, node2, node3):
    ids = list(get_child_ids(per, root))
    expected = [node1.id, node2.id, node3.id]
    assert ids == expected


def test_get_children_count(per, root):
    assert get_children_count(per, root) == 3


def test_get_ancestors(per, root, node2, node2_1):
    ancestors = list(get_ancestors(per, node2_1))
    assert len(ancestors) == 2
    assert ancestors[0].id == root.id
    assert ancestors[1].id == node2.id


def test_get_ancestors(per, root, node2, node2_1, node2_1_1, node2_leaf):
    expected = {root.id, node2.id, node2_1.id, node2_1_1.id}
    ids = set(map(int, get_ancestors(per, node2_leaf, sort=False)))
    assert ids == expected


def test_get_ancestors_returns_correct_order(per, root, node2, node2_1,
                                             node2_1_1, node2_leaf):
    expected = [root.id, node2.id, node2_1.id, node2_1_1.id]
    ids = list(map(int, get_ancestors(per, node2_leaf, sort=True)))
    assert ids == expected


# TODO: mock always returns False, why?
def xtest_get_ancestors_calls_vectorize_nodes(per, node2_leaf):
    with patch.object(libtree.tree, 'vectorize_nodes') as func:
        get_ancestors(per, node2_leaf, sort=True)
        assert func.called


def test_get_descendant_ids(per, root, node1, node2, node3, node2_1, node2_1_1,
                            node2_leaf):
    ids = get_descendant_ids(per, root)
    expected_nodes = {node1, node2, node3, node2_1, node2_1_1, node2_leaf}
    expected_ids = {node.id for node in expected_nodes}
    assert set(ids) == expected_ids


def test_get_descendants(per, root, node1, node2, node3, node2_1, node2_1_1,
                         node2_leaf):
    nodes = get_descendants(per, root)
    ids = {node.id for node in nodes}
    expected_nodes = {node1, node2, node3, node2_1, node2_1_1, node2_leaf}
    expected_ids = {node.id for node in expected_nodes}
    assert ids == expected_ids


def xtest_get_inherited_properties():
    raise NotImplementedError


def xtest_get_inherited_property():
    raise NotImplementedError
