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
    with tree(write=True) as transaction:

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
        # <NodeData id='0301770b-fe53-4447-88cc-87ce313e8d9a'>
        #   <NodeData id='726241b7-d1d0-4f50-8db4-1f45e133b52c', title='Binary folder'>
        #   <NodeData id='1afce8e3-975a-4daa-93e7-88d879c05224', title='Config folder'>
        #     <NodeData id='4db559b8-97b0-4b67-ad69-20644fcc3cfe', title='Hosts file'>
        #     <NodeData id='8f458921-d6db-4f34-8ee4-211c15e78471', title='Bash executable'>
        #     <NodeData id='4312a7bf-53c9-4c14-80a3-5f7dd385b25c', title='Password file'>
