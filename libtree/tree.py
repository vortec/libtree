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


def create_node(per, parent, type, position=None, description=''):
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
    id = int(node)
    sql = """
        DELETE FROM
            nodes
        WHERE
            id=%s;
    """
    per.execute(sql, (id, ))


def move_node(per, node, new_parent):
    sql = """
        UPDATE
            nodes
        SET
            parent=%s
        WHERE
            id=%s;
    """
    per.execute(sql, (int(new_parent), int(node)))
