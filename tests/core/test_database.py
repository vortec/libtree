# Copyright (c) 2016 Fabian Kochem


from libtree.core.database import (is_compatible_postgres_version,
                                   make_dsn_from_env)
from mock import Mock


def test_is_compatible_postgres_version():
    cur = Mock()
    cur.fetchone.return_value = {'server_version': '9.5.0'}
    assert is_compatible_postgres_version(cur) is True

    cur.fetchone.return_value = {'server_version': '9.3.8'}
    assert is_compatible_postgres_version(cur) is False


def test_make_dsn_from_env():
    env = {
        'PGHOST': 'localhost',
        'PGPORT': 5432,
        'PGUSER': 'foo',
        'PGPASSWORD': 'secret',
        'PGDATABASE': 'mydb'
    }

    conn_string = make_dsn_from_env(env)
    expected = 'host=localhost port=5432 user=foo password=secret dbname=mydb'
    assert conn_string == expected
