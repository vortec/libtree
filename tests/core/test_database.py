# Copyright (c) 2016 Fabian Kochem


from uuid import uuid4

from mock import Mock

from libtree.core.database import (is_compatible_postgres_version,
                                   is_installed, make_dsn_from_env,
                                   table_exists)


def test_is_compatible_postgres_version():
    cur = Mock()
    cur.fetchone.return_value = {'server_version': '9.5.0'}
    assert is_compatible_postgres_version(cur) is True

    cur.fetchone.return_value = {'server_version': '9.3.8'}
    assert is_compatible_postgres_version(cur) is False


def test_is_installed(trans, cur):
    assert is_installed(cur) is True

    trans.uninstall()
    assert is_installed(cur) is False

    trans.install()
    assert is_installed(cur) is True


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


def test_table_exists(cur):
    assert table_exists(cur, 'nodes') is True
    assert table_exists(cur, str(uuid4()).split('-')[-1]) is False
