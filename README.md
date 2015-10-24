libtree
=======
[![Build Status](https://travis-ci.org/conceptsandtraining/libtree.svg?branch=master)](https://travis-ci.org/conceptsandtraining/libtree)
[![Coverage Status](https://coveralls.io/repos/conceptsandtraining/libtree/badge.svg?branch=master&service=github)](https://coveralls.io/github/conceptsandtraining/libtree?branch=master)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/conceptsandtraining/libtree/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/conceptsandtraining/libtree/?branch=master)
[![Documentation Status](https://readthedocs.org/projects/libtree/badge/?version=latest)](https://libtree.readthedocs.org/en/latest/?badge=latest)


**libtree** is a Python library which assists you in dealing with **large,
hierarchical data sets**. It runs on top of **PostgreSQL 9.4** and is
compatible with **all major Python interpreters** (2.7, 3.3-3.5, PyPy2
and PyPy3).

Why use **libtree**? Because...

 - the usage is **super simple**
 - it scales up to **billions of nodes**
 - the reads and writes are **blazingly fast**
 - it supports **attribute inheritance**


But there's even more, **libtree**...

 - offers **thread-safety** by working inside transactions
 - enforces **integrity** by moving tree logic to inside the database
 - provides a **convenient** high level API and **fast** low level functions
 - core is **fully integration tested**, the testsuite covers >90% of the code


Installation
============
Install **libtree** directly via ``pip`:

```bash
$ pip install libtree
```


Quickstart
==========
Start the interactive Python interpreter of your choice to start working with
**libtree**:

```python
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
    # <NodeData id=1, parent=None, position=0>
    #   <NodeData id=2, title='Binary folder'>
    #   <NodeData id=4, title='Config folder'>
    #     <NodeData id=5, title='Hosts file'>
    #     <NodeData id=6, title='Password file'>
    #     <NodeData id=3, title='Bash executable'>
```


Documentation
=============
The **full documentation** including **API reference** and **database model**
description can be found at
**[ReadTheDocs.org](https://libtree.readthedocs.org/en/latest/)**.


Authors
=======
**libtree** is written and maintained by **Fabian Kochem** for **CaT Concepts
and Training GmbH**.
