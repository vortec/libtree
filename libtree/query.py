from libtree.node import Node


def get_ancestors(per, node):
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
