def vectorize_nodes(nodes):
    ret = []
    parents = {node.parent: node for node in nodes}

    last_parent = None
    for _ in range(len(parents)):
        node = parents[last_parent]
        ret.append(node)
        last_parent = node.id

    return ret
