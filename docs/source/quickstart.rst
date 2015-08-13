Quickstart
==========

After you've installed libtree correctly, you can create the table schema and create some nodes::

    from libtree import *

    # Connect to Postgres and create tables
    per = PostgreSQLPersistance("dbname=test_tree user=vortec")
    per.install()

    # Create a few nodes to get going
    root = insert_node(per, None, properties={'title': 'Root node'})
    bin = insert_node(per, root, properties={'title': 'Binary folder'})
    etc = insert_node(per, root, properties={'title': 'Config folder'})
    bash = insert_node(per, etc, properties={'title': 'Bash executable'})
    hosts = insert_node(per, etc, properties={'title': 'Hosts file'})
    passwd = insert_node(per, etc, properties={'title': 'Password file'})

    # Get direct children of root node
    children = list(get_children(per, root))
    print(children)
    # Output:
    # [<Node id=2, title='Binary folder'>, <Node id=3, title='Config folder'>]

    # Move bash node into correct parent node
    change_parent(per, bash, bin)

    # Print entire tree
    print_tree(per)
    # Output:
    # <Node id=1, title='Root node'>
    #   <Node id=2, title='Binary folder'>
    #     <Node id=4, title='Bash executable'>
    #   <Node id=3, title='Config folder'>
    #     <Node id=5, title='Hosts file'>
    #     <Node id=6, title='Password file'>

    # Commit transaction
    per.commit()
