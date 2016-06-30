# Copyright (c) 2016 Fabian Kochem


from libtree.core.positioning import (ensure_free_position,
                                      find_highest_position,
                                      set_position, shift_positions,
                                      swap_node_positions)
from libtree.core.query import get_children, get_node, get_node_at_position
from libtree.core.tree import change_parent, delete_node, insert_node
import uuid
from pdb import set_trace as trace  # noqa
import pytest


def test_set_position(cur, root):
    set_position(cur, root, 0, auto_position=False)
    assert get_node(cur, root.id).position == 0


def test_set_position_autoposition(cur, root, nd1, nd2, nd3):
    set_position(cur, nd1, 0, auto_position=True)
    set_position(cur, nd2, 2, auto_position=True)
    set_position(cur, nd3.id, -1, auto_position=True)
    assert get_node(cur, nd1.id).position == 0
    assert get_node(cur, nd2.id).position == 2
    assert get_node(cur, nd3.id).position == nd3.position + 1


def test_set_positions_with_gap_in_sequence(cur, nd1, nd2, nd3):
    set_position(cur, nd1, 0, auto_position=False)
    set_position(cur, nd2, 1, auto_position=False)
    set_position(cur, nd3, 3, auto_position=False)
    assert get_node(cur, nd1.id).position == 0
    assert get_node(cur, nd2.id).position == 1
    assert get_node(cur, nd3.id).position == 3


def test_find_highest_position(cur, root):
    assert find_highest_position(cur, root) == 3


def test_find_highest_position_non_existing_node(cur):
    assert find_highest_position(cur, str(uuid.uuid4())) == -1


def test_shift_positions_to_the_right(cur, root, nd1, nd2, nd3):
    shift_positions(cur, root, nd2.position, +1)
    assert get_node(cur, nd1.id).position == 0
    assert get_node(cur, nd2.id).position == 2
    assert get_node(cur, nd3.id).position == 4


def test_shift_positions_to_the_left(cur, root, nd1, nd2, nd3):
    shift_positions(cur, root, nd2.position, -1)
    assert get_node(cur, nd1.id).position == 0
    assert get_node(cur, nd2.id).position == 1
    assert get_node(cur, nd3.id).position == 3


def test_get_node_at_position(cur, root, nd3):
    node = get_node_at_position(cur, root, nd3.position)
    assert node.position == nd3.position


def test_get_node_at_position_non_existing(cur, root, nd3):
    with pytest.raises(ValueError):
        get_node_at_position(cur, root, -1)
    with pytest.raises(ValueError):
        get_node_at_position(cur, str(uuid.uuid4()), 1)


def test_swap_node_positions(cur, nd1, nd2):
    swap_node_positions(cur, nd1, nd2)
    assert get_node(cur, nd1.id).position == nd2.position
    assert get_node(cur, nd2.id).position == nd1.position


def test_insert_node_starts_counting_at_zero(cur, nd1):
    nd1_1 = insert_node(cur, nd1, 'nd1-1', auto_position=True)
    assert nd1_1.position == 0


def test_insert_nodes_at_highest_position(cur, root):
    highest_position = find_highest_position(cur, root)
    node4 = insert_node(cur, root, position=None, auto_position=True)
    node5 = insert_node(cur, root, position=-1, auto_position=True)
    assert node4.position == highest_position + 1
    assert node5.position == highest_position + 2

    delete_node(cur, node4)
    delete_node(cur, node5)


def test_ensure_free_position(cur, root):
    ensure_free_position(cur, root, 4)
    positions = map(lambda n: n.position, get_children(cur, root))
    assert list(positions) == [0, 1, 3]


def test_insert_node_at_specific_position(cur, root):
    node0 = insert_node(cur, root, position=0, auto_position=True)
    positions = map(lambda n: n.position, get_children(cur, root))
    assert node0.position == 0
    assert list(positions) == [0, 1, 2, 4]


def test_delete_node_shifts_positions(cur, root, nd1):
    delete_node(cur, nd1, auto_position=True)
    positions = map(lambda n: n.position, get_children(cur, root))
    assert list(positions) == [0, 1, 3]


def test_change_parent_to_highest_position(cur, root, nd2, nd2_1):
    highest_position = find_highest_position(cur, root)
    change_parent(cur, nd2_1, root, position=None, auto_position=True)
    nd2_1 = get_node(cur, nd2_1.id)
    assert nd2_1.position == highest_position + 1


def test_change_parent_starts_couting_at_zero(cur, root, nd2, nd2_1):
    change_parent(cur, nd2_1, nd2, position=None, auto_position=True)
    nd2_1 = get_node(cur, nd2_1.id)
    assert nd2_1.position == 0


def test_change_parent_to_specific_position(cur, root, nd2_1):
    change_parent(cur, nd2_1, root, position=0, auto_position=True)
    positions = map(lambda n: n.position, get_children(cur, root))
    assert list(positions) == [0, 1, 2, 4]
