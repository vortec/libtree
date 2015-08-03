from libtree.positioning import (ensure_free_position, find_highest_position,
                                 get_node_at_position, set_position,
                                 shift_positions, swap_node_positions)
from libtree.tree import get_children, get_node, insert_node
from pdb import set_trace as trace  # noqa
import pytest


def test_set_position(per, root):
    set_position(per, root, 0, auto_position=False)
    assert get_node(per, root.id).position == 0


def test_set_position_with_gap_in_sequence(per, node1, node2, node3):
    set_position(per, node1, 0, auto_position=False)
    set_position(per, node2, 1, auto_position=False)
    set_position(per, node3, 3, auto_position=False)
    assert get_node(per, node1.id).position == 0
    assert get_node(per, node2.id).position == 1
    assert get_node(per, node3.id).position == 3


def test_shift_positions_to_the_right(per, root, node1, node2, node3):
    shift_positions(per, root, node2.position, +1)
    assert get_node(per, node1.id).position == 0
    assert get_node(per, node2.id).position == 2
    assert get_node(per, node3.id).position == 4


def test_shift_positions_to_the_left(per, root, node1, node2, node3):
    shift_positions(per, root, node2.position, -1)
    assert get_node(per, node1.id).position == 0
    assert get_node(per, node2.id).position == 1
    assert get_node(per, node3.id).position == 3


def test_get_node_at_position(per, root, node3):
    node = get_node_at_position(per, root, node3.position)
    assert node.position == node3.position


def test_get_node_at_position_non_existing(per, root, node3):
    with pytest.raises(ValueError):
        get_node_at_position(per, root, -1)
    with pytest.raises(ValueError):
        get_node_at_position(per, -1, 1)


def test_find_highest_position(per, root):
    assert find_highest_position(per, root) == 3


def test_find_highest_position_non_existing_node(per):
    with pytest.raises(ValueError):
        find_highest_position(per, -1)


def test_swap_node_positions(per, node1, node2):
    swap_node_positions(per, node1, node2)
    assert get_node(per, node1.id).position == node2.position
    assert get_node(per, node2.id).position == node1.position


def test_insert_node_at_highest_position(per, root, node1, node2, node3):
    node4 = insert_node(per, root, 'node4', position=None, auto_position=True)
    node5 = insert_node(per, root, 'node5', position=-1, auto_position=True)
    assert node4.position == 4
    assert node5.position == 5


def test_ensure_free_position(per, root):
    ensure_free_position(per, root, 4)
    positions = map(lambda n: n.position, get_children(per, root))
    assert list(positions) == [0, 1, 3, 5, 6]


def test_insert_node_at_specific_position(per, root):
    node0 = insert_node(per, root, 'node0', position=0, auto_position=True)
    positions = map(lambda n: n.position, get_children(per, root))
    assert node0.position == 0
    assert list(positions) == [0, 1, 2, 4, 6, 7]


def x___test_move_node_before(per, root, node1, node2, node3):
    assert node1.position < node2.position < node3.position
    move_node_before(per, node3, node2)
    node1 = get_node(node1.id)
    node2 = get_node(node2.id)
    node3 = get_node(node3.id)
    assert node1.position < node3.position < node2.position


def x___xtest_move_node_before(per, root, node1, node2, node3):
    assert node1.position < node2.position < node3.position
    move_node_before(per, node3, node2)
    node1 = get_node(node1.id)
    node2 = get_node(node2.id)
    node3 = get_node(node3.id)
    assert node1.position < node3.position < node2.position
