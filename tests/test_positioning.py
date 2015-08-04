from libtree.positioning import (ensure_free_position, find_highest_position,
                                 get_node_at_position, set_position,
                                 shift_positions, swap_node_positions)
from libtree.tree import (change_parent, delete_node, get_children, get_node,
                          insert_node)
from libtree.tree import print_tree  # noqa
from pdb import set_trace as trace  # noqa
import pytest


def test_set_position(per, root):
    set_position(per, root, 0, auto_position=False)
    assert get_node(per, root.id).position == 0


def test_set_positions_with_gap_in_sequence(per, node1, node2, node3):
    set_position(per, node1, 0, auto_position=False)
    set_position(per, node2, 1, auto_position=False)
    set_position(per, node3, 3, auto_position=False)
    assert get_node(per, node1.id).position == 0
    assert get_node(per, node2.id).position == 1
    assert get_node(per, node3.id).position == 3


def test_find_highest_position(per, root):
    assert find_highest_position(per, root) == 3


def test_find_highest_position_non_existing_node(per):
    assert find_highest_position(per, -1) == -1


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


def test_swap_node_positions(per, node1, node2):
    swap_node_positions(per, node1, node2)
    assert get_node(per, node1.id).position == node2.position
    assert get_node(per, node2.id).position == node1.position


def test_insert_node_starts_counting_at_zero(per, node1):
    node1_1 = insert_node(per, node1, 'node1-1', auto_position=True)
    assert node1_1.position == 0


def test_insert_nodes_at_highest_position(per, root):
    highest_position = find_highest_position(per, root)
    node4 = insert_node(per, root, 'node4', position=None, auto_position=True)
    node5 = insert_node(per, root, 'node5', position=-1, auto_position=True)
    assert node4.position == highest_position + 1
    assert node5.position == highest_position + 2

    delete_node(per, node4)
    delete_node(per, node5)


def test_ensure_free_position(per, root):
    ensure_free_position(per, root, 4)
    positions = map(lambda n: n.position, get_children(per, root))
    assert list(positions) == [0, 1, 3]


def test_insert_node_at_specific_position(per, root):
    node0 = insert_node(per, root, 'node0', position=0, auto_position=True)
    positions = map(lambda n: n.position, get_children(per, root))
    assert node0.position == 0
    assert list(positions) == [0, 1, 2, 4]


def test_delete_node_shifts_positions(per, root, node1):
    delete_node(per, node1, auto_position=True)
    positions = map(lambda n: n.position, get_children(per, root))
    assert list(positions) == [0, 1, 3]


def xtest_change_parent_to_highest_position(per, root, node2, node2_1):
    change_parent(per, node3, root, position=None, auto_position=True)
    print_tree(per)
    assert False


def x___test_move_node_before(per, root, node1, node2, node3):
    assert node1.position < node2.position < node3.position
    move_node_before(per, node3, node2)
    node1 = get_node(node1.id)
    node2 = get_node(node2.id)
    node3 = get_node(node3.id)
    assert node1.position < node3.position < node2.position


def x___xtest_move_node_after(per, root, node1, node2, node3):
    assert node1.position < node2.position < node3.position
    move_node_before(per, node3, node2)
    node1 = get_node(node1.id)
    node2 = get_node(node2.id)
    node3 = get_node(node3.id)
    assert node1.position < node3.position < node2.position
