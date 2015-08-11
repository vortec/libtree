"""
Auto position basics
--------------------

``libtree`` has a feature called `auto position` which is turned on by
default and makes sure that whenever you insert, move or delete a node
its siblings stay correctly ordered.

Let's assume you have a node sequence like this::

    0 | 1
    A | B

If you now insert a new node without any further arguments, auto
position will insert it at the end of the sequence::

    0 | 1 | 2
    A | B | C

But if you insert the node at a certain position (1 in this example),
auto position will free the desired spot and shift the following
siblings to the right like this::

    0 | 1 | 2
    A | C | B

Likewise, if you want to delete the node at position 1, auto position
will left-shift all following nodes, so you end up with the same
sequence as at the beginning again.

This is default behaviour because most users expect a tree
implementation to behave like this.


Disable auto position
---------------------
If you're working on a dataset in which you know the final positions of
your nodes before feeding them into ``libtree``, you can disable auto
position altogether. This means lesser queries to the database and thus,
faster insert speeds. On the other hand this means that no constraint
checks are being made and you could end up with non-continuative
position sequences, multiple nodes at the same position or no position
at all. Don't worry - libtree supports those cases perfectly well - but
it might be confusing in the end.

To disable auto position you must pass ``auto_position=False`` to any
function that manipulates the tree (see :ref:`tree`).


Related: :func:`libtree.query.get_node_at_position`
"""

from libtree.query import get_node_at_position


def ensure_free_position(per, node, position):
    """
    Move siblings away to have a free slot at ``position`` in the
    children of ``node``.

    :param node:
    :type node: Node or int
    :param int position:
    """
    try:
        get_node_at_position(per, node, position)
        node_exists_at_position = True
    except ValueError:
        node_exists_at_position = False

    if node_exists_at_position:
        shift_positions(per, node, position, +1)


def find_highest_position(per, node):
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
    per.execute(sql, (id, ))
    result = per.fetchone()[0]

    if result is not None:
        return result
    else:
        return -1


def set_position(per, node, position, auto_position=True):
    """
    Set ``position`` for ``node``.

    :param node:
    :type node: Node or int
    :param int position:
    """
    # TODO: run auto position!
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
    per.execute(sql, (id, position))


def swap_node_positions(per, node1, node2):
    """
    Swap positions of ``node1`` and ``node2``.

    :param node1:
    :type node1: Node or int
    :param node2:
    :type node2: Node or int
    """
    set_position(per, node1, node2.position, auto_position=False)
    set_position(per, node2, node1.position, auto_position=False)
