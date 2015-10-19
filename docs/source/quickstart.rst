Quickstart
==========

After you've installed libtree correctly, you can create the table schema and create some nodes::

    from libtree import Tree
    from libtree.core import *
    import psycopg2

    # Connect to Postgres
    connection = psycopg2.connect("dbname=test_tree user=vortec")
    tree = Tree(connection)

    with tree() as transaction:
        transaction.install()
        cur = transaction.cursor

        # Create a few nodes to get going
        root = insert_node(cur, None, properties={'title': 'Root node'})
        binx = insert_node(cur, root, properties={'title': 'Binary folder'})
        etc = insert_node(cur, root, properties={'title': 'Config folder'})
        bash = insert_node(cur, etc, properties={'title': 'Bash executable'})
        hosts = insert_node(cur, etc, properties={'title': 'Hosts file'})
        passwd = insert_node(cur, etc, properties={'title': 'Password file'})

        # Get direct children of root node
        children = list(get_children(cur, root))
        print(children)
        # Output:
        # [<Node id=2, title='Binary folder'>, <Node id=3, title='Config folder'>]

        # Move bash node into correct parent node
        change_parent(cur, bash, binx)

        # Print entire tree
        print_tree(cur)
        # Output:
        # <Node id=1, title='Root node'>
        #   <Node id=2, title='Binary folder'>
        #     <Node id=4, title='Bash executable'>
        #   <Node id=3, title='Config folder'>
        #     <Node id=5, title='Hosts file'>
        #     <Node id=6, title='Password file'>
