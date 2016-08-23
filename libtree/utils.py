# Copyright (c) 2016 Fabian Kochem


import collections
from copy import deepcopy


def recursive_dict_merge(left, right, first_run=True):
    """
    Merge ``right`` into ``left`` and return a new dictionary.
    """
    if first_run is True:
        left = deepcopy(left)

    for key in right:
        if key in left:
            if isinstance(left[key], dict) and isinstance(right[key], dict):
                recursive_dict_merge(left[key], right[key], False)
            else:
                left[key] = right[key]
        else:
            left[key] = right[key]
    return left


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
