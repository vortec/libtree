from libtree.node import Node


def print_tree(per, node=None, intend=0):
    if node is None:
        node = get_root_node(per)

    print('{}{}'.format(' '*intend, node.type))  # noqa

    for child in list(get_children(per, node)):
        print_tree(per, child, intend=intend+2)


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


def create_node(per, parent, type, position=0, description=''):
    """ non-atomic """
    parent_id = None
    if parent is not None:
        parent_id = int(parent)

    sql = """
        INSERT INTO
            nodes
            (parent, type, position, description)
        VALUES
            (%s, %s, %s, %s);
    """
    per.execute(sql, (parent_id, type, position, description))
    id = per.get_last_row_id()
    node = Node(id, parent_id, type, position)

    return node


def insert_ancestors(per, node, ancestors):
    id = int(node)
    data = []

    for ancestor in ancestors:
        data.append((id, int(ancestor)))

    sql = """
        INSERT INTO
            ancestor
            (node, ancestor)
        VALUES
            (%s, %s);
    """
    per.executemany(sql, data)


def delete_ancestors(per, node, ancestors):
    id = int(node)

    sql = """
        DELETE FROM
            ancestor
        WHERE
            node=%s
        AND
            ancestor=%s;
    """
    per.execute(sql, (id, ','.join(map(str, ancestors))))


def get_ancestor_ids(per, node):
    sql = """
        SELECT
            ancestor
        FROM
            ancestor
        WHERE
            node=%s;
    """
    per.execute(sql, (int(node), ))
    for result in per:
        yield int(result['ancestor'])


def get_ancestors(per, node):
    sql = """
        SELECT
            nodes.*
        FROM
            ancestor
        INNER JOIN
            nodes
        ON
            ancestor.ancestor=nodes.id
        WHERE
            ancestor.node=%s;
    """
    per.execute(sql, (int(node), ))
    for result in per:
        yield Node(**result)


def get_descendant_ids(per, node):
    sql = """
        SELECT
            node
        FROM
            ancestor
        WHERE
            ancestor=%s;
    """
    per.execute(sql, (int(node), ))
    # TODO: check if fetchmany() is fast and not uses more memory
    for result in per:
        yield int(result['node'])


def get_descendants(per, node):
    raise NotImplementedError("could be billions of objects")


def get_children(per, node):
    sql = """
        SELECT
            *
        FROM
            nodes
        WHERE
            parent=%s;
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
            parent=%s;
    """
    per.execute(sql, (int(node), ))
    for result in per:
        yield int(result['id'])


def delete_node(per, node):
    """ non-atomic """
    id = int(node)

    old_objects = set(get_descendant_ids(per, id))
    old_objects.add(id)
    old_object_ids = ','.join(map(str, old_objects))

    sql = """
        DELETE FROM
            ancestor
        WHERE
            node IN ({})
        OR
            ancestor IN ({});
    """.format(old_object_ids, old_object_ids)
    per.execute(sql)

    sql = """
        DELETE FROM
            nodes
        WHERE
            id IN ({});
    """.format(old_object_ids)
    per.execute(sql)


def move_node(per, node, new_parent):
    """ non-atomic """
    id = int(node)
    parent_id = int(new_parent)

    # Update ancestors by comparing the ancestor list of both the node
    # and the new parent node. Delete all entries that are not in the
    # parents list, add entries that are not in the nodes list.
    # Also add the new parents ID and we're set.
    # Hint for undestanding: Both (the nodes and the parent nodes)
    # ancestor lists contain the root node, and there might be others,
    # therefore we dont need to remove and re-add them to the database.

    sql = """
        DELETE FROM
            ancestor
        WHERE
            ancestor
        IN
            (
                SELECT
                    ancestor
                FROM
                    ancestor
                WHERE
                    node=%s
            )
        AND
            node
        IN
            (
                SELECT
                    node
                FROM
                    ancestor
                WHERE
                    ancestor=%s
                OR
                    node=%s
            );
    """
    per.execute(sql, (id, id, id))

    sql = """
        INSERT INTO
            ancestor
        SELECT
            sub.node, par.ancestor
        FROM
            ancestor AS sub
        JOIN
            (
                SELECT
                    ancestor
                FROM
                    ancestor
                WHERE
                    node= %s
                UNION SELECT %s
            ) AS par
        ON TRUE
        WHERE
            sub.ancestor = %s
        OR
            sub.node = %s;
    """
    per.execute(sql, (parent_id, parent_id, id, id))

    parent_ancestors = set(get_ancestor_ids(per, parent_id))
    parent_ancestors.add(parent_id)
    insert_ancestors(per, node, parent_ancestors)

    # change parent in nodes
    sql = """
        UPDATE
            nodes
        SET
            parent=%s
        WHERE
            id=%s;
    """
    per.execute(sql, (int(new_parent), int(node)))
