# Copyright (c) 2015 Fabian Kochem


from libtree.core.node_data import NodeData
from libtree.utils import vectorize_nodes


def get_tree_size(cur):
    """
    Return the total amount of tree nodes.
    """
    sql = """
      SELECT
        COUNT(*)
      FROM
        nodes;
    """
    cur.execute(sql)
    result = cur.fetchone()
    return result['count']


def get_root_node(cur):
    """
    Return root node. Raise ``ValueError`` if root node doesn't exist.
    """
    sql = """
        SELECT
          *
        FROM
          nodes
        WHERE
          parent IS NULL;
    """
    cur.execute(sql)
    result = cur.fetchone()

    if result is None:
        raise ValueError('No root node.')
    else:
        return NodeData(**result)


def get_node(cur, id):
    """
    Return ``NodeData`` object for given ``id``. Raises ``ValueError``
    if ID doesn't exist.

    :param int id: Database ID
    """
    if type(id) != int:
        raise TypeError('Need numerical id.')

    sql = """
        SELECT
          *
        FROM
          nodes
        WHERE
          id = %s;
    """
    cur.execute(sql, (id, ))
    result = cur.fetchone()

    if result is None:
        raise ValueError('Node does not exist.')
    else:
        return NodeData(**result)


def get_node_at_position(cur, node, position):
    """
    Return node at ``position`` in the children of ``node``.

    :param node:
    :type node: Node or int
    :param int position:
    """
    sql = """
      SELECT
        *
      FROM
        nodes
      WHERE
        parent=%s
      AND
        position=%s
    """

    cur.execute(sql, (int(node), position))
    result = cur.fetchone()

    if result is None:
        raise ValueError('Node does not exist.')
    else:
        return NodeData(**result)


def get_children(cur, node):
    """
    Return an iterator that yields a ``NodeData`` object of every
    immediate child.

    :param node:
    :type node: Node or int
    """
    sql = """
        SELECT
          *
        FROM
          nodes
        WHERE
          parent=%s
        ORDER BY
          position;
    """
    cur.execute(sql, (int(node), ))
    for result in cur:
        yield NodeData(**result)


def get_child_ids(cur, node):
    """
    Return an iterator that yields the ID of every immediate child.

    :param node:
    :type node: Node or int
    """
    sql = """
        SELECT
          id
        FROM
          nodes
        WHERE
          parent=%s
        ORDER BY
          position;
    """
    cur.execute(sql, (int(node), ))
    for result in cur:
        yield int(result['id'])


def get_children_count(cur, node):
    """
    Get amount of immediate children.

    :param node: Node
    :type node: Node or int
    """
    sql = """
      SELECT
        COUNT(*)
      FROM
        nodes
      WHERE
        parent=%s;
    """
    cur.execute(sql, (int(node), ))
    result = cur.fetchone()
    return result['count']


def get_ancestors(cur, node, sort=True):
    """
    Return an iterator that yields a ``NodeData`` object of every
    element while traversing from ``node`` to the root node.

    :param node:
    :type node: Node or int
    :param bool sort: Start with closest node and end with root node.
                      (default: True)
    """
    # TODO: benchmark if vectorize_nodes() or WITH RECURSIVE is faster
    sql = """
        SELECT
          nodes.*
        FROM
          ancestors
        INNER JOIN
          nodes
        ON
          ancestors.ancestor=nodes.id
        WHERE
          ancestors.node=%s;
    """
    cur.execute(sql, (int(node), ))

    if sort:
        make_node = lambda r: NodeData(**r)
        for node in vectorize_nodes(map(make_node, cur)):
            yield node
    else:
        for result in cur:
            yield NodeData(**result)


def get_ancestor_ids(cur, node):
    """
    Return an iterator that yields the ID of every element while
    traversing from ``node`` to the root node.

    :param node:
    :type node: Node or int
    """
    # TODO: add sort parameter
    sql = """
        SELECT
          ancestor
        FROM
          ancestors
        WHERE
          node=%s;
    """
    cur.execute(sql, (int(node), ))
    for result in cur:
        yield int(result['ancestor'])


def get_descendants(cur, node):
    """
    Return an iterator that yields the ID of every element while
    traversing from ``node`` to the root node.

    :param node:
    :type node: Node or int
    """
    sql = """
        SELECT
          nodes.*
        FROM
          ancestors
        INNER JOIN
          nodes
        ON
          ancestors.node=nodes.id
        WHERE
          ancestors.ancestor=%s;
    """
    cur.execute(sql, (int(node), ))
    for result in cur:
        yield NodeData(**result)


def get_descendant_ids(cur, node):
    """
    Return an iterator that yields a ``NodeData`` object of each element
    in the nodes subtree. Be careful when converting this iterator to an
    iterable (like list or set) because it could contain billions of
    objects.

    :param node:
    :type node: Node or int
    """
    sql = """
        SELECT
          node
        FROM
          ancestors
        WHERE
          ancestor=%s;
    """
    cur.execute(sql, (int(node), ))
    for result in cur:
        yield int(result['node'])
