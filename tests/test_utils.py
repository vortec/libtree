# Copyright (c) 2015 Fabian Kochem


from libtree.utils import vectorize_nodes


def test_vectorize_nodes(cur, root, node2, node2_1, node2_1_1):
    nodes = [node2_1_1, node2, root, node2_1]
    expected = [root, node2, node2_1, node2_1_1]
    assert vectorize_nodes(nodes) == expected
    assert vectorize_nodes(*nodes) == expected
