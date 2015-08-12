import json


def update_property(per, node, key, value):
    pass
    # props[key] = value


def set_properties(per, node, properties):
    """ destructive """
    sql = """
        UPDATE
          nodes
        SET
          properties=%s
        WHERE
          id=%s;
    """
    per.execute(sql, (json.dumps(properties), int(node)))


def update_properties(per, node, attrs):
    pass
    # props.update(attrs)
