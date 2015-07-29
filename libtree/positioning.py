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


def swap_node_positions(per, node1, node2):
    set_position(per, node1, node2.position, auto_position=False)
    set_position(per, node2, node1.position, auto_position=False)
