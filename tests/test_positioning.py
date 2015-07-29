from libtree.positioning import set_position, swap_node_positions  # noqa
from libtree.tree import get_children, get_child_ids, get_node  # noqa
from pdb import set_trace as trace  # noqa


def test_set_position(per, node2_leaf):
    new_position = 1
    set_position(per, node2_leaf, new_position)
    new_node = get_node(per, node2_leaf.id)
    assert new_node.position == new_position


def test_swap_node_positions(per, node1, node2):
    swap_node_positions(per, node1, node2)

    new_node1 = get_node(per, node1.id)
    new_node2 = get_node(per, node2.id)
    assert new_node1.position == node2.position
    assert new_node2.position == node1.position


# def test_shift_node


def xtest_move_node_before(per, root, node1, node2, node3):
    assert node1.position < node2.position < node3.position
    move_node_before(per, node3, node2)
    node1 = get_node(node1.id)
    node2 = get_node(node2.id)
    node3 = get_node(node3.id)
    assert node1.position < node3.position < node2.position


def xtest_move_node_before(per, root, node1, node2, node3):
    assert node1.position < node2.position < node3.position
    move_node_before(per, node3, node2)
    node1 = get_node(node1.id)
    node2 = get_node(node2.id)
    node3 = get_node(node3.id)
    assert node1.position < node3.position < node2.position
