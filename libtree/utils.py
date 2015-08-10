import collections


def merge_properties(*nodes):
    if len(nodes) == 1 and isinstance(nodes[0], collections.Iterable):
        nodes = nodes[0]

    ret = {}
    # Iterate over reversed list because get_ancestors() starts bottom-first
    for node in reversed(nodes):
        ret.update(node.properties)

    return ret


def vectorize_nodes(*nodes):
    if len(nodes) == 1 and isinstance(nodes[0], collections.Iterable):
        nodes = nodes[0]

    ret = []
    parents = {node.parent: node for node in nodes}

    last_parent = None
    for _ in range(len(parents)):
        node = parents[last_parent]
        ret.append(node)
        last_parent = node.id

    return ret
