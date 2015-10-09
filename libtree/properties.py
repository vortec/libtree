# Copyright (c) 2015 CaT Concepts and Training GmbH


from libtree.node import Node
from libtree.query import get_ancestors, get_node
import json


def get_nodes_by_property_dict(per, query):
    """
    Return an iterator that yields a ``Node`` object of every node which
    contains all key/value pairs of ``query`` in its property
    dictionary. Inherited keys are not considered.

    :param dict query: The dictionary to search for
    """
    sql = """
        SELECT
          *
        FROM
          nodes
        WHERE
          properties @> %s;
    """
    per.execute(sql, (json.dumps(query), ))
    for result in per:
        yield Node(**result)


def get_nodes_by_property_key(per, key):
    """
    Return an iterator that yields a ``Node`` object of every node which
    contains ``key`` in its property dictionary. Inherited keys are not
    considered.

    :param str key: The key to search for
    """
    sql = """
        SELECT
          *
        FROM
          nodes
        WHERE
          properties ? %s;
    """
    per.execute(sql, (key, ))
    for result in per:
        yield Node(**result)


def get_nodes_by_property_value(per, key, value):
    """
    Return an iterator that yields a ``Node`` object of every node which
    has ``key`` exactly set to ``value`` in its property dictionary.
    Inherited keys are not considered.

    :param str key: The key to search for
    :param object value: The exact value to sarch for
    """
    query = {key: value}
    for node in get_nodes_by_property_dict(per, query):
        yield node


def get_inherited_properties(per, node):
    """
    Get the entire inherited property dictionary.

    To calculate this, the trees path from root node till ``node`` will
    be traversed. For each level, the property dictionary will be merged
    into the previous one. This is a simple merge, only the first level
    of keys will be combined.

    :param node:
    :type node: Node or int
    :rtype: dict
    """
    ret = {}
    id = int(node)
    if type(node) == int:
        node = get_node(per, id)

    ancestors = list(get_ancestors(per, id))

    for ancestor in ancestors:
        ret.update(ancestor.properties)

    ret.update(node.properties)

    return ret


def get_inherited_property_value(per, node, key):
    """
    Get the inherited value for a single property key.

    :param node:
    :type node: Node or int
    :param key: str
    """
    return get_inherited_properties(per, node)[key]


def set_properties(per, node, new_properties):
    """
    Set the property dictionary to ``new_properties``.
    Return ``Node`` object with updated properties.

    :param node:
    :type node: Node or int
    :param new_properties: dict
    """
    if type(new_properties) != dict:
        raise TypeError('Only dictionaries are supported.')

    id = int(node)
    if type(node) == int:
        node = get_node(per, id)

    sql = """
        UPDATE
          nodes
        SET
          properties=%s
        WHERE
          id=%s;
    """
    per.execute(sql, (json.dumps(new_properties), int(node)))

    kwargs = node.to_dict()
    kwargs['properties'] = new_properties
    return Node(**kwargs)


def update_properties(per, node, new_properties):
    """
    Update existing property dictionary with another dictionary.
    Return ``Node`` object with updated properties.

    :param node:
    :type node: Node or int
    :param new_properties: dict
    """
    if type(new_properties) != dict:
        raise TypeError('Only dictionaries are supported.')

    id = int(node)
    if type(node) == int:
        node = get_node(per, id)

    properties = node.properties.copy()
    properties.update(new_properties)
    return set_properties(per, node, properties)


def set_property_value(per, node, key, value):
    """
    Set the value for a single property key.
    Return ``Node`` object with updated properties.

    :param node:
    :type node: Node or int
    :param key: str
    :param value: object
    """
    id = int(node)
    if type(node) == int:
        node = get_node(per, id)

    properties = node.properties.copy()
    properties[key] = value
    set_properties(per, node, properties)

    kwargs = node.to_dict()
    kwargs['properties'] = properties
    return Node(**kwargs)
