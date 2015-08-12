from libtree.query import get_properties
import json


def update_property(per, node, key, value):
    properties = get_properties(per, node)
    properties[key] = value
    set_properties(per, node, properties)


def set_properties(per, node, new_properties):
    """ destructive """
    sql = """
        UPDATE
          nodes
        SET
          properties=%s
        WHERE
          id=%s;
    """
    per.execute(sql, (json.dumps(new_properties), int(node)))


def update_properties(per, node, new_properties):
    properties = get_properties(per, node)
    properties.update(new_properties)
    set_properties(per, node, properties)
