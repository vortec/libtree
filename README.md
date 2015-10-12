libtree
=======
[![Build Status](https://travis-ci.org/conceptsandtraining/libtree.svg?branch=master)](https://travis-ci.org/conceptsandtraining/libtree)
[![Coverage Status](https://coveralls.io/repos/conceptsandtraining/libtree/badge.svg?branch=master&service=github)](https://coveralls.io/github/conceptsandtraining/libtree?branch=master)
[![Documentation Status](https://readthedocs.org/projects/libtree/badge/?version=latest)](https://libtree.readthedocs.org/en/latest/?badge=latest)


**libtree** is a Python library which assists you in dealing with **large,
hierarchical data sets**. It runs on top of **PostgreSQL 9.4** and is
compatible with Python **2.7**, **3.4**, **3.5** and **PyPy 3**.

Why use **libtree**? Because...

 - the API is **super simple**
 - it scales up to **billions of nodes**
 - the reads and writes are **blazingly fast**
 - it supports **attribute inheritance**


But there's even more, **libtree**...

 - lets you decide when and how to deal with **transactions**
 - is **memory efficient** because iterators are widely available
 - enforces **integrity** by moving tree logic to inside the database
 - is **fully integration tested**, the testsuite covers >90% of the code


Installation
============
Install libtree directly via pip:

```bash
$ pip install libtree
```


Quickstart
==========
After you've installed libtree correctly, you can create the table schema and
create some nodes::

```python
from libtree import *

# Connect to Postgres and create tables
per = PostgreSQLPersistance("dbname=test_tree user=vortec")
per.install()

# Create a few nodes to get going
root = insert_node(per, None, properties={'title': 'Root node'})
binx = insert_node(per, root, properties={'title': 'Binary folder'})
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
change_parent(per, bash, binx)

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


Documentation
=============
The full documentation including API reference and database model description
can be found at [ReadTheDocs.org](https://libtree.readthedocs.org/en/latest/).


Authors
=======
**libtree** is written and maintained by Fabian Kochem for CaT Concepts and
Training GmbH.
