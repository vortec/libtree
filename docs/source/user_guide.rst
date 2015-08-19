.. _user_guide:

User Guide
==========

Database Connection
-------------------
To start working with `libtree`, make sure PostgreSQL 9.4 is running. If
you don't have a database yet, create one now::

    $ createdb libtree

Next, start a Python interpreter, import libtree and create a
:ref:`api-persistance`. To make it connect to PostgreSQL, you must
supply a `libpq connection string
<http://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-CONNSTRING>`_. After that, you can install libtree::

    $ python
    Python 3.4.2 (default, Nov 12 2014, 10:43:21)
    >>> from libtree import *
    >>> per = PostgreSQLPersistance("dbname=libtree user=vortec")
    >>> per.install()
    >>> per.commit()

The ``per`` objects holds your connection to PostgreSQL and must be
passed to every function when you want to query or modify the tree.
Running ``install()`` creates the SQL tables and must only be executed
if you haven't done so before. Executing ``commit()`` writes the changes
you made to the database. If you want to discard the changes, run
``per.rollback()``.

Modify the tree
---------------
Now, you can create some nodes::

    >>> html = insert_node(per, None, {'title': 'html'})
    >>> title = insert_node(per, html, {'title': 'title', 'content': 'libtree'})
    >>> head = insert_node(per, html, {'title': 'head'})
    >>> body = insert_node(per, html, {'title': 'body'})
    >>> insert_node(per, body, {'title': 'h2', 'content': 'to libtree'})
    >>> per.commit()

This should render as a nice, DOM-like tree::

    >>> print_tree(per)
    <Node id=1, title='html'>
      <Node id=2, title='title'>
      <Node id=3, title='head'>
      <Node id=4, title='body'>
        <Node id=5, title='h2'>

But do you spot the mistake? In HTML, a ``<title>`` tag goes beneath the
``<head>`` tag, so let's move it::

    >>> change_parent(per, title, head)
    <Node id=2, title='title'>
    >>> print_tree(per)
    <Node id=1, title='html'>
      <Node id=3, title='head'>
        <Node id=2, title='title'>
      <Node id=4, title='body'>
        <Node id=5, title='h2'>

And you also forgot the ``<h1>`` node, let's insert it before ``<h2>``::

    >>> insert_node(per, body, {'title': 'h1', 'content': 'Welcome'}, position=0)
    <Node id=6, title='h1'>
    >>> print_tree(per)
    <Node id=1, title='html'>
      <Node id=3, title='head'>
        <Node id=2, title='title'>
      <Node id=4, title='body'>
        <Node id=6, title='h1'>
        <Node id=5, title='h2'>

Since you know the ID, you can easily delete nodes without a ``Node``
object::

    >>> delete_node(per, 5)
    >>> print_tree(per)
    <Node id=1, title='html'>
      <Node id=3, title='head'>
        <Node id=2, title='title'>
      <Node id=4, title='body'>
        <Node id=6, title='h1'>
    >>> per.commit()

Query the tree
--------------
If you want to get a ``Node`` object, you can easily get one by querying
for the ID::

    >>> get_node(per, 2)
    <Node id=2, title='title'>
    >>> get_node(per, 2).properties
    {'content': 'libtree', 'title': 'title'}

You can get the immediate children of a node::

    >>> list(get_children(per, html))
    [<Node id=3, title='head'>, <Node id=4, title='body'>]

You can get all nodes that have a certain property key set:

    >>> list(get_nodes_by_property_key(per, 'content'))
    [<Node id=2, title='title'>, <Node id=6, title='h1'>]

Or ask for nodes that have a certain property value set::

    >>> list(get_nodes_by_property_value(per, 'content', 'Welcome'))
    [<Node id=6, title='h1'>]

If you have a node, you can output the path from the root node to it
too::

    >>> list(get_ancestors(per, 6))
    [<Node id=1, title='html'>, <Node id=4, title='body'>]

