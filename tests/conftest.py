from libtree.config import config
from libtree.tree import insert_node, get_node
from libtree.persistance import PostgreSQLPersistance
import pytest


"""
Create this structure:

/
  - node1
  - node2
    - node2-1
      - node2-1-1
        - node2-leaf
  - node3
"""

node_ids = {}


def make_persistance():
    return PostgreSQLPersistance(config['postgres']['test_details'])


def get_or_create_node(per, parent, type, *args, **kwargs):
    node_id = node_ids.get(type, None)
    if node_id is None:
        node = insert_node(per, parent, type, *args, **kwargs)
        node_ids[type] = node.id
        return node
    return get_node(per, node_id)


@pytest.fixture(scope='module')
def per(request):
    per = make_persistance()
    per.set_autocommit(False)

    node_ids.clear()
    per.drop_tables()
    per.create_schema()
    per.create_triggers()

    def fin():
        per.rollback()
    request.addfinalizer(fin)

    return per


@pytest.fixture
def root(per):
    attrs = {
        'title': 'Root'
    }
    props = {
        'boolean': False,
        'string': 'a',
        'integer': 1
    }
    return get_or_create_node(per, None, 'root', auto_position=False,
                              attributes=attrs, properties=props)


@pytest.fixture
def node1(per, root):
    return get_or_create_node(per, root, 'node1', position=4,
                              auto_position=False)


@pytest.fixture
def node2(per, root):
    props = {
        'boolean': True,
        'string': 'b',
        'foo': 'bar'
    }
    return get_or_create_node(per, root, 'node2', position=5,
                              auto_position=False, properties=props)


@pytest.fixture
def node3(per, root):
    return get_or_create_node(per, root, 'node3', position=6,
                              auto_position=False)


@pytest.fixture
def node2_1(per, node2):
    return get_or_create_node(per, node2, 'node2-1', auto_position=False)


@pytest.fixture
def node2_1_1(per, node2_1):
    props = {
        'boolean': False,
        'string': 'c'
    }
    return get_or_create_node(per, node2_1, 'node2-1-1', auto_position=False,
                              properties=props)


@pytest.fixture
def node2_leaf(per, node2_1_1):
    return get_or_create_node(per, node2_1_1, 'node2-leaf',
                              auto_position=False)
