import json
from libtree.node import Node
from libtree.positioning import (ensure_free_position,
                                 find_highest_position, set_position,
                                 shift_positions)
from libtree.query import (get_children, get_descendant_ids, get_node,
                           get_root_node)


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


def insert_node(per, parent, position=None, properties=None,
                auto_position=True):
    """
    Create a ``Node`` object, insert it into the tree and then return
    it.

    :param parent: Reference to its parent node. If `None`, this will
                   be the root node.
    :type parent: Node or int
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

    if properties is None:
        properties = {}

    if auto_position:
        if type(position) == int and position >= 0:
            ensure_free_position(per, parent, position)
        else:
            position = find_highest_position(per, parent) + 1

    sql = """
        INSERT INTO
          nodes
          (parent, position, properties)
        VALUES
          (%s, %s, %s);
    """
    per.execute(sql, (parent_id, position, json.dumps(properties)))
    id = per.get_last_row_id()
    node = Node(id, parent_id, position, properties)

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


def change_parent(per, node, new_parent, position=None, auto_position=True):
    """
    Move node and its subtree from its current to another parent node.
    Return updated ``Node`` object with new parent set.

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
    new_id = int(new_parent)
    if new_id in get_descendant_ids(per, node):
        raise ValueError('Cannot move node into its own subtree.')

    if auto_position:
        if type(position) == int and position >= 0:
            ensure_free_position(per, new_id, position)
        else:
            position = find_highest_position(per, new_id) + 1
        set_position(per, node, position)

    sql = """
        UPDATE
          nodes
        SET
          parent=%s
        WHERE
          id=%s;
    """
    per.execute(sql, (new_id, int(node)))

    kwargs = node.to_dict()
    kwargs['parent'] = new_id
    return Node(**kwargs)
