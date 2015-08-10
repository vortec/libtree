# libtree 0.0.1

libtree is a Python library which assists you dealing with large, hierarchical data sets. Its main features are:

  - handles billions of nodes
  - fast reads and fast writes
  - attribute inheritance (called "properties")
  - no transaction requirements

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
from libtree.persistance import *
from libtree.tree import *

# Connect to Postgres and create tables
per = PostgreSQLPersistance("dbname=tree user=james")
per.install()

# Create three nodes, including root node, to get going
root = insert_node(per, None, 'folder', attributes={'title': 'Root node'}, auto_position=False)
bin = insert_node(per, root, 'folder', attributes={'title': 'Binary folder'})
etc = insert_node(per, root, 'folder', attributes={'title': 'Config folder'})
bash = insert_node(per, etc, 'file', attributes={'title': 'Bash executable'})
hosts = insert_node(per, etc, 'file', attributes={'title': 'Hosts file'})
passwd = insert_node(per, etc, 'file', attributes={'title': 'Password file'})

# Get children
children = list(get_children(per, root))
print(children) # <Node

# Move
print_tree(per)
per.commit()
```
This code establishes a connection to Postgres, creates three nodes, prints the tree structure to stdout and commits the changes to the database. libtree doesn't deal with transactions, therefore it is your responsibility to call `commit()` or `rollback()`.
