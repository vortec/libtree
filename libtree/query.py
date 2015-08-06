from libtree.node import Node
from libtree.tree import vectorize_nodes


def get_ancestors(per, node, sort=True):
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
