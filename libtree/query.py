# Copyright (c) 2015 CaT Concepts and Training GmbH


from libtree.node import Node
from libtree.utils import vectorize_nodes


def get_tree_size(per):
    """
    Return the total amount of tree nodes.
    """
    sql = """
      SELECT
        COUNT(*)
      FROM
        nodes;
    """
    per.execute(sql)
    result = per.fetchone()
    return result[0]


def get_root_node(per):
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
    per.execute(sql)
    result = per.fetchone()

    if result is None:
        raise ValueError('No root node.')
    else:
        return Node(**result)


def get_node(per, id):
    """
    Return ``Node`` object for given ``id``. Raises ``ValueError`` if
    ID doesn't exist.

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
    per.execute(sql, (id, ))
    result = per.fetchone()

    if result is None:
        raise ValueError('Node does not exist.')
    else:
        return Node(**result)


def get_node_at_position(per, node, position):
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

    per.execute(sql, (int(node), position))
    result = per.fetchone()

    if result is None:
        raise ValueError('Node does not exist.')
    else:
        return Node(**result)


def get_children(per, node):
    """
    Return an iterator that yields a ``Node`` object of every immediate
    child.

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
    per.execute(sql, (int(node), ))
    for result in per:
        yield Node(**result)


def get_child_ids(per, node):
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
    per.execute(sql, (int(node), ))
    for result in per:
        yield int(result['id'])


def get_children_count(per, node):
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
    per.execute(sql, (int(node), ))
    result = per.fetchone()
    return result[0]


def get_ancestors(per, node, sort=True):
    """
    Return an iterator that yields a ``Node`` object of every element
    while traversing from ``node`` to the root node.

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
    per.execute(sql, (int(node), ))

    if sort:
        make_node = lambda r: Node(**r)
        for node in vectorize_nodes(map(make_node, per)):
            yield node
    else:
        for result in per:
            yield Node(**result)


def get_ancestor_ids(per, node):
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
    per.execute(sql, (int(node), ))
    for result in per:
        yield int(result['ancestor'])


def get_descendants(per, node):
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
    per.execute(sql, (int(node), ))
    for result in per:
        yield Node(**result)


def get_descendant_ids(per, node):
    """
    Return an iterator that yields a ``Node`` object of each element in
    the nodes subtree. Be careful when converting this iterator to an
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
    per.execute(sql, (int(node), ))
    for result in per:
        yield int(result['node'])
