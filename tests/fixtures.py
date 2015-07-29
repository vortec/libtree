from libtree.config import config
from libtree.tree import insert_node
from libtree.persistance import PostgreSQLPersistance
import pytest


@pytest.fixture(scope='session')
def per(request):
    per = PostgreSQLPersistance(config['postgres']['test_details'])

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
