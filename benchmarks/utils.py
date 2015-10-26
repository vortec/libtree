import psycopg2
import math
import libtree

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'
REFRESH_TERMINAL_DELAY = 30


def postgres_create_db(dsn, dbname):
    conn = psycopg2.connect(dsn)
    conn.set_isolation_level(0)
    cur = conn.cursor()
    try:
        cur.execute("DROP DATABASE {}".format(dbname))
        print("dropped database {}".format(dbname))
    except psycopg2.ProgrammingError:
        # database does not exist
        pass
    cur.execute("CREATE DATABASE {}".format(dbname))
    print("created database {}".format(dbname))


def postgres_analyze_db(cur):
    cur.execute('ANALYZE VERBOSE')


def calculate_tree_size(levels, per_level):
    # time.sleep(0.5)
    if per_level == 1:
        return levels
    return int(((1 - per_level ** (levels + 1)) / (1 - per_level)) - 1)


def generate_tree(transaction, levels, per_level):
    def insert_node(*args, **kwargs):
        # wrap libtree.insert_node so we can print the current progress
        nonlocal n_inserted, expected_nodes
        node = libtree.core.insert_node(*args, **kwargs)
        n_inserted += 1
        
        # only print progress at certain points 
        if not n_inserted % REFRESH_TERMINAL_DELAY or n_inserted == expected_nodes:
            if n_inserted > REFRESH_TERMINAL_DELAY:
                print(CURSOR_UP_ONE + ERASE_LINE, end="")
            print(n_inserted)

        return node

    def insert_children(parent, label, current_depth=1):
        label.append("x")
        for x in range(per_level):
            label2 = label.copy()
            label2.append(x)
            title = "".join(map(str, label2))
            properties = {"title": title}
            node = insert_node(
                transaction.cursor, parent, properties, position=x, auto_position=False)
            if current_depth < levels:
                insert_children(node, label2, current_depth + 1)

    n_inserted = 0
    expected_nodes = calculate_tree_size(levels, per_level)
    print("generating tree with {} nodes..".format(expected_nodes))
    root = insert_node(transaction.cursor, None, properties={"title": "0"})
    insert_children(root, [0])
    print("done")


def format_duration(seconds):
    """
    pretty-print a duration.

    :param float seconds: duration to be formatted.
    """
    units = ["s", "ms", 'us', "ns"]
    scaling = [1, 1e3, 1e6, 1e9]
    if seconds > 0.0 and seconds < 1000.0:
        order = min(-int(math.floor(math.log10(seconds)) // 3), 3)
    elif seconds >= 1000.0:
        order = 0
    else:
        order = 3
    return "{:.2f}{}".format(seconds * scaling[order], units[order])
