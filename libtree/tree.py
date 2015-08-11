"""

"""

import json
from libtree.node import Node
from libtree.positioning import (ensure_free_position,
                                 find_highest_position, set_position,
                                 shift_positions)
from libtree.query import get_descendant_ids

try:
    import builtins
except ImportError:
    import __builtin__ as builtins


def print_tree(per, start_node=None, indent=2, _level=0):
    """
    Print tree to stdout.

    :param start_node: Starting point for tree output.
                       If ``None``, start at root node.
    :type start_node: int, Node or None
    :param int indent: Amount of whitespaces per level (default: 2)
    """
    if start_node is None:
        start_node = get_root_node(per)

    print('{}{}'.format(' '*indent, start_node))  # noqa

    for child in list(get_children(per, start_node)):
        print_tree(per, child, _level=_level+indent)


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
    Return root node. Raises ``ValueError`` if root node doesn't exist.
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


def insert_node(per, parent, type, position=None, attributes=None,
                properties=None, auto_position=True):
    """
    Create a ``Node`` object, insert it into the tree and then return
    it.

    :param parent: Reference to its parent node. If `None`, this will
                   be the root node.
    :type parent: Node or int
    :param str type: Arbitrary string, can be used for filtering
    :param int position: Position in between siblings. If 0, the node
                         will be inserted at the beginning of the
                         parents children. If -1, the node will be
                         inserted the the end of the parents children.
                         If `auto_position` is disabled, this is just a
                         value.
    :param dict attributes: Non-inheritable key/value pairs
                            (see :ref:`attributes`)
    :param dict properties: Inheritable key/value pairs
                             (see :ref:`properties`)
    :param bool auto_position: See :ref:`positioning`
    """
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
    """
    Delete node and its subtree.

    :param node:
    :type node: Node or int
    :param bool auto_position: See :ref:`positioning`
    """
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


def change_parent(per, node, new_parent, position=None, auto_position=True):
    """
    Move node and its subtree from its current to another parent node.

    :param node:
    :type node: Node or int
    :param new_parent: Reference to the new parent node
    :type new_parent: Node or int
    :param int position: Position in between siblings. If 0, the node
                         will be inserted at the beginning of the
                         parents children. If -1, the node will be
                         inserted the the end of the parents children.
                         If `auto_position` is disabled, this is just a
                         value.
    :param bool auto_position: See :ref:`positioning`.
    """
    if int(new_parent) in get_descendant_ids(per, node):
        raise ValueError('Cannot move node into its own subtree.')

    if auto_position:
        if type(position) == int and position >= 0:
            ensure_free_position(per, new_parent, position)
        else:
            position = find_highest_position(per, new_parent) + 1
        set_position(per, node, position)

    sql = """
        UPDATE
          nodes
        SET
          parent=%s
        WHERE
          id=%s;
    """
    per.execute(sql, (int(new_parent), int(node)))
