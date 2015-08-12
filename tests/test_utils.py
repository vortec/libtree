from libtree.query import get_ancestors
from libtree.utils import merge_properties, vectorize_nodes


def test_vectorize_nodes(per, root, node2, node2_1, node2_1_1):
    nodes = [node2_1_1, node2, root, node2_1]
    expected = [root, node2, node2_1, node2_1_1]
    assert vectorize_nodes(nodes) == expected
    assert vectorize_nodes(*nodes) == expected


def test_merge_properties_no_inheritance(root):
    expected = {
        'title': 'Root',
        'type': 'root',
        'boolean': False,
        'integer': 1
    }
    assert merge_properties(root) == expected


def test_merge_properties_simple_inheritance(per, node2):
    expected = {
        'title': 'Node 2',
        'type': 'node2',
        'boolean': True,
        'foo': 'bar',
        'integer': 1
    }
    assert merge_properties(node2, *get_ancestors(per, node2)) == expected


def test_merge_properties_multiple_inheritance(per, node2_1_1):
    expected = {
        'title': 'Node 2-1-1',
        'type': 'node2_1_1',
        'boolean': False,
        'integer': 1,
        'foo': 'bar'
    }
    ancestors = get_ancestors(per, node2_1_1)
    assert merge_properties(node2_1_1, *ancestors) == expected
