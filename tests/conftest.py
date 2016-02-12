# Copyright (c) 2015 Fabian Kochem


from libtree import Node, Transaction
from libtree.core.database import make_dsn_from_env
from libtree.core.query import get_node
from libtree.core.tree import insert_node
import os
import pytest

try:
    from psycopg2cffi import compat
except ImportError:
    pass
else:
    compat.register()

import psycopg2


"""
Create this structure:

/
  - nd1
  - nd2
    - nd2-1
      - nd2-1-1
        - nd2-leaf
  - nd3
"""

node_ids = {}


def get_or_create_nd(cur, parent, properties, *args, **kwargs):
    xtype = properties.get('type')
    node_id = node_ids.get(xtype, None)
    if node_id is None:
        node = insert_node(cur, parent, properties=properties, *args, **kwargs)
        node_ids[xtype] = node.id
        return node
    return get_node(cur, node_id)


@pytest.fixture(scope='module')
def trans(request):
    dsn = make_dsn_from_env(os.environ)
    connection = psycopg2.connect(dsn)
    transaction = Transaction(connection, Node)

    node_ids.clear()
    transaction.install()
    transaction.commit()

    def fin():
        transaction.uninstall()
        transaction.commit()
    request.addfinalizer(fin)

    return transaction


@pytest.fixture(scope='module')
def cur(trans):
    return trans.cursor


@pytest.fixture
def root(cur):
    props = {
        'type': 'root',
        'boolean': False,
        'integer': 1
    }
    return get_or_create_nd(cur, None, auto_position=False, properties=props)


@pytest.fixture
def nd1(cur, root):
    props = {
        'type': 'nd1',
        'title': 'Node 1'
    }
    return get_or_create_nd(cur, root, position=4, auto_position=False,
                            properties=props)


@pytest.fixture
def nd2(cur, root):
    props = {
        'type': 'nd2',
        'title': 'Node 2',
        'boolean': True,
        'foo': 'bar'
    }
    return get_or_create_nd(cur, root, position=5, auto_position=False,
                            properties=props)


@pytest.fixture
def nd3(cur, root):
    props = {
        'type': 'nd3',
        'title': 'Node 3'
    }
    return get_or_create_nd(cur, root, position=6, auto_position=False,
                            properties=props)


@pytest.fixture
def nd2_1(cur, nd2):
    props = {
        'type': 'nd2_1',
        'title': 'Node 2-1'
    }
    return get_or_create_nd(cur, nd2, auto_position=False,
                            properties=props)


@pytest.fixture
def nd2_1_1(cur, nd2_1):
    props = {
        'type': 'nd2_1_1',
        'title': 'Node 2-1-1',
        'boolean': False
    }
    return get_or_create_nd(cur, nd2_1, auto_position=False,
                            properties=props)


@pytest.fixture
def nd2_leaf(cur, nd2_1_1):
    props = {
        'type': 'nd2_leaf',
        'title': 'Node 2-leaf'
    }
    return get_or_create_nd(cur, nd2_1_1, auto_position=False,
                            properties=props)
