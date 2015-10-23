# Copyright (c) 2015 Fabian Kochem


from libtree import Transaction
from mock import Mock, MagicMock


def test_it_takes_a_connection():
    conn = Mock()
    assert Transaction(conn, Mock()).connection is conn


def test_it_disables_autocommit():
    conn = Mock()
    transaction = Transaction(conn, Mock())
    assert transaction.connection.autocommit is False


def test_it_creates_a_cursor():
    conn = Mock()
    Transaction(conn, Mock())
    assert conn.cursor.called


def test_commit():
    conn = Mock()
    Transaction(conn, Mock()).commit()
    assert conn.commit.called


def test_rollback():
    conn = Mock()
    Transaction(conn, Mock()).rollback()
    assert conn.rollback.called


def test_is_compatible_postgres_version():
    transaction = Transaction(MagicMock(), Mock())
    transaction.cursor.fetchone.return_value = {'server_version': '9.4.1'}
    assert transaction.is_compatible_postgres_version() is True
    transaction.cursor.fetchone.return_value = {'server_version': '9.3.8'}
    assert transaction.is_compatible_postgres_version() is False


def xtest_install():
    raise NotImplementedError


def xtest_uninstall():
    raise NotImplementedError


def xtest_clear():
    raise NotImplementedError


def xtest_print_tree():
    raise NotImplementedError


def xtest_get_tree_size():
    raise NotImplementedError


def xtest_get_root_node():
    raise NotImplementedError


def xtest_insert_root_node():
    raise NotImplementedError


def xtest_get_node():
    raise NotImplementedError


def xtest_get_node_at_position():
    raise NotImplementedError


def xtest_get_nodes_by_property_dict():
    raise NotImplementedError


def xtest_get_nodes_by_property_key():
    raise NotImplementedError


def xtest_get_nodes_by_property_value():
    raise NotImplementedError
