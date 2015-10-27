.. _quickstart:

Quickstart
==========

Install ``libtree`` via ``pip install libtree``. Then start the
interactive Python interpreter of your choice to start working with
``libtree``::

    # Imports
    from libtree import Tree
    import psycopg2

    # Connect to PostgreSQL
    connection = psycopg2.connect("dbname=test_tree user=vortec")
    tree = Tree(connection)

    # Start working with libtree inside a database transaction
    with tree() as transaction:

        # Create tables
        transaction.install()

        # Create nodes
        root = transaction.insert_root_node()
        binx = root.insert_child({'title': 'Binary folder'})
        bash = binx.insert_child({'title': 'Bash executable', 'chmod': 755})
        etc = root.insert_child({'title': 'Config folder'})
        hosts = etc.insert_child({'title': 'Hosts file'})
        passwd = etc.insert_child({'title': 'Password file', 'chmod': 644})

        # Direct attribute access
        root.children  # => binx, etc
        len(root)  # => 2
        binx.parent  # => root
        bash.ancestors  # => binx, root
        root.descendants  # => binx, bash, etc, hosts, passwd

        # Query by property
        transaction.get_nodes_by_property_key('chmod')  # bash, passwd
        transaction.get_nodes_by_property_dict({'chmod': 644})  # passwd

        # Move bash node into etc node
        bash.move(etc)
        etc.children  # => hosts, passwd, bash
        bash.set_position(1)
        etc.children  # => hosts, bash, passwd

        # Print entire tree
        transaction.print_tree()
        # Output:
        # <NodeData id=1, parent=None>
        #   <NodeData id=2, title='Binary folder'>
        #   <NodeData id=4, title='Config folder'>
        #     <NodeData id=5, title='Hosts file'>
        #     <NodeData id=6, title='Password file'>
        #     <NodeData id=3, title='Bash executable'>
