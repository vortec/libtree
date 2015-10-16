# Copyright (c) 2015 Fabian Kochem


from libtree import Transaction
from mock import Mock


def test_it_takes_a_connection():
    conn = Mock()
    assert Transaction(connection=conn).connection is conn


def test_it_disables_autocommit():
    conn = Mock()
    transaction = Transaction(connection=conn)
    assert transaction.connection.autocommit is False


def test_it_creates_a_cursor():
    conn = Mock()
    Transaction(connection=conn)
    assert conn.cursor.called


def test_commit():
    conn = Mock()
    Transaction(connection=conn).commit()
    assert conn.commit.called


def test_rollback():
    conn = Mock()
    Transaction(connection=conn).rollback()
    assert conn.rollback.called


def xtest_check_postgres_version():
    raise NotImplementedError


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
