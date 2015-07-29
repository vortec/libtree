from libtree.config import config
from libtree.tree import insert_node
from libtree.persistance import PostgreSQLPersistance
import pytest


def make_persistance():
    return PostgreSQLPersistance(config['postgres']['test_details'])


@pytest.fixture(scope='session')
def per(request):
    per = make_persistance()
    per.set_autocommit(True)

    per.drop_tables()
    per.create_tables()
    per.create_triggers()

    return per


@pytest.fixture(scope='session')
def root(per):
    return insert_node(per, None, 'root')


@pytest.fixture(scope='session')
def node1(per, root):
    return insert_node(per, root, 'node1', position=0)


@pytest.fixture(scope='session')
def node2(per, root):
    return insert_node(per, root, 'node2', position=1)


@pytest.fixture(scope='session')
def node3(per, root):
    return insert_node(per, root, 'node3', position=2)


@pytest.fixture(scope='session')
def node2_1(per, node2):
    return insert_node(per, node2, 'node2-1')


@pytest.fixture(scope='session')
def node2_1_1(per, node2_1):
    return insert_node(per, node2_1, 'node2-1-1')


@pytest.fixture(scope='session')
def node2_leaf(per, node2_1_1):
    return insert_node(per, node2_1_1, 'node2-leaf')


"""
    ins = insert_node
    nodes = {}
    nodes['root'] = ins(per, None, 'root')
    nodes['node1'] = ins(per, nodes['root'], 'node1', position=0)
    nodes['node2'] = ins(per, nodes['root'], 'node2', position=1)
    nodes['node3'] = ins(per, nodes['root'], 'node3', position=2)
    nodes['node2_1'] = ins(per, nodes['node2'], 'node2_1')
    nodes['node2_1_1'] = ins(per, nodes['node2_1'], 'node2_1_1')
    nodes['node2_leaf'] = ins(per, nodes['node2_1_1'], 'node2_leaf')
"""
