# Copyright (c) 2015 Fabian Kochem


from libtree import core, Transaction
from mock import Mock, patch


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


@patch.object(core, 'is_compatible_postgres_version')
def test_is_compatible_postgres_version(mock):
    transaction = Transaction(Mock(), Mock())
    transaction.is_compatible_postgres_version()
    mock.assert_called_with(transaction.cursor)


@patch.object(core, 'create_schema')
@patch.object(core, 'create_triggers')
def test_install(mock1, mock2):
    transaction = Transaction(Mock(), Mock())
    transaction.install()
    mock1.assert_called_with(transaction.cursor)
    mock2.assert_called_with(transaction.cursor)


@patch.object(core, 'drop_tables')
def test_uninstall(mock):
    transaction = Transaction(Mock(), Mock())
    transaction.uninstall()
    mock.assert_called_with(transaction.cursor)


@patch.object(core, 'flush_tables')
def test_clear(mock):
    transaction = Transaction(Mock(), Mock())
    transaction.clear()
    mock.assert_called_with(transaction.cursor)


@patch.object(core, 'print_tree')
def test_print_tree(mock):
    transaction = Transaction(Mock(), Mock())
    transaction.print_tree()
    mock.assert_called_with(transaction.cursor)


@patch.object(core, 'get_tree_size')
def test_get_tree_size(mock):
    transaction = Transaction(Mock(), Mock())
    transaction.get_tree_size()
    mock.assert_called_with(transaction.cursor)


@patch.object(core, 'get_root_node')
def test_get_root_node(mock):
    transaction = Transaction(Mock(), Mock())
    transaction.get_root_node()
    mock.assert_called_with(transaction.cursor)


@patch.object(core, 'insert_node')
def test_insert_root_node(mock):
    transaction = Transaction(Mock(), Mock())
    transaction.insert_root_node()
    mock.assert_called_with(transaction.cursor, None, None)


@patch.object(core, 'get_node')
def test_get_node(mock):
    transaction = Transaction(Mock(), Mock())
    transaction.get_node(1337)
    mock.assert_called_with(transaction.cursor, 1337)


@patch.object(core, 'get_nodes_by_property_dict')
def test_get_nodes_by_property_dict(mock):
    mock.return_value = [Mock(id=1), Mock(id=2)]
    transaction = Transaction(Mock(), Mock())
    query = {'key': 'value'}
    transaction.get_nodes_by_property_dict(query)
    mock.assert_called_with(transaction.cursor, query)


@patch.object(core, 'get_nodes_by_property_key')
def test_get_nodes_by_property_key(mock):
    mock.return_value = [Mock(id=1), Mock(id=2)]
    transaction = Transaction(Mock(), Mock())
    transaction.get_nodes_by_property_key('foobar')
    mock.assert_called_with(transaction.cursor, 'foobar')


@patch.object(core, 'get_nodes_by_property_value')
def test_get_nodes_by_property_value(mock):
    mock.return_value = [Mock(id=1), Mock(id=2)]
    transaction = Transaction(Mock(), Mock())
    transaction.get_nodes_by_property_value('key', 'value')
    mock.assert_called_with(transaction.cursor, 'key', 'value')
