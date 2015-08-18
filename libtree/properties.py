from libtree.node import Node
from libtree.query import get_ancestors, get_node
import json


def get_inherited_properties(per, node):
    """
    Get the entire inherited property dictionary.

    To calculate this, the trees path from root node till ``node`` will
    be traversed. For each level, the property dictionary will be merged
    into the previous one.

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
