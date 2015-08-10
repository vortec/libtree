# libtree 0.0.1

libtree is a Python library which assists you dealing with large, hierarchical data sets. Its main features are:

  - handles billions of nodes
  - fast reads and fast writes
  - attribute inheritance (called "properties")
  - no transaction requirements
  - memory efficient (iterators available everywhere)

To use libtree, you need to have a running Postgres 9.4 server and either Python 2.7, 3.4 or PyPy3.

### Installation
You should be able to install libtree directly via pip:
```sh
pip install libtree
```

If this fails, you probably must setup our [PyPi server](https://www.wiki.local/doku.php?id=dev:ci:pypi) or install some [postgres-dev packages](http://initd.org/psycopg/docs/install.html#installation).

### Quickstart

After you've installed libtree correctly, you can create the table schema and create some nodes.

```py
from libtree import *

# Connect to Postgres and create tables
per = PostgreSQLPersistance("dbname=test_tree user=vortec")
per.install()

# Create a few nodes to get going
root = insert_node(per, None, 'folder', attributes={'title': 'Root node'}, auto_position=False)
bin = insert_node(per, root, 'folder', attributes={'title': 'Binary folder'})
etc = insert_node(per, root, 'folder', attributes={'title': 'Config folder'})
bash = insert_node(per, etc, 'file', attributes={'title': 'Bash executable'})
hosts = insert_node(per, etc, 'file', attributes={'title': 'Hosts file'})
passwd = insert_node(per, etc, 'file', attributes={'title': 'Password file'})

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
```
This code example shows the basics how to work with libtree. It's pretty straight-forwards once you see

libtree doesn't deal with transactions, therefore it is your responsibility to call `commit()` or `rollback()`.
