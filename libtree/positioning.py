from libtree.node import Node


def ensure_free_position(per, node, position):
    try:
        get_node_at_position(per, node, position)
        node_exists_at_position = True
    except:
        node_exists_at_position = False

    if node_exists_at_position:
        shift_positions(per, node, position, +1)


def find_highest_position(per, node):
    sql = """
      SELECT
        MAX(position)
      FROM
        nodes
      WHERE
        parent=%s;
    """
    per.execute(sql, (int(node), ))
    result = per.fetchone()[0]

    if result is not None:
        return result
    else:
        return -1


def get_node_at_position(per, node, position):
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


def set_position(per, node, position, auto_position=True):
    sql = """
        UPDATE
          nodes
        SET
          position=%s
        WHERE
          id=%s;
    """
    per.execute(sql, (position, int(node)))


def shift_positions(per, node, position, offset):
    sql = """
        UPDATE
          nodes
        SET
          position=position{}
        WHERE
          parent=%s
        AND
          position >= %s;
    """
    delta = ''
    if offset > 0:
        delta = '+{}'.format(offset)
    elif offset < 0:
        delta = '{}'.format(offset)

    sql = sql.format(delta)
    per.execute(sql, (int(node), position))


def swap_node_positions(per, node1, node2):
    set_position(per, node1, node2.position, auto_position=False)
    set_position(per, node2, node1.position, auto_position=False)
