.. _user_guide:

User Guide
==========

Database Connection
-------------------
To start working with `libtree`, make sure PostgreSQL 9.4 is running. If
you don't have a database yet, create one now::

    $ createdb libtree

Next, start a Python interpreter, import libtree and create a
:ref:`tree` object. To make it connect to PostgreSQL, you must create a
`psycopg2` connection. After that, you can install libtree::

    $ python
    Python 3.5.0 (default, Oct 12 2015, 13:41:59)
    >>> from libtree import Tree
    >>> import psycopg2
    >>> connection = psycopg2.connect("dbname=test_tree user=vortec")
    >>> transaction = Tree(connection).make_transaction(write=True)
    >>> transaction.install()
    >>> transaction.commit()

The ``transaction`` objects represent a database transaction and must be
passed to every function whenever you want to query or modify the tree.
Running ``install()`` creates the SQL tables and must only be executed
if you haven't done so before. Executing ``commit()`` writes the changes
you made to the database. If you want to discard the changes, run
``transaction.rollback()``.

For more convenience, you can use the auto-committing context manager::

    >>> tree = Tree(connection)
    >>> with tree(write=True) as transaction:
    ...     transaction.install()

When the context manager leaves it will commit the transaction to the
database. If an exception occurs, it will rollback automatically.

If you want to modify the database, you must pass ``write=True`` to the
context manager. The default behaviour is read-only.

Modify the tree
---------------
Now, you can create some nodes::

    >>> html = transaction.insert_root_node()
    >>> title = html.insert_child({'title': 'title', 'content': 'libtree'})
    >>> head = html.insert_child({'title': 'head'})
    >>> body = html.insert_child({'title': 'body'})
    >>> h2 = body.insert_child({'title': 'h2', 'content': 'to libtree'})
    >>> transaction.commit()

This should render as a nice, DOM-like tree::

    >>> transaction.print_tree()
    <NodeData id=..>
      <NodeData id=.., title='title'>
      <NodeData id=.., title='head'>
      <NodeData id=.., title='body'>
        <NodeData id=.., title='h2'>

But do you spot the mistake? In HTML, a ``<title>`` tag goes beneath the
``<head>`` tag, so let's move it::

    >>> title.move(head)
    >>> transaction.print_tree()
    <NodeData id=..>
      <NodeData id=.., title='head'>
        <NodeData id=.., title='title'>
      <NodeData id=.., title='body'>
        <NodeData id=.., title='h2'>

And you also forgot the ``<h1>`` node, let's insert it before ``<h2>``::

    >>> body.insert_child({'title': 'h1', 'content': 'Welcome'}, position=0)
    <Node id=.., title='h1'>
    >>> transaction.print_tree()
    <NodeData id=..>
      <NodeData id=.., title='head'>
        <NodeData id=.., title='title'>
      <NodeData id=.., title='body'>
        <NodeData id=.., title='h1'>
        <NodeData id=.., title='h2'>

Since you know the ID, you can easily delete nodes without a ``Node``
object::

    >>> h2.delete()
    >>> transaction.print_tree()
    <NodeData id=..>
      <NodeData id=.., title='head'>
        <NodeData id=.., title='title'>
      <NodeData id=.., title='body'>
        <NodeData id=.., title='h1'>
    >>> transaction.commit()

Query the tree
--------------
If you want to get a ``Node`` object, you can easily get one by querying
for the ID::

    >>> title = transaction.get_node('1afce8e3-975a-4daa-93e7-88d879c05224')
    >>> title.properties
    {'content': 'libtree', 'title': 'title'}

You can get the immediate children of a node::

    >>> html.children
    [<Node id=.., title='head'>, <Node id=..

You can get all nodes that have a certain property key set:

    >>> transaction.get_nodes_by_property_key('content')
    {<Node id=.., title='h1'>, <Node id=.., title='title'>}

Or ask for nodes that have a certain property value set::

    >>> transaction.get_nodes_by_property_value('content', 'Welcome')
    {<Node id=.., title='h1'>}

If you have a node, you can output the path from the root node to it
too::

    >>> h1.ancestors
    [<Node id=..>, <Node id=.., title='body'>]
