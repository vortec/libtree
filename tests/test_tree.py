# Copyright (c) 2015 CaT Concepts and Training GmbH


from libtree.tree import change_parent, delete_node, insert_node
from libtree.query import (get_ancestor_ids, get_child_ids, get_children,
                           get_descendant_ids, get_node)
from pdb import set_trace as trace  # noqa
import pytest


def test_insert_root_node_with_auto_position(per):
    root = insert_node(per, None, 'folder', auto_position=True)
    delete_node(per, root)


def test_insert_node(per, root, node1, node2, node2_1, node2_1_1, node3):
    assert root.parent is None
    assert node1.parent == root.id
    assert node2.parent == root.id
    assert node2_1.parent == node2.id
    assert node2_1_1.parent == node2_1.id
    assert node3.parent == root.id


def test_insert_node_sets_properties(root):
    assert root.properties == {
        'title': 'Root',
        'type': 'root',
        'boolean': False,
        'integer': 1
    }


def test_insert_node_sets_position(node1):
    assert node1.position == 4


def test_change_parent(per, root, node1, node2, node2_1, node2_1_1,
                       node2_leaf):
    """
    Tree layout before move:
    /
      - node1
      - node2
        - node2-1
          - node2-1-1
            - node2-leaf
      - node3

    Expected tree layout after move:

    /
      - node1
        - node2-1
          - node2-1-1
            - node2-leaf
      - node2
      - node3
    """
    # We expect node2-1 to be child of node2 and node2-1-1 to be child
    # of node2-1.

    # Move node2-1 from node2 to node1
    _temp_node = change_parent(per, node2_1, node1, auto_position=False)

    # Return value should have new parent set
    assert _temp_node.parent == node1.id

    # node2-1 should have node1 as parent
    node = get_node(per, node2_1.id)
    assert node.parent == node1.id

    # node2-1-1 should still have the same parent (node2-1)
    child_node = get_node(per, node2_1_1.id)
    assert child_node.parent == node2_1.id

    # node2-leaf should still have the same parent (node2-1-1)
    child_node = get_node(per, node2_leaf.id)
    assert child_node.parent == node2_1_1.id

    # The ancestor set of node2-1 should now contain node1 and root
    assert set(get_ancestor_ids(per, node2_1)) == {root.id, node1.id}

    # The ancestor set of node2-1-1 should now contain node2-1, node1 and root
    expected = {root.id, node1.id, node2_1.id}
    assert set(get_ancestor_ids(per, node2_1_1)) == expected

    # The ancestor set of node2-leaf should now contain node-2-1-1, node2-1,
    # node1 and root
    expected = {root.id, node1.id, node2_1.id, node2_1_1.id}
    assert set(get_ancestor_ids(per, node2_leaf)) == expected

    # The ancestor set of node2 should now only contain root
    assert set(get_ancestor_ids(per, node2)) == {root.id}

    # Check if node2-1, node2-1-1 and node2-leaf are part of node1's descendant
    # set now
    expected = {node2_1.id, node2_1_1.id, node2_leaf.id}
    assert set(get_descendant_ids(per, node1)) == expected

    # node2's descendant set should be empty now
    assert set(get_descendant_ids(per, node2)) == set()

    # Last but not least, the children function proof what we checked above too
    assert len(set(get_children(per, node1))) == 1
    assert len(set(get_children(per, node2))) == 0


def test_change_parent_dont_move_into_own_subtree(per, node1, node2_1):
    with pytest.raises(ValueError):
        change_parent(per, node1, node2_1)


def test_delete_node(per, node1, node2_1, node2_1_1, node2_leaf):
    """
        Tree layout before delete:
        /
          - node1
            - node2-1
              - node2-1-1
                - node2-leaf
          - node2
          - node3

        Expected tree layout after move:
        /
          - node1
            - node2-1
          - node2
          - node3
    """
    delete_node(per, node2_1_1, auto_position=False)

    # Deleted node doesn't exist anymore
    with pytest.raises(ValueError):
        get_node(per, node2_1_1.id)

    # node2-1 has no children and no descendants
    assert set(get_child_ids(per, node2_1)) == set()
    assert set(get_child_ids(per, node2_1_1)) == set()
    assert set(get_descendant_ids(per, node2_1)) == set()

    # node1 just contains node2-1
    assert set(get_child_ids(per, node1)) == {node2_1.id}
    assert set(get_descendant_ids(per, node1)) == {node2_1.id}

    # Ancestor and descendant sets of node2-1-1 and node2-leaf are empty
    # (or raise error in the future because they don't exist anymore)
    assert set(get_ancestor_ids(per, node2_1_1)) == set()
    assert set(get_ancestor_ids(per, node2_leaf)) == set()
    assert set(get_descendant_ids(per, node2_1_1)) == set()
    assert set(get_descendant_ids(per, node2_leaf)) == set()
