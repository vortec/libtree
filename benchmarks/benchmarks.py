from benchmark import Benchmark
import libtree


def _get_node_by_title(per, title):
    return next(libtree.get_nodes_by_property_value(per, "title", title))


def change_parent_worst_case(per):
    node = _get_node_by_title(per, "0x0")
    new_parent = _get_node_by_title(per, "0x1")
    return lambda: libtree.change_parent(per, node, new_parent)


def change_parent_best_case(per):
    node = _get_node_by_title(per, "0x0x0x0x0x0x0x1")
    new_parent = _get_node_by_title(per, "0x0x0x0x0x0")
    return lambda: libtree.change_parent(per, node, new_parent)


def delete_node_best_case(per):
    node = _get_node_by_title(per, "0x0x0x0x0x0x0x0")
    return lambda: libtree.delete_node(per, node)


def delete_node_worst_case(per):
    node = _get_node_by_title(per, "0x0")
    return lambda: libtree.delete_node(per, node)


def iterate_get_ancestors(per):
    node = _get_node_by_title(per, "0x0x0x0x0x0x0x0")

    def method():
        nonlocal node
        ancestors = libtree.get_ancestors(per, node)
        for node in ancestors:
            pass

    return method


def create_benchmarks(per, config):

    test_node_id = config['test_node_id']

    bs = [
        Benchmark(
            lambda: libtree.get_tree_size(per),
            "get_tree_size"
        ),
        Benchmark(
            lambda: libtree.get_root_node(per),
            "get_root_node"
        ),
        Benchmark(
            lambda: libtree.get_node(per, test_node_id),
            "get_node"
        ),
        Benchmark(
            lambda: libtree.get_children(per, test_node_id),
            "get_children"
        ),
        Benchmark(
            lambda: libtree.get_children_count(per, test_node_id),
            "get_children_count"
        ),
        Benchmark(
            lambda: libtree.get_ancestors(per, test_node_id),
            "get_ancestors"
        ),
        Benchmark(
            lambda: libtree.get_descendants(per, test_node_id),
            "get_descendants"
        ),
        Benchmark(
            lambda: libtree.insert_node(per, test_node_id),
            "insert_node"
        ),
        Benchmark(
            delete_node_worst_case(per),
            "delete_node_worst_case"
        ),
        Benchmark(
            delete_node_best_case(per),
            "delete_node_best_case"
        ),
        Benchmark(
            change_parent_worst_case(per),
            "change_parent_worst_case"
        ),
        Benchmark(
            change_parent_best_case(per),
            "change_parent_best_case"
        ),
        Benchmark(
            iterate_get_ancestors(per),
            "iterate_get_ancestors"
        ),
    ]
    return bs
