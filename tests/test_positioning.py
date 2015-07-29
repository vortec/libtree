from .fixtures import per, root, node1, node2, node3  # noqa
from .fixtures import node2_1, node2_1_1, node2_leaf  # noqa
from libtree.tree import get_children, get_child_ids
from pdb import set_trace as trace  # noqa


def test_get_children_correct_positioning(per, root, node1, node2, node3):
    ids = [child.id for child in get_children(per, root)]
    expected = [node1.id, node2.id, node3.id]
    assert ids == expected


def test_get_child_ids_correct_positioning(per, root, node1, node2, node3):
    ids = list(get_child_ids(per, root))
    expected = [node1.id, node2.id, node3.id]
    assert ids == expected
