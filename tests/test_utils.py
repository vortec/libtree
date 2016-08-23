# Copyright (c) 2016 Fabian Kochem


from libtree.utils import recursive_dict_merge, vectorize_nodes


def test_recursive_dict_merge():
    left = {
        1: {'a': 'A'},
        2: {'b': 'B'},
        3: {'c': {'c': 'C'}}
    }
    right = {
        2: {'b': 'b', 'c': 'C'},
        3: {'c': {'c': 'c'}, 'd': 'D'}
    }
    expected = {
        1: {'a': 'A'},
        2: {'b': 'b', 'c': 'C'},
        3: {'c': {'c': 'c'}, 'd': 'D'}
    }

    assert recursive_dict_merge(left, right) == expected


def test_vectorize_nodes(cur, root, nd2, nd2_1, nd2_1_1):
    nodes = [nd2_1_1, nd2, root, nd2_1]
    expected = [root, nd2, nd2_1, nd2_1_1]
    assert vectorize_nodes(nodes) == expected
    assert vectorize_nodes(*nodes) == expected
