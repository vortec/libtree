import builtins
import json
from libtree.node import Node
from libtree.positioning import (ensure_free_position,
                                 find_highest_position, set_position,
                                 shift_positions)
from libtree.query import get_descendant_ids


def print_tree(per, node=None, intend=0):
    if node is None:
        node = get_root_node(per)

    print('{}{}'.format(' '*intend, node.type))  # noqa

    for child in list(get_children(per, node)):
        print_tree(per, child, intend=intend+2)


def get_tree_size(per):
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


def insert_node(per, parent, type, position=None, attributes=None,
                properties=None, auto_position=True):
    parent_id = None
    if parent is not None:
        parent_id = int(parent)

    if attributes is None:
        attributes = {}

    if properties is None:
        properties = {}

    if auto_position:
        if builtins.type(position) == int and position >= 0:
            ensure_free_position(per, parent, position)
        else:
            position = find_highest_position(per, parent) + 1

    sql = """
        INSERT INTO
          nodes
          (parent, type, position, attributes, properties)
        VALUES
          (%s, %s, %s, %s, %s);
    """
    per.execute(sql, (parent_id, type, position, json.dumps(attributes),
                      json.dumps(properties)))
    id = per.get_last_row_id()
    node = Node(id, parent_id, type, position, attributes, properties)

    return node

# IDEA: def mass_insert()
# CREATE TEMP SEQUENCE


def delete_node(per, node, auto_position=True):
    id = int(node)

    # Get Node object if integer (ID) was passed
    if auto_position and type(node) != Node:
        node = get_node(per, id)

    sql = """
        DELETE FROM
          nodes
        WHERE
          id=%s;
    """
    per.execute(sql, (id, ))

    if auto_position:
        shift_positions(per, node.parent, node.position, -1)


def get_children(per, node):
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


def insert_ancestors(per, node, ancestors):
    id = int(node)
    data = []

    for ancestor in ancestors:
        data.append((id, int(ancestor)))

    sql = """
        INSERT INTO
          ancestors
          (node, ancestor)
        VALUES
          (%s, %s);
    """
    per.executemany(sql, data)


def delete_ancestors(per, node, ancestors):
    id = int(node)

    sql = """
        DELETE FROM
          ancestors
        WHERE
          node=%s
        AND
          ancestor IN ({});
    """
    sql = sql.format(','.join(map(str, map(int, ancestors))))
    per.execute(sql, (id, ))


def change_parent(per, node, new_parent, position=None, auto_position=True):
    if int(new_parent) in get_descendant_ids(per, node):
        raise ValueError('Cannot move node into its own subtree.')

    if auto_position:
        if type(position) == int and position >= 0:
            ensure_free_position(per, new_parent, position)
        else:
            position = find_highest_position(per, new_parent) + 1
        set_position(per, node, position)

    # TODO: dont move into its own subtree
    sql = """
        UPDATE
          nodes
        SET
          parent=%s
        WHERE
          id=%s;
    """
    per.execute(sql, (int(new_parent), int(node)))
