# Copyright (c) 2015 CaT Concepts and Training GmbH


try:
    from libtree.config import config
except ImportError:
    config = {
        'postgres': {
            'test_details': 'dbname=test_libtree user=postgres'
        }
    }

from libtree.persistance import PostgreSQLPersistance
from libtree.query import get_node
from libtree.tree import insert_node
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


def get_or_create_node(per, parent, properties, *args, **kwargs):
    xtype = properties.get('type')
    node_id = node_ids.get(xtype, None)
    if node_id is None:
        node = insert_node(per, parent, properties=properties, *args, **kwargs)
        node_ids[xtype] = node.id
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
    props = {
        'title': 'Root',
        'type': 'root',
        'boolean': False,
        'integer': 1
    }
    return get_or_create_node(per, None, auto_position=False, properties=props)


@pytest.fixture
def node1(per, root):
    props = {
        'type': 'node1',
        'title': 'Node 1'
    }
    return get_or_create_node(per, root, position=4, auto_position=False,
                              properties=props)


@pytest.fixture
def node2(per, root):
    props = {
        'type': 'node2',
        'title': 'Node 2',
        'boolean': True,
        'foo': 'bar'
    }
    return get_or_create_node(per, root, position=5, auto_position=False,
                              properties=props)


@pytest.fixture
def node3(per, root):
    props = {
        'type': 'node3',
        'title': 'Node 3'
    }
    return get_or_create_node(per, root, position=6, auto_position=False,
                              properties=props)


@pytest.fixture
def node2_1(per, node2):
    props = {
        'type': 'node2_1',
        'title': 'Node 2-1'
    }
    return get_or_create_node(per, node2, auto_position=False,
                              properties=props)


@pytest.fixture
def node2_1_1(per, node2_1):
    props = {
        'type': 'node2_1_1',
        'title': 'Node 2-1-1',
        'boolean': False
    }
    return get_or_create_node(per, node2_1, auto_position=False,
                              properties=props)


@pytest.fixture
def node2_leaf(per, node2_1_1):
    props = {
        'type': 'node2_leaf',
        'title': 'Node 2-leaf'
    }
    return get_or_create_node(per, node2_1_1, auto_position=False,
                              properties=props)
