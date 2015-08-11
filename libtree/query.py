from libtree.node import Node
from libtree.utils import vectorize_nodes


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
    raise NotImplementedError('This could create billions of Python objects.')


def get_descendant_ids(per, node):
    """
    Return an iterator that yields the ID of each element in the nodes
    subtree.

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
