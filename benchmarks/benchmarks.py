from benchmark import Benchmark
import libtree


def _get_node_by_title(transaction, title):
    nodes = transaction.get_nodes_by_property_value("title", title)
    return nodes.pop() if nodes else None


def change_parent_worst_case(transaction):
    node = _get_node_by_title(transaction, "0x0")
    new_parent = _get_node_by_title(transaction, "0x1")
    return lambda: node.move(new_parent)


def change_parent_best_case(transaction):
    node = _get_node_by_title(transaction, "0x0x0x0x0x0x0x1")
    new_parent = _get_node_by_title(transaction, "0x0x0x0x0x0")
    return lambda: node.move(new_parent)


def delete_node_best_case(transaction):
    node = _get_node_by_title(transaction, "0x0x0x0x0x0x0x0")
    return lambda: node.delete()


def delete_node_worst_case(transaction):
    node = _get_node_by_title(transaction, "0x0")
    return lambda: node.delete()


def iterate_get_ancestors(transaction):
    node = _get_node_by_title(transaction, "0x0x0x0x0x0x0x0")
    def method():
        nonlocal node
        for a in node.ancestors:
            pass
    return method


def create_benchmarks(transaction, config):

    test_node_id = config['test_node_id']
    test_node = transaction.get_node(test_node_id)

    bs = [
        Benchmark(
            lambda: transaction.get_tree_size(),
            "get_tree_size"
        ),
        Benchmark(
            lambda: transaction.get_root_node(),
            "get_root_node"
        ),
        Benchmark(
            lambda: transaction.get_node(test_node_id),
            "get_node"
        ),
        Benchmark(
            lambda: test_node.children,
            "get_children"
        ),
        Benchmark(
            lambda: test_node.ancestors,
            "get_ancestors"
        ),
        Benchmark(
            lambda: test_node.descendants,
            "get_descendants"
        ),
        Benchmark(
            lambda: test_node.insert_child(),
            "insert_child"
        ),
        Benchmark(
            delete_node_worst_case(transaction),
            "delete_node_worst_case"
        ),
        Benchmark(
            delete_node_best_case(transaction),
            "delete_node_best_case"
        ),
        Benchmark(
            change_parent_worst_case(transaction),
            "change_parent_worst_case"
        ),
        Benchmark(
            change_parent_best_case(transaction),
            "change_parent_best_case"
        ),
        Benchmark(
            iterate_get_ancestors(transaction),
            "iterate_get_ancestors"
        ),
    ]
    return bs
