from libtree.query import (get_ancestors, get_descendants, get_descendant_ids)
import libtree
import pytest


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
    nodes = {node1, node2, node3, node2_1, node2_1_1, node2_leaf}
    expected = {node.id for node in nodes}
    assert set(ids) == expected


def test_get_descendants(per, root):
    with pytest.raises(NotImplementedError):
        get_descendants(per, root)
