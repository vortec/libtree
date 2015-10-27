# Copyright (c) 2015 Fabian Kochem


"""
**Auto position**

``libtree`` has a feature called `auto position` which is turned on by
default and makes sure that whenever you insert, move or delete a node
its siblings stay correctly ordered.

Let's assume you have a node sequence like this::

    position | 0 | 1
    node     | A | B

If you now insert a new node without any further arguments, auto
position will insert it at the end of the sequence::

    position | 0 | 1 | 2
    node     | A | B | C

But if you insert the node at a certain position (1 in this example),
auto position will free the desired spot and shift the following
siblings to the right like this::

    position | 0 | 1 | 2
    node     | A | C | B

Likewise, if you want to delete the node at position 1, auto position
will left-shift all following nodes, so you end up with the same
sequence as at the beginning again.

This is default behaviour because most users expect a tree
implementation to behave like this.


**Disable auto position**

If you're working on a dataset in which you know the final positions of
your nodes before feeding them into ``libtree``, you can disable auto
position altogether. This means lesser queries to the database and thus,
faster insert speeds. On the other hand this means that no constraint
checks are being made and you could end up with non-continuative
position sequences, multiple nodes at the same position or no position
at all. Don't worry - libtree supports those cases perfectly well - but
it might be confusing in the end.

To disable auto position you must pass ``auto_position=False`` to any
function that manipulates the tree (see :ref:`core-tree`).


**API**

Related: :func:`libtree.query.get_node_at_position`
"""

from libtree.core.query import get_node, get_node_at_position


def ensure_free_position(cur, node, position):
    """
    Move siblings away to have a free slot at ``position`` in the
    children of ``node``.

    :param node:
    :type node: Node or int
    :param int position:
    """
    try:
        get_node_at_position(cur, node, position)
        node_exists_at_position = True
    except ValueError:
        node_exists_at_position = False

    if node_exists_at_position:
        shift_positions(cur, node, position, +1)


def find_highest_position(cur, node):
    """
    Return highest, not occupied position in the children of ``node``.

    :param node:
    :type node: Node or int
    """
    if node is not None:
        id = int(node)
    else:
        id = None

    sql = """
      SELECT
        MAX(position)
      FROM
        nodes
      WHERE
        parent=%s;
    """
    cur.execute(sql, (id, ))
    result = cur.fetchone()['max']

    if result is not None:
        return result
    else:
        return -1


def set_position(cur, node, position, auto_position=True):
    """
    Set ``position`` for ``node``.

    :param node:
    :type node: Node or int
    :param int position: Position in between siblings. If 0, the node
                         will be inserted at the beginning of the
                         parents children. If -1, the node will be
                         inserted the the end of the parents children.
                         If `auto_position` is disabled, this is just a
                         value.
    :param bool auto_position: See :ref:`core-positioning`
    """
    if auto_position:
        id = int(node)
        if type(node) == int:
            node = get_node(cur, id)

        if type(position) == int and position >= 0:
            ensure_free_position(cur, node.parent, position)
        else:
            position = find_highest_position(cur, node.parent) + 1
    else:
        id = int(node)

    sql = """
        UPDATE
          nodes
        SET
          position=%s
        WHERE
          id=%s;
    """
    cur.execute(sql, (position, int(node)))
    return position


def shift_positions(cur, node, position, offset):
    """
    Shift all children of ``node`` at ``position`` by ``offset``.

    :param node:
    :type node: Node or int
    :param int position:
    :param int offset: Positive value for right shift, negative value
                       for left shift
    """
    if node is not None:
        id = int(node)
    else:
        id = None

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
    cur.execute(sql, (id, position))


def swap_node_positions(cur, node1, node2):
    """
    Swap positions of ``node1`` and ``node2``.

    :param node1:
    :type node1: Node or int
    :param node2:
    :type node2: Node or int
    """
    set_position(cur, node1, node2.position, auto_position=False)
    set_position(cur, node2, node1.position, auto_position=False)
