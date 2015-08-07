from libtree.tree import (print_tree, get_tree_size, get_root_node, get_node,
                          delete_node, get_children, get_child_ids,
                          get_children_count, change_parent)
from libtree.query import (get_ancestor_ids, get_descendant_ids)
from pdb import set_trace as trace  # noqa
import pytest


def test_get_root_node_non_existing(per):
    with pytest.raises(ValueError):
        get_root_node(per)


def test_get_node_non_existing(per):
    with pytest.raises(ValueError):
        get_node(per, 1)


def test_insert_node(per, root, node1, node2, node2_1, node2_1_1, node3):
    assert root.parent is None
    assert node1.parent == root.id
    assert node2.parent == root.id
    assert node2_1.parent == node2.id
    assert node2_1_1.parent == node2_1.id
    assert node3.parent == root.id


def test_get_root_node(per):
    root = get_root_node(per)
    assert root.parent is None


def test_get_node(per, node1):
    node = get_node(per, node1.id)
    assert node.id == node1.id
    assert node.parent == node1.parent


def test_print_tree(per, capsys):
    print_tree(per)
    out, _ = capsys.readouterr()
    expected = """root
  node1
  node2
    node2-1
      node2-1-1
  node3
"""
    assert out == expected


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
    change_parent(per, node2_1, node1, auto_position=False)

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
