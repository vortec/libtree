# Copyright (c) 2015 Fabian Kochem


from libtree.utils import vectorize_nodes


def test_vectorize_nodes(cur, root, nd2, nd2_1, nd2_1_1):
    nodes = [nd2_1_1, nd2, root, nd2_1]
    expected = [root, nd2, nd2_1, nd2_1_1]
    assert vectorize_nodes(nodes) == expected
    assert vectorize_nodes(*nodes) == expected
