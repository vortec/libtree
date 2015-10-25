# Copyright (c) 2015 Fabian Kochem


from libtree.core.database import is_compatible_postgres_version
from mock import Mock


def test_is_compatible_postgres_version():
    cur = Mock()
    cur.fetchone.return_value = {'server_version': '9.4.1'}
    assert is_compatible_postgres_version(cur) is True

    cur.fetchone.return_value = {'server_version': '9.3.8'}
    assert is_compatible_postgres_version(cur) is False
