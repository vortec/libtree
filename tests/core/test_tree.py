# Copyright (c) 2015 Fabian Kochem


from libtree.core.tree import change_parent, delete_node, insert_node
from libtree.core.query import (get_ancestor_ids, get_child_ids, get_children,
                                get_descendant_ids, get_node)
from pdb import set_trace as trace  # noqa
import pytest


def test_insert_root_node_with_auto_position(cur):
    root = insert_node(cur, None, 'folder', auto_position=True)
    delete_node(cur, root)


def test_insert_node(cur, root, nd1, nd2, nd2_1, nd2_1_1, nd3):
    assert root.parent is None
    assert nd1.parent == root.id
    assert nd2.parent == root.id
    assert nd2_1.parent == nd2.id
    assert nd2_1_1.parent == nd2_1.id
    assert nd3.parent == root.id


def test_insert_node_sets_properties(root):
    assert root.properties == {
        'type': 'root',
        'boolean': False,
        'integer': 1
    }


def test_insert_node_sets_position(nd1):
    assert nd1.position == 4


def test_change_parent(cur, root, nd1, nd2, nd2_1, nd2_1_1,
                       nd2_leaf):
    """
    Tree layout before move:
    /
      - nd1
      - nd2
        - nd2-1
          - nd2-1-1
            - nd2-leaf
      - nd3

    Expected tree layout after move:

    /
      - nd1
        - nd2-1
          - nd2-1-1
            - nd2-leaf
      - nd2
      - nd3
    """
    # We expect nd2-1 to be child of nd2 and nd2-1-1 to be child
    # of nd2-1.

    # Move nd2-1 from nd2 to nd1
    _temp_node = change_parent(cur, nd2_1.id, nd1, auto_position=False)

    # Return value should have new parent set
    assert _temp_node.parent == nd1.id

    # nd2-1 should have nd1 as parent
    node = get_node(cur, nd2_1.id)
    assert node.parent == nd1.id

    # nd2-1-1 should still have the same parent (nd2-1)
    child_node = get_node(cur, nd2_1_1.id)
    assert child_node.parent == nd2_1.id

    # nd2-leaf should still have the same parent (nd2-1-1)
    child_node = get_node(cur, nd2_leaf.id)
    assert child_node.parent == nd2_1_1.id

    # The ancestor set of nd2-1 should now contain nd1 and root
    assert set(get_ancestor_ids(cur, nd2_1)) == {root.id, nd1.id}

    # The ancestor set of nd2-1-1 should now contain nd2-1, nd1 and root
    expected = {root.id, nd1.id, nd2_1.id}
    assert set(get_ancestor_ids(cur, nd2_1_1)) == expected

    # The ancestor set of nd2-leaf should now contain node-2-1-1, nd2-1,
    # nd1 and root
    expected = {root.id, nd1.id, nd2_1.id, nd2_1_1.id}
    assert set(get_ancestor_ids(cur, nd2_leaf)) == expected

    # The ancestor set of nd2 should now only contain root
    assert set(get_ancestor_ids(cur, nd2)) == {root.id}

    # Check if nd2-1, nd2-1-1 and nd2-leaf are part of nd1's descendant
    # set now
    expected = {nd2_1.id, nd2_1_1.id, nd2_leaf.id}
    assert set(get_descendant_ids(cur, nd1)) == expected

    # nd2's descendant set should be empty now
    assert set(get_descendant_ids(cur, nd2)) == set()

    # Last but not least, the children function proof what we checked above too
    assert len(set(get_children(cur, nd1))) == 1
    assert len(set(get_children(cur, nd2))) == 0


def test_change_parent_dont_move_into_own_subtree(cur, nd1, nd2_1):
    with pytest.raises(ValueError):
        change_parent(cur, nd1, nd2_1)


def test_delete_node(cur, nd1, nd2_1, nd2_1_1, nd2_leaf):
    """
        Tree layout before delete:
        /
          - nd1
            - nd2-1
              - nd2-1-1
                - nd2-leaf
          - nd2
          - nd3

        Expected tree layout after move:
        /
          - nd1
            - nd2-1
          - nd2
          - nd3
    """
    delete_node(cur, nd2_1_1, auto_position=False)

    # Deleted node doesn't exist anymore
    with pytest.raises(ValueError):
        get_node(cur, nd2_1_1.id)

    # nd2-1 has no children and no descendants
    assert set(get_child_ids(cur, nd2_1)) == set()
    assert set(get_child_ids(cur, nd2_1_1)) == set()
    assert set(get_descendant_ids(cur, nd2_1)) == set()

    # nd1 just contains nd2-1
    assert set(get_child_ids(cur, nd1)) == {nd2_1.id}
    assert set(get_descendant_ids(cur, nd1)) == {nd2_1.id}

    # Ancestor and descendant sets of nd2-1-1 and nd2-leaf are empty
    # (or raise error in the future because they don't exist anymore)
    assert set(get_ancestor_ids(cur, nd2_1_1)) == set()
    assert set(get_ancestor_ids(cur, nd2_leaf)) == set()
    assert set(get_descendant_ids(cur, nd2_1_1)) == set()
    assert set(get_descendant_ids(cur, nd2_leaf)) == set()


def test_delete_node_by_id(cur, nd1, nd2_1):
    delete_node(cur, nd2_1.id, auto_position=True)

    assert set(get_child_ids(cur, nd1)) == set()
