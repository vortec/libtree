from libtree.config import config
from libtree.persistance import *  # noqa
from libtree.tree import *  # noqa
from pdb import set_trace as trace  # noqa
import pytest


@pytest.fixture(scope='module')
def per():
    if config['mysql']['enabled']:
        conf = config['mysql']
        per = MySQLPersistance(host=conf['host'],
                               user=conf['user'],
                               passwd=conf['password'],
                               db=conf['test_database'])
    else:
        per = PostgreSQLPersistance(config['postgres']['test_details'])

    per.drop_tables()
    per.create_tables()
    per.flush_tables()
    return per


@pytest.fixture(scope='module')
def root(per):
    return create_node(per, None, 'root')


@pytest.fixture(scope='module')
def node1(per, root):
    return create_node(per, root, 'node1')


@pytest.fixture(scope='module')
def node2(per, root):
    return create_node(per, root, 'node2')


@pytest.fixture(scope='module')
def node2_1(per, node2):
    return create_node(per, node2, 'node2-1')


@pytest.fixture(scope='module')
def node2_1_1(per, node2_1):
    return create_node(per, node2_1, 'node2-1-1')


@pytest.fixture(scope='module')
def node2_leaf(per, node2_1_1):
    return create_node(per, node2_1_1, 'node2-leaf')


def test_create_node(root, node1, node2, node2_1, node2_1_1):
    assert root.parent is None
    assert node1.parent == root.id
    assert node2.parent == root.id
    assert node2_1.parent == node2.id
    assert node2_1_1.parent == node2_1.id


def test_get_node(per, node1):
    node = get_node(per, node1.id)
    assert node.id == node1.id
    assert node.parent == node1.parent


def test_get_node_needs_number(per, root):
    with pytest.raises(TypeError):
        get_node(per, root)


def test_get_ancestors(per, root, node2, node2_1):
    ancestors = list(get_ancestors(per, node2_1))
    assert len(ancestors) == 2
    assert ancestors[0].id == root.id
    assert ancestors[1].id == node2.id


def test_get_descendant_ids(per, root, node1, node2, node2_1, node2_1_1,
                            node2_leaf):
    ids = get_descendant_ids(per, root)
    expected = {node1.id, node2.id, node2_1.id, node2_1_1.id, node2_leaf.id}
    assert set(ids) == expected


def test_get_children(per, root, node1, node2):
    ids = {child.id for child in get_children(per, root)}
    assert len(ids) == 2
    assert node1.id in ids
    assert node2.id in ids


def test_move_node(per, root, node1, node2, node2_1, node2_1_1, node2_leaf):
    """
        Expected tree layout after move:

        /  (#1)
          - node1  (#2)
            - node2-1  (#4)
              - node2-1-1  (#5)
                - node2-leaf (#6)
          - node2  (#3)

    """
    # We expect node2-1 to be child of node2 and node2-1-1 to be child
    # of node2-1.

    # Move node2-1 from node2 to node1
    move_node(per, node2_1, node1)

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
