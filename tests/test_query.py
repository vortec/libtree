from libtree.query import (get_ancestors, get_descendants, get_descendant_ids)
import pytest


def test_get_ancestors(per, root, node2, node2_1):
    ancestors = list(get_ancestors(per, node2_1))
    assert len(ancestors) == 2
    assert ancestors[0].id == root.id
    assert ancestors[1].id == node2.id


def test_get_descendant_ids(per, root, node1, node2, node3, node2_1, node2_1_1,
                            node2_leaf):
    ids = get_descendant_ids(per, root)
    nodes = {node1, node2, node3, node2_1, node2_1_1, node2_leaf}
    expected = {node.id for node in nodes}
    assert set(ids) == expected


def test_get_descendants(per, root):
    with pytest.raises(NotImplementedError):
        get_descendants(per, root)
